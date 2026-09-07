import FanMeter from "./FanMeter";

export default function FranchiseHeader({ city, teamName, seasonNumber, totalSeasons, fanSupport }) {
  return (
    <div className="ptm-franchise-header">
      <div>
        <p className="ptm-franchise-header__name">
          {city} {teamName}
        </p>
        <p className="ptm-franchise-header__season">
          SEASON {seasonNumber} OF {totalSeasons}
        </p>
      </div>
      {typeof fanSupport === "number" && <FanMeter value={fanSupport} />}
    </div>
  );
}
