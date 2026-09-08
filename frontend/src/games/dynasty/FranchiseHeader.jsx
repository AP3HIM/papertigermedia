import FanMeter from "./FanMeter";
import HotSeatMeter from "./HotSeatMeter";

export default function FranchiseHeader({ city, teamName, seasonNumber, totalSeasons, fanSupport, hotSeat }) {
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
      <div className="ptm-franchise-header__meters">
        {typeof fanSupport === "number" && <FanMeter value={fanSupport} />}
        {typeof hotSeat === "number" && <HotSeatMeter value={hotSeat} />}
      </div>
    </div>
  );
}
