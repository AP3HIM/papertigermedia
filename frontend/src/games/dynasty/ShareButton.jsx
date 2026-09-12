import { useState } from "react";
import html2canvas from "html2canvas";
import "./ShareButton.css";

function buildShareText(city, teamName, history, maxStreak, threePeat, legacyScore) {
  const championships = (history || []).filter((h) => h.champion).length;
  const bestSeason = (history || []).reduce(
    (best, h) => (h.wins > (best?.wins ?? -1) ? h : best),
    null
  );

  let text = `${city} ${teamName}, a 10 season dynasty.\n`;
  if (typeof legacyScore === "number") {
    text += `Legacy Score: ${legacyScore}\n`;
  }
  text += `${championships} championship${championships === 1 ? "" : "s"}.\n`;
  if (bestSeason) {
    text += `Best season: ${bestSeason.wins}-${bestSeason.losses} (${bestSeason.result}).\n`;
  }
  if (threePeat) {
    text += `Three-peat champions.\n`;
  } else if (maxStreak >= 2) {
    text += `${maxStreak}-peat at the peak.\n`;
  }
  text += `Beat my score:\n`;
  return text;
}

export default function ShareButton({
  city, teamName, history, maxStreak, threePeat, legacyScore, captureRef,
}) {
  const [status, setStatus] = useState("idle"); // idle | working | copied | saved

  async function handleShare() {
    setStatus("working");
    const text = buildShareText(city, teamName, history, maxStreak, threePeat, legacyScore);
    const url = window.location.href;

    let file = null;
    if (captureRef?.current) {
      try {
        const canvas = await html2canvas(captureRef.current, {
          backgroundColor: "#f7f3ea",
          scale: 2,
        });
        const blob = await new Promise((resolve) => canvas.toBlob(resolve, "image/png"));
        if (blob) {
          file = new File([blob], `${city}-${teamName}-dynasty.png`, { type: "image/png" });
        }
      } catch {
        file = null; // screenshot failed, fall back to text-only sharing below
      }
    }

    if (file && navigator.canShare && navigator.canShare({ files: [file] })) {
      try {
        await navigator.share({ files: [file], title: `${city} ${teamName} Dynasty`, text });
        setStatus("idle");
        return;
      } catch (err) {
        if (err.name === "AbortError") {
          setStatus("idle");
          return;
        }
        // fall through to the download fallback below
      }
    }

    if (file) {
      const link = document.createElement("a");
      link.href = URL.createObjectURL(file);
      link.download = file.name;
      link.click();
      URL.revokeObjectURL(link.href);
      setStatus("saved");
      setTimeout(() => setStatus("idle"), 2500);
      return;
    }

    if (navigator.share) {
      try {
        await navigator.share({ title: `${city} ${teamName} Dynasty`, text, url });
        setStatus("idle");
        return;
      } catch (err) {
        if (err.name === "AbortError") {
          setStatus("idle");
          return;
        }
      }
    }

    try {
      await navigator.clipboard.writeText(`${text}\n${url}`);
      setStatus("copied");
      setTimeout(() => setStatus("idle"), 2000);
    } catch {
      setStatus("idle");
    }
  }

  const label = {
    idle: "SHARE YOUR DYNASTY",
    working: "CAPTURING...",
    copied: "COPIED TO CLIPBOARD",
    saved: "IMAGE SAVED",
  }[status];

  return (
    <button className="ptm-share-button" onClick={handleShare} type="button" disabled={status === "working"}>
      {label}
    </button>
  );
}