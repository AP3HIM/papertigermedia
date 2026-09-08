import { Link } from "react-router-dom";
import "./Footer.css";

export default function Footer() {
  return (
    <footer className="ptm-footer">
      <div className="ptm-container ptm-footer__inner">
        <p>
          &copy; {new Date().getFullYear()} <strong>Paper Tigers Media</strong> &middot;{" "}
          <Link to="/privacy">Privacy Policy</Link> &middot;{" "}
          <Link to="/contact">Contact Us</Link> &middot;{" "}
          <Link to="/">Home</Link>
        </p>
        
        <p className="footer-note">
          Independent sports coverage, predictions, and analysis. Follow us on{" "}
          <a href="https://x.com/PaperTigrMedia" target="_blank" rel="noopener noreferrer">Twitter</a>,{" "}
          <a href="https://www.youtube.com/@PaperTigrMedia" target="_blank" rel="noopener noreferrer">YouTube</a>, and{" "}
          <a href="https://www.instagram.com/papertigermedia" target="_blank" rel="noopener noreferrer">Instagram</a>.
        </p>
      </div>
    </footer>
  );
}
