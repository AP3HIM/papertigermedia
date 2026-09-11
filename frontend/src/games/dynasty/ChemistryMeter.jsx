import "./ChemistryMeter.css";

function chemistryLabel(value) {
  if (value >= 80) return "LOCKER ROOM IS TIGHT";
  if (value >= 55) return "GOOD VIBES";
  if (value >= 40) return "SOME FRICTION";
  if (value >= 20) return "TENSION IN THE ROOM";
  return "LOCKER ROOM IS TOXIC";
}

export default function ChemistryMeter({ value }) {
  return (
    <div className="ptm-chemistry-meter">
      <div className="ptm-chemistry-meter__label">
        <span>CHEMISTRY</span>
        <span>{value}</span>
      </div>
      <div className="ptm-chemistry-meter__track">
        <div className="ptm-chemistry-meter__fill" style={{ width: `${value}%` }} />
      </div>
      <p className="ptm-chemistry-meter__status">{chemistryLabel(value)}</p>
    </div>
  );
}