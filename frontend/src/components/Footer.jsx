import "./Footer.css";

export default function Footer() {
  return (
    <footer className="ptm-footer">
      <div className="ptm-container ptm-footer__inner">
        <p>
          &copy; {new Date().getFullYear()} Paper Tigers Media &middot;{" "}
          <a href="/privacy.html">Privacy</a> &middot; <a href="/contact.html">Contact</a>
        </p>
        <p className="ptm-footer__social">
          <a href="https://x.com/PaperTigrMedia" target="_blank" rel="noreferrer">
            X
          </a>{" "}
          &middot;{" "}
          <a href="https://www.youtube.com/@PaperTigrMedia" target="_blank" rel="noreferrer">
            YouTube
          </a>{" "}
          &middot;{" "}
          <a href="https://www.instagram.com/papertigermedia" target="_blank" rel="noreferrer">
            Instagram
          </a>
        </p>
      </div>
    </footer>
  );
}
