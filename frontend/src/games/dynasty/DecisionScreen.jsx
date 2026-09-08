import FranchiseHeader from "./FranchiseHeader";
import RosterPanel from "./RosterPanel";

export default function DecisionScreen({
  city,
  teamName,
  seasonNumber,
  totalSeasons,
  fanSupport,
  hotSeat,
  pickNumber,
  options,
  onChoose,
  priorResult,
  roster,
  depthRating,
}) {
  const isDraft = options.some((o) => o.prospect && o.type !== "trade_up");

  return (
    <div className="ptm-dynasty">
      <FranchiseHeader
        city={city}
        teamName={teamName}
        seasonNumber={seasonNumber}
        totalSeasons={totalSeasons}
        fanSupport={fanSupport}
        hotSeat={hotSeat}
      />

      {priorResult && (
        <p className="ptm-dynasty__context">
          Coming off a {priorResult.wins}-{priorResult.losses} season ({priorResult.result}).
        </p>
      )}

      {isDraft && (
        <p className="ptm-dynasty__context">
          {pickNumber === 1
            ? "You have the No. 1 pick."
            : `You have the No. ${pickNumber} pick in the Draft Lottery.`}
        </p>
      )}

      <div className="ptm-dynasty__options">
        {options.map((option) => (
          <button key={option.id} className="ptm-dynasty__option" onClick={() => onChoose(option)}>
            {option.prospect ? (
              <>
                <div className="ptm-dynasty__option-top">
                  <span className="ptm-dynasty__option-name">{option.prospect.name}</span>
                  <span className="ptm-dynasty__option-tag">{option.label}</span>
                </div>
                <p className="ptm-dynasty__option-measurables">
                  {option.prospect.position} · {option.prospect.height} · {option.prospect.weight} lbs ·
                  Age {option.prospect.age}
                  {option.prospect.accolade ? ` · ${option.prospect.accolade}` : ""}
                </p>
                <p className="ptm-dynasty__option-traits">{option.prospect.traits.join(", ")}</p>
              </>
            ) : (
              <span className="ptm-dynasty__option-label">{option.label}</span>
            )}
            <span className="ptm-dynasty__option-blurb">{option.blurb}</span>
          </button>
        ))}
      </div>

      <RosterPanel roster={roster} depthRating={depthRating} />
    </div>
  );
}
