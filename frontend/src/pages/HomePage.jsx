import Button from "../components/Button";
import Badge from "../components/Badge";
import GameCard from "../components/GameCard";
import "./HomePage.css";

const MORE = [
  {
    to: "/games/23-guesses",
    title: "23 Guesses",
    subtitle: "Today's mystery, one clue at a time.",
    status: "live",
    label: "LIVE",
  },
  {
    to: "/articles",
    title: "Archive",
    subtitle: "Original reporting and analysis, preserved.",
    status: "live",
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
        <p className="ptm-featured__eyebrow">FEATURED</p>
        <div className="ptm-featured__row">
          <div>
            <h2 className="ptm-featured__title">Dynasty</h2>
            <p className="ptm-featured__subtitle">Ten seasons. Build an era. Live with every decision.</p>
            <Badge tone="live">LIVE</Badge>
          </div>
          <Button to="/games/dynasty">PLAY</Button>
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