import Button from "../components/Button";
import Badge from "../components/Badge";
import GameCard from "../components/GameCard";
import "./HomePage.css";

const MORE = [
  {
    to: "/games/dynasty",
    title: "Dynasty",
    subtitle: "Build a multi-season franchise. Live with every decision.",
    status: "muted",
    label: "LIVE",
  },
  {
    to: "/games/stat-challenge",
    title: "Stat Challenge",
    subtitle: "Turn sports statistics into a puzzle.",
    status: "muted",
    label: "PLANNED",
  },
  {
    to: "/lab",
    title: "Sports Lab",
    subtitle: "Simulations, experiments, and 'what if' scenarios.",
    status: "muted",
    label: "PLANNED",
  },
  {
    to: "/articles",
    title: "Archive",
    subtitle: "Original reporting and analysis, preserved.",
    status: "active",
    label: "READ",
  },
];

export default function HomePage() {
  return (
    <div>
      <section className="ptm-hero">
        <div className="ptm-container">
          <h1 className="ptm-hero__wordmark">
            PAPER <span>TIGERS</span>
          </h1>
          <p className="ptm-hero__tagline">SPORTS, BUT INTERACTIVE.</p>
          <div className="ptm-hero__actions">
            <Button to="/games" variant="primary">
              PLAY
            </Button>
            <Button to="/lab" variant="secondary">
              LAB
            </Button>
          </div>
        </div>
      </section>

      <section className="ptm-container ptm-featured">
        <p className="ptm-featured__eyebrow">TODAY</p>
        <div className="ptm-featured__row">
          <div>
            <h2 className="ptm-featured__title">23 Guesses</h2>
            <p className="ptm-featured__subtitle">Today's mystery is waiting.</p>
            <Badge tone="live">LIVE</Badge>
          </div>
          <Button to="/games/23-guesses">PLAY</Button>
        </div>
      </section>

      <section className="ptm-container ptm-more">
        <p className="ptm-more__eyebrow">MORE FROM THE LAB</p>
        <div className="ptm-more__grid">
          {MORE.map((item) => (
            <GameCard key={item.to} {...item} />
          ))}
        </div>
      </section>
    </div>
  );
}
