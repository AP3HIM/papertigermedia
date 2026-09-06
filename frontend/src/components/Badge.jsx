import "./Badge.css";

export default function Badge({ children, tone = "muted" }) {
  return <span className={`ptm-badge ptm-badge--${tone}`}>{children}</span>;
}
