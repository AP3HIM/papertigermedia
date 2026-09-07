from django.test import SimpleTestCase

from . import engine


class EngineTests(SimpleTestCase):
    def test_new_game_top_pick_has_boom_bust_option(self):
        game = engine.new_game()
        ids = [o["id"] for o in game["decision"]["options"]]
        self.assertIn("boom_bust", ids)
        self.assertEqual(game["decision"]["pick_number"], 1)

    def test_late_lottery_pick_excludes_boom_bust(self):
        options = engine.generate_draft_options(pick_number=10)
        ids = [o["id"] for o in options]
        self.assertNotIn("boom_bust", ids)
        self.assertIn("safe", ids)
        self.assertIn("trade_for_veteran", ids)

    def test_draft_options_include_full_scouting_profile(self):
        options = engine.generate_draft_options(pick_number=1)
        for option in options:
            prospect = option["prospect"]
            self.assertIn(prospect["position"], engine.POSITIONS)
            self.assertTrue(prospect["height"])
            self.assertTrue(prospect["weight"])
            self.assertEqual(len(prospect["traits"]), 2)
            self.assertTrue(prospect["origin"])

    def test_resolved_player_matches_shown_prospect(self):
        options = engine.generate_draft_options(pick_number=1)
        safe_option = next(o for o in options if o["id"] == "safe")
        roster = engine.new_starting_roster()

        roster, _, _ = engine.resolve_offseason_choice(
            "safe", roster, depth_rating=40, prospect=safe_option["prospect"]
        )
        drafted = next(s["player"] for s in roster if s["player"] and s["player"]["origin"] == safe_option["prospect"]["origin"])
        self.assertEqual(drafted["name"], safe_option["prospect"]["name"])
        self.assertEqual(drafted["position"], safe_option["prospect"]["position"])

    def test_team_rating_within_bounds(self):
        roster = engine.new_starting_roster()
        roster[0]["player"] = engine.make_player(ovr=70, age=25)
        rating = engine.compute_team_rating(roster, depth_rating=50)
        self.assertTrue(20 <= rating <= 99)

    def test_full_ten_season_run_ends_with_game_over(self):
        game = engine.new_game()
        state = game["state"]
        decision = game["decision"]
        result = None

        for _ in range(engine.TOTAL_SEASONS):
            option = decision["options"][0]
            result = engine.advance_dynasty(state, option["id"], prospect=option.get("prospect"))
            state = result["state"]
            decision = result["next_decision"]

        self.assertTrue(result["game_over"])
        self.assertIsNone(decision)
        self.assertEqual(len(state["history"]), engine.TOTAL_SEASONS)

    def test_unknown_choice_raises(self):
        game = engine.new_game()
        with self.assertRaises(ValueError):
            engine.advance_dynasty(game["state"], "not_a_real_choice")
