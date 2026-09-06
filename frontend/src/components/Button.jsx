import { Link } from "react-router-dom";
import "./Button.css";

/**
 * Shared button. Renders a <Link> when `to` is given, otherwise a <button>.
 * variant: "primary" (solid black) | "secondary" (outline)
 */
export default function Button({ to, variant = "primary", disabled = false, children, ...rest }) {
  const className = `ptm-btn ptm-btn--${variant}`;

  if (to && !disabled) {
    return (
      <Link to={to} className={className} {...rest}>
        {children}
      </Link>
    );
  }

  return (
    <button className={className} disabled={disabled} {...rest}>
      {children}
    </button>
  );
}
