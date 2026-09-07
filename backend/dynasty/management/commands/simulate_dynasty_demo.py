import random

from django.core.management.base import BaseCommand

from dynasty import engine


class Command(BaseCommand):
    help = "Simulate a full 10-season Dynasty run with random decisions and print the results."

    def handle(self, *args, **options):
        game = engine.new_game()
        state = game["state"]
        decision = game["decision"]

        self.stdout.write(self.style.SUCCESS("=== NEW DYNASTY ==="))
        self.stdout.write("Last season: 18-65. You have the No. 1 pick.\n")

        result = None
        while decision is not None:
            choice = random.choice(decision["options"])
            label = choice["label"]
            if choice.get("prospect"):
                label = f"{choice['prospect']['name']} ({label})"

            pick_line = f" [pick #{decision['pick_number']}]" if decision.get("pick_number") else ""
            self.stdout.write(f"Season {decision['season_number']}{pick_line} decision: {label}")

            result = engine.advance_dynasty(state, choice["id"], prospect=choice.get("prospect"))
            state = result["state"]
            season_result = result["season_result"]

            self.stdout.write(
                f"  -> {season_result['wins']}-{season_result['losses']} "
                f"({season_result['result']}) [team rating {season_result['team_rating']}]"
            )
            for note in season_result["notes"]:
                self.stdout.write(f"     - {note}")

            decision = result["next_decision"]

        self.stdout.write(self.style.SUCCESS("\n=== FINAL ROSTER ==="))
        for slot in state["roster"]:
            p = slot["player"]
            if p:
                self.stdout.write(
                    f"{p['name']} — {p['ovr']} OVR, {p['position']}, {p['height']}, "
                    f"{p['weight']} lbs, Age {p['age']} ({p['origin']})"
                )

        self.stdout.write(self.style.SUCCESS("\n=== DYNASTY COMPLETE ==="))
        for h in state["history"]:
            champ = " \U0001F3C6" if h["champion"] else ""
            self.stdout.write(f"Season {h['season_number']}: {h['wins']}-{h['losses']} — {h['result']}{champ}")

        self.stdout.write(f"\nLongest championship streak: {state['max_streak']}")
        if state["max_streak"] >= 3:
            self.stdout.write(self.style.SUCCESS("YOU BUILT A 3-PEAT DYNASTY!"))
