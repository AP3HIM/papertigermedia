import { useMemo, useState } from "react";
import Button from "../../components/Button";

function randomRecord() {
  const wins = 10 + Math.floor(Math.random() * 15); // 10-24
  return { wins, losses: 82 - wins };
}

const PHILOSOPHIES = [
  {
    id: "win_now",
    label: "WIN NOW",
    note: "Veteran development, free agents prefer you \u2014 older players decline faster.",
  },
  {
    id: "development",
    label: "DEVELOPMENT",
    note: "Young players improve faster \u2014 veterans are less interested in joining.",
  },
  {
    id: "small_market",
    label: "SMALL MARKET",
    note: "Cheap players develop better, draft picks matter more \u2014 stars are harder to keep.",
  },
  {
    id: "superteam",
    label: "SUPERTEAM",
    note: "Stars are more likely to join you \u2014 the cap pressure is real.",
  },
];

export default function IntroScreen({ onStart }) {
  const record = useMemo(randomRecord, []);
  const [city, setCity] = useState("");
  const [teamName, setTeamName] = useState("");
  const [philosophy, setPhilosophy] = useState("win_now");

  return (
    <div className="ptm-dynasty ptm-dynasty--intro">
      <p className="ptm-dynasty__eyebrow">DYNASTY</p>
      <h1 className="ptm-dynasty__record">
        {record.wins}–{record.losses}
      </h1>
      <p className="ptm-dynasty__intro-line">
        That was last season. You've got the No. 1 pick, a salary cap to manage,
        and ten years to turn this into something.
      </p>

      <div className="ptm-dynasty__setup">
        <label className="ptm-dynasty__field">
          <span>City</span>
          <input type="text" value={city} onChange={(e) => setCity(e.target.value)} placeholder="Portland" maxLength={30} />
        </label>
        <label className="ptm-dynasty__field">
          <span>Team Name</span>
          <input
            type="text"
            value={teamName}
            onChange={(e) => setTeamName(e.target.value)}
            placeholder="Timberwolves"
            maxLength={30}
          />
        </label>
      </div>

      <p className="ptm-philosophy__label">CHOOSE YOUR FRONT OFFICE</p>
      <div className="ptm-philosophy__grid">
        {PHILOSOPHIES.map((p) => (
          <button
            key={p.id}
            type="button"
            className={"ptm-philosophy__card" + (philosophy === p.id ? " is-selected" : "")}
            onClick={() => setPhilosophy(p.id)}
          >
            <span className="ptm-philosophy__card-title">{p.label}</span>
            <span className="ptm-philosophy__card-note">{p.note}</span>
          </button>
        ))}
      </div>

      <Button onClick={() => onStart(city, teamName, philosophy)}>MAKE YOUR PICK</Button>
    </div>
  );
}
