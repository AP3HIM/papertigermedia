import "./Stat.css";

export default function Stat({ value, label }) {
  return (
    <div className="ptm-stat">
      <span className="ptm-stat__value">{value}</span>
      <span className="ptm-stat__label">{label}</span>
    </div>
  );
}
