const SAVE_KEY = "ptm:dynasty:save";

export function readSave() {
  try {
    const raw = window.sessionStorage.getItem(SAVE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

export function writeSave(save) {
  try {
    window.sessionStorage.setItem(SAVE_KEY, JSON.stringify(save));
  } catch {
    // sessionStorage unavailable — the game still works, it just won't
    // survive an accidental refresh.
  }
}

export function clearSave() {
  try {
    window.sessionStorage.removeItem(SAVE_KEY);
  } catch {
    // ignore
  }
}
