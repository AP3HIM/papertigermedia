import { useEffect } from "react";
import Button from "../components/Button";
import "./StaticPages.css";

export default function ContactPage() {
  useEffect(() => {
    document.title = "Contact | Paper Tigers Media";
    return () => {
      document.title = "Paper Tigers Media | Sports, But Interactive";
    };
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    alert("Message logged into the lab system simulation template! (Form is currently structurally in fallback mode).");
  };

  return (
    <div className="ptm-container ptm-static-page">
      <header className="ptm-static-header">
        <p className="ptm-featured__eyebrow">TRANSMISSIONS</p>
        <h1 className="ptm-static-title">Ping the Lab</h1>
        <p className="ptm-static-subtitle">Feedback on 23 Guesses? Bug report in Dynasty? Drop a note below.</p>
      </header>

      <div className="ptm-contact-grid">
        <form className="ptm-contact-form" onSubmit={handleSubmit}>
          <div className="ptm-form-group">
            <label htmlFor="name">Name</label>
            <input type="text" id="name" required placeholder="Manager Name" />
          </div>

          <div className="ptm-form-group">
            <label htmlFor="email">Email</label>
            <input type="email" id="email" required placeholder="name@domain.com" />
          </div>

          <div className="ptm-form-group">
            <label htmlFor="message">Message</label>
            <textarea id="message" rows="5" required placeholder="What needs adjusting in the engine?"></textarea>
          </div>

          <Button variant="primary" style={{ border: "none", cursor: "pointer", width: "100%" }}>
            Send Transmission
          </Button>
        </form>

        <div className="ptm-contact-sidebar">
          <h3>Connect With Us</h3>
          <p>For all inquiries, email us directly at:</p>
          <p><a href="mailto:papertigrmedia@gmail.com" className="ptm-static-link"><strong>papertigrmedia@gmail.com</strong></a></p>
          
          <h4 style={{ marginTop: "1.5rem", marginBottom: "0.5rem", textTransform: "uppercase", fontSize: "0.8rem", color: "var(--ptm-black)", opacity: 0.6 }}>Social Channels</h4>
          <ul className="ptm-social-links">
            <li><a href="https://x.com/PaperTigrMedia" target="_blank" rel="noopener noreferrer">Twitter / X &rarr;</a></li>
            <li><a href="https://www.youtube.com/@PaperTigrMedia" target="_blank" rel="noopener noreferrer">YouTube &rarr;</a></li>
            <li><a href="https://www.instagram.com/papertigermedia" target="_blank" rel="noopener noreferrer">Instagram &rarr;</a></li>
          </ul>
        </div>
      </div>
    </div>
  );
}
