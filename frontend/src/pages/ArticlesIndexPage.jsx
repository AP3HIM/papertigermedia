import { Link } from "react-router-dom";
import { ARTICLES } from "../lib/articlesData";
import "./Articles.css"; // We will create this simple stylesheet next

export default function ArticlesIndexPage() {
  return (
    <div className="ptm-container ptm-articles-page">
      <header className="ptm-articles-header">
        <p className="ptm-featured__eyebrow">ARCHIVE & NEWS</p>
        <h1 className="ptm-featured__title" style={{ fontSize: "2.5rem" }}>The Paper Tigers Ledger</h1>
        <p className="ptm-featured__subtitle">Deep dives, milestones, and reports from the lab.</p>
      </header>

      <div className="ptm-articles-list">
        {ARTICLES.map((article) => (
          <article key={article.slug} className="ptm-article-card">
            <span className="ptm-article-date">{article.date}</span>
            <h2>
              <Link to={`/articles/${article.slug}`} className="ptm-article-link">
                {article.title}
              </Link>
            </h2>
            <p className="ptm-article-excerpt">{article.excerpt}</p>
            <Link to={`/articles/${article.slug}`} className="ptm-article-more">
              Read Article &rarr;
            </Link>
          </article>
        ))}
      </div>
    </div>
  );
}
