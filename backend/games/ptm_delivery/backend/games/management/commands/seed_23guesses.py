from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from games.models import DailyPuzzle

# Sample launch-week puzzles. These are placeholders built from well-known,
# publicly documented facts — swap them out (or add more) via the Django
# admin whenever you're ready. Clues are ordered obscure -> obvious.
SAMPLE_PUZZLES = [
    dict(
        sport=DailyPuzzle.Sport.NBA,
        category=DailyPuzzle.Category.PLAYER,
        difficulty=DailyPuzzle.Difficulty.MEDIUM,
        answer="LeBron James",
        accepted_answers=["lebron", "lebron james", "king james"],
        clues=[
            "This player has played in 10 NBA Finals over his career.",
            "He has suited up for four different NBA franchises.",
            "He's won championships with three different teams.",
            "He passed Kareem Abdul-Jabbar to become the NBA's all-time leading scorer.",
            "His nickname is 'King James.'",
            "He was the No. 1 overall pick in the 2003 NBA Draft, straight out of high school.",
        ],
    ),
    dict(
        sport=DailyPuzzle.Sport.NBA,
        category=DailyPuzzle.Category.TEAM,
        difficulty=DailyPuzzle.Difficulty.MEDIUM,
        answer="Golden State Warriors",
        accepted_answers=["warriors", "golden state warriors", "golden state", "dubs"],
        clues=[
            "This franchise's history traces back to Philadelphia, with stops in "
            "San Francisco and Oakland before its current arena.",
            "The team set the all-time regular-season wins record in 2015-16, going 73-9.",
            "Two of its star guards became known as the 'Splash Brothers.'",
            "This franchise won four championships between 2015 and 2022.",
            "Stephen Curry has spent his entire career with this franchise.",
            "They currently play their home games at Chase Center in San Francisco.",
        ],
    ),
    dict(
        sport=DailyPuzzle.Sport.NBA,
        category=DailyPuzzle.Category.RECORD,
        difficulty=DailyPuzzle.Difficulty.HARD,
        answer="Wilt Chamberlain's 100-point game",
        accepted_answers=[
            "wilt chamberlain",
            "100 point game",
            "wilt's 100 point game",
            "the 100 point game",
        ],
        clues=[
            "This record has stood since March 1962.",
            "It happened in a game played in Hershey, Pennsylvania.",
            "The player made 36 of his 63 field-goal attempts that night.",
            "He also grabbed 25 rebounds in the same game.",
            "It remains the most points ever scored by one player in a single NBA game.",
            "The player who set it also holds the NBA's career rebounding record.",
        ],
    ),
    dict(
        sport=DailyPuzzle.Sport.NBA,
        category=DailyPuzzle.Category.SEASON,
        difficulty=DailyPuzzle.Difficulty.MEDIUM,
        answer="1995-96 Chicago Bulls",
        accepted_answers=["bulls", "1995-96 bulls", "95-96 bulls", "chicago bulls"],
        clues=[
            "This team started the season by winning 41 of its first 44 games.",
            "They finished the regular season 72-10 — a mark that stood for 20 years.",
            "Their head coach was Phil Jackson.",
            "The roster featured Michael Jordan, Scottie Pippen, and Dennis Rodman.",
            "They capped the season with a championship, their fourth of the decade.",
            "Their 72-10 record stood until the Warriors went 73-9 in 2015-16.",
        ],
    ),
    dict(
        sport=DailyPuzzle.Sport.NFL,
        category=DailyPuzzle.Category.PLAYER,
        difficulty=DailyPuzzle.Difficulty.EASY,
        answer="Tom Brady",
        accepted_answers=["tom brady", "brady", "tb12"],
        clues=[
            "This player was picked 199th overall in the 2000 NFL Draft.",
            "He won six Super Bowls with one franchise before winning a seventh with another.",
            "He spent 20 seasons with the New England Patriots.",
            "He finished his career with more passing yards than anyone in NFL history.",
            "His final championship came with the Tampa Bay Buccaneers.",
            "He's widely nicknamed 'The GOAT.'",
        ],
    ),
    dict(
        sport=DailyPuzzle.Sport.NBA,
        category=DailyPuzzle.Category.GAME,
        difficulty=DailyPuzzle.Difficulty.HARD,
        answer="1998 NBA Finals, Game 6",
        accepted_answers=[
            "game 6 1998 finals",
            "1998 finals game 6",
            "the last shot",
            "jordan's last shot",
            "1998 nba finals game 6",
        ],
        clues=[
            "This game was played in Salt Lake City on June 14, 1998.",
            "It was Game 6 of the NBA Finals, with the road team leading the series 3-2.",
            "The home team trailed by three points inside the final minute.",
            "The game's signature moment came off a steal near midcourt.",
            "It ended with a jump shot with 5.2 seconds left, final score 87-86.",
            "It's remembered as Michael Jordan's last shot in a Bulls uniform.",
        ],
    ),
]


class Command(BaseCommand):
    help = "Seed sample '23 Guesses' puzzles for the next several days."

    def handle(self, *args, **options):
        start = timezone.localdate()
        created, skipped = 0, 0

        for i, data in enumerate(SAMPLE_PUZZLES):
            puzzle_date = start + timedelta(days=i)
            _, was_created = DailyPuzzle.objects.get_or_create(
                date=puzzle_date, defaults=data
            )
            if was_created:
                created += 1
            else:
                skipped += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {created} puzzle(s), skipped {skipped} (date already had one)."
            )
        )
