import Badge from "./Badge";
import Button from "./Button";
import "./GameCard.css";

export default function GameCard({ title, subtitle, status, label, to, ctaLabel }) {
  const isLive = status === "live";

  return (
    <div className={`ptm-game-card${isLive ? " is-live" : ""}`}>
      <Badge tone={isLive ? "live" : "muted"}>{isLive ? "LIVE" : label}</Badge>
      <h3 className="ptm-game-card__title">{title}</h3>
      <p className="ptm-game-card__subtitle">{subtitle}</p>
      <Button to={to} variant={isLive ? "primary" : "secondary"}>
        {ctaLabel || (isLive ? "PLAY" : "LEARN MORE")}
      </Button>
    </div>
  );
}
