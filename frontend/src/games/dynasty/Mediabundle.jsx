import "./MediaBundle.css";

/**
 * Renders the `media` array the backend attaches to season_result
 * (see engine.generate_media_bundle). Each item already carries its own
 * `team_theme` (hsl primary/secondary), so nothing here needs to know
 * the team name — it just reads what the server sent.
 *
 * Usage: <MediaBundle items={result.media} />
 */
export default function MediaBundle({ items }) {
  if (!items || items.length === 0) return null;

  return (
    <div className="ptm-media-bundle">
      {items.map((item, i) => {
        switch (item.type) {
          case "newspaper":
            return <NewspaperCard key={i} item={item} />;
          case "tweet":
            return <TweetCard key={i} item={item} />;
          case "headline":
            return <HeadlineCard key={i} item={item} />;
          default:
            return null;
        }
      })}
    </div>
  );
}

function NewspaperCard({ item }) {
  const { headline, subhead, team_theme, masthead } = item;
  return (
    <div
      className="ptm-newspaper"
      style={{ "--ptm-primary": team_theme.primary, "--ptm-secondary": team_theme.secondary }}
    >
      <div className="ptm-newspaper__bar" />
      <div className="ptm-newspaper__eyebrow">{masthead || "EXTRA EDITION"}</div>
      <h2 className="ptm-newspaper__headline">{headline}</h2>
      <p className="ptm-newspaper__subhead">{subhead}</p>
      <div className="ptm-newspaper__bar" />
    </div>
  );
}

function TweetCard({ item }) {
  const { handle, text, team_theme } = item;
  return (
    <div className="ptm-tweet" style={{ "--ptm-secondary": team_theme.secondary }}>
      <div className="ptm-tweet__avatar" aria-hidden="true" />
      <div className="ptm-tweet__body">
        <span className="ptm-tweet__handle">{handle}</span>
        <p className="ptm-tweet__text">{text}</p>
      </div>
    </div>
  );
}

function HeadlineCard({ item }) {
  const { headline, team_theme } = item;
  return (
    <div className="ptm-headline" style={{ "--ptm-primary": team_theme.primary }}>
      <span className="ptm-headline__eyebrow">SOURCES SAY</span>
      <p className="ptm-headline__text">{headline}</p>
    </div>
  );
}