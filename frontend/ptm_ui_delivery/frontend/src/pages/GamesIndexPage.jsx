import PageHeader from "../components/PageHeader";
import SectionHeader from "../components/SectionHeader";
import Badge from "../components/Badge";
import Button from "../components/Button";
import "./GamesIndexPage.css";

const GAMES = [
  {
    to: "/games/23-guesses",
    title: "23 Guesses",
    subtitle: "Today's mystery, one clue at a time.",
    status: "live",
  },
  {
    to: "/games/dynasty",
    title: "Dynasty",
    subtitle: "Build a multi-season sports franchise.",
    status: "muted",
    label: "IN DEVELOPMENT",
  },
  {
    to: "/games/stat-challenge",
    title: "Stat Challenge",
    subtitle: "Turn sports data into a puzzle.",
    status: "muted",
    label: "PLANNED",
  },
];

export default function GamesIndexPage() {
  return (
    <div>
      <PageHeader eyebrow="PLAY" title="Games" blurb="Sports data, turned into things you can play with." />
      <div className="ptm-container ptm-games-list">
        {GAMES.map((game) => (
          <div key={game.to} className="ptm-games-list__item">
            <SectionHeader title={game.title} subtitle={game.subtitle} />
            <Badge tone={game.status === "live" ? "live" : "muted"}>
              {game.status === "live" ? "LIVE" : game.label}
            </Badge>
            <div className="ptm-block__cta">
              <Button to={game.to} variant={game.status === "live" ? "primary" : "secondary"}>
                {game.status === "live" ? "PLAY" : "LEARN MORE"}
              </Button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
