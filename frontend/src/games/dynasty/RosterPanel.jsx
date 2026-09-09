export default function RosterPanel({ roster, depthRating }) {
  return (
    <div className="ptm-roster">
      <p className="ptm-roster__heading">Your Team</p>

      <div className="ptm-roster__list">
        {roster.map((slot) => (
          <div key={slot.slot} className="ptm-roster__player">
            {slot.player ? (
              <>
                <div className="ptm-roster__player-top">
                  <span className="ptm-roster__player-name">{slot.player.name}</span>
                  <span className="ptm-roster__player-ovr-badge">{slot.player.ovr}</span>
                </div>
                <p className="ptm-roster__player-meta">
                  {slot.player.position} · {slot.player.height} · {slot.player.weight} lbs · Age{" "}
                  {slot.player.age} · ${slot.player.salary}M
                  {slot.player.origin ? ` · ${slot.player.origin}` : ""}
                </p>
                {slot.player.traits && slot.player.traits.length > 0 && (
                  <p className="ptm-roster__player-traits">{slot.player.traits.join(", ")}</p>
                )}
                {slot.player.injury_note && (
                  <p className="ptm-roster__player-injury">{slot.player.injury_note}</p>
                )}
              </>
            ) : (
              <p className="ptm-roster__player-empty">Open roster spot.</p>
            )}
          </div>
        ))}
      </div>

      <div className="ptm-roster__bench">
        <span>Bench Depth</span>
        <span>
          {depthRating}
          <span className="ptm-roster__bench-note"> (not a player rating)</span>
        </span>
      </div>
    </div>
  );
}
