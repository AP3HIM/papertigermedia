import { useState } from "react";
import "./ShareButton.css";

function buildShareText(city, teamName, history, maxStreak, threePeat, legacyScore) {
  const championships = (history || []).filter((h) => h.champion).length;
  const bestSeason = (history || []).reduce(
    (best, h) => (h.wins > (best?.wins ?? -1) ? h : best),
    null
  );

  let text = `🏀 ${city} ${teamName} — a 10-season dynasty.\n`;
  if (typeof legacyScore === "number") {
    text += `Legacy Score: ${legacyScore}\n`;
  }
  text += `${championships} championship${championships === 1 ? "" : "s"}.\n`;
  if (bestSeason) {
    text += `Best season: ${bestSeason.wins}-${bestSeason.losses} (${bestSeason.result}).\n`;
  }
  if (threePeat) {
    text += `Three-peat champions. 👑\n`;
  } else if (maxStreak >= 2) {
    text += `${maxStreak}-peat at the peak.\n`;
  }
  text += `Beat my score:\n`;
  return text;
}

export default function ShareButton({ city, teamName, history, maxStreak, threePeat, legacyScore }) {
  const [copied, setCopied] = useState(false);

  async function handleShare() {
    const text = buildShareText(city, teamName, history, maxStreak, threePeat, legacyScore);
    const url = window.location.href;

    if (navigator.share) {
      try {
        await navigator.share({ title: `${city} ${teamName} Dynasty`, text, url });
        return;
      } catch (err) {
        if (err.name === "AbortError") return; // user cancelled the share sheet
        // fall through to clipboard on any other failure
      }
    }

    try {
      await navigator.clipboard.writeText(`${text}\n${url}`);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // clipboard blocked (rare) — nothing sensible left to do silently
    }
  }

  return (
    <button className="ptm-share-button" onClick={handleShare} type="button">
      {copied ? "COPIED TO CLIPBOARD" : "SHARE YOUR DYNASTY"}
    </button>
  );
}