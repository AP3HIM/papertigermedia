import { useState } from "react";
import FranchiseHeader from "./FranchiseHeader";
import RosterPanel from "./RosterPanel";

const DRAFT_CLASS_INFO = {
  generational: { label: "THE GENERATIONAL CLASS", note: "Scouts won't shut up about one name in this class." },
  deep: { label: "THE DEEP CLASS", note: "No superstar, but the floor on every prospect is higher than usual." },
  weak: { label: "THE WEAK CLASS", note: "Scouts are already calling this one a bust year." },
  guard_heavy: { label: "THE GUARD CLASS", note: "Loaded at point guard and shooting guard. Thin everywhere else." },
  big_man: { label: "THE BIG MAN CLASS", note: "A rare year where the best prospects are all up front." },
};

const BENCH_ALLOCATION_BASE = 6;
const BENCH_ALLOCATION_SCALE = 24;
const SALARY_CAP = 140;

function estimateCapSpace(roster, depthRating) {
  const coreSalary = (roster || []).reduce((sum, s) => sum + (s.player?.salary || 0), 0);
  const benchAllocation = BENCH_ALLOCATION_BASE + ((depthRating || 0) / 99) * BENCH_ALLOCATION_SCALE;
  return Math.round((SALARY_CAP - coreSalary - benchAllocation) * 10) / 10;
}

function ChemistryTag({ value }) {
  if (typeof value !== "number" || value === 0) return null;
  const sign = value > 0 ? "+" : "";
  return (
    <span className={"ptm-dynasty__option-chemistry" + (value > 0 ? " is-positive" : " is-negative")}>
      {sign}
      {value} CHEM
    </span>
  );
}

function OptionCard({ option, selected, onClick }) {
  return (
    <button
      className={"ptm-dynasty__option" + (selected ? " is-selected" : "")}
      onClick={onClick}
      type="button"
    >
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
          {option.prospect.traits && (
            <p className="ptm-dynasty__option-traits">
              {option.prospect.traits.join(", ")}
              <ChemistryTag value={option.prospect.chemistry_preview} />
            </p>
          )}
        </>
      ) : (
        <span className="ptm-dynasty__option-label">{option.label}</span>
      )}
      <span className="ptm-dynasty__option-blurb">{option.blurb}</span>
    </button>
  );
}

export default function DecisionScreen({
  city,
  teamName,
  seasonNumber,
  totalSeasons,
  fanSupport,
  hotSeat,
  chemistry,
  pickNumber,
  draftClass,
  options,
  onChoose,
  priorResult,
  roster,
  depthRating,
}) {
  const isDraft = pickNumber !== null && pickNumber !== undefined;
  const classInfo = isDraft ? DRAFT_CLASS_INFO[draftClass] : null;
  const capSpace = estimateCapSpace(roster, depthRating);

  const primaryOptions = options.filter((o) => o.type !== "free_agent" && o.type !== "trade_offer");
  const faOptions = options.filter((o) => o.type === "free_agent");
  const tradeOptions = options.filter((o) => o.type === "trade_offer");

  const [primaryId, setPrimaryId] = useState(null);
  const [faIds, setFaIds] = useState([]);
  const [tradeIds, setTradeIds] = useState([]);

  function toggleFa(id) {
    setFaIds((prev) => (prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]));
  }

  function toggleTrade(id) {
    setTradeIds((prev) => (prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]));
  }

  function handleSubmit() {
    const chosen = [];
    const primary = primaryOptions.find((o) => o.id === primaryId);
    if (primary) chosen.push(primary);
    faOptions.forEach((o) => {
      if (faIds.includes(o.id)) chosen.push(o);
    });
    tradeOptions.forEach((o) => {
      if (tradeIds.includes(o.id)) chosen.push(o);
    });
    onChoose(chosen);
  }

  const canSubmit = Boolean(primaryId);

  return (
    <div className="ptm-dynasty ptm-dynasty--offseason">
      <FranchiseHeader
        city={city}
        teamName={teamName}
        seasonNumber={seasonNumber}
        totalSeasons={totalSeasons}
        fanSupport={fanSupport}
        hotSeat={hotSeat}
        chemistry={chemistry}
      />

      <div className="ptm-offseason__grid">
        <div className="ptm-offseason__column">
          <p className="ptm-offseason__heading">{isDraft ? "DRAFT" : "YOUR MOVE"}</p>
          {isDraft && (
            <p className="ptm-dynasty__context">
              {pickNumber === 1
                ? "You have the No. 1 pick."
                : `You have the No. ${pickNumber} pick in the Draft Lottery.`}
            </p>
          )}
          {classInfo && (
            <div className="ptm-draft-class-banner">
              <p className="ptm-draft-class-banner__label">{classInfo.label}</p>
              <p className="ptm-draft-class-banner__note">{classInfo.note}</p>
            </div>
          )}
          <div className="ptm-dynasty__options">
            {primaryOptions.map((option) => (
              <OptionCard
                key={option.id}
                option={option}
                selected={primaryId === option.id}
                onClick={() => setPrimaryId(option.id)}
              />
            ))}
          </div>
        </div>

        <div className="ptm-offseason__column ptm-offseason__column--center">
          <p className="ptm-cap-space">
            CAP SPACE <span className={capSpace < 0 ? "is-over" : ""}>${capSpace}M</span>
          </p>
          {priorResult && (
            <p className="ptm-dynasty__context">
              Coming off a {priorResult.wins}-{priorResult.losses} season ({priorResult.result}).
            </p>
          )}
          <RosterPanel roster={roster} depthRating={depthRating} />
        </div>

        <div className="ptm-offseason__column">
          <p className="ptm-offseason__heading">FREE AGENCY</p>
          {faOptions.length === 0 && (
            <p className="ptm-dynasty__context">No cap space to work with this offseason.</p>
          )}
          <div className="ptm-dynasty__options">
            {faOptions.map((option) => (
              <OptionCard
                key={option.id}
                option={option}
                selected={faIds.includes(option.id)}
                onClick={() => toggleFa(option.id)}
              />
            ))}
          </div>
        </div>
      </div>

      {tradeOptions.length > 0 && (
        <div className="ptm-offseason__trade">
          <p className="ptm-offseason__heading">TRADE {tradeOptions.length > 1 ? "OFFERS" : "OFFER"}</p>
          <div className="ptm-dynasty__options">
            {tradeOptions.map((option) => (
              <OptionCard
                key={option.id}
                option={option}
                selected={tradeIds.includes(option.id)}
                onClick={() => toggleTrade(option.id)}
              />
            ))}
          </div>
        </div>
      )}

      <button
        className="ptm-offseason__submit"
        onClick={handleSubmit}
        disabled={!canSubmit}
        type="button"
      >
        Confirm Offseason Moves
      </button>
    </div>
  );
}