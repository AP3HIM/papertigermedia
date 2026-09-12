import { useEffect, useState } from "react";

const LOADING_MESSAGES = [
  "Building your franchise...",
  "Tying the laces...",
  "Hiring the coaching staff...",
  "Scheduling the first press conference...",
  "Getting mic'd up for a podcast...",
  "Negotiating with the equipment manager...",
  "Painting the logo at center court...",
  "Setting the ticket prices...",
  "Ordering way too much team merch...",
];

const FADE_MS = 300;
const HOLD_MS = 1800;

export default function LoadingCycler() {
  const [index, setIndex] = useState(0);
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    const interval = setInterval(() => {
      setVisible(false);
      setTimeout(() => {
        setIndex((i) => (i + 1) % LOADING_MESSAGES.length);
        setVisible(true);
      }, FADE_MS);
    }, HOLD_MS);
    return () => clearInterval(interval);
  }, []);

  return (
    <p className={"ptm-dynasty__loading" + (visible ? " is-visible" : "")}>
      {LOADING_MESSAGES[index]}
    </p>
  );
}