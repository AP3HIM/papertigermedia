const STREAK_KEY = "ptm:23guesses:streak";
const progressKey = (dateStr) => `ptm:23guesses:progress:${dateStr}`;

function safeRead(key, fallback) {
  try {
    const raw = window.localStorage.getItem(key);
    return raw ? JSON.parse(raw) : fallback;
  } catch {
    return fallback;
  }
}

function safeWrite(key, value) {
  try {
    window.localStorage.setItem(key, JSON.stringify(value));
  } catch {
    // localStorage unavailable (private browsing, etc.) — fail silently,
    // the game still works, it just won't persist across reloads.
  }
}

// --- per-day game progress, so a page refresh doesn't reset you ---

export function readProgress(dateStr) {
  return safeRead(progressKey(dateStr), null);
}

export function writeProgress(dateStr, progress) {
  safeWrite(progressKey(dateStr), progress);
}

// --- streak, tracked across days ---

function isYesterday(dateStr, todayStr) {
  const d = new Date(`${dateStr}T00:00:00`);
  const today = new Date(`${todayStr}T00:00:00`);
  const oneDay = 24 * 60 * 60 * 1000;
  return Math.round((today - d) / oneDay) === 1;
}

export function getStreak() {
  return safeRead(STREAK_KEY, { count: 0, lastWonDate: null }).count;
}

export function recordResult(todayStr, won) {
  const streak = safeRead(STREAK_KEY, { count: 0, lastWonDate: null });

  if (!won) {
    const next = { count: 0, lastWonDate: streak.lastWonDate };
    safeWrite(STREAK_KEY, next);
    return next.count;
  }

  if (streak.lastWonDate === todayStr) {
    return streak.count; // already recorded a win today
  }

  const continuing = streak.lastWonDate && isYesterday(streak.lastWonDate, todayStr);
  const next = { count: continuing ? streak.count + 1 : 1, lastWonDate: todayStr };
  safeWrite(STREAK_KEY, next);
  return next.count;
}
