import FranchiseHeader from "./FranchiseHeader";

export default function SituationScreen({
  city,
  teamName,
  seasonNumber,
  totalSeasons,
  fanSupport,
  hotSeat,
  chemistry,
  situation,
  onChoose,
}) {
  return (
    <div className="ptm-dynasty">
      <FranchiseHeader
        city={city}
        teamName={teamName}
        seasonNumber={seasonNumber}
        totalSeasons={totalSeasons}
        fanSupport={fanSupport}
        hotSeat={hotSeat}
        chemistry={chemistry}
      />

      <p className="ptm-situation__eyebrow">DEVELOPING</p>
      <p className="ptm-situation__prompt">{situation.prompt}</p>

      <div className="ptm-dynasty__options">
        {situation.options.map((option) => (
          <button
            key={option.id}
            className="ptm-dynasty__option"
            onClick={() => onChoose(option)}
          >
            <span className="ptm-dynasty__option-label">{option.label}</span>
            <span className="ptm-dynasty__option-blurb">{option.blurb}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
