"""Dynasty simulation engine.

Deliberately stateless: every function here takes plain dicts/lists in and
returns plain dicts/lists out. There's no database model backing a
"dynasty run" — the frontend holds the whole game state (roster, history,
season number) and sends it back with each decision.

Design note on prospects: the frontend shows a full scouting profile
(name, position, measurables, traits) for every draft/trade option BEFORE
the player picks. Only the final overall rating is decided at pick time —
that's the "boom or bust" suspense, not the player's identity. The client
echoes back whichever option's `prospect` dict it displayed, and this file
uses that exact data rather than regenerating a new player, so the guy you
saw on the card is the guy who joins your team.

10-season loop, target: string together 3 championships in a row.
"""

import datetime
import math
import random

FIRST_NAMES = [
    "Brock", "Colt", "Tank", "Maverick", "Gunnar", "Jax", "Duke", "Buster", "Tremaine", "Zeke",
    "Knox", "Major", "Chase", "Hunter", "Ryder", "Wyatt", "Chance", "Dash", "King", "Flint",
    "Quantavious", "Jaquan", "Deandre", "Marquis", "Treavon", "Demetrius", "Keyon", "Terrell", 
    "Ladarius", "Dequan", "Trevion", "Jamarcus", "Keshawn", "Antwan", "Davonte", "Jermaine", 
    "Tyrell", "Rondale", "Jacory", "Malique"
]

LAST_NAMES = [
    "Steele", "Stone", "Powers", "Savage", "Storm", "Knight", "Stryker", "Briggs", "Sharpe", "Woodson",
    "Gore", "Slater", "Fletcher", "Butcher", "Irons", "Walker", "Wheeler", "Garrett", "Hardaway", "Vance",
    "Washington", "Jackson", "Williams", "Jefferson", "Robinson", "Banks", "Brooks", "Gaines", "Diggs", "Mack",
    "Boyd", "Moss", "Clay", "Patterson", "Samuels", "Rhodes", "Vaughn", "Hardy", "Tolbert", "Coleman"
]

TRAIT_POOL = [
    "Athletic", "Mobile", "Leader", "High IQ", "Streaky", "Undersized",
    "Injury Prone", "Elite Shooter", "Lockdown Defender", "High Motor",
    "Raw", "Crafty", "Explosive", "Unselfish", "Volume Scorer",
    "Rim Protector", "Vocal", "Quiet Worker", "Clutch", "Inconsistent",
]

POSITIONS = ["PG", "SG", "SF", "PF", "C"]
POSITION_BODY_RANGES = {
    "PG": {"height_in": (72, 76), "weight_lb": (170, 200)},
    "SG": {"height_in": (75, 79), "weight_lb": (190, 215)},
    "SF": {"height_in": (78, 81), "weight_lb": (210, 230)},
    "PF": {"height_in": (80, 83), "weight_lb": (225, 250)},
    "C": {"height_in": (82, 86), "weight_lb": (240, 270)},
}

ROSTER_SLOTS = ["core_1", "core_2", "core_3", "core_4"]
PLAYOFF_ROUNDS = ["Round 1", "Round 2", "Conference Finals", "Finals"]
PLAYOFF_WIN_THRESHOLD = 42  # wins needed (out of 82) to make the playoffs
TOTAL_SEASONS = 10
TOP_LOTTERY_CUTOFF = 4  # picks 1-4 get the Boom-or-Bust option; 5-14 don't


def random_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def format_height(total_inches):
    feet, inches = divmod(total_inches, 12)
    return f"{feet}'{inches}\""


def generate_prospect_profile():
    """A scouting profile: everything about a player except how good he'll
    actually turn out to be. Age/origin get set by whoever calls this,
    depending on context (rookie vs. veteran, draft slot, etc.)."""
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
        "potential": potential if potential is not None else min(99, ovr + random.randint(0, 15)),
        "origin": origin,
        "injury_note": None,
    }


def new_starting_roster():
    """The bad team you inherit: 3 mediocre holdover vets + one open slot
    for the incoming top pick. One vet is flagged as recovering from
    injury — a narrative beat, not a mechanical penalty beyond this
    season's rating."""
    vets = [
        make_player(ovr=random.randint(58, 66), age=random.randint(26, 31), origin="Holdover"),
        make_player(ovr=random.randint(55, 63), age=random.randint(24, 29), origin="Holdover"),
        make_player(ovr=random.randint(52, 60), age=random.randint(23, 30), origin="Holdover"),
    ]
    random.choice(vets)["injury_note"] = (
        "Recovering from injury — expected back at full strength next season."
    )

    return [
        {"slot": "core_1", "player": None},
        {"slot": "core_2", "player": vets[0]},
        {"slot": "core_3", "player": vets[1]},
        {"slot": "core_4", "player": vets[2]},
    ]


DRAFT_ARCHETYPES = [
    {
        "id": "safe",
        "label": "The Safe Pick",
        "blurb": "High floor, limited ceiling. Whatever you see is close to what you get.",
        "ovr_range": (68, 75),
        "potential_bonus_range": (0, 6),
    },
    {
        "id": "balanced",
        "label": "The Balanced Prospect",
        "blurb": "Solid tools across the board. No red flags, no obvious star trait either.",
        "ovr_range": (63, 72),
        "potential_bonus_range": (5, 14),
    },
    {
        "id": "boom_bust",
        "label": "The Boom-or-Bust Swing",
        "blurb": "Scouts are split. Could be a franchise piece — could be out of the league in three years.",
        "ovr_range": (55, 90),
        "potential_bonus_range": (0, 20),
    },
]


def compute_lottery_pick(wins):
    """Worse records skew toward better (lower) picks, same as the real
    lottery — but with real lottery-style luck, not a hard guarantee."""
    min_wins, max_wins = 5, PLAYOFF_WIN_THRESHOLD - 1
    span = max(1, max_wins - min_wins)
    raw = 1 + (wins - min_wins) / span * (14 - 1)
    pick = round(raw)
    pick += random.choice([-2, -1, -1, 0, 0, 0, 1, 1, 2])
    return max(1, min(14, pick))


def generate_draft_options(pick_number):
    """Builds this year's draft board. Picks 1-4 see all three archetypes;
    picks 5-14 don't get the Boom-or-Bust swing — the lottery only gives
    you a real shot at a franchise piece if you're picking near the top."""
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


def generate_offseason_options(made_playoffs, wins=None):
    if not made_playoffs:
        pick_number = compute_lottery_pick(wins)
        return {"pick_number": pick_number, "options": generate_draft_options(pick_number)}

    return {
        "pick_number": None,
        "options": [
            {"id": "run_it_back", "type": "hold", "label": "Run It Back",
             "blurb": "Keep the roster as-is. Stability has value."},
            {"id": "chase_a_star", "type": "trade_up", "label": "Chase a Star",
             "blurb": "Trade assets for a shot at a big talent upgrade. Might not pan out."},
            {"id": "invest_in_depth", "type": "depth", "label": "Invest in Depth",
             "blurb": "Bring in role players. Raises your floor, not your ceiling."},
        ],
    }


def _resolve_draft_choice(choice_id, prospect):
    if choice_id == "trade_for_veteran":
        ovr = random.randint(74, 82)
        potential = ovr
    else:
        arch = next(a for a in DRAFT_ARCHETYPES if a["id"] == choice_id)
        lo, hi = arch["ovr_range"]
        ovr = random.randint(lo, hi)
        potential = min(99, ovr + random.randint(*arch["potential_bonus_range"]))

    return {
        "name": prospect["name"],
        "position": prospect["position"],
        "height": prospect["height"],
        "weight": prospect["weight"],
        "traits": prospect["traits"],
        "age": prospect["age"],
        "ovr": ovr,
        "potential": potential,
        "origin": prospect.get("origin", ""),
        "injury_note": None,
    }


def resolve_offseason_choice(choice_id, roster, depth_rating, prospect=None):
    """Applies the player's decision. Returns (roster, depth_rating, notes).
    `prospect` is the exact scouting profile the client displayed for
    whichever draft/trade option was chosen — reused as-is so the player
    who joins the roster is the same one shown on the card."""
    notes = []

    if choice_id in ("safe", "balanced", "boom_bust", "trade_for_veteran"):
        if prospect is None:
            # Defensive fallback if the client didn't echo back a prospect —
            # shouldn't normally happen, but better than a crash.
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
        if random.random() < 0.45:
            target = min(roster, key=lambda s: s["player"]["ovr"])
            boosted = min(96, target["player"]["ovr"] + random.randint(12, 22))
            target["player"]["ovr"] = boosted
            target["player"]["potential"] = max(target["player"]["potential"], boosted)
            notes.append(f"The trade lands. {target['player']['name']} jumps to a {boosted} overall.")
        else:
            depth_rating = max(0, depth_rating - 8)
            notes.append("The trade talks collapse. You gave up depth pieces for nothing.")

    elif choice_id == "invest_in_depth":
        depth_rating = min(99, depth_rating + random.randint(6, 12))
        notes.append("The bench gets deeper.")

    else:
        raise ValueError(f"Unknown choice_id: {choice_id!r}")

    return roster, depth_rating, notes


def age_and_develop(roster):
    """Applies a year of aging, development/decline, and rare breakout/
    injury events. Mutates player dicts in place; returns narrative notes."""
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
    core_avg = sum(core_ratings) / len(core_ratings) if core_ratings else 40
    rating = 0.72 * core_avg + 0.28 * depth_rating
    return round(max(20, min(99, rating)))


def simulate_regular_season(team_rating):
    win_pct = max(0.10, min(0.85, 0.10 + (team_rating / 100) * 0.80))
    wins = round(win_pct * 82 + random.uniform(-6, 6))
    wins = max(5, min(75, wins))
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


def new_game():
    """Bootstraps a fresh dynasty. Returns the initial state plus the first
    pending decision — always the No. 1 pick, per the inherited 18-65 team."""
    state = {
        "season_number": 1,
        "roster": new_starting_roster(),
        "depth_rating": random.randint(30, 40),
        "history": [],
        "streak": 0,
        "max_streak": 0,
    }
    decision = {
        "season_number": 1,
        "pick_number": 1,
        "options": generate_draft_options(1),
    }
    return {"state": state, "decision": decision}


def advance_dynasty(state, choice_id, prospect=None):
    """Applies one year: resolves the offseason choice, simulates the
    season, and returns the updated state plus the next decision (or None
    if all 10 seasons are done)."""
    roster = state["roster"]
    depth_rating = state["depth_rating"]

    roster, depth_rating, offseason_notes = resolve_offseason_choice(
        choice_id, roster, depth_rating, prospect=prospect
    )

    season_result = simulate_season(roster, depth_rating, state["season_number"])
    season_result["notes"] = offseason_notes + season_result["notes"]

    streak = state["streak"] + 1 if season_result["champion"] else 0
    max_streak = max(state.get("max_streak", 0), streak)
    history = state["history"] + [season_result]

    next_season_number = state["season_number"] + 1
    game_over = next_season_number > TOTAL_SEASONS

    new_state = {
        "season_number": next_season_number,
        "roster": roster,
        "depth_rating": depth_rating,
        "history": history,
        "streak": streak,
        "max_streak": max_streak,
    }

    next_decision = None
    if not game_over:
        offseason = generate_offseason_options(season_result["made_playoffs"], season_result["wins"])
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
