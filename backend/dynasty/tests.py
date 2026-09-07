from django.test import SimpleTestCase

from . import engine


class EngineTests(SimpleTestCase):
    def test_new_game_has_five_roster_slots(self):
        game = engine.new_game(city="Testville", team_name="Testers")
        self.assertEqual(len(game["state"]["roster"]), 5)
        self.assertEqual(game["state"]["city"], "Testville")
        self.assertEqual(game["state"]["team_name"], "Testers")

    def test_new_game_defaults_when_blank(self):
        game = engine.new_game()
        self.assertEqual(game["state"]["city"], "Your City")
        self.assertEqual(game["state"]["team_name"], "The Franchise")

    def test_new_game_starts_with_fan_support(self):
        game = engine.new_game()
        self.assertEqual(game["state"]["fan_support"], 50)

    def test_late_lottery_pick_excludes_boom_bust(self):
        options = engine.generate_draft_options(pick_number=10)
        ids = [o["id"] for o in options]
        self.assertNotIn("boom_bust", ids)

    def test_playoff_options_include_named_star_and_depth_signees(self):
        roster = engine.new_starting_roster()
        roster[0]["player"] = engine.make_player(ovr=75, age=25)
        offseason = engine.generate_offseason_options(made_playoffs=True, wins=50, roster=roster)
        by_id = {o["id"]: o for o in offseason["options"]}
        self.assertIn("prospect", by_id["chase_a_star"])
        self.assertEqual(len(by_id["invest_in_depth"]["depth_signees"]), 2)

    def test_average_roster_plays_close_to_500(self):
        # 5 players all at a middling ~62 OVR, average depth, should land
        # near a .500 record, not a 50-win season.
        roster = [{"slot": f"core_{i}", "player": engine.make_player(ovr=62, age=27)} for i in range(5)]
        rating = engine.compute_team_rating(roster, depth_rating=40)
        wins, _ = engine.simulate_regular_season(rating)
        self.assertTrue(30 <= wins <= 52)

    def test_one_great_pick_does_not_spike_wins_to_50(self):
        roster = [{"slot": f"core_{i}", "player": engine.make_player(ovr=58, age=27)} for i in range(4)]
        roster.append({"slot": "core_5", "player": engine.make_player(ovr=83, age=22)})
        rating = engine.compute_team_rating(roster, depth_rating=34)
        wins, _ = engine.simulate_regular_season(rating)
        self.assertLess(wins, 45)

    def test_full_ten_season_run_ends_with_game_over(self):
        game = engine.new_game()
        state = game["state"]
        decision = game["decision"]
        result = None

        for _ in range(engine.TOTAL_SEASONS):
            option = decision["options"][0]
            result = engine.advance_dynasty(
                state, option["id"], prospect=option.get("prospect"), depth_signees=option.get("depth_signees")
            )
            state = result["state"]
            decision = result["next_decision"]

        self.assertTrue(result["game_over"])
        self.assertIsNone(decision)
        self.assertEqual(len(state["history"]), engine.TOTAL_SEASONS)
        self.assertIn("fan_support", state)

    def test_unknown_choice_raises(self):
        game = engine.new_game()
        with self.assertRaises(ValueError):
            engine.advance_dynasty(game["state"], "not_a_real_choice")
