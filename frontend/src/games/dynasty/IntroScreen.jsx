import { useMemo, useState } from "react";
import Button from "../../components/Button";

function randomRecord() {
  const wins = 10 + Math.floor(Math.random() * 15); // 10-24
  return { wins, losses: 82 - wins };
}

export default function IntroScreen({ onStart }) {
  const record = useMemo(randomRecord, []);
  const [city, setCity] = useState("");
  const [teamName, setTeamName] = useState("");

  return (
    <div className="ptm-dynasty ptm-dynasty--intro">
      <p className="ptm-dynasty__eyebrow">DYNASTY</p>
      <h1 className="ptm-dynasty__record">
        {record.wins}–{record.losses}
      </h1>
      <p className="ptm-dynasty__intro-line">
        That was last season. You've got the No. 1 pick, no real budget
        constraints, and ten years to turn this into something.
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

      <Button onClick={() => onStart(city, teamName)}>MAKE YOUR PICK</Button>
    </div>
  );
}
