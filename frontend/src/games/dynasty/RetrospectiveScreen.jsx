import { useRef } from "react";
import Button from "../../components/Button";
import RosterPanel from "./RosterPanel";
import ShareButton from "./ShareButton";

function closingLine(championships, threePeat) {
  if (threePeat) return "History remembers dynasties. This was one.";
  if (championships >= 4) return `${championships} banners. A legitimate dynasty.`;
  if (championships >= 2) return `${championships} banners. You built something real.`;
  if (championships === 1) return "One banner. Not bad for ten years of work.";
  return "No rings this time. Some rebuilds just take longer.";
}

export default function RetrospectiveScreen({
  city,
  teamName,
  history,
  roster,
  depthRating,
  maxStreak,
  threePeat,
  legacyScore,
  onRestart,
}) {
  const championships = history.filter((h) => h.champion).length;
  const captureRef = useRef(null);

  return (
    <div className="ptm-dynasty">
      <div ref={captureRef} className="ptm-dynasty__capture">
        <p className="ptm-dynasty__eyebrow">TEN SEASONS</p>
        <h1 className="ptm-dynasty__title">
          {city} {teamName}
        </h1>

        {threePeat && <p className="ptm-dynasty__three-peat">YOU BUILT A 3-PEAT.</p>}

        {typeof legacyScore === "number" && (
          <div className="ptm-dynasty__legacy-score">
            <span className="ptm-dynasty__legacy-score-value">{legacyScore}</span>
            <span className="ptm-dynasty__legacy-score-label">LEGACY SCORE</span>
          </div>
        )}

        <table className="ptm-dynasty__table">
          <thead>
            <tr>
              <th>Season</th>
              <th>Record</th>
              <th>Result</th>
            </tr>
          </thead>
          <tbody>
            {history.map((h) => (
              <tr key={h.season_number} className={h.champion ? "is-champion" : ""}>
                <td>{h.season_number}</td>
                <td>
                  {h.wins}-{h.losses}
                </td>
                <td>{h.result}</td>
              </tr>
            ))}
          </tbody>
        </table>

        <div className="ptm-dynasty__summary">
          <div>
            <span className="ptm-dynasty__summary-value">{championships}</span>
            <span className="ptm-dynasty__summary-label">CHAMPIONSHIPS</span>
          </div>
          <div>
            <span className="ptm-dynasty__summary-value">{maxStreak}</span>
            <span className="ptm-dynasty__summary-label">BEST STREAK</span>
          </div>
        </div>

        <p className="ptm-dynasty__closing-line">{closingLine(championships, threePeat)}</p>
      </div>

      <div className="ptm-dynasty__continue">
        <ShareButton
          city={city}
          teamName={teamName}
          history={history}
          maxStreak={maxStreak}
          threePeat={threePeat}
          legacyScore={legacyScore}
          captureRef={captureRef}
        />
        <Button onClick={onRestart}>START A NEW DYNASTY</Button>
      </div>

      <RosterPanel roster={roster} depthRating={depthRating} />
    </div>
  );
}