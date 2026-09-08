const API_BASE = import.meta.env.VITE_API_BASE_URL || "/api";

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!res.ok) {
    let detail = `Request failed (${res.status})`;
    try {
      const body = await res.json();
      detail = body.detail || detail;
    } catch {
      // response body wasn't JSON — stick with the generic message
    }
    throw new Error(detail);
  }

  return res.json();
}

export function getTodayPuzzle() {
  return request("/games/23-guesses/today/");
}

export function submitGuess({ puzzleId, guess, clueIndex }) {
  return request("/games/23-guesses/guess/", {
    method: "POST",
    body: JSON.stringify({ puzzle_id: puzzleId, guess, clue_index: clueIndex }),
  });
}

export function newDynastyGame({ city, teamName } = {}) {
  return request("/dynasty/new-game/", {
    method: "POST",
    body: JSON.stringify({ city, team_name: teamName }),
  });
}

export function advanceDynasty({ state, choiceId, chosenOption }) {
  return request("/dynasty/advance/", {
    method: "POST",
    body: JSON.stringify({ state, choice_id: choiceId, chosen_option: chosenOption }),
  });
}

export function resolveDynastySituation({ state, situationId, choiceId, context }) {
  return request("/dynasty/resolve-situation/", {
    method: "POST",
    body: JSON.stringify({ state, situation_id: situationId, choice_id: choiceId, context }),
  });
}
