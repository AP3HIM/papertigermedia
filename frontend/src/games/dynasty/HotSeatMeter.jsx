function heatLabel(value) {
  if (value >= 80) return "ON THE HOT SEAT";
  if (value >= 55) return "OWNERSHIP IS WATCHING";
  return "JOB SECURE";
}

export default function HotSeatMeter({ value }) {
  return (
    <div className="ptm-hot-seat-meter">
      <div className="ptm-hot-seat-meter__label">
        <span>HOT SEAT</span>
        <span>{value}</span>
      </div>
      <div className="ptm-hot-seat-meter__track">
        <div className="ptm-hot-seat-meter__fill" style={{ width: `${value}%` }} />
      </div>
      <p className="ptm-hot-seat-meter__status">{heatLabel(value)}</p>
    </div>
  );
}
