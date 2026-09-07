import Button from "../../components/Button";

export default function IntroScreen({ onStart }) {
  return (
    <div className="ptm-dynasty ptm-dynasty--intro">
      <p className="ptm-dynasty__eyebrow">DYNASTY</p>
      <h1 className="ptm-dynasty__record">18–65</h1>
      <p className="ptm-dynasty__intro-line">
        That was last season. You've got the No. 1 pick, no real budget
        constraints, and ten years to turn this into a dynasty.
      </p>
      <Button onClick={onStart}>MAKE YOUR PICK</Button>
    </div>
  );
}
