import { useEffect, useState } from "react";
import Button from "../../components/Button";
import RosterPanel from "./RosterPanel";

function useCountUp(target, durationMs = 500) {
  const [value, setValue] = useState(0);

  useEffect(() => {
    let start = null;
    let frame;

    function step(timestamp) {
      if (start === null) start = timestamp;
      const progress = Math.min(1, (timestamp - start) / durationMs);
      setValue(Math.round(progress * target));
      if (progress < 1) frame = requestAnimationFrame(step);
    }

    frame = requestAnimationFrame(step);
    return () => cancelAnimationFrame(frame);
  }, [target, durationMs]);

  return value;
}

export default function SeasonResultScreen({ result, totalSeasons, onContinue, roster, depthRating }) {
  const wins = useCountUp(result.wins);
  const losses = useCountUp(result.losses);
  const isChampion = result.champion;

  return (
    <div className="ptm-dynasty">
      <div className="ptm-dynasty__meta">
        <span>
          SEASON {result.season_number} OF {totalSeasons}
        </span>
        <span className="ptm-dynasty__dot">·</span>
        <span>TEAM RATING {result.team_rating}</span>
      </div>

      <p className={"ptm-dynasty__record" + (isChampion ? " is-champion" : "")}>
        {wins}–{losses}
      </p>
      <p className={"ptm-dynasty__result-line" + (isChampion ? " is-champion" : "")}>{result.result}</p>

      {result.notes.length > 0 && (
        <ul className="ptm-dynasty__notes">
          {result.notes.map((note, i) => (
            <li key={i}>{note}</li>
          ))}
        </ul>
      )}

      <div className="ptm-dynasty__continue">
        <Button onClick={onContinue}>CONTINUE</Button>
      </div>

      <RosterPanel roster={roster} depthRating={depthRating} />
    </div>
  );
}
