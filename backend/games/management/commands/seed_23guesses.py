from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from games.models import DailyPuzzle

# ~3 weeks of launch content. Built from well-documented, widely known facts
# — swap/add more anytime via the Django admin. Clues are ordered obscure
# (clue_1) to obvious (clue_8) on purpose: the goal is that a casual fan
# needs several clues, not that the answer is guessable from clue 1.
SAMPLE_PUZZLES = [
    dict(
        sport=DailyPuzzle.Sport.NBA, category=DailyPuzzle.Category.PLAYER, difficulty=DailyPuzzle.Difficulty.EASY,
        answer="Michael Jordan", accepted_answers_extra="MJ, Air Jordan",
        clue_1="This player was left off his high school's varsity roster as a sophomore.",
        clue_2="He hit the title-winning shot for North Carolina in the 1982 NCAA championship, as a freshman.",
        clue_3="He was picked third overall in the 1984 draft, behind Hakeem Olajuwon and Sam Bowie.",
        clue_4="He retired twice during his career, once to play minor league baseball.",
        clue_5="He won six NBA championships, all with the same franchise, and was Finals MVP every time.",
        clue_6="His signature shoe line began in 1985 and is still one of the best-selling in the world.",
        clue_7="He won five regular-season MVP awards.",
        clue_8="He's widely regarded as the greatest basketball player of all time.",
    ),
    dict(
        sport=DailyPuzzle.Sport.NBA, category=DailyPuzzle.Category.PLAYER, difficulty=DailyPuzzle.Difficulty.HARD,
        answer="Kareem Abdul-Jabbar", accepted_answers_extra="Kareem, Lew Alcindor",
        clue_1="This player competed in college under the name Lew Alcindor before changing it in 1971.",
        clue_2="He won three consecutive NCAA championships at UCLA.",
        clue_3="His signature shot was the 'skyhook.'",
        clue_4="He won six NBA championships across two different franchises.",
        clue_5="He was a six-time NBA MVP, the most in league history.",
        clue_6="He held the NBA's all-time scoring record for nearly 40 years.",
        clue_7="That record was broken by LeBron James in 2023.",
        clue_8="He played most of his 20 seasons for the Los Angeles Lakers.",
    ),
    dict(
        sport=DailyPuzzle.Sport.NBA, category=DailyPuzzle.Category.PLAYER, difficulty=DailyPuzzle.Difficulty.HARD,
        answer="Bill Russell", accepted_answers_extra="",
        clue_1="This player won two NCAA championships at the University of San Francisco.",
        clue_2="He won an Olympic gold medal in 1956 before his NBA career even started.",
        clue_3="He was known primarily as a defensive anchor and rebounder rather than a scorer.",
        clue_4="He became the first Black head coach in any major U.S. pro sport, coaching the same team he played for.",
        clue_5="He won 11 NBA championships in 13 seasons — the most of any player in any major sport.",
        clue_6="The NBA Finals MVP award is named after him.",
        clue_7="He played his entire career with the Boston Celtics.",
        clue_8="He's often cited as the greatest winner in North American sports history.",
    ),
    dict(
        sport=DailyPuzzle.Sport.NBA, category=DailyPuzzle.Category.SEASON, difficulty=DailyPuzzle.Difficulty.HARD,
        answer="2015-16 Golden State Warriors", accepted_answers_extra="Warriors 73-9, 73-9 Warriors",
        clue_1="This team started 24-0, the best start to a season in NBA history.",
        clue_2="Two guards on this roster were nicknamed the 'Splash Brothers.'",
        clue_3="Their head coach won Coach of the Year this season.",
        clue_4="One of their players broke the single-season three-point record, making over 400.",
        clue_5="They finished the regular season 73-9, breaking the 1995-96 Bulls' record.",
        clue_6="Despite that record, they lost the NBA Finals that year in seven games.",
        clue_7="They blew a 3-1 series lead in that Finals loss.",
        clue_8="The team that beat them was led by LeBron James.",
    ),
    dict(
        sport=DailyPuzzle.Sport.NBA, category=DailyPuzzle.Category.SEASON, difficulty=DailyPuzzle.Difficulty.MEDIUM,
        answer="2000-01 Los Angeles Lakers", accepted_answers_extra="2001 Lakers",
        clue_1="This team lost only one game during their entire playoff run.",
        clue_2="Their coach had also won championships with the Chicago Bulls.",
        clue_3="Their star guard was still in his early twenties this season.",
        clue_4="Their center won Finals MVP for the second of three straight years.",
        clue_5="They swept their first three playoff series before losing one game in the Finals.",
        clue_6="They beat the Philadelphia 76ers in the Finals.",
        clue_7="Their center-guard duo was simply known as 'Shaq and Kobe.'",
        clue_8="This was the second of three straight championships for the Los Angeles Lakers.",
    ),
    dict(
        sport=DailyPuzzle.Sport.NBA, category=DailyPuzzle.Category.RECORD, difficulty=DailyPuzzle.Difficulty.HARD,
        answer="Wilt Chamberlain's 100-point game", accepted_answers_extra="100 point game, The 100 Point Game",
        clue_1="This record has stood since March 2, 1962.",
        clue_2="It was set in a game played at a neutral site in Hershey, Pennsylvania.",
        clue_3="The player made 36 of his 63 field goal attempts that night.",
        clue_4="He also made 28 of 32 free throws — both unusually high volumes for him.",
        clue_5="He grabbed 25 rebounds in the same game.",
        clue_6="The opposing team was the New York Knicks.",
        clue_7="It remains the most points scored by one player in a single NBA game.",
        clue_8="The player who set it also holds the NBA's career rebounding record.",
    ),
    dict(
        sport=DailyPuzzle.Sport.NBA, category=DailyPuzzle.Category.SEASON, difficulty=DailyPuzzle.Difficulty.MEDIUM,
        answer="1995-96 Chicago Bulls", accepted_answers_extra="95-96 Bulls",
        clue_1="This team started the season by winning 41 of their first 44 games.",
        clue_2="Their power forward had once been suspended for head-butting a referee.",
        clue_3="Their head coach also won titles with this same core roster in two separate three-peats.",
        clue_4="They finished the regular season 72-10, a record that stood for 20 years.",
        clue_5="Their star player had returned from his second retirement partway through the previous season.",
        clue_6="Their roster featured Michael Jordan, Scottie Pippen, and Dennis Rodman together for the first time.",
        clue_7="They won the championship that year, their fourth of the decade.",
        clue_8="Their 72-10 record stood until the Warriors went 73-9 in 2015-16.",
    ),
    dict(
        sport=DailyPuzzle.Sport.NFL, category=DailyPuzzle.Category.PLAYER, difficulty=DailyPuzzle.Difficulty.MEDIUM,
        answer="Tom Brady", accepted_answers_extra="TB12",
        clue_1="This player was picked 199th overall in his draft class, in the sixth round.",
        clue_2="He didn't become a starter until an injury to the player ahead of him on the depth chart.",
        clue_3="He won his first Super Bowl in just his second professional season.",
        clue_4="He spent 20 seasons with the same franchise before switching teams late in his career.",
        clue_5="He won six Super Bowls with one franchise, then a seventh with another.",
        clue_6="His final championship came with the Tampa Bay Buccaneers.",
        clue_7="He retired holding the records for most career passing yards and touchdowns in NFL history.",
        clue_8="He's widely nicknamed 'The GOAT.'",
    ),
    dict(
        sport=DailyPuzzle.Sport.NBA, category=DailyPuzzle.Category.GAME, difficulty=DailyPuzzle.Difficulty.HARD,
        answer="1998 NBA Finals, Game 6",
        accepted_answers_extra="Game 6 1998 Finals, The Last Shot, Jordan's Last Shot",
        clue_1="This game was played on the road for the winning team, in Salt Lake City.",
        clue_2="The home team led the series 3-2 going into this game.",
        clue_3="The road team trailed by three points with under a minute remaining.",
        clue_4="The signature sequence began with a steal near midcourt against the home team's star forward.",
        clue_5="The road team's star player hit the go-ahead shot with 5.2 seconds left.",
        clue_6="The final score was 87-86.",
        clue_7="It clinched the road team's sixth championship in eight seasons.",
        clue_8="It's remembered as Michael Jordan's final shot in a Chicago Bulls uniform.",
    ),
    dict(
        sport=DailyPuzzle.Sport.NBA, category=DailyPuzzle.Category.PLAYER, difficulty=DailyPuzzle.Difficulty.HARD,
        answer="Larry Bird", accepted_answers_extra="",
        clue_1="This player grew up in French Lick, Indiana.",
        clue_2="He led Indiana State to the NCAA championship game as a senior.",
        clue_3="He lost that NCAA final to a team led by Magic Johnson.",
        clue_4="He was drafted a year early by his NBA team, who held his rights until he finished college.",
        clue_5="He won three straight NBA MVP awards in the mid-1980s.",
        clue_6="He was known for trash-talking opponents right before hitting difficult shots.",
        clue_7="He won three NBA championships, all with the same franchise.",
        clue_8="He played his entire career for the Boston Celtics.",
    ),
    dict(
        sport=DailyPuzzle.Sport.NBA, category=DailyPuzzle.Category.PLAYER, difficulty=DailyPuzzle.Difficulty.HARD,
        answer="Magic Johnson", accepted_answers_extra="",
        clue_1="This player won an NCAA championship as a college sophomore, then left school early.",
        clue_2="He started at center in the deciding game of his first NBA Finals, filling in for an injured teammate.",
        clue_3="That Finals performance came in his rookie season.",
        clue_4="He won five NBA championships, all with the same franchise.",
        clue_5="His era with that franchise was nicknamed 'Showtime.'",
        clue_6="He announced his retirement in 1991 after testing positive for HIV.",
        clue_7="He returned to play in the 1992 All-Star Game and the 1992 Olympics.",
        clue_8="His college and NBA rivalry with Larry Bird defined the 1980s.",
    ),
    dict(
        sport=DailyPuzzle.Sport.GENERAL, category=DailyPuzzle.Category.PLAYER, difficulty=DailyPuzzle.Difficulty.MEDIUM,
        answer="Serena Williams", accepted_answers_extra="",
        clue_1="This player won her first major singles title in 1999 at the US Open.",
        clue_2="She and her sister won multiple Olympic gold medals together in doubles.",
        clue_3="She completed a calendar-year 'Serena Slam,' holding all four major titles at once, on two separate occasions.",
        clue_4="She won the 2017 Australian Open while pregnant.",
        clue_5="Her older sister was also a top-ranked professional player.",
        clue_6="She finished her career with 23 Grand Slam singles titles, an Open Era record.",
        clue_7="She retired following the 2022 US Open.",
        clue_8="She's widely considered the greatest women's tennis player of the Open Era.",
    ),
    dict(
        sport=DailyPuzzle.Sport.GENERAL, category=DailyPuzzle.Category.PLAYER, difficulty=DailyPuzzle.Difficulty.HARD,
        answer="Usain Bolt", accepted_answers_extra="Lightning Bolt",
        clue_1="This athlete first drew global attention at the 2002 World Junior Championships as a teenager.",
        clue_2="He set his first individual world record in the 100m in 2008, months before that year's Olympics.",
        clue_3="His 100m world record, set in Berlin in 2009, still stands.",
        clue_4="He's from Jamaica.",
        clue_5="He retired after the 2017 World Championships in London.",
        clue_6="He won gold in the same two individual sprint events at three consecutive Olympics, plus relay.",
        clue_7="He was nicknamed for the obvious pun on his last name.",
        clue_8="He's widely regarded as the fastest sprinter in history.",
    ),
    dict(
        sport=DailyPuzzle.Sport.NFL, category=DailyPuzzle.Category.PLAYER, difficulty=DailyPuzzle.Difficulty.MEDIUM,
        answer="Peyton Manning", accepted_answers_extra="The Sheriff",
        clue_1="This player was the first overall pick in the 1998 NFL Draft.",
        clue_2="His father and both his brothers also played quarterback professionally or in college.",
        clue_3="He missed an entire season with a neck injury before being released by the team that drafted him.",
        clue_4="He won a Super Bowl with a second franchise after that release.",
        clue_5="He set the single-season passing touchdown record in 2004, then broke his own record again in 2013.",
        clue_6="He won five NFL MVP awards, the most in league history.",
        clue_7="He spent most of his career with the Indianapolis Colts.",
        clue_8="He's nicknamed 'The Sheriff' for his pre-snap audibles.",
    ),
    dict(
        sport=DailyPuzzle.Sport.NFL, category=DailyPuzzle.Category.PLAYER, difficulty=DailyPuzzle.Difficulty.HARD,
        answer="Jerry Rice", accepted_answers_extra="",
        clue_1="This player attended a small Division I-AA college, Mississippi Valley State.",
        clue_2="He was famous for running extra conditioning sprints up a steep hill during the offseason.",
        clue_3="He played the first 16 seasons of his career with one franchise, then finished with two others.",
        clue_4="He wore No. 80 for most of his career.",
        clue_5="He won three Super Bowls, all with the San Francisco 49ers.",
        clue_6="He retired holding nearly every major career receiving record in NFL history.",
        clue_7="His career receiving yardage record still stands by a wide margin.",
        clue_8="He's widely regarded as the greatest wide receiver of all time.",
    ),
    dict(
        sport=DailyPuzzle.Sport.NFL, category=DailyPuzzle.Category.SEASON, difficulty=DailyPuzzle.Difficulty.HARD,
        answer="2007 New England Patriots", accepted_answers_extra="",
        clue_1="This team's quarterback set the single-season touchdown pass record this year.",
        clue_2="Their top receiver set the single-season receiving touchdown record the same year.",
        clue_3="They were fined earlier that season over a videotaping scandal.",
        clue_4="They became the first team in over 30 years to finish a regular season 16-0.",
        clue_5="They reached the Super Bowl undefeated at 18-0.",
        clue_6="They lost that Super Bowl to the New York Giants.",
        clue_7="The game-winning drive against them featured a famous catch pinned against a defender's helmet.",
        clue_8="Their quarterback was Tom Brady and head coach was Bill Belichick.",
    ),
    dict(
        sport=DailyPuzzle.Sport.NHL, category=DailyPuzzle.Category.PLAYER, difficulty=DailyPuzzle.Difficulty.MEDIUM,
        answer="Wayne Gretzky", accepted_answers_extra="The Great One",
        clue_1="This player was nicknamed for his dominance in Canadian minor hockey as a kid.",
        clue_2="He won four championships in the 1980s with one franchise before a blockbuster 1988 trade.",
        clue_3="That trade to a Los Angeles franchise is credited with growing the sport's popularity in the U.S.",
        clue_4="He wore No. 99 for almost his entire career.",
        clue_5="He won eight consecutive MVP awards in his league.",
        clue_6="He played most of his early career for the Edmonton Oilers.",
        clue_7="He retired holding the all-time records for goals, assists, and points.",
        clue_8="His career assists total alone exceeds any other player's career point total.",
    ),
    dict(
        sport=DailyPuzzle.Sport.NBA, category=DailyPuzzle.Category.PLAYER, difficulty=DailyPuzzle.Difficulty.MEDIUM,
        answer="Stephen Curry", accepted_answers_extra="Steph Curry",
        clue_1="This player wasn't offered a scholarship by any major conference program out of high school.",
        clue_2="He set the single-season three-point record as a college junior at Davidson.",
        clue_3="He was picked 7th overall in the 2009 NBA Draft.",
        clue_4="He's broken the single-season three-point record multiple times over his own career.",
        clue_5="He won back-to-back MVP awards, the second one unanimous — the only unanimous MVP in league history.",
        clue_6="He's widely credited with making the three-point shot central to modern NBA offenses.",
        clue_7="He's won four championships, all with the same franchise.",
        clue_8="He plays for the Golden State Warriors.",
    ),
    dict(
        sport=DailyPuzzle.Sport.GENERAL, category=DailyPuzzle.Category.PLAYER, difficulty=DailyPuzzle.Difficulty.MEDIUM,
        answer="Tiger Woods", accepted_answers_extra="",
        clue_1="This athlete appeared on a television show demonstrating his skills at age 2.",
        clue_2="He won three consecutive US Junior Amateur titles as a teenager.",
        clue_3="He won the Masters in 1997 by a record margin, in his first major as a professional.",
        clue_4="He held all four major championship trophies at once in 2000-01, though not in the same calendar year.",
        clue_5="He was involved in a serious car accident in 2021 that threatened his ability to walk.",
        clue_6="He returned to win the Masters again in 2019, over a decade after his previous major win.",
        clue_7="He's tied for the most PGA Tour wins in history.",
        clue_8="He's widely considered the greatest golfer of his generation, if not all time.",
    ),
    dict(
        sport=DailyPuzzle.Sport.GENERAL, category=DailyPuzzle.Category.PLAYER, difficulty=DailyPuzzle.Difficulty.HARD,
        answer="Michael Phelps", accepted_answers_extra="",
        clue_1="This athlete qualified for his first Olympics at age 15, the youngest male on his country's team in 68 years.",
        clue_2="He set his first world record less than a year after that Olympics.",
        clue_3="He competed in freestyle, butterfly, and individual medley events.",
        clue_4="He won eight gold medals at a single Olympics, a record for any athlete in any sport.",
        clue_5="Those eight golds came at the 2008 Beijing Games.",
        clue_6="He finished his career with 23 Olympic gold medals.",
        clue_7="He announced his final retirement after the 2016 Rio Olympics.",
        clue_8="He's widely regarded as the greatest Olympian of all time.",
    ),
    dict(
        sport=DailyPuzzle.Sport.MLB, category=DailyPuzzle.Category.PLAYER, difficulty=DailyPuzzle.Difficulty.HARD,
        answer="Babe Ruth", accepted_answers_extra="The Bambino, The Sultan of Swat",
        clue_1="This player broke into the majors as a star left-handed pitcher before switching positions.",
        clue_2="He was sold by the Boston Red Sox to the New York Yankees in an infamous 1919 transaction.",
        clue_3="That sale is often blamed for an 86-year championship drought for the team that sold him.",
        clue_4="He set the single-season home run record multiple times, eventually reaching 60 in 1927.",
        clue_5="That 60-home-run season came as part of a Yankees lineup nicknamed 'Murderer's Row.'",
        clue_6="He won seven World Series titles across his career.",
        clue_7="His career home run record stood for nearly 40 years until Hank Aaron broke it.",
        clue_8="He's nicknamed 'The Sultan of Swat' and 'The Bambino.'",
    ),
]


class Command(BaseCommand):
    help = "Seed '23 Guesses' puzzles for the next several weeks."

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
