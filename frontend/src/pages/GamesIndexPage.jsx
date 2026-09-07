import PageHeader from "../components/PageHeader";
import GameCard from "../components/GameCard";
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
    subtitle: "Ten seasons. Build an era.",
    status: "live",
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
      <div className="ptm-container ptm-games-grid">
        {GAMES.map((game) => (
          <GameCard key={game.to} {...game} />
        ))}
      </div>
    </div>
  );
}
