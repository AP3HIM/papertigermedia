"""Dynasty simulation engine.

Deliberately stateless. v5 adds: a post-season Situations system (2-choice
events with real meter consequences, drawn from an expandable pool covering
everything from a donut named after your PG to an FBI raid on your
facility), a Hot Seat meter tracking GM job security separate from public
Fan Support, positions actually mattering (redundant-position rosters take
a real rating hit), and a Finals spectacle — a named opponent, a real
series score, and a Finals MVP pulled from your actual roster.
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
    "5x All-Star", "Scoring Champion","Certified Bucket Getter", "Former Finals MVP", 
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
SITUATION_CHANCE = 0.5

# Redundant positions are a real cost now — stacking 4 centers is a build,
# not a shortcut. A single backup at the same spot is normal roster
# construction and isn't penalized; 3+ at one position is where it bites.
POSITION_FULL_COVERAGE_BONUS = 2
POSITION_STACK_THRESHOLD = 3
POSITION_STACK_PENALTY_PER_PLAYER = 4

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
]

OPPONENT_CITIES = [
    "Moscow", "Libjuana", "Basel", "Tundra City", "Port Halloway",
    "New Cascadia", "Redstone", "Vantage", "Ashport", "Cobalt Bay",
    "Glasswing", "Hartford Falls", "Northgate", "Silvermine", "Eastpoint", "Quicksilver", "Ironwood", "Frosthaven", "Shadowport", "Rivermouth",
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


def make_player(ovr, age, potential=None, profile=None, origin=""):
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
    }


def new_starting_roster():
    """The bad team you inherit: 4 mediocre holdover vets across 4 distinct
    positions + one open slot for the incoming top pick."""
    positions = random.sample(POSITIONS, 4)
    ovr_bands = [(60, 68), (58, 66), (56, 64), (54, 62)]
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
        "ovr_range": (58, 92),
        "potential_bonus_range": (0, 20),
    },
]


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


def generate_draft_options(pick_number, roster=None):
    draft_year = datetime.date.today().year
    archetypes = DRAFT_ARCHETYPES if pick_number <= TOP_LOTTERY_CUTOFF else [
        a for a in DRAFT_ARCHETYPES if a["id"] != "boom_bust"
    ]
    need = _missing_position(roster) if roster else None

    options = []
    for arch in archetypes:
        profile = generate_prospect_profile()
        # Bias one archetype's prospect toward the team's positional need
        # so filling the gap isn't a total coin flip.
        if need and random.random() < 0.6:
            profile["position"] = need
            body = POSITION_BODY_RANGES[need]
            profile["height"] = format_height(random.randint(*body["height_in"]))
            profile["weight"] = random.randint(*body["weight_lb"])
        profile["age"] = random.randint(19, 22)
        profile["origin"] = f"{draft_year} \u00b7 R1 Pick {pick_number}"
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


def generate_offseason_options(made_playoffs, wins, roster):
    if not made_playoffs:
        pick_number = compute_lottery_pick(wins)
        return {"pick_number": pick_number, "options": generate_draft_options(pick_number, roster)}

    best = max((s["player"] for s in roster if s["player"]), key=lambda p: p["ovr"], default=None)
    run_it_back_blurb = (
        f"Keep this exact group — led by {best['name']} — together for one more year."
        if best else "Keep the roster as-is. Stability has value."
    )
    depth_names = [random_name(), random_name()]

    return {
        "pick_number": None,
        "options": [
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
        ],
    }


def _resolve_draft_choice(choice_id, prospect):
    if choice_id == "trade_for_veteran":
        ovr = random.randint(78, 85)
        potential = ovr
    else:
        arch = next(a for a in DRAFT_ARCHETYPES if a["id"] == choice_id)
        lo, hi = arch["ovr_range"]
        ovr = random.randint(lo, hi)
        potential = min(99, ovr + random.randint(*arch["potential_bonus_range"]))

    return {
        "name": prospect["name"], "position": prospect["position"], "height": prospect["height"],
        "weight": prospect["weight"], "traits": prospect["traits"], "age": prospect["age"],
        "ovr": ovr, "potential": potential, "origin": prospect.get("origin", ""),
        "injury_note": None,
    }


def _weakest_slot(roster):
    """Prefer replacing the weakest player at the *most duplicated*
    position — that's how a roster actually corrects a 4-centers problem
    instead of just swapping in a 5th one."""
    counts = {}
    for s in roster:
        if s["player"]:
            counts[s["player"]["position"]] = counts.get(s["player"]["position"], 0) + 1

    def score(slot):
        if not slot["player"]:
            return (1, 0)  # open slots go first
        dup = counts.get(slot["player"]["position"], 1)
        return (0, -dup, -( -slot["player"]["ovr"]))

    filled_dupes = [s for s in roster if s["player"] and counts.get(s["player"]["position"], 1) > 1]
    if filled_dupes:
        return min(filled_dupes, key=lambda s: s["player"]["ovr"])
    return min(roster, key=lambda s: s["player"]["ovr"] if s["player"] else -1)


def resolve_offseason_choice(choice_id, roster, depth_rating, prospect=None, depth_signees=None):
    """Applies the player's decision. Returns (roster, depth_rating, notes).
    `prospect`/`depth_signees` are the exact data the client displayed for
    the chosen option, reused as-is so the identity shown matches reality."""
    notes = []

    if choice_id in ("safe", "balanced", "boom_bust", "trade_for_veteran"):
        if prospect is None:
            prospect = generate_prospect_profile()
            prospect["age"] = random.randint(19, 22)
            prospect["origin"] = ""
        new_player = _resolve_draft_choice(choice_id, prospect)
        target = _weakest_slot(roster)
        old = target["player"]
        target["player"] = new_player
        if old:
            notes.append(f"{old['name']} moves on. {new_player['name']} steps into the lineup.")
        else:
            notes.append(f"{new_player['name']} joins the roster.")

    elif choice_id == "run_it_back":
        notes.append("The front office stands pat.")

    elif choice_id == "chase_a_star":
        if prospect and random.random() < 0.45:
            ovr = random.randint(83, 93)
            new_player = {
                "name": prospect["name"], "position": prospect["position"], "height": prospect["height"],
                "weight": prospect["weight"], "traits": prospect["traits"], "age": prospect["age"],
                "ovr": ovr, "potential": ovr, "origin": "Trade", "injury_note": None,
            }
            target = _weakest_slot(roster)
            old = target["player"]
            target["player"] = new_player
            old_name = old["name"] if old else "a roster spot"
            notes.append(f"The trade lands. {new_player['name']} joins the roster — {old_name} is dealt away.")
        else:
            star_name = prospect["name"] if prospect else "The star"
            depth_rating = max(0, depth_rating - 8)
            notes.append(f"The {star_name} talks collapse. He signs elsewhere for more money.")

    elif choice_id == "invest_in_depth":
        depth_rating = min(99, depth_rating + random.randint(8, 14))
        names = depth_signees if depth_signees else [random_name(), random_name()]
        notes.append(f"{names[0]} and {names[1]} sign on as depth pieces off the bench.")

    else:
        raise ValueError(f"Unknown choice_id: {choice_id!r}")

    return roster, depth_rating, notes


def age_and_develop(roster):
    notes = []
    for slot in roster:
        p = slot["player"]
        if p is None:
            continue

        p["age"] += 1

        if p["injury_note"]:
            p["injury_note"] = None
            notes.append(f"{p['name']} is back to full strength.")

        if p["age"] <= 26 and p["ovr"] < p["potential"]:
            p["ovr"] = min(p["potential"], p["ovr"] + random.randint(1, 4))
        elif p["age"] >= 31:
            p["ovr"] = max(35, p["ovr"] - random.randint(1, 5))

        if random.random() < 0.06 and p["ovr"] < 90:
            jump = random.randint(6, 12)
            p["ovr"] = min(96, p["ovr"] + jump)
            p["potential"] = max(p["potential"], p["ovr"])
            notes.append(f"{p['name']} breaks out, jumping to a {p['ovr']} overall.")

        if random.random() < 0.07:
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


def compute_team_rating(roster, depth_rating):
    core_ratings = [s["player"]["ovr"] for s in roster if s["player"]]
    core_avg = sum(core_ratings) / len(core_ratings) if core_ratings else 45
    rating = 0.75 * core_avg + 0.25 * depth_rating
    rating += _position_balance_adjustment(roster)
    return round(max(20, min(99, rating)))


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
        "headline": f"{{team}} defeat the {opponent} in {4 + games_against}, "
        f"with {mvp_name} named Finals MVP.",
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


def _hot_seat_delta(season_result):
    if season_result["champion"]:
        return -15
    if season_result["made_playoffs"]:
        return -5
    if season_result["wins"] >= 35:
        return 0
    if season_result["wins"] >= 20:
        return 6
    return 12


def simulate_season(roster, depth_rating, season_number):
    dev_notes = age_and_develop(roster)
    rating = compute_team_rating(roster, depth_rating)
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
    }
    if playoff["champion"]:
        result.update(_finals_spectacle(roster))
    return result


# --- Post-season situations. Pure data — add more entries any time. ---
# `requires_player` picks a random current roster player and makes their
# name available as {player_name} in the prompt. `requires_champion`
# restricts a situation to seasons that just won it all. `effects` are
# meter deltas applied on resolution (fan_support / hot_seat / depth_rating,
# all optional). A few situations have extra mechanical consequences beyond
# simple meter math — see `_apply_situation_special_effects`.
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
             "effects": {"fan_support": -25, "hot_seat": -4}},
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
             "effects": {"hot_seat": -1}},
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
             "effects": {"hot_seat": -2}},
        ],
    },
    {
        "id": "locker_room_dispute",
        "requires_player": True,
        "prompt": "Word gets out that {player_name} clashed with a teammate at practice.",
        "options": [
            {"id": "let_it_be", "label": "Let Them Work It Out",
             "blurb": "Trust the locker room to police itself.",
             "effects": {"fan_support": -6}},
            {"id": "mediate", "label": "Step In and Mediate",
             "blurb": "Handle it before it becomes a distraction.",
             "effects": {"hot_seat": -1, "depth_rating": 1}},
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
             "effects": {"fan_support": -6, "hot_seat": 4}},
            {"id": "dig_in", "label": "Refuse to Trade Him",
             "blurb": "Make him play it out. Could blow up, could blow over.",
             "effects": {"fan_support": 2, "hot_seat": -3}},
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
        "prompt": "A reporter asks: \u201cWhat did you think of {player_name}'s podcast where he "
        "said this team \u2018doesn't have an identity\u2019?\u201d",
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
            {"id": "distance_yourself", "label": "\u201cThat's a Personal Belief, Not a Team Position\u201d",
             "blurb": "Boring, safe, correct.",
             "effects": {"fan_support": -1, "hot_seat": -2}},
        ],
    },
        {
        "id": "finals_hennessy_celebration",
        "requires_player": True,
        "requires_champion": True,
        "prompt": "Reporter Buster Briggs catches you drenched in champagne: \u201cWe saw {player_name} chugging Hennessy out of a timberland boot on the parade float. Is this the culture you envisioned?\u201d",
        "options": [
            {"id": "embrace_henny", "label": "\u201cThat's Culture Leadership\u201d", "blurb": "You defend the boot-chug. Fans instantly order the jersey. Ownership is scheduling a dynamic intervention.", "effects": {"fan_support": 15, "hot_seat": 12}},
            {"id": "condemn_boot", "label": "\u201cWe Will Handle It Internally\u201d", "blurb": "You kill the vibe entirely. You look like a cop on national television.", "effects": {"fan_support": -10, "hot_seat": -5}},
        ],
    },
    {
        "id": "finals_fbi_raid_rings",
        "requires_player": True,
        "requires_champion": True,
        "prompt": "A reporter pulls up a fresh tweet: \u201c{player_name} just claimed on Instagram Live that this championship ring is 'filled with tracking devices from the deep state' and he's flushing his down the toilet. Your thoughts?\u201d",
        "options": [
            {"id": "agree_deep_state", "label": "\u201cHe Might Be Onto Something\u201d", "blurb": "You look directly into the camera and squint. The league office fines you $50k before you leave the podium.", "effects": {"fan_support": 14, "hot_seat": 18}},
            {"id": "buy_new_ring", "label": "\u201cWe'll Order Him a Plastic One\u201d", "blurb": "You treat your Finals MVP like a toddler. It diffuses the media but might mess up vibes.", "effects": {"fan_support": -4, "hot_seat": -4}},
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


def maybe_generate_situation(roster, fan_support, hot_seat, champion=False, finals_mvp_name=None):
    has_player = any(slot["player"] for slot in roster)

    if champion:
        champion_only = [q for q in REPORTER_QUESTIONS if q.get("requires_champion")]
        template = random.choice(champion_only)
        context = {"player_name": finals_mvp_name or "your best player"}
        return _build_situation_payload(template, context)

    has_player = any(slot["player"] for slot in roster)

    # Guarantee something every season, and give reporter questions real
    # airtime instead of drowning them in the bigger situations pool.
    if random.random() < 0.5:
        pool = [q for q in REPORTER_QUESTIONS if not q.get("requires_champion")]
    else:
        pool = SITUATIONS

    eligible = [s for s in pool if not s.get("requires_player") or has_player]
    if not eligible:
        eligible = [s for s in SITUATIONS if not s.get("requires_player") or has_player]

    template = random.choice(eligible)
    context = {}
    if template.get("requires_player"):
        candidates = [slot["player"] for slot in roster if slot["player"]]
        context["player_name"] = random.choice(candidates)["name"]

    return _build_situation_payload(template, context)


def _all_situation_templates():
    return SITUATIONS + REPORTER_QUESTIONS


def _apply_situation_special_effects(situation_id, choice_id, roster, context, notes):
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

    elif situation_id == "weight_gain" and player_name:
        target = next((s for s in roster if s["player"] and s["player"]["name"] == player_name), None)
        if target:
            if choice_id == "let_it_ride":
                target["player"]["ovr"] = max(35, target["player"]["ovr"] - 6)
                notes.append(f"{player_name} never really rounds back into shape this year.")
            elif choice_id == "conditioning_program":
                target["player"]["ovr"] = max(35, target["player"]["ovr"] - 2)
                notes.append(f"{player_name} grinds back into game shape by midseason.")

    return roster


def resolve_situation(state, situation_id, choice_id, context=None):
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
    notes = []

    effects = option.get("effects", {})
    fan_support = max(5, min(99, fan_support + effects.get("fan_support", 0)))
    hot_seat = max(0, min(99, hot_seat + effects.get("hot_seat", 0)))
    depth_rating = max(0, min(99, depth_rating + effects.get("depth_rating", 0)))

    roster = _apply_situation_special_effects(situation_id, choice_id, roster, context, notes)
    note = notes[0] if notes else option["blurb"]

    new_state = {
        **state, "roster": roster, "depth_rating": depth_rating,
        "fan_support": fan_support, "hot_seat": hot_seat,
    }
    return {"state": new_state, "note": note}


def new_game(city="", team_name=""):
    city = (city or "").strip()[:30] or "Your City"
    team_name = (team_name or "").strip()[:30] or "The Franchise"

    state = {
        "season_number": 1,
        "city": city,
        "team_name": team_name,
        "roster": new_starting_roster(),
        "depth_rating": random.randint(30, 40),
        "fan_support": 50,
        "hot_seat": 20,
        "history": [],
        "streak": 0,
        "max_streak": 0,
    }
    decision = {"season_number": 1, "pick_number": 1, "options": generate_draft_options(1, state["roster"])}
    return {"state": state, "decision": decision}


def advance_dynasty(state, choice_id, prospect=None, depth_signees=None):
    roster = state["roster"]
    depth_rating = state["depth_rating"]

    roster, depth_rating, offseason_notes = resolve_offseason_choice(
        choice_id, roster, depth_rating, prospect=prospect, depth_signees=depth_signees
    )

    season_result = simulate_season(roster, depth_rating, state["season_number"])

    fan_support = max(5, min(99, state.get("fan_support", 50) + _fan_support_delta(season_result)))
    hot_seat = max(0, min(99, state.get("hot_seat", 20) + _hot_seat_delta(season_result)))
    season_result["fan_support"] = fan_support
    season_result["hot_seat"] = hot_seat

    flavor = _flavor_note(season_result, roster, last_flavor=state.get("last_flavor"))
    extra_notes = [flavor]

    if hot_seat >= 80:
        extra_notes.append("Ownership is one bad month from a change.")
    season_result["notes"] = offseason_notes + season_result["notes"] + extra_notes

    streak = state["streak"] + 1 if season_result["champion"] else 0
    max_streak = max(state.get("max_streak", 0), streak)
    history = state["history"] + [season_result]

    next_season_number = state["season_number"] + 1
    game_over = next_season_number > TOTAL_SEASONS

    new_state = {
        "season_number": next_season_number,
        "city": state["city"],
        "team_name": state["team_name"],
        "roster": roster,
        "depth_rating": depth_rating,
        "fan_support": fan_support,
        "hot_seat": hot_seat,
        "last_flavor": flavor,
        "history": history,
        "streak": streak,
        "max_streak": max_streak,
    }

    next_decision = None
    if not game_over:
        offseason = generate_offseason_options(season_result["made_playoffs"], season_result["wins"], roster)
        next_decision = {
            "season_number": next_season_number,
            "pick_number": offseason["pick_number"],
            "options": offseason["options"],
        }

    pending_situation = maybe_generate_situation(
        roster, fan_support, hot_seat,
        champion=season_result["champion"],
        finals_mvp_name=season_result.get("finals_mvp"),
    )

    return {
        "state": new_state,
        "season_result": season_result,
        "next_decision": next_decision,
        "game_over": game_over,
        "three_peat": max_streak >= 3,
        "pending_situation": pending_situation,
    }
