import { useEffect } from "react";
import "./StaticPages.css";

export default function PrivacyPage() {
  useEffect(() => {
    document.title = "Privacy Policy | Paper Tigers Media";
    return () => {
      document.title = "Paper Tigers Media | Sports, But Interactive";
    };
  }, []);

  return (
    <div className="ptm-container--narrow ptm-static-page">
      <header className="ptm-static-header">
        <p className="ptm-featured__eyebrow">LEGAL DECK</p>
        <h1 className="ptm-static-title">Privacy Policy</h1>
        <p className="ptm-static-subtitle">Last Updated: September 2026</p>
      </header>

      <div className="ptm-static-content">
        <section>
          <h2>1. Data Collection & Analytics</h2>
          <p>
            Paper Tigers Media operates primarily as an interactive gaming and data laboratory. 
            We do not collect personally identifiable information (PII) unless you explicitly submit it. 
            We utilize standard proxy network analysis and optional client-side tracking configurations 
            to monitor broad site performance, page traffic metrics, and system stability.
          </p>
        </section>

        <section>
          <h2>2. Local Storage & Local State</h2>
          <p>
            To power interactive game frameworks like <strong>23 Guesses</strong> and our sandbox simulation engines, 
            your browser utilizes local cache resources (such as <code>localStorage</code> or session tokens). 
            This is used exclusively to store game history sequences, active win/loss streaks, and local operational parameters 
            so your game states stay intact across separate browse cycles.
          </p>
        </section>

        <section>
          <h2>3. Third-Party Connections</h2>
          <p>
            Our web distribution pipelines leverage host architectures like Netlify and Render. 
            These external server environments may track structural diagnostic details like IP footprints 
            solely to avoid unauthorized access and confirm framework up-times.
          </p>
        </section>

        <section>
          <h2>4. Updates to This Policy</h2>
          <p>
            As the development lab evolves and introduces expansive cloud features (including profile logins), 
            these policy parameters may be modified periodically. Your continuous navigation of the framework 
            indicates your baseline validation of these terms.
          </p>
        </section>
      </div>
    </div>
  );
}
