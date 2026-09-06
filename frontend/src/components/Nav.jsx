import { NavLink } from "react-router-dom";
import "./Nav.css";

const LINKS = [
  { to: "/games", label: "PLAY" },
  { to: "/lab", label: "LAB" },
  { to: "/articles", label: "ARCHIVE" },
];

export default function Nav() {
  return (
    <header className="ptm-nav">
      <div className="ptm-container ptm-nav__inner">
        <NavLink to="/" className="ptm-nav__wordmark">
          PAPER <span>TIGERS</span>
        </NavLink>
        <nav className="ptm-nav__links">
          {LINKS.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) => "ptm-nav__link" + (isActive ? " is-active" : "")}
            >
              {link.label}
            </NavLink>
          ))}
        </nav>
      </div>
    </header>
  );
}
