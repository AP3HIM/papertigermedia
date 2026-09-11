"""Dynasty simulation engine.

Deliberately stateless. v6 adds: a salary cap with real contracts, an
expanded draft (more archetypes + draft classes with their own
personality), free agency and contextual trade offers folded into the
existing offseason-options screen, and a front-office philosophy picked
at game start that nudges a few numbers throughout the run. Builds on v5
(post-season Situations system, Hot Seat meter, positions mattering,
Finals spectacle).
"""

import datetime
import math
import random

FIRST_NAMES = [
    # --- Original List ---
    "Jaylen", "Marcus", "Tyree", "Devon", "Malik", "Xavier", "Isaiah", "Andre",
    "Darius", "Cameron", "Elijah", "Trevon", "Kendrick", "Jamal", "Deshawn",
    "Antoine", "Rashad", "Corey", "Terrence", "Jalen", "Buster", "Colt", "Spike",
    "Dash", "Ace", "Mack", "Duke", "Rex", "Flash", "Zane",

    # --- Retro Bowl & Video Game Style ---
    "Brick", "Blade", "Tank", "Diesel", "Laser", "Trigger", "Cruze", "Jax",
    "Ryder", "Wilder", "Rocco", "Zeke", "Axel", "Striker", "Gunner", "Gage",
    "Breaker", "Talon", "Knuckles", "Bane", "Riddick", "Shadow", "Titan",
    "Ranger", "Hunter", "Maverick", "Chaz", "Jolt", "Kodiak", "Vance",
    "Bodie", "Riot", "Grit", "Flint", "Dash", "Talon", "Bolo", "Ruger",

    # --- "Quantavious" & Elaborate Style ---
    "Quantavious", "Javarious", "D'Marcus", "De'Gario", "Kevonte", "Tremandous",
    "Marquise", "Jamarious", "Tequavious", "Ladarius", "Devonte", "Antavious",
    "Jacquavious", "Quintavious", "D'Anfernee", "Tyquavious", "Montavious",
    "Dontavious", "Rashardious", "Keyshawn", "Ja'Kobe", "Trevonte", "Deandreon",
    "Sir'Dominic", "Tymarious", "Zaquavious", "Demarquise", "Brycen", "Kavion", "D'Vontay",
    "Dreavious", "Kelavious", "Trayvond", "Maliquious", "Zavonte", "Kevondre"
]

LAST_NAMES = [
    # --- Original List ---
    "Cross", "Vale", "Holloway", "Reeves", "Sinclair", "Boateng", "Marsh",
    "Whitfield", "Okafor", "Prentice", "Larkin", "Bishop", "Calloway", "Marchetti",
    "Osei", "Delgado", "Hargrove", "Winslow", "Beaumont", "Trask", "Sledge",
    "Steele", "Gore", "Storm", "Gunn", "Blitz", "Cannon", "Stone", "Maddox", "Hardy",

    # --- Retro Bowl & Video Game Style ---
    "Iron", "Hammer", "Slaughter", "Powers", "Savage", "Grizzly", "Bullet",
    "Danger", "Wolf", "Brawler", "Frost", "Rage", "Bane", "Thunder", "Havoc",
    "Maverick", "Titan", "Viper", "Garrison", "Colt", "Ryder", "Crossfire",
    "Wild", "Blaze", "Flint", "Steel", "Brimstone", "Locke", "Chief", "Striker",
    "Overkill", "Wildcat", "Rex", "Rumble", "Talon", "Blackwood", "Frost", "Grimm",

    # --- Elaborate & Generated Style ---
    "Cunningham", "Washington", "Livingston", "Richardson", "Drummond", "Covington",
    "Valentin", "McDaniels", "Barrington", "Davenport", "Goldwire", "Blackshear",
    "Kingsley", "Archibald", "Taliaferro", "Pendergast", "Fontenot", "Gallagher",
    "Fitzroy", "Moncrief", "Bridgewater", "Harrington", "Ellington", "Kennington"
]

TRAIT_POOL = [
    "Athletic", "Mobile", "Leader", "High IQ", "Streaky", "Undersized",
    "Injury Prone", "Elite Shooter", "Lockdown Defender", "High Motor",
    "Raw", "Crafty", "Explosive", "Unselfish", "Volume Scorer",
    "Rim Protector", "Vocal", "Quiet Worker", "Clutch", "Inconsistent",
]
STAR_ACCOLADES = [
    "Former MVP", "2x All-Star", "3x All-NBA", "Former DPOY",
    "5x All-Star", "Scoring Champion", "Certified Bucket Getter", "Former Finals MVP",
]

POSITIONS = ["PG", "SG", "SF", "PF", "C"]
POSITION_BODY_RANGES = {
    "PG": {"height_in": (72, 76), "weight_lb": (170, 200)},
    "SG": {"height_in": (75, 79), "weight_lb": (190, 215)},
    "SF": {"height_in": (78, 81), "weight_lb": (210, 230)},
    "PF": {"height_in": (80, 83), "weight_lb": (225, 250)},
    "C": {"height_in": (82, 86), "weight_lb": (240, 270)},
}

ROSTER_SLOTS = ["core_1", "core_2", "core_3", "core_4", "core_5"]
PLAYOFF_ROUNDS = ["Round 1", "Round 2", "Conference Finals", "Finals"]
PLAYOFF_WIN_THRESHOLD = 42
TOTAL_SEASONS = 10
TOP_LOTTERY_CUTOFF = 4
RETIREMENT_AGE_FLOOR = 36

# Redundant positions are a real cost now — stacking 4 centers is a build,
# not a shortcut. A single backup at the same spot is normal roster
# construction and isn't penalized; 3+ at one position is where it bites.
POSITION_FULL_COVERAGE_BONUS = 2
POSITION_STACK_THRESHOLD = 3
POSITION_STACK_PENALTY_PER_PLAYER = 4

SLANDER_BEST = [
    "{name} threw a party the night before a back-to-back and the whole team knew about it by morning.",
    "{name} told a reporter he could \"do this in his sleep.\" Local radio has not let it go.",
    "{name} showed up to shootaround in a coat that cost more than three bench salaries combined.",
    "Ticket resale prices spike every time {name} is questionable. Scalpers love him more than fans do.",
    "{name} was overheard ordering the most expensive thing on the menu and tipping 9%.",
    "Drake shouted out {name} in his newest song: \"I don't need no help, I got {name} on my team.\"",
    "{name} was spotted at a local bar with a \"Free Agent of the Year\" sash. He was alone.",
    "{name} was seen at a local charity event, but he was only there for the free food.",
]
SLANDER_WORST = [
    "{name} got benched and the PA \"accidentally\" played a sad trombone. Ownership is investigating who authorized that.",
    "A kid asked {name} for an autograph and threw it in the trash in front of him.",
    "{name}'s jersey has been the only one on the clearance rack for six months straight.",
    "The scoreboard operator looped {name}'s worst play of the season during a TV timeout. Twice.",
    "Local sports radio has a running bit where they just sigh whenever {name}'s name comes up.",
    "A popular sports analyst said if {name} were a car, he'd be a Yugo. The team is considering legal action.",
    "The following tweet went viral: If I was in a room with a glass of water in my hand and {name} was on fire, I would drink the water and punch him.",
    "Lana Del Rey tweeted that {name} is \"the worst thing to happen to basketball since the shot clock.\"",
    "A local bar is offering a free drink to anyone who can name a single good thing about {name}.",
    "A local sports radio host said {name} is \"the kind of player who makes you miss the guy he replaced.\"",
    "Fans made a Wiggle.ai video of {name} speaking Chinese; the Guangzhou Loong Lions offered him a contract the next day. He declined.",
    "The local McDonalds reportedly reached out to {name} for a new job. No info at this moment on his decision.",
]

def _headline_for(name, pool):
    return random.choice(pool).format(name=name)

def generate_media_bundle(roster, team_name, season_result):
    """Structured 'this world is alive' content. Pure data — no images
    generated server-side. Frontend renders each item by `type` using
    team_theme() for colors, so nothing here is hand-designed per team."""
    ranked = sorted((s["player"] for s in roster if s["player"]), key=lambda p: p["ovr"], reverse=True)
    theme = team_theme(team_name)
    items = []

    if ranked:
        best, worst = ranked[0], ranked[-1]
        items.append({"type": "headline", "tone": "slander",
                       "headline": _headline_for(best["name"], SLANDER_BEST), "team_theme": theme})
        if worst is not best:
            items.append({"type": "headline", "tone": "slander",
                           "headline": _headline_for(worst["name"], SLANDER_WORST), "team_theme": theme})

    injured = [s["player"] for s in roster if s["player"] and s["player"].get("injury_note")]
    if injured:
        p = random.choice(injured)
        items.append({
            "type": "tweet",
            "handle": f"@{team_name.replace(' ', '')}Hoops",
            "text": f"Injury report: {p['name']} — {p['injury_note']}",
            "team_theme": theme,
        })

    for d in season_result.get("fa_departures", []):
        items.append({
            "type": "tweet",
            "handle": "@LeagueInsider",
            "text": f"BREAKING: {d['name']} ({d['ovr']} OVR) is signing elsewhere in free agency. "
                    f"{team_name} could not compete financially.",
            "team_theme": theme,
        })

    if season_result.get("champion"):
        items.append({
            "type": "newspaper",
            "headline": f"{team_name.upper()} ARE CHAMPIONS",
            "subhead": f"{season_result.get('finals_mvp', 'Your star')} named Finals MVP after "
                       f"a {season_result.get('series_score', '')} series win over "
                       f"the {season_result.get('opponent_name', 'the league')}.",
            "team_theme": theme,
        })

    return items



def _effective_depth_contribution(depth_rating):
    """Diminishing returns past ~70 — stacking bench investment every
    offseason can't out-scale actual star talent forever."""
    if depth_rating <= 70:
        return depth_rating
    return 70 + (depth_rating - 70) * 0.4

def compute_team_rating(roster, depth_rating, chemistry=65):
    core_ratings = [s["player"]["ovr"] for s in roster if s["player"]]
    core_avg = sum(core_ratings) / len(core_ratings) if core_ratings else 45
    rating = 0.75 * core_avg + 0.25 * _effective_depth_contribution(depth_rating)
    rating += _position_balance_adjustment(roster)
    rating += _chemistry_adjustment(chemistry)
    return round(max(20, min(99, rating)))
# --- Salary cap -------------------------------------------------------
SALARY_CAP = 140.0  # $M, soft — going over just eats your cap space

def salary_for_ovr(ovr):
    """Anchor points so a superstar costs real money and a bench guy
    costs almost nothing, with a little noise per player. Figures in $M."""
    anchors = [(55, 2.5), (65, 6), (75, 12), (82, 20), (88, 30), (94, 42), (99, 48)]
    if ovr <= anchors[0][0]:
        base = anchors[0][1]
    elif ovr >= anchors[-1][0]:
        base = anchors[-1][1]
    else:
        base = anchors[-1][1]
        for (lo_ovr, lo_sal), (hi_ovr, hi_sal) in zip(anchors, anchors[1:]):
            if lo_ovr <= ovr <= hi_ovr:
                t = (ovr - lo_ovr) / (hi_ovr - lo_ovr)
                base = lo_sal + t * (hi_sal - lo_sal)
                break
    return round(base * random.uniform(0.9, 1.1), 1)


def bench_salary_allocation(depth_rating):
    """Depth isn't modeled player-by-player, so its cap hit is
    approximated off the single depth_rating number."""
    return round(6 + (depth_rating / 99) * 24, 1)


def team_salary(roster, depth_rating):
    core = sum(s["player"].get("salary", 0) for s in roster if s["player"])
    return round(core + bench_salary_allocation(depth_rating), 1)


def cap_space(roster, depth_rating):
    return round(SALARY_CAP - team_salary(roster, depth_rating), 1)


# --- Front office philosophy -------------------------------------------
# Each one is a real trade-off, not a strict upgrade — "superteam" landing
# a star far more often is the whole identity, but it pays for that in
# free-agent/trade premiums and a much shorter ownership leash. Balance
# these together, not in isolation.
FRONT_OFFICE_PHILOSOPHIES = {
    "win_now": {
        "label": "WIN NOW",
        "note": "Veteran-friendly \u2014 free agents like joining you and vets develop a "
        "little longer, but your older players decline faster and get hurt more.",
        "dev_age_ceiling_delta": 3,
        "decline_age_start_delta": -2,
        "fa_discount": 0.9,
        "chase_a_star_success_delta": 0.0,
        "veteran_injury_bonus": 0.04,
    },
    "development": {
        "label": "DEVELOPMENT",
        "note": "Young players improve fastest and draft picks carry extra upside \u2014 but "
        "veterans want no part of a rebuild, so free agency runs expensive.",
        "young_dev_multiplier": 1.6,
        "fa_discount": 1.15,
        "chase_a_star_success_delta": -0.1,
        "draft_potential_bonus": 3,
    },
    "small_market": {
        "label": "SMALL MARKET",
        "note": "Cheap players develop better and your draft classes run deeper \u2014 but "
        "star free agents rarely call, and any star you land gets restless and may "
        "demand out.",
        "cheap_dev_bonus": True,
        "draft_class_ovr_bonus": 2,
        "chase_a_star_success_delta": -0.15,
        "fa_discount": 1.2,
        "star_flight_risk": True,
    },
    "superteam": {
        "label": "SUPERTEAM",
        "note": "Stars want to play for you and the blockbuster swing lands far more "
        "often \u2014 but everyone knows it, so free agents and trade partners charge "
        "you a premium, and anything short of a title puts you on the hot seat fast.",
        "chase_a_star_success_delta": 0.22,
        "fa_discount": 1.2,
        "trade_quality_delta": -2,
        "hot_seat_pressure": True,
    },
}

PLAYOFF_FLAVOR = [
    "Ticket prices creep up. Nobody's complaining yet.",
    "Merch sales are up. Ownership is pleased.",
    "The city actually shows up for the parade rumors.",
    "Your team's Twitter Community praises your actions. Keep it up.",
    "The team's social media account is trending. For once, it's not a disaster.",
    "The King of England praises your team.",
    "The mayor is considering a key to the city for your team.",
    "Tony Soprano is spotted at a game. He seems happy.",
    "Chet Holmgren rates your team as a 4/4 on his podcast and says he wants to play for you.",
    "Kevin Durant wants to join your team. He says he likes the city and the fans.",
]
DECENT_FLAVOR = [
    "Fans are cautiously optimistic. Cautiously.",
    "The arena's still mostly full. For now.",
    "Local radio is calling for a few changes. Just a few.",
    "Local schools are holding pep rallies for the team. That's a good sign.",
    "The team is so average that the city is whelmed."
    "Fans are already checking the playoff bubble standings with mild confusion.",
    "The team slogan this year is: We are technically competing.",
    "The post-game show spent twenty minutes discussing the parking lot traffic.",


]
BAD_FLAVOR = [
    "Ownership is \u201cexploring all options,\u201d which is never good.",
    "Tickets are basically free at this point.",
    "Local radio is calling for changes. All of them.",
    "Someone's mom skipped the game. That's how you know.",
    "A McDonald's Big Mac combo costs more than a ticket. That's not a good sign.",
    "Taco Bell is giving away free tacos to anyone who shows a ticket stub. Not many tacos were given out.",
    "The United Nations is considering sanctions against the city for how bad the team is.",
    "The mayor is considering a tax on the team for how bad they are. The mayor is considering a tax on the mayor for how bad the team is.",
    "Democrats and Republicans are both blaming each other for how bad the team is. The team is still bad.",
    "The team is so bad that even the mascot is considering quitting.",
    "Podcasts are protesting the team and refuse to cover them.",
    "Olivia Rodrigo said her song less is about the team. She said she wrote it after watching a game.",
    "Sabrina Carpenter is spotted at a game. She seems disappointed.",
]

OPPONENT_CITIES = [
    "Moscow", "Libjuana", "Basel", "Tundra City", "Port Halloway",
    "New Cascadia", "Redstone", "Vantage", "Ashport", "Cobalt Bay",
    "Glasswing", "Hartford Falls", "Northgate", "Silvermine", "Eastpoint",
    "Quicksilver", "Ironwood", "Frosthaven", "Shadowport", "Rivermouth",
]
OPPONENT_NICKNAMES = [
    "Cows", "Laptops", "Wolves", "Ironclads", "Marauders", "Static",
    "Vultures", "Anchors", "Foghorns", "Longshots", "Renegades",
    "Comets", "Drifters", "Watchmen", "Outlaws", "Sentinels", "Ravens", "Hawks", "Titans", "Vipers",
]

FIRST_NAME_HEADLINE_TAKES = [
    "is a flat earther",
    "won't eat anything that isn't beige",
    "thinks the moon landing was shot on a treadmill",
    "has never seen a Pixar movie and is proud of it",
    "believes his pregame ritual is the reason it doesn't rain",
    "has worn his lucky sock every game since 2012",
    "is convinced the team mascot is a spy for the other team",
    "hasn't seen a single episode of Game of Thrones and doesn't care",
    "hasn't drank water since 2015 and is thriving",
    "needs to poop but refuses to leave the locker room until after the game",
    "thinks the team bus is a time machine and refuses to get off",
    "started a podcast about his favorite type of cheese and it has 3 million listeners",
    "doesn't believe in gravity and is still somehow playing basketball",
    "hates spoons and refuses to use them, even for soup",
]


def random_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def random_team_name():
    return f"{random.choice(OPPONENT_CITIES)} {random.choice(OPPONENT_NICKNAMES)}"


def format_height(total_inches):
    feet, inches = divmod(total_inches, 12)
    return f"{feet}'{inches}\""


def generate_prospect_profile():
    position = random.choice(POSITIONS)
    body = POSITION_BODY_RANGES[position]
    return {
        "name": random_name(),
        "position": position,
        "height": format_height(random.randint(*body["height_in"])),
        "weight": random.randint(*body["weight_lb"]),
        "traits": random.sample(TRAIT_POOL, 2),
    }


def make_player(ovr, age, potential=None, profile=None, origin="", salary=None):
    profile = profile or generate_prospect_profile()
    return {
        "name": profile["name"],
        "position": profile["position"],
        "height": profile["height"],
        "weight": profile["weight"],
        "traits": profile["traits"],
        "age": age,
        "ovr": ovr,
        "potential": potential if potential is not None else min(99, ovr + random.randint(0, 12)),
        "origin": origin,
        "injury_note": None,
        "salary": salary if salary is not None else salary_for_ovr(ovr),
    }


def new_starting_roster():
    """The bad team you inherit: 4 holdover vets across 4 distinct positions
    + one open slot for the incoming top pick. Not uniformly mediocre —
    one legitimately solid piece, two average-to-below guys, and one
    genuine weak link, the way even a lottery team usually has at least
    one player worth building around."""
    positions = random.sample(POSITIONS, 4)
    ovr_bands = [(73, 78), (60, 66), (55, 61), (48, 54)]
    random.shuffle(ovr_bands)
    vets = [
        make_player(
            ovr=random.randint(*band),
            age=random.randint(22, 31),
            profile={**generate_prospect_profile(), "position": pos},
            origin="Holdover",
        )
        for pos, band in zip(positions, ovr_bands)
    ]
    # Correct height/weight now that position was overridden after profile gen.
    for v in vets:
        body = POSITION_BODY_RANGES[v["position"]]
        v["height"] = format_height(random.randint(*body["height_in"]))
        v["weight"] = random.randint(*body["weight_lb"])

    random.choice(vets)["injury_note"] = (
        "Recovering from injury — expected back at full strength next season."
    )

    return [
        {"slot": "core_1", "player": None},
        {"slot": "core_2", "player": vets[0]},
        {"slot": "core_3", "player": vets[1]},
        {"slot": "core_4", "player": vets[2]},
        {"slot": "core_5", "player": vets[3]},
    ]


DRAFT_ARCHETYPES = [
    {
        "id": "safe",
        "label": "The Safe Pick",
        "blurb": "High floor, limited ceiling. Whatever you see is close to what you get.",
        "ovr_range": (72, 78),
        "potential_bonus_range": (0, 6),
    },
    {
        "id": "balanced",
        "label": "The Balanced Prospect",
        "blurb": "Solid tools across the board. No red flags, no obvious star trait either.",
        "ovr_range": (68, 76),
        "potential_bonus_range": (6, 14),
    },
    {
        "id": "boom_bust",
        "label": "The Boom-or-Bust Swing",
        "blurb": "Scouts are split. Could be a franchise piece — could be out of the league in three years.",
        "ovr_range": (60, 88),
        "potential_bonus_range": (0, 16),
    },
    {
        "id": "international",
        "label": "The International Mystery",
        "blurb": "Big overseas numbers, thin scouting reports. Nobody's totally sure what "
        "translates to the NBA.",
        "ovr_range": (62, 90), "potential_bonus_range": (0, 18),
    },
    {
        "id": "old_man_knees",
        "label": "Old Man Knees, High Potential",
        "blurb": "Freak talent, but he already moves like a 30-year-old. Either a steal or a "
        "medical redshirt.",
        "ovr_range": (65, 80), "potential_bonus_range": (8, 16),
    },
    {
        "id": "acl_recovery",
        "label": "Coming Off an ACL Tear",
        "blurb": "Would've been a lottery lock healthy. Falls in the draft purely on the knee.",
        "ovr_range": (55, 70), "potential_bonus_range": (10, 18),
    },
    {
        "id": "aging_high_iq",
        "label": "The 23-Year-Old Rookie",
        "blurb": "Four years overseas or in a weird league. Ready to contribute now, not much "
        "runway left to grow.",
        "ovr_range": (70, 80), "potential_bonus_range": (0, 3),
    },
]

DRAFT_CLASSES = {
    "generational": {
        "label": "THE GENERATIONAL CLASS",
        "note": "Scouts won't shut up about one name in this class.",
        "ovr_bonus": 8,
    },
    "deep": {
        "label": "THE DEEP CLASS",
        "note": "No superstar, but the floor on every prospect is higher than usual.",
        "ovr_bonus": 3,
    },
    "weak": {
        "label": "THE WEAK CLASS",
        "note": "Scouts are already calling this one a bust year.",
        "ovr_bonus": -6,
    },
    "guard_heavy": {
        "label": "THE GUARD CLASS",
        "note": "Loaded at point guard and shooting guard. Thin everywhere else.",
        "ovr_bonus": 0,
        "position_bias": ["PG", "SG"],
    },
    "big_man": {
        "label": "THE BIG MAN CLASS",
        "note": "A rare year where the best prospects are all up front.",
        "ovr_bonus": 0,
        "position_bias": ["PF", "C"],
    },
}


def roll_draft_class():
    weights = {"generational": 1, "deep": 3, "weak": 3, "guard_heavy": 2, "big_man": 2}
    ids = list(weights.keys())
    return random.choices(ids, weights=[weights[i] for i in ids])[0]


def _missing_position(roster):
    """The one position (if any) not currently on the roster — used to
    nudge draft/depth prospects toward what the team actually needs."""
    held = {s["player"]["position"] for s in roster if s["player"]}
    missing = [p for p in POSITIONS if p not in held]
    return random.choice(missing) if missing else None


def compute_lottery_pick(wins):
    min_wins, max_wins = 5, PLAYOFF_WIN_THRESHOLD - 1
    span = max(1, max_wins - min_wins)
    raw = 1 + (wins - min_wins) / span * (14 - 1)
    pick = round(raw)
    pick += random.choice([-2, -1, -1, 0, 0, 0, 1, 1, 2])
    return max(1, min(14, pick))


def generate_draft_options(pick_number, roster=None, draft_class=None, philosophy=None):
    draft_year = datetime.date.today().year
    archetypes = DRAFT_ARCHETYPES if pick_number <= TOP_LOTTERY_CUTOFF else [
        a for a in DRAFT_ARCHETYPES if a["id"] != "boom_bust"
    ]
    class_info = DRAFT_CLASSES.get(draft_class, {})
    phil_info = FRONT_OFFICE_PHILOSOPHIES.get(philosophy, {})
    need = _missing_position(roster) if roster else None
    position_bias = class_info.get("position_bias")
    ovr_bonus = class_info.get("ovr_bonus", 0) + phil_info.get("draft_class_ovr_bonus", 0)

    options = []
    for arch in archetypes:
        profile = generate_prospect_profile()
        profile["chemistry_preview"] = max(-6, min(6, _trait_chemistry_base(profile["traits"])))
        target_pos = None
        if position_bias and random.random() < 0.5:
            target_pos = random.choice(position_bias)
        elif need and random.random() < 0.6:
            target_pos = need
        if target_pos:
            profile["position"] = target_pos
            body = POSITION_BODY_RANGES[target_pos]
            profile["height"] = format_height(random.randint(*body["height_in"]))
            profile["weight"] = random.randint(*body["weight_lb"])
        profile["age"] = random.randint(19, 22)
        profile["origin"] = f"{draft_year} \u00b7 R1 Pick {pick_number}"
        profile["draft_class_ovr_bonus"] = ovr_bonus
        options.append({
            "id": arch["id"], "type": "draft", "label": arch["label"], "blurb": arch["blurb"],
            "prospect": profile,
        })

    vet_profile = generate_prospect_profile()
    vet_profile["age"] = random.randint(28, 34)
    vet_profile["origin"] = "Trade"
    options.append({
        "id": "trade_for_veteran",
        "type": "trade",
        "label": "Trade the Pick",
        "blurb": "Ship the pick for an established veteran — ready to contribute now, "
        "though wear and tear is a question mark.",
        "prospect": vet_profile,
    })
    return options


def _build_chase_a_star_option():
    profile = generate_prospect_profile()
    profile["age"] = random.randint(30, 37)
    profile["accolade"] = random.choice(STAR_ACCOLADES)
    profile["origin"] = "Trade"
    return {
        "id": "chase_a_star",
        "type": "trade_up",
        "label": "Chase a Star",
        "blurb": f"{profile['name']} ({profile['accolade']}, age {profile['age']}) might be "
        "available. A blockbuster swing — might not pan out, and he won't be this good forever.",
        "prospect": profile,
    }


def generate_free_agent_options(cap_space_amount, philosophy=None):
    """0-3 offers, filtered to what you can actually afford — the tension
    comes from watching your cap space shrink as you consider one, not
    from being shown deals you can never take."""
    if cap_space_amount < 3:
        return []

    phil_info = FRONT_OFFICE_PHILOSOPHIES.get(philosophy, {})
    discount = phil_info.get("fa_discount", 1.0)

    count = 1 if cap_space_amount < 12 else (2 if cap_space_amount < 25 else 3)
    options = []
    used_ovrs = set()
    for _ in range(count):
        ovr = random.randint(58, min(92, 60 + int(cap_space_amount)))
        for _try in range(6):
            if ovr not in used_ovrs:
                break
            ovr = random.randint(58, min(92, 60 + int(cap_space_amount)))
        used_ovrs.add(ovr)

        profile = generate_prospect_profile()
        age = random.randint(23, 33)
        salary = round(salary_for_ovr(ovr) * discount, 1)
        if salary > cap_space_amount:
            salary = round(cap_space_amount * random.uniform(0.7, 0.95), 1)
        years = random.choice([1, 2, 3, 4])
        profile["age"] = age
        profile["origin"] = "Free Agency"
        options.append({
            "id": f"sign_fa_{len(options)}", "type": "free_agent",
            "label": f"Sign {profile['name']}",
            "blurb": f"{ovr} OVR {profile['position']} \u00b7 asking ${salary}M / {years}"
            f" yr{'s' if years > 1 else ''}.",
            "prospect": {**profile, "ovr_hint": ovr},
        })
    return options


def _trade_give_candidates(roster, incoming_position, contending):
    """Players you could plausibly send back, ranked best-default-first —
    and handed to the frontend so the PERSON picks who leaves, instead of
    the engine silently deciding. Same-position depth comes first (a real
    positional swap when you've got it); after that, the weakest player on
    a contender's roster or the best trade chip on a rebuilder's; capped
    at 3 so it's a real choice, not a dropdown of the whole roster."""
    filled = [s for s in roster if s["player"]]
    if not filled:
        return []

    same_pos = sorted(
        (s for s in filled if s["player"]["position"] == incoming_position),
        key=lambda s: s["player"]["ovr"],
    )
    by_ovr = sorted(filled, key=lambda s: s["player"]["ovr"])
    rest = by_ovr if contending else list(reversed(by_ovr))

    ordered, seen = [], set()
    for s in list(same_pos) + rest:
        if s["slot"] in seen:
            continue
        seen.add(s["slot"])
        ordered.append(s)

    return [
        {"slot": s["slot"], "name": s["player"]["name"],
         "position": s["player"]["position"], "ovr": s["player"]["ovr"]}
        for s in ordered[:3]
    ]

TRADE_SWING_RANGES = [(-18, -8), (-6, 2), (3, 8)]
TRADE_SWING_WEIGHTS = [25, 55, 20]

def _roll_trade_swing():
    lo, hi = random.choices(TRADE_SWING_RANGES, weights=TRADE_SWING_WEIGHTS)[0]
    return random.randint(lo, hi)

TRAIT_CHEMISTRY_IMPACT = {
    "Leader": 3, "Vocal": 2, "Unselfish": 2, "High IQ": 1, "Lockdown Defender": 1,
    "Quiet Worker": 1, "Clutch": 1, "High Motor": 1,
    "Streaky": -1, "Inconsistent": -1, "Injury Prone": -1, "Volume Scorer": -2,
}

def _trait_chemistry_base(traits):
    return sum(TRAIT_CHEMISTRY_IMPACT.get(t, 0) for t in traits)

def player_chemistry_impact(player):
    """Net chemistry delta a player brings when added to the roster.
    Stars (85+ OVR) carry double weight, good or bad — they set the
    locker-room tone more than a bench piece does."""
    if not player:
        return 0
    base = _trait_chemistry_base(player.get("traits", []))
    if player.get("ovr", 0) >= 85:
        base *= 2
    return max(-6, min(6, base))


def generate_trade_offer(roster, contending, philosophy=None, exclude_slots=None):
    """The player you'd give up IS the anchor for the incoming player's
    value — a contender ships its weakest piece for a vet near that same
    value; a rebuilder ships its best veteran for a young player near
    that same value. Most offers land near-fair or a little light; a
    real overpay is the exception, and lowballs are common."""
    filled = [s for s in roster if s["player"]]
    exclude_slots = exclude_slots or set()
    filled = [s for s in filled if s["slot"] not in exclude_slots]
    if not filled:
        return None

    phil_info = FRONT_OFFICE_PHILOSOPHIES.get(philosophy, {})
    quality_bonus = phil_info.get("trade_quality_delta", 0)

    if contending:
        give = min(filled, key=lambda s: s["player"]["ovr"])
        flavor = "is interested in your bench piece for a proven vet who can help right now."
        incoming_age = random.randint(28, 35)
    else:
        give = max(filled, key=lambda s: s["player"]["ovr"])
        flavor = "wants your veteran for a young player who fits a rebuild timeline."
        incoming_age = random.randint(20, 26)

    anchor_ovr = give["player"]["ovr"]
    swing = _roll_trade_swing()
    incoming_ovr = max(35, min(99, anchor_ovr + swing + round(quality_bonus)))

    suitor = random_team_name()
    incoming_profile = generate_prospect_profile()
    incoming_profile["age"] = incoming_age
    incoming_player = make_player(
        ovr=incoming_ovr, age=incoming_age, profile=incoming_profile, origin="Trade"
    )
    incoming_player["chemistry_preview"] = player_chemistry_impact(incoming_player)

    return {
        "id": "accept_trade_offer",
        "type": "trade_offer",
        "label": f"The {suitor} Offer",
        "blurb": f"The {suitor} {flavor} They're offering {incoming_player['name']} "
        f"({incoming_ovr} OVR {incoming_player['position']}) for "
        f"{give['player']['name']} ({anchor_ovr} OVR).",
        "trade_give_slot": give["slot"],
        "prospect": incoming_player,
    }

def _generate_trade_offers(roster, contending, philosophy=None):
    offers = []
    first = generate_trade_offer(roster, contending, philosophy)
    if not first:
        return offers
    first["id"] = "accept_trade_offer_0"
    offers.append(first)

    second_chance = 0.35 if contending else 0.22
    if random.random() < second_chance:
        second = generate_trade_offer(
            roster, contending, philosophy,
            exclude_slots={first["trade_give_slot"]},
        )
        if second and second["blurb"] != first["blurb"]:
            second["id"] = "accept_trade_offer_1"
            offers.append(second)
    return offers


def generate_offseason_options(made_playoffs, wins, roster, depth_rating=40, draft_class=None,
                                philosophy=None, cap_multiplier=1.0):
    space = round(cap_space(roster, depth_rating) * cap_multiplier, 1)
    trade_offers = _generate_trade_offers(roster, contending=made_playoffs, philosophy=philosophy)

    if not made_playoffs:
        pick_number = compute_lottery_pick(wins)
        options = generate_draft_options(pick_number, roster, draft_class, philosophy)
        options += generate_free_agent_options(space, philosophy)
        options += trade_offers
        return {"pick_number": pick_number, "options": options}

    best = max((s["player"] for s in roster if s["player"]), key=lambda p: p["ovr"], default=None)
    run_it_back_blurb = (
        f"Keep this exact group — led by {best['name']} — together for one more year."
        if best else "Keep the roster as-is. Stability has value."
    )
    depth_names = [random_name(), random_name()]

    options = [
        {"id": "run_it_back", "type": "hold", "label": "Run It Back", "blurb": run_it_back_blurb},
        _build_chase_a_star_option(),
        {
            "id": "invest_in_depth",
            "type": "depth",
            "label": "Invest in Depth",
            "blurb": f"Sign {depth_names[0]} and {depth_names[1]} off the open market. "
            "Raises your floor, not your ceiling.",
            "depth_signees": depth_names,
        },
    ]
    options += generate_free_agent_options(space, philosophy)
    options += trade_offers
    return {"pick_number": None, "options": options}


KNEES_TAG = " \u00b7 Chronic Knees"


def _resolve_draft_choice(choice_id, prospect):
    if choice_id == "trade_for_veteran":
        ovr = random.randint(78, 85)
        potential = ovr
    else:
        arch = next(a for a in DRAFT_ARCHETYPES if a["id"] == choice_id)
        lo, hi = arch["ovr_range"]
        ovr = random.randint(lo, hi)
        ovr = max(35, min(99, ovr + prospect.get("draft_class_ovr_bonus", 0)))
        potential = min(99, ovr + random.randint(*arch["potential_bonus_range"]))

    origin = prospect.get("origin", "")
    if choice_id == "old_man_knees":
        origin = f"{origin}{KNEES_TAG}"

    return {
        "name": prospect["name"], "position": prospect["position"], "height": prospect["height"],
        "weight": prospect["weight"], "traits": prospect["traits"], "age": prospect["age"],
        "ovr": ovr, "potential": potential, "origin": origin,
        "injury_note": None, "salary": salary_for_ovr(ovr),
    }


def _weakest_slot(roster, protected_slots=None):
    """Prefer replacing the weakest player at the *most duplicated*
    position — that's how a roster actually corrects a 4-centers problem
    instead of just swapping in a 5th one. `protected_slots` excludes
    slots already filled earlier in the SAME offseason batch, so signing
    two free agents in one turn can't have the second immediately
    overwrite the first. Position-agnostic — use this only when the
    incoming move has no position of its own (e.g. a forced cap-driven
    release). Anything bringing in an actual player should go through
    `_target_slot_for_position` instead."""
    protected_slots = protected_slots or set()
    candidates = [s for s in roster if s["slot"] not in protected_slots]
    if not candidates:
        candidates = roster  # every slot protected — fall back to all

    counts = {}
    for s in roster:
        if s["player"]:
            counts[s["player"]["position"]] = counts.get(s["player"]["position"], 0) + 1

    filled_dupes = [s for s in candidates if s["player"] and counts.get(s["player"]["position"], 1) > 1]
    if filled_dupes:
        return min(filled_dupes, key=lambda s: s["player"]["ovr"])
    return min(candidates, key=lambda s: s["player"]["ovr"] if s["player"] else -1)


def _target_slot_for_position(roster, position, protected_slots=None):
    """Where a new player of `position` actually lands. Positions matter
    now: an incoming SF replaces your current SF first, full stop — it
    doesn't get routed to whichever slot happens to be weakest overall.
    That's how a roster ends up with three centers by accident. Order of
    preference:
      1. The weakest player already AT that position (a real swap).
      2. An empty slot (new coverage at a position you're missing).
      3. The weakest player at whatever position is already stacked
         2+ deep (trims a redundant duplicate to make room).
      4. Only as a last resort, the single weakest player anywhere.
    `protected_slots` excludes slots already touched earlier in the same
    offseason batch."""
    protected_slots = protected_slots or set()
    candidates = [s for s in roster if s["slot"] not in protected_slots]
    if not candidates:
        candidates = roster

    same_position = [s for s in candidates if s["player"] and s["player"]["position"] == position]
    if same_position:
        return min(same_position, key=lambda s: s["player"]["ovr"])

    empty = [s for s in candidates if s["player"] is None]
    if empty:
        return empty[0]

    counts = {}
    for s in roster:
        if s["player"]:
            counts[s["player"]["position"]] = counts.get(s["player"]["position"], 0) + 1
    dupes = [s for s in candidates if s["player"] and counts.get(s["player"]["position"], 1) > 1]
    if dupes:
        return min(dupes, key=lambda s: s["player"]["ovr"])

    return min(candidates, key=lambda s: s["player"]["ovr"] if s["player"] else -1)


def resolve_offseason_choice(
    choice_id, roster, depth_rating, prospect=None, depth_signees=None,
    trade_give_slot=None, chemistry=65, philosophy=None, protected_slots=None,
):
    notes = []
    changed_slot = None
    phil_info = FRONT_OFFICE_PHILOSOPHIES.get(philosophy, {})

    def _apply_new_player_chemistry(new_player):
        nonlocal chemistry
        delta = player_chemistry_impact(new_player)
        chemistry = max(0, min(99, chemistry + delta))
        if delta > 0:
            notes.append(f"{new_player['name']} fits right in — chemistry +{delta}.")
        elif delta < 0:
            notes.append(f"{new_player['name']} takes some adjusting to — chemistry {delta}.")

    if choice_id in ("safe", "balanced", "boom_bust", "international", "old_man_knees",
                      "acl_recovery", "aging_high_iq", "trade_for_veteran"):
        if prospect is None:
            prospect = generate_prospect_profile()
            prospect["age"] = random.randint(19, 22)
            prospect["origin"] = ""
        new_player = _resolve_draft_choice(choice_id, prospect)
        if philosophy == "development":
            new_player["potential"] = min(99, new_player["potential"] + phil_info.get("draft_potential_bonus", 0))
        target = _target_slot_for_position(roster, new_player["position"], protected_slots)
        old = target["player"]
        target["player"] = new_player
        changed_slot = target["slot"]
        if old:
            notes.append(f"{old['name']} moves on. {new_player['name']} steps into the lineup.")
        else:
            notes.append(f"{new_player['name']} joins the roster.")
        _apply_new_player_chemistry(new_player)

    elif choice_id == "run_it_back":
        notes.append("The front office stands pat.")

    elif choice_id == "chase_a_star":
        success_chance = 0.45 + phil_info.get("chase_a_star_success_delta", 0)
        if prospect and random.random() < success_chance:
            ovr = random.randint(83, 93)
            new_player = {
                "name": prospect["name"], "position": prospect["position"], "height": prospect["height"],
                "weight": prospect["weight"], "traits": prospect["traits"], "age": prospect["age"],
                "ovr": ovr, "potential": ovr, "origin": "Trade", "injury_note": None,
                "salary": salary_for_ovr(ovr),
            }
            target = _target_slot_for_position(roster, new_player["position"], protected_slots)
            old = target["player"]
            target["player"] = new_player
            changed_slot = target["slot"]
            old_name = old["name"] if old else "a roster spot"
            notes.append(f"The trade lands. {new_player['name']} joins the roster — {old_name} is dealt away.")
            _apply_new_player_chemistry(new_player)
        else:
            star_name = prospect["name"] if prospect else "The star"
            depth_rating = max(0, depth_rating - 8)
            notes.append(f"The {star_name} talks collapse. He signs elsewhere for more money.")

    elif choice_id == "invest_in_depth":
        depth_rating = min(99, depth_rating + random.randint(8, 14))
        names = depth_signees if depth_signees else [random_name(), random_name()]
        notes.append(f"{names[0]} and {names[1]} sign on as depth pieces off the bench.")

    elif choice_id.startswith("sign_fa"):
        if prospect is None:
            raise ValueError("Free agent signing is missing prospect data.")
        target = _target_slot_for_position(roster, prospect["position"], protected_slots)
        old = target["player"]
        new_player = make_player(
            ovr=prospect.get("ovr_hint", 65), age=prospect["age"], profile=prospect, origin="Free Agency",
        )
        target["player"] = new_player
        changed_slot = target["slot"]
        old_name = old["name"] if old else "a roster spot"
        notes.append(f"{new_player['name']} signs as a free agent, ${new_player['salary']}M on the books. "
                      f"{old_name} is waived to make room.")
        _apply_new_player_chemistry(new_player)

    elif choice_id.startswith("accept_trade_offer"):
        if prospect is None:
            raise ValueError("Trade offer is missing incoming player data.")
        protected_slots = protected_slots or set()
        target = None
        if trade_give_slot and trade_give_slot not in protected_slots:
            target = next((s for s in roster if s["slot"] == trade_give_slot), None)
        if target is None:
            target = _target_slot_for_position(roster, prospect["position"], protected_slots)
        old = target["player"]
        target["player"] = prospect
        changed_slot = target["slot"]
        old_name = old["name"] if old else "a roster spot"
        notes.append(f"The trade goes through. {prospect['name']} joins the roster — {old_name} is dealt away.")
        _apply_new_player_chemistry(prospect)

    else:
        raise ValueError(f"Unknown choice_id: {choice_id!r}")

    return roster, depth_rating, chemistry, notes, changed_slot

def resolve_offseason_choices(choices, roster, depth_rating, chemistry=65, philosophy=None):
    all_notes = []
    protected_slots = set()
    for choice in choices:
        choice_id = choice.get("id") or choice.get("choice_id")
        if not choice_id:
            continue
        roster, depth_rating, chemistry, notes, changed_slot = resolve_offseason_choice(
            choice_id, roster, depth_rating,
            prospect=choice.get("prospect"),
            depth_signees=choice.get("depth_signees"),
            trade_give_slot=choice.get("trade_give_slot"),
            chemistry=chemistry,
            philosophy=philosophy,
            protected_slots=protected_slots,
        )
        if changed_slot:
            protected_slots.add(changed_slot)
        all_notes.extend(notes)

    if not all_notes:
        all_notes.append("The front office stands pat.")
    return roster, depth_rating, chemistry, all_notes


def age_and_develop(roster, philosophy=None):
    phil_info = FRONT_OFFICE_PHILOSOPHIES.get(philosophy, {})
    dev_ceiling = 26 + phil_info.get("dev_age_ceiling_delta", 0)
    decline_start = 31 + phil_info.get("decline_age_start_delta", 0)
    young_mult = phil_info.get("young_dev_multiplier", 1.0)
    cheap_dev_bonus = phil_info.get("cheap_dev_bonus", False)
    veteran_injury_bonus = phil_info.get("veteran_injury_bonus", 0.0)

    notes = []
    for slot in roster:
        p = slot["player"]
        if p is None:
            continue

        p["age"] += 1

        if p["age"] >= RETIREMENT_AGE_FLOOR:
            retire_chance = min(0.6, 0.10 + (p["age"] - RETIREMENT_AGE_FLOOR) * 0.08)
            if random.random() < retire_chance:
                notes.append(f"{p['name']} calls it a career and retires. The roster spot is open.")
                slot["player"] = None
                continue

        if p["injury_note"]:
            p["injury_note"] = None
            notes.append(f"{p['name']} is back to full strength.")

        knees = KNEES_TAG in p.get("origin", "")

        if p["age"] <= dev_ceiling and p["ovr"] < p["potential"]:
            gain = random.randint(1, 4)
            if cheap_dev_bonus and p.get("salary", 0) < 10:
                gain += 1
            gain = round(gain * young_mult)
            p["ovr"] = min(p["potential"], p["ovr"] + gain)
        elif p["age"] >= decline_start:
            decline = random.randint(1, 5)
            if knees:
                decline += random.randint(1, 3)
            p["ovr"] = max(35, p["ovr"] - decline)

        if random.random() < 0.06 and p["ovr"] < 90:
            jump = random.randint(6, 12)
            p["ovr"] = min(96, p["ovr"] + jump)
            p["potential"] = max(p["potential"], p["ovr"])
            notes.append(f"{p['name']} breaks out, jumping to a {p['ovr']} overall.")

        injury_chance = 0.07 + (veteran_injury_bonus if p["age"] >= decline_start else 0.0)
        injury_chance += 0.05 if knees else 0.0
        if random.random() < injury_chance:
            p["injury_note"] = "Banged up — playing through it this season."
            notes.append(f"{p['name']} is dealing with an injury.")

    return notes


def _position_balance_adjustment(roster):
    """Small bonus for full 5-position coverage. A single backup at a
    position (count of 2) is normal roster-building and costs nothing —
    the real penalty only kicks in once a position is stacked 3+ deep,
    which is what makes "just draft four centers" an actual mistake."""
    positions = [s["player"]["position"] for s in roster if s["player"]]
    if not positions:
        return 0
    counts = {}
    for pos in positions:
        counts[pos] = counts.get(pos, 0) + 1

    if len(counts) == 5:
        return POSITION_FULL_COVERAGE_BONUS

    over = sum(
        (c - POSITION_STACK_THRESHOLD + 1) for c in counts.values() if c >= POSITION_STACK_THRESHOLD
    )
    return -(over * POSITION_STACK_PENALTY_PER_PLAYER)


def _chemistry_adjustment(chemistry):
    """A small nudge, not a second cap — locker-room chemistry shouldn't
    swing a season the way roster talent does, but a genuinely toxic or
    genuinely tight locker room should be visible on the scoreboard."""
    if chemistry >= 80:
        return 3
    if chemistry <= 20:
        return -5
    if chemistry <= 40:
        return -2
    return 0

def simulate_regular_season(team_rating):
    """Logistic curve centered so an average roster (~62 rating) plays
    like a .500 team. Requires real, sustained roster quality — not one
    lucky pick — to reach 50+ win seasons."""
    z = (team_rating - 62) / 7
    sigmoid = 1 / (1 + math.exp(-z))
    win_pct = 0.08 + sigmoid * 0.80
    wins = round(win_pct * 82 + random.uniform(-5, 5))
    wins = max(3, min(76, wins))
    return wins, 82 - wins


def simulate_playoffs(team_rating, wins):
    if wins < PLAYOFF_WIN_THRESHOLD:
        return {"made_playoffs": False, "result": "Missed Playoffs", "champion": False}

    for round_name in PLAYOFF_ROUNDS:
        opponent_rating = max(30, min(99, random.gauss(60, 14)))
        diff = team_rating - opponent_rating
        win_prob = 1 / (1 + math.exp(-diff / 12))
        if random.random() > win_prob:
            return {"made_playoffs": True, "result": f"Lost in {round_name}", "champion": False}

    return {"made_playoffs": True, "result": "NBA Champions", "champion": True}


def _finals_spectacle(roster):
    """Named opponent, a real series score, and a Finals MVP pulled from
    the actual roster — the champion result should feel like an event."""
    best = max((s["player"] for s in roster if s["player"]), key=lambda p: p["ovr"], default=None)
    mvp_name = best["name"] if best else "Your best player"
    opponent = random_team_name()
    games_against = random.choice([1, 2, 3])  # series ends 4-1, 4-2, or 4-3
    return {
        "opponent_name": opponent,
        "series_score": f"4\u2013{games_against}",
        "finals_mvp": mvp_name,
    }


def _flavor_note(season_result, roster, last_flavor=None):
    if season_result["champion"]:
        best = max((s["player"] for s in roster if s["player"]), key=lambda p: p["ovr"], default=None)
        name = best["name"] if best else "the whole roster"
        pool = [
            f"The parade route is already blocked off downtown \u2014 {name} leads the celebration.",
            f"Ownership quietly orders a bigger trophy case for the {name}-led champions.",
            f"Local news leads with you for a change, {name} on every front page.",
            f"Fans are already petitioning for a statue of {name} outside the arena.",
            f"Jimmy Fallon wants {name} on his show. He says he has a great sense of humor.",
            f"Kevin Durant tweets that {name} is the best player in the league and he wants to play for you.",
        ]
    elif season_result["made_playoffs"]:
        pool = PLAYOFF_FLAVOR
    elif season_result["wins"] >= 32:
        pool = DECENT_FLAVOR
    else:
        pool = BAD_FLAVOR

    choices = [line for line in pool if line != last_flavor] or pool
    return random.choice(choices)


def _fan_support_delta(season_result):
    if season_result["champion"]:
        return 20
    if season_result["made_playoffs"]:
        return 8
    if season_result["wins"] >= 35:
        return 2
    if season_result["wins"] >= 20:
        return -8
    return -16


def _hot_seat_delta(season_result, philosophy=None):
    phil_info = FRONT_OFFICE_PHILOSOPHIES.get(philosophy, {})
    pressure = phil_info.get("hot_seat_pressure", False)
    if season_result["champion"]:
        return -15
    if season_result["made_playoffs"]:
        return -2 if pressure else -5
    if season_result["wins"] >= 35:
        return 6 if pressure else 0
    if season_result["wins"] >= 20:
        return 14 if pressure else 6
    return 20 if pressure else 12

FA_DEPARTURE_OVR_FLOOR = 88
FA_DEPARTURE_BASE_CHANCE = 0.05

def _fa_poaching_departures(roster, philosophy=None):
    """Season-end chance a bona fide star walks for more money elsewhere.
    No user choice, same beat as retirement — it just happens and the
    note says so. Only fires on players good enough to have real market
    demand and young enough that it isn't just a retirement in disguise."""
    departures = []
    for slot in roster:
        p = slot["player"]
        if p is None or p["ovr"] < FA_DEPARTURE_OVR_FLOOR or p["age"] >= RETIREMENT_AGE_FLOOR:
            continue
        chance = FA_DEPARTURE_BASE_CHANCE + max(0, p["ovr"] - FA_DEPARTURE_OVR_FLOOR) * 0.01
        if philosophy == "small_market":
            chance += 0.05  # can't hold onto stars once they're proven
        if random.random() < chance:
            departures.append({"name": p["name"], "ovr": p["ovr"], "position": p["position"]})
            slot["player"] = None
    return departures

def team_theme(team_name):
    seed = sum(ord(c) for c in team_name) + len(team_name) * 17
    hue = seed % 360
    return {
        "primary": f"hsl({hue}, 65%, 35%)",
        "secondary": f"hsl({(hue + 40) % 360}, 55%, 45%)",
        "hue": hue,
    }

def simulate_season(roster, depth_rating, season_number, philosophy=None, chemistry=65):
    dev_notes = age_and_develop(roster, philosophy)
    fa_departures = _fa_poaching_departures(roster, philosophy)
    for d in fa_departures:
        dev_notes.append(
            f"{d['name']} ({d['ovr']} overall) leaves in free agency for more money. "
            "There was nothing the front office could do."
        )
    rating = compute_team_rating(roster, depth_rating, chemistry)
    wins, losses = simulate_regular_season(rating)
    playoff = simulate_playoffs(rating, wins)

    result = {
        "season_number": season_number,
        "team_rating": rating,
        "wins": wins,
        "losses": losses,
        "result": playoff["result"],
        "champion": playoff["champion"],
        "made_playoffs": playoff["made_playoffs"],
        "notes": dev_notes,
        "fa_departures": fa_departures,
    }
    if playoff["champion"]:
        result.update(_finals_spectacle(roster))
    return result


# --- Post-season situations. Pure data — add more entries any time. ---
# `requires_player` picks a random current roster player and makes their
# name available as {player_name} in the prompt. `requires_champion`
# restricts a situation/question to seasons that just won it all.
# `effects` are meter deltas applied on resolution (fan_support / hot_seat
# / depth_rating, all optional). A few situations have extra mechanical
# consequences beyond simple meter math — see `_apply_situation_special_effects`.
SITUATIONS = [
    {
        "id": "bust_question",
        "requires_player": True,
        "prompt": "A reporter asks: \u201cWas drafting {player_name} a mistake?\u201d",
        "options": [
            {"id": "defend", "label": "Defend Him Publicly",
             "blurb": "Back your guy in front of the cameras.",
             "effects": {"fan_support": 3, "hot_seat": -1}},
            {"id": "deflect", "label": "Admit It Was a Swing and a Miss",
             "blurb": "Honesty plays well with ownership, less so with the fans.",
             "effects": {"fan_support": -3, "hot_seat": -3}},
        ],
    },
    {
        "id": "dui_incident",
        "requires_player": True,
        "prompt": "{player_name} was arrested for a DUI last night. The story's already out.",
        "options": [
            {"id": "support", "label": "Stand By Him",
             "blurb": "Keep him on the roster and let him work through it.",
             "effects": {"fan_support": -2, "hot_seat": 8}},
            {"id": "cut", "label": "Cut Him Immediately",
             "blurb": "Zero tolerance. Ownership will approve; the locker room might not.",
             "effects": {"fan_support": -5, "hot_seat": -3}},
        ],
    },
    {
        "id": "cap_investigation",
        "requires_player": False,
        "prompt": "The league office says it's \u201clooking into\u201d your front office for cap "
        "circumvention. Probably nothing.",
        "options": [
            {"id": "cooperate", "label": "Cooperate Fully",
             "blurb": "Hand over everything they ask for.",
             "effects": {"fan_support": 1, "hot_seat": 20}},
            {"id": "stonewall", "label": "Stonewall It",
             "blurb": "Lawyer up and say nothing. If the league finds something anyway, "
             "expect draft compensation to disappear.",
             "effects": {"fan_support": -1, "hot_seat": 6, "depth_rating": -10}},
        ],
    },
    {
        "id": "stadium_funding",
        "requires_player": False,
        "prompt": "The owner wants a new $650 million stadium. The city says it won't foot "
        "the bill with tax dollars. What's the play?",
        "options": [
            {"id": "owner_pays", "label": "Convince the Owner to Self-Fund",
             "blurb": "A hard sell, but the fans will love you for it.",
             "effects": {"fan_support": 6, "hot_seat": 15}},
            {"id": "tax_fans", "label": "Back a Ticket Tax",
             "blurb": "A 4% surcharge on every ticket sold. Ownership's thrilled.",
             "effects": {"fan_support": -25, "hot_seat": -25}},
        ],
    },
    {
        "id": "rival_taunt",
        "requires_player": False,
        "prompt": "A rival GM took a shot at your franchise in the press. Cameras are rolling.",
        "options": [
            {"id": "fire_back", "label": "Fire Back",
             "blurb": "Give the fans something to cheer about off the court.",
             "effects": {"fan_support": 2, "hot_seat": 1}},
            {"id": "stay_classy", "label": "No Comment",
             "blurb": "Take the high road.",
             "effects": {"hot_seat": -10}},
        ],
    },
    {
        "id": "bakery_donut",
        "requires_player": True,
        "prompt": "A local bakery names a donut after {player_name}. It's... actually pretty good.",
        "options": [
            {"id": "acknowledge", "label": "Continue",
             "blurb": "Some stories don't need a decision.",
             "effects": {"fan_support": 1}},
        ],
    },
    {
        "id": "mascot_mishap",
        "requires_player": False,
        "prompt": "The mascot's costume ripped mid-timeout. Local news can't stop replaying it.",
        "options": [
            {"id": "acknowledge", "label": "Continue",
             "blurb": "It happens.",
             "effects": {"fan_support": 1}},
        ],
    },
    {
        "id": "hype_bet",
        "requires_player": False,
        "prompt": "A sportsbook lists your team as a trendy title bet. Fans are feeling it.",
        "options": [
            {"id": "lean_in", "label": "Lean Into the Hype",
             "blurb": "Let the city dream a little.",
             "effects": {"fan_support": 4, "hot_seat": 3}},
            {"id": "downplay", "label": "Downplay It",
             "blurb": "Manage expectations before they get away from you.",
             "effects": {"hot_seat": -20}},
        ],
    },
    {
        "id": "locker_room_dispute",
        "requires_player": True,
        "prompt": "Word gets out that {player_name} clashed with a teammate at practice.",
        "options": [
            {"id": "let_it_be", "label": "Let Them Work It Out",
             "blurb": "Trust the locker room to police itself.",
             "effects": {"fan_support": -6, "chemistry": -5}},
            {"id": "mediate", "label": "Step In and Mediate",
             "blurb": "Handle it before it becomes a distraction.",
             "effects": {"hot_seat": -1, "depth_rating": 1, "chemistry": 2}},
        ],
    },
    {
        "id": "ticket_drive",
        "requires_player": False,
        "prompt": "The front office wants a big season-ticket sales push.",
        "options": [
            {"id": "full_press", "label": "Full-Court Press",
             "blurb": "Go all in on the campaign.",
             "effects": {"fan_support": 3}},
            {"id": "low_key", "label": "Keep It Low-Key",
             "blurb": "Let the on-court product speak for itself.",
             "effects": {}},
        ],
    },
    {
        "id": "trade_demand",
        "requires_player": True,
        "prompt": "{player_name}'s agent leaks a trade request. \u201cHe wants to win somewhere else.\u201d",
        "options": [
            {"id": "grant_it", "label": "Grant the Trade",
             "blurb": "Move him for whatever you can get before the leverage gets worse.",
             "effects": {"fan_support": -6, "hot_seat": 4, "chemistry": 3}},
            {"id": "dig_in", "label": "Refuse to Trade Him",
             "blurb": "Make him play it out. Could blow up, could blow over.",
             "effects": {"fan_support": 2, "hot_seat": -3, "chemistry": -6}},
        ],
    },
    {
        "id": "fbi_raid",
        "requires_player": False,
        "prompt": "Federal agents raid the practice facility over the team's finances. "
        "Nobody in the building will say why.",
        "options": [
            {"id": "transparent", "label": "Get Ahead of It Publicly",
             "blurb": "Address it before the leaks do.",
             "effects": {"fan_support": -2, "hot_seat": 20}},
            {"id": "silence", "label": "Say Nothing",
             "blurb": "No comment, on advice of counsel.",
             "effects": {"fan_support": -6, "hot_seat": 12}},
        ],
    },
    {
        "id": "owner_scandal",
        "requires_player": False,
        "prompt": "The owner is caught on tape doing something deeply strange at a gala. "
        "It's everywhere by morning.",
        "options": [
            {"id": "defend_owner", "label": "Publicly Defend Him",
             "blurb": "Loyalty first. Ownership remembers who backed them.",
             "effects": {"fan_support": -5, "hot_seat": -6}},
            {"id": "distance", "label": "Quietly Distance the Franchise",
             "blurb": "Let it blow over without your fingerprints on it.",
             "effects": {"fan_support": 2, "hot_seat": 14}},
        ],
    },
    {
        "id": "weight_gain",
        "requires_player": True,
        "prompt": "{player_name} shows up to camp noticeably out of shape. It's become a punchline.",
        "options": [
            {"id": "conditioning_program", "label": "Put Him on a Program",
             "blurb": "Mandatory conditioning. He won't like it, but it's fixable.",
             "effects": {"fan_support": 1, "hot_seat": -1}},
            {"id": "let_it_ride", "label": "Let It Ride",
             "blurb": "He's a professional. It's on him.",
             "effects": {"fan_support": -2}},
        ],
    },
    {
        "id": "flat_earth_headline",
        "requires_player": True,
        "prompt": lambda: "Local radio runs a segment: \u201c{player_name} " +
        random.choice(FIRST_NAME_HEADLINE_TAKES) + ".\u201d",
        "options": [
            {"id": "acknowledge", "label": "Continue",
             "blurb": "Some headlines are just headlines.",
             "effects": {"fan_support": 1}},
        ],
    },
    {
        "id": "governor_criticism",
        "requires_player": False,
        "prompt": "The governor takes a swipe at the team on live TV: \u201cFrankly, they're an "
        "embarrassment to this state.\u201d",
        "options": [
            {"id": "fire_back", "label": "Fire Back",
             "blurb": "Fans love a fight with a politician.",
             "effects": {"fan_support": 4, "hot_seat": 2}},
            {"id": "ignore", "label": "Ignore It",
             "blurb": "Don't dignify it with a response.",
             "effects": {"hot_seat": -1}},
        ],
    },
    {
        "id": "sponsorship_dilemma",
        "requires_player": True,
        "prompt": "{player_name} is offered a lucrative sponsorship deal that reflects poorly "
        "on the franchise. Do you advise him to take it?",
        "options": [
            {"id": "let_him_take_it", "label": "It's His Money, Let Him Take It",
             "blurb": "Not your business what he does off the court.",
             "effects": {"fan_support": -4, "hot_seat": -7}},
            {"id": "advise_against", "label": "Advise Him Against It",
             "blurb": "Protect the brand, even if it costs him a payday.",
             "effects": {"fan_support": 2, "hot_seat": 10}},
        ],
    },
    {
        "id": "budget_cuts",
        "requires_player": False,
        "prompt": "Ownership tells you flatly: no real spending this year. Your cap space "
        "is getting cut in half, and someone on the roster has to go to make the "
        "numbers work.",
        "options": [
            {"id": "comply", "label": "Make the Cuts They Want",
             "blurb": "Release your weakest deal and eat the smaller budget for one season.",
             "effects": {"fan_support": -3, "hot_seat": -4, "chemistry": -3}},
            {"id": "push_back", "label": "Push Back on Ownership",
             "blurb": "You talk them into a smaller cut instead \u2014 they'll remember you "
             "fighting them on it.",
             "effects": {"fan_support": 1, "hot_seat": 14}},
        ],
    },
    {
        "id": "practice_blowup",
        "requires_best_player": True,
        "prompt": "{player_name} loafs through a walkthrough and the coaching staff is "
        "fuming. How do you handle your best player?",
        "options": [
            {"id": "yell", "label": "Yell At Him",
             "blurb": "Get in his face in front of the team. Discipline for some, a spark "
             "for others.",
             "effects": {"fan_support": -1, "hot_seat": 2}},
            {"id": "glaze", "label": "Glaze Him",
             "blurb": "Public praise, private pass. He loves you for it \u2014 the locker room "
             "notices too.",
             "effects": {"fan_support": 2}},
        ],
    },
    {
        "id": "star_injury_scare",
        "requires_best_player": True,
        "prompt": "{player_name} goes down awkwardly in practice. The team holds its "
        "breath waiting on the MRI.",
        "options": [
            {"id": "rest_him", "label": "Shut Him Down, Don't Rush It",
             "blurb": "He sits extra time now so he's right when it matters.",
             "effects": {"fan_support": -2}},
            {"id": "play_through", "label": "Clear Him to Play Through It",
             "blurb": "He plays hurt. Risky, but you need him on the floor.",
             "effects": {"fan_support": 1, "hot_seat": 12}},
        ],
    },
    {
        "id": "second_star_arrest",
        "requires_second_best_player": True,
        "prompt": "{player_name} is arrested overnight on a serious charge. The story is "
        "already national news by shootaround.",
        "options": [
            {"id": "cut_immediately", "label": "Release Him Immediately",
             "blurb": "Zero tolerance, full stop \u2014 the roster spot sits empty.",
             "effects": {"fan_support": 3, "hot_seat": -4, "chemistry": 2}},
            {"id": "wait_for_facts", "label": "Wait for the Facts",
             "blurb": "Due process, but the longer he's around the worse the optics get.",
             "effects": {"fan_support": -8, "hot_seat": 14, "chemistry": -4}},
        ],
    },
    {
        "id": "knees_flare_up",
        "requires_knees_player": True,
        "prompt": "{player_name}'s knees are barking again \u2014 exactly what the scouts "
        "warned you about on draft day.",
        "options": [
            {"id": "shut_down", "label": "Shut Him Down for a Stretch",
             "blurb": "Load management now to protect the long-term investment.",
             "effects": {"fan_support": -1}},
            {"id": "push_through", "label": "Push Through It",
             "blurb": "You need the minutes now. The knees might not forgive you.",
             "effects": {"hot_seat": 1}},
        ],
    },
]

REPORTER_QUESTIONS = [
    {
        "id": "finals_reporter_question",
        "requires_player": True,
        "requires_champion": True,
        "prompt": "Reporter Tank Ostrowski has a question for you: \u201cWho's your favorite "
        "player on this team?\u201d",
        "options": [
            {"id": "name_the_star", "label": "Name {player_name}",
             "blurb": "Give the Finals MVP his flowers publicly.",
             "effects": {"fan_support": 5, "hot_seat": -2, "depth_rating": -2}},
            {"id": "no_favorites", "label": "\u201cI Don't Have Favorites\u201d",
             "blurb": "Keep the locker room even. Safer, less memorable.",
             "effects": {"fan_support": 2}},
        ],
    },
    {
        "id": "finals_hennessy_celebration",
        "requires_player": True,
        "requires_champion": True,
        "prompt": "Reporter Buster Briggs catches you drenched in champagne: \u201cWe saw "
        "{player_name} chugging Hennessy out of a Timberland boot on the parade float. Is "
        "this the culture you envisioned?\u201d",
        "options": [
            {"id": "embrace_henny", "label": "\u201cThat's Culture Leadership\u201d",
             "blurb": "You defend the boot-chug. Fans instantly order the jersey. Ownership "
             "is scheduling a very dynamic intervention.",
             "effects": {"fan_support": 15, "hot_seat": 12}},
            {"id": "condemn_boot", "label": "\u201cWe Will Handle It Internally\u201d",
             "blurb": "You kill the vibe entirely. You look like a cop on national television.",
             "effects": {"fan_support": -10, "hot_seat": -5}},
        ],
    },
    {
        "id": "finals_fbi_raid_rings",
        "requires_player": True,
        "requires_champion": True,
        "prompt": "A reporter pulls up a fresh post: \u201c{player_name} just claimed on "
        "Instagram Live that this championship ring is \u2018filled with tracking devices "
        "from the deep state\u2019 and he's flushing his down the toilet. Your thoughts?\u201d",
        "options": [
            {"id": "agree_deep_state", "label": "\u201cHe Might Be Onto Something\u201d",
             "blurb": "You look directly into the camera and squint. The league office "
             "fines you $50k before you leave the podium.",
             "effects": {"fan_support": 14, "hot_seat": 18}},
            {"id": "buy_new_ring", "label": "\u201cWe'll Order Him a Plastic One\u201d",
             "blurb": "You treat your Finals MVP like a toddler. It diffuses the media but "
             "might mess up the vibes.",
             "effects": {"fan_support": -4, "hot_seat": -4}},
        ],
    },
    {
        "id": "roman_empire_question",
        "requires_player": False,
        "requires_champion": False,
        "prompt": "Reporter L'Hopital Duckdoo has a question for you: \u201cWhat are your "
        "thoughts on the collapse of the Roman Empire?\u201d",
        "options": [
            {"id": "profound_answer", "label": "Give a Surprisingly Deep Answer",
             "blurb": "You ramble about currency debasement for two minutes. It goes viral.",
             "effects": {"fan_support": 6, "hot_seat": 11}},
            {"id": "deflect", "label": "\u201cI Only Think About Basketball\u201d",
             "blurb": "Safe, forgettable, exactly what a reporter expects to hear.",
             "effects": {"fan_support": -5}},
        ],
    },
    {
        "id": "trade_rumor_fish",
        "requires_player": True,
        "requires_champion": False,
        "prompt": "A reporter fishes for a headline: \u201cAny truth to the rumor {player_name} "
        "is on the block?\u201d",
        "options": [
            {"id": "shut_it_down", "label": "Shut It Down Immediately",
             "blurb": "\u201cAbsolutely not. He's part of the future here.\u201d",
             "effects": {"fan_support": 4, "hot_seat": 2}},
            {"id": "stay_coy", "label": "Stay Coy",
             "blurb": "\u201cWe listen on everything.\u201d Technically true. Also a headline now.",
             "effects": {"fan_support": -5, "hot_seat": -5}},
        ],
    },
    {
        "id": "podcast_take",
        "requires_player": True,
        "requires_champion": False,
        "prompt": "A reporter asks: \u201cWhat did you think of {player_name}'s podcast where "
        "he said this team \u2018doesn't have an identity\u2019?\u201d",
        "options": [
            {"id": "laugh_it_off", "label": "Laugh It Off",
             "blurb": "\u201cHe's a character. That's why we love him.\u201d",
             "effects": {"fan_support": 3}},
            {"id": "call_him_out", "label": "Call Him Out Publicly",
             "blurb": "You fire back at your own player on live TV. Bold. Reckless.",
             "effects": {"fan_support": -11, "hot_seat": 15}},
        ],
    },
    {
        "id": "moon_landing_gotcha",
        "requires_player": True,
        "requires_champion": False,
        "prompt": "A reporter, grinning: \u201cIs it true {player_name} thinks the moon landing "
        "was staged, and does that concern you as an organization?\u201d",
        "options": [
            {"id": "embrace_the_chaos", "label": "\u201cWe Encourage Free Thinkers\u201d",
             "blurb": "Fully unhinged answer. The city loves it. Ownership does not.",
             "effects": {"fan_support": 12, "hot_seat": 15}},
            {"id": "distance_yourself", "label": "\u201cThat's a Personal Belief, Not a Team "
             "Position\u201d",
             "blurb": "Boring, safe, correct.",
             "effects": {"fan_support": -1, "hot_seat": -2}},
        ],
    },
]


def _fmt(text, context):
    return text.format(**context) if context else text


def _situation_prompt_text(template, context):
    raw_prompt = template["prompt"]
    prompt = raw_prompt() if callable(raw_prompt) else raw_prompt
    return _fmt(prompt, context)


def _build_situation_payload(template, context):
    return {
        "situation_id": template["id"],
        "prompt": _situation_prompt_text(template, context),
        "options": [
            {"id": o["id"], "label": _fmt(o["label"], context), "blurb": _fmt(o["blurb"], context)}
            for o in template["options"]
        ],
        "context": context,
    }


def maybe_generate_situation(roster, fan_support, hot_seat, champion=False, finals_mvp_name=None,
                              philosophy=None):
    has_player = any(slot["player"] for slot in roster)
    ranked = sorted(
        (slot["player"] for slot in roster if slot["player"]),
        key=lambda p: p["ovr"], reverse=True,
    )
    best_player = ranked[0] if ranked else None
    second_player = ranked[1] if len(ranked) > 1 else None
    knees_player = next(
        (p for p in ranked if KNEES_TAG in p.get("origin", "")), None
    )

    if champion:
        champion_only = [q for q in REPORTER_QUESTIONS if q.get("requires_champion")]
        template = random.choice(champion_only)
        context = {"player_name": finals_mvp_name or "your best player"}
        return _build_situation_payload(template, context)

    # Small market's identity cost: a star who's earned his way out gets
    # restless. Weighted, not guaranteed — this doesn't fire every season.
    phil_info = FRONT_OFFICE_PHILOSOPHIES.get(philosophy, {})
    if phil_info.get("star_flight_risk") and best_player and best_player["ovr"] >= 85:
        if random.random() < 0.3:
            template = next(s for s in SITUATIONS if s["id"] == "trade_demand")
            context = {"player_name": best_player["name"]}
            return _build_situation_payload(template, context)

    # Guarantee something every season, and give reporter questions real
    # airtime instead of drowning them in the bigger situations pool.
    if random.random() < 0.5:
        pool = [q for q in REPORTER_QUESTIONS if not q.get("requires_champion")]
    else:
        pool = SITUATIONS

    def is_eligible(s):
        if s.get("requires_player") and not has_player:
            return False
        if s.get("requires_best_player") and not best_player:
            return False
        if s.get("requires_second_best_player") and not second_player:
            return False
        if s.get("requires_knees_player") and not knees_player:
            return False
        return True

    eligible = [s for s in pool if is_eligible(s)]
    if not eligible:
        eligible = [s for s in SITUATIONS if is_eligible(s)]
    if not eligible:
        eligible = [s for s in SITUATIONS if not s.get("requires_player") and not s.get("requires_best_player")
                    and not s.get("requires_second_best_player") and not s.get("requires_knees_player")]

    template = random.choice(eligible)
    context = {}
    if template.get("requires_best_player"):
        context["player_name"] = best_player["name"]
    elif template.get("requires_second_best_player"):
        context["player_name"] = second_player["name"]
    elif template.get("requires_knees_player"):
        context["player_name"] = knees_player["name"]
    elif template.get("requires_player"):
        candidates = [slot["player"] for slot in roster if slot["player"]]
        context["player_name"] = random.choice(candidates)["name"]

    return _build_situation_payload(template, context)


def _all_situation_templates():
    return SITUATIONS + REPORTER_QUESTIONS


def _apply_situation_special_effects(situation_id, choice_id, roster, context, notes, state_updates):
    player_name = context.get("player_name")

    if situation_id == "dui_incident" and player_name:
        target = next((s for s in roster if s["player"] and s["player"]["name"] == player_name), None)
        if target:
            if choice_id == "cut":
                notes.append(f"{player_name} is waived immediately. The roster spot sits open until your next move.")
                target["player"] = None
            elif choice_id == "support":
                target["player"]["ovr"] = max(35, target["player"]["ovr"] - 4)
                notes.append(f"{player_name} stays on the roster, but the distraction shows on the court.")

    elif situation_id == "trade_demand" and player_name and choice_id == "grant_it":
        target = next((s for s in roster if s["player"] and s["player"]["name"] == player_name), None)
        if target:
            return_ovr = max(35, target["player"]["ovr"] - random.randint(8, 16))
            return_player = make_player(
                ovr=return_ovr, age=random.randint(24, 30), origin="Trade Return"
            )
            notes.append(f"{player_name} is dealt away. {return_player['name']} comes back in the deal.")
            target["player"] = return_player
            state_updates["chemistry_delta"] = state_updates.get("chemistry_delta", 0) + player_chemistry_impact(return_player)

    elif situation_id == "weight_gain" and player_name:
        target = next((s for s in roster if s["player"] and s["player"]["name"] == player_name), None)
        if target:
            if choice_id == "let_it_ride":
                target["player"]["ovr"] = max(35, target["player"]["ovr"] - 6)
                notes.append(f"{player_name} never really rounds back into shape this year.")
            elif choice_id == "conditioning_program":
                target["player"]["ovr"] = max(35, target["player"]["ovr"] - 2)
                notes.append(f"{player_name} grinds back into game shape by midseason.")

    elif situation_id == "budget_cuts":
        if choice_id == "comply":
            weak = _weakest_slot(roster)
            if weak and weak["player"]:
                notes.append(f"{weak['player']['name']} is released to satisfy the budget cut.")
                weak["player"] = None
            state_updates["cap_multiplier"] = 0.5
        elif choice_id == "push_back":
            state_updates["cap_multiplier"] = 0.75

    elif situation_id == "practice_blowup" and player_name:
        target = next((s for s in roster if s["player"] and s["player"]["name"] == player_name), None)
        if target:
            if choice_id == "yell":
                if random.random() < 0.6:
                    target["player"]["ovr"] = min(99, target["player"]["ovr"] + 2)
                    notes.append(f"{player_name} responds to the callout and plays with an edge all year.")
                else:
                    target["player"]["ovr"] = max(35, target["player"]["ovr"] - 2)
                    state_updates["chemistry_delta"] = state_updates.get("chemistry_delta", 0) - 6
                    notes.append(f"{player_name} shuts down after getting shown up in front of the team.")
            elif choice_id == "glaze":
                state_updates["chemistry_delta"] = state_updates.get("chemistry_delta", 0) + 5
                if random.random() < 0.2:
                    target["player"]["ovr"] = max(35, target["player"]["ovr"] - 2)
                    notes.append(f"{player_name} coasts a little, knowing there's no real accountability.")
                else:
                    notes.append(f"{player_name} feels backed and the locker room stays loose.")

    elif situation_id == "star_injury_scare" and player_name:
        target = next((s for s in roster if s["player"] and s["player"]["name"] == player_name), None)
        if target:
            if choice_id == "rest_him":
                target["player"]["injury_note"] = (
                    "Recovering from injury — expected back at full strength next season."
                )
                notes.append(f"{player_name} is shut down for the year but should be fine long-term.")
            elif choice_id == "play_through":
                if random.random() < 0.4:
                    target["player"]["ovr"] = max(35, target["player"]["ovr"] - random.randint(4, 9))
                    target["player"]["injury_note"] = "Playing through a nagging injury — never fully right this year."
                    notes.append(f"{player_name} grinds through it, but he's clearly compromised.")
                else:
                    notes.append(f"{player_name} gets through it fine and never misses a beat.")

    elif situation_id == "second_star_arrest" and player_name:
        target = next((s for s in roster if s["player"] and s["player"]["name"] == player_name), None)
        if target:
            if choice_id == "cut_immediately":
                notes.append(f"{player_name} is released immediately. The roster spot sits open.")
                target["player"] = None
            elif choice_id == "wait_for_facts":
                target["player"]["ovr"] = max(35, target["player"]["ovr"] - 5)
                notes.append(f"{player_name} stays on the roster while it plays out. The distraction lingers.")

    elif situation_id == "knees_flare_up" and player_name:
        target = next((s for s in roster if s["player"] and s["player"]["name"] == player_name), None)
        if target:
            if choice_id == "shut_down":
                target["player"]["injury_note"] = "Load-managing chronic knee soreness."
                notes.append(f"{player_name} sits stretches at a time, but the knee holds up better for it.")
            elif choice_id == "push_through":
                if random.random() < 0.5:
                    target["player"]["ovr"] = max(35, target["player"]["ovr"] - random.randint(5, 10))
                    notes.append(f"{player_name}'s knees give out on him. He's a different player the rest of the year.")
                else:
                    notes.append(f"{player_name} grits through it and holds up fine \u2014 this time.")

    return roster


def resolve_situation(state, situation_id, choice_id, context=None, made_playoffs=None, wins=None):
    template = next((s for s in _all_situation_templates() if s["id"] == situation_id), None)
    if template is None:
        raise ValueError(f"Unknown situation_id: {situation_id!r}")
    option = next((o for o in template["options"] if o["id"] == choice_id), None)
    if option is None:
        raise ValueError(f"Unknown choice_id: {choice_id!r} for situation {situation_id!r}")

    context = context or {}
    roster = state["roster"]
    fan_support = state.get("fan_support", 50)
    hot_seat = state.get("hot_seat", 20)
    depth_rating = state["depth_rating"]
    chemistry = state.get("chemistry", 65)
    notes = []
    state_updates = {}

    effects = option.get("effects", {})
    fan_support = max(5, min(99, fan_support + effects.get("fan_support", 0)))
    hot_seat = max(0, min(99, hot_seat + effects.get("hot_seat", 0)))
    depth_rating = max(0, min(99, depth_rating + effects.get("depth_rating", 0)))
    chemistry = max(0, min(99, chemistry + effects.get("chemistry", 0)))

    roster = _apply_situation_special_effects(situation_id, choice_id, roster, context, notes, state_updates)
    chemistry = max(0, min(99, chemistry + state_updates.get("chemistry_delta", 0)))
    note = notes[0] if notes else option["blurb"]

    new_state = {
        **state, "roster": roster, "depth_rating": depth_rating,
        "fan_support": fan_support, "hot_seat": hot_seat, "chemistry": chemistry,
    }

    next_decision = None
    cap_multiplier = state_updates.get("cap_multiplier", 1.0)
    if made_playoffs is not None and wins is not None:
        offseason = generate_offseason_options(
            made_playoffs, wins, roster, depth_rating=depth_rating,
            draft_class=state.get("draft_class"), philosophy=state.get("philosophy"),
            cap_multiplier=cap_multiplier,
        )
        next_decision = {
            "season_number": state["season_number"],
            "pick_number": offseason["pick_number"],
            "options": offseason["options"],
        }

    return {"state": new_state, "note": note, "next_decision": next_decision}


def new_game(city="", team_name="", philosophy="win_now"):
    city = (city or "").strip()[:30] or "Your City"
    team_name = (team_name or "").strip()[:30] or "The Franchise"
    if philosophy not in FRONT_OFFICE_PHILOSOPHIES:
        philosophy = "win_now"

    draft_class = roll_draft_class()
    roster = new_starting_roster()

    state = {
        "season_number": 1,
        "city": city,
        "team_name": team_name,
        "philosophy": philosophy,
        "roster": roster,
        "depth_rating": random.randint(30, 40),
        "fan_support": 50,
        "hot_seat": 20,
        "chemistry": 65,
        "draft_class": draft_class,
        "last_flavor": None,
        "history": [],
        "streak": 0,
        "max_streak": 0,
    }
    decision = {
        "season_number": 1, "pick_number": 1,
        "options": generate_draft_options(1, roster, draft_class, philosophy),
    }
    return {"state": state, "decision": decision}


def advance_dynasty(state, choices):
    """`choices` is a list of 0+ option objects the frontend displayed and
    the player selected this offseason — e.g. [draft_pick_option,
    free_agent_option]. Each is applied in order via
    resolve_offseason_choices."""
    roster = state["roster"]
    depth_rating = state["depth_rating"]
    philosophy = state.get("philosophy")
    chemistry = state.get("chemistry", 65)

    if choices is None:
        choices = []
    roster, depth_rating, chemistry, offseason_notes = resolve_offseason_choices(
        choices, roster, depth_rating, chemistry=chemistry, philosophy=philosophy
    )

    season_result = simulate_season(roster, depth_rating, state["season_number"], philosophy, chemistry=chemistry)
    season_result["media"] = generate_media_bundle(roster, state["team_name"], season_result)

    fan_support = max(5, min(99, state.get("fan_support", 50) + _fan_support_delta(season_result)))
    hot_seat = max(0, min(99, state.get("hot_seat", 20) + _hot_seat_delta(season_result, philosophy)))

    # Give the cap real teeth. It was purely cosmetic before — you could
    # blow past it forever with zero consequence. Now going over costs you:
    # a luxury-tax-sized hot seat bump and a chemistry hit (an expensive,
    # crowded roster breeds its own tension), scaling with how far over
    # you are. A superteam running a stacked, over-cap roster should feel
    # that pressure every single season, not just on the scoreboard.
    end_of_season_cap_space = cap_space(roster, depth_rating)
    over_cap = max(0.0, -end_of_season_cap_space)
    if over_cap > 0:
        tax_hot_seat = min(15, round(over_cap / 4))
        tax_chemistry = min(8, round(over_cap / 6))
        hot_seat = max(0, min(99, hot_seat + tax_hot_seat))
        chemistry = max(0, min(99, chemistry - tax_chemistry))

    season_result["fan_support"] = fan_support
    season_result["hot_seat"] = hot_seat
    season_result["cap_space"] = end_of_season_cap_space

    flavor = _flavor_note(season_result, roster, last_flavor=state.get("last_flavor"))
    extra_notes = [flavor]
    if over_cap > 0:
        extra_notes.append(f"You're ${over_cap:.1f}M over the cap — ownership isn't thrilled about the tax bill.")
    if hot_seat >= 80:
        extra_notes.append("Ownership is one bad month from a change.")
    season_result["notes"] = offseason_notes + season_result["notes"] + extra_notes

    streak = state["streak"] + 1 if season_result["champion"] else 0
    max_streak = max(state.get("max_streak", 0), streak)
    history = state["history"] + [season_result]

    next_season_number = state["season_number"] + 1
    game_over = next_season_number > TOTAL_SEASONS
    next_draft_class = roll_draft_class()

    new_state = {
        "season_number": next_season_number,
        "city": state["city"],
        "team_name": state["team_name"],
        "philosophy": philosophy,
        "roster": roster,
        "depth_rating": depth_rating,
        "fan_support": fan_support,
        "hot_seat": hot_seat,
        "chemistry": chemistry,
        "draft_class": next_draft_class,
        "last_flavor": flavor,
        "history": history,
        "streak": streak,
        "max_streak": max_streak,
    }

    next_decision = None
    if not game_over:
        offseason = generate_offseason_options(
            season_result["made_playoffs"], season_result["wins"], roster,
            depth_rating=depth_rating, draft_class=next_draft_class, philosophy=philosophy,
        )
        next_decision = {
            "season_number": next_season_number,
            "pick_number": offseason["pick_number"],
            "options": offseason["options"],
        }

    pending_situation = maybe_generate_situation(
        roster, fan_support, hot_seat,
        champion=season_result["champion"],
        finals_mvp_name=season_result.get("finals_mvp"),
        philosophy=philosophy,
    )

    return {
        "state": new_state,
        "season_result": season_result,
        "next_decision": next_decision,
        "game_over": game_over,
        "three_peat": max_streak >= 3,
        "pending_situation": pending_situation,
    }