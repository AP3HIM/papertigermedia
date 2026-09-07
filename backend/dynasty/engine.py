"""Dynasty simulation engine.

Deliberately stateless — see engine module history in chat for the full
rationale. v3 changes: rescaled ratings so numbers feel familiar to anyone
used to 2K/Madden, a steeper win curve so one great pick can't single-
handedly swing 20 wins, a fan support meter with flavor text, named
specifics for the "Chase a Star" and "Invest in Depth" offseason options,
a 5th roster slot, and custom city/team name.
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
    "Former MVP", "2x All-Star", "3x All-Star", "Former DPOY",
    "5x All-Star", "Scoring Champion",
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

CHAMPION_FLAVOR = [
    "The parade route is already blocked off downtown.",
    "Ownership quietly orders a bigger trophy case.",
    "Local news leads with you for a change.",
]
PLAYOFF_FLAVOR = [
    "Ticket prices creep up. Nobody's complaining yet.",
    "Merch sales are up. Ownership is pleased.",
    "The city actually shows up for the parade rumors.",
]
DECENT_FLAVOR = [
    "Fans are cautiously optimistic. Cautiously.",
    "The arena's still mostly full. For now.",
]
BAD_FLAVOR = [
    "Ownership is \u201cexploring all options,\u201d which is never good.",
    "Tickets are basically free at this point.",
    "Local radio is calling for changes. All of them.",
    "Someone's mom skipped the game. That's how you know.",
]


def random_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


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
    """The bad team you inherit: 4 mediocre holdover vets + one open slot
    for the incoming top pick."""
    vets = [
        make_player(ovr=random.randint(60, 68), age=random.randint(26, 31), origin="Holdover"),
        make_player(ovr=random.randint(58, 66), age=random.randint(24, 29), origin="Holdover"),
        make_player(ovr=random.randint(56, 64), age=random.randint(23, 30), origin="Holdover"),
        make_player(ovr=random.randint(54, 62), age=random.randint(22, 29), origin="Holdover"),
    ]
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


def compute_lottery_pick(wins):
    min_wins, max_wins = 5, PLAYOFF_WIN_THRESHOLD - 1
    span = max(1, max_wins - min_wins)
    raw = 1 + (wins - min_wins) / span * (14 - 1)
    pick = round(raw)
    pick += random.choice([-2, -1, -1, 0, 0, 0, 1, 1, 2])
    return max(1, min(14, pick))


def generate_draft_options(pick_number):
    draft_year = datetime.date.today().year
    archetypes = DRAFT_ARCHETYPES if pick_number <= TOP_LOTTERY_CUTOFF else [
        a for a in DRAFT_ARCHETYPES if a["id"] != "boom_bust"
    ]

    options = []
    for arch in archetypes:
        profile = generate_prospect_profile()
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
        return {"pick_number": pick_number, "options": generate_draft_options(pick_number)}

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
        target = min(roster, key=lambda s: s["player"]["ovr"] if s["player"] else -1)
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
            target = min(roster, key=lambda s: s["player"]["ovr"] if s["player"] else -1)
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


def compute_team_rating(roster, depth_rating):
    core_ratings = [s["player"]["ovr"] for s in roster if s["player"]]
    core_avg = sum(core_ratings) / len(core_ratings) if core_ratings else 45
    rating = 0.75 * core_avg + 0.25 * depth_rating
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


def _flavor_note(season_result):
    if season_result["champion"]:
        pool = CHAMPION_FLAVOR
    elif season_result["made_playoffs"]:
        pool = PLAYOFF_FLAVOR
    elif season_result["wins"] >= 32:
        pool = DECENT_FLAVOR
    else:
        pool = BAD_FLAVOR
    return random.choice(pool)


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


def simulate_season(roster, depth_rating, season_number):
    dev_notes = age_and_develop(roster)
    rating = compute_team_rating(roster, depth_rating)
    wins, losses = simulate_regular_season(rating)
    playoff = simulate_playoffs(rating, wins)

    return {
        "season_number": season_number,
        "team_rating": rating,
        "wins": wins,
        "losses": losses,
        "result": playoff["result"],
        "champion": playoff["champion"],
        "made_playoffs": playoff["made_playoffs"],
        "notes": dev_notes,
    }


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
        "history": [],
        "streak": 0,
        "max_streak": 0,
    }
    decision = {"season_number": 1, "pick_number": 1, "options": generate_draft_options(1)}
    return {"state": state, "decision": decision}


def advance_dynasty(state, choice_id, prospect=None, depth_signees=None):
    roster = state["roster"]
    depth_rating = state["depth_rating"]

    roster, depth_rating, offseason_notes = resolve_offseason_choice(
        choice_id, roster, depth_rating, prospect=prospect, depth_signees=depth_signees
    )

    season_result = simulate_season(roster, depth_rating, state["season_number"])
    fan_support = max(5, min(99, state.get("fan_support", 50) + _fan_support_delta(season_result)))
    season_result["fan_support"] = fan_support
    season_result["notes"] = offseason_notes + season_result["notes"] + [_flavor_note(season_result)]

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

    return {
        "state": new_state,
        "season_result": season_result,
        "next_decision": next_decision,
        "game_over": game_over,
        "three_peat": max_streak >= 3,
    }
