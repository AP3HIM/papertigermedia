import Button from "../components/Button";
import SectionHeader from "../components/SectionHeader";
import Badge from "../components/Badge";
import "./HomePage.css";

export default function HomePage() {
  return (
    <div>
      <section className="ptm-hero">
        <div className="ptm-container">
          <h1 className="ptm-hero__wordmark">PAPER TIGERS</h1>
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

      <section className="ptm-container ptm-block">
        <SectionHeader eyebrow="TODAY" title="23 Guesses" subtitle="Today's mystery is waiting." />
        <Badge tone="live">LIVE</Badge>
        <div className="ptm-block__cta">
          <Button to="/games/23-guesses">PLAY</Button>
        </div>
      </section>

      <section className="ptm-container ptm-block">
        <SectionHeader
          eyebrow="PLAY"
          title="Build a Dynasty"
          subtitle="Take a team. Make the decisions. See how long you can dominate."
        />
        <Badge tone="muted">IN DEVELOPMENT</Badge>
        <div className="ptm-block__cta">
          <Button to="/games/dynasty" variant="secondary">
            LEARN MORE
          </Button>
        </div>
      </section>

      <section className="ptm-container ptm-block">
        <SectionHeader eyebrow="PLAY" title="Stat Challenge" subtitle="Can you find the answer?" />
        <Badge tone="muted">PLANNED</Badge>
        <div className="ptm-block__cta">
          <Button to="/games/stat-challenge" variant="secondary">
            LEARN MORE
          </Button>
        </div>
      </section>

      <section className="ptm-container ptm-block">
        <SectionHeader eyebrow="EXPLORE" title="The Data" subtitle="Players. Teams. Seasons. Records. History." />
        <Badge tone="muted">PLANNED</Badge>
      </section>

      <section className="ptm-container ptm-block">
        <SectionHeader eyebrow="ARCHIVE" title="From the Archive" subtitle="Reporting and analysis, preserved." />
        <Badge tone="muted">PLANNED</Badge>
      </section>
    </div>
  );
}
