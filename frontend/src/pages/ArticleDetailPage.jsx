import { useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { ARTICLES } from "../lib/articlesData";

export default function ArticleDetailPage() {
  const { slug } = useParams();
  const article = ARTICLES.find((a) => a.slug === slug);

  // Dynamic SEO implementation
  useEffect(() => {
    if (article) {
      // 1. Update browser tab title
      document.title = `${article.title} | Paper Tigers Media`;
      
      // 2. Dynamically injection meta descriptions for crawlers
      let metaDesc = document.querySelector('meta[name="description"]');
      if (metaDesc) {
        metaDesc.setAttribute("content", article.excerpt);
      }
    }
    
    // Clean up title when navigating away
    return () => {
      document.title = "Paper Tigers Media | Sports, But Interactive";
    };
  }, [article]);

  if (!article) {
    return (
      <div className="ptm-container" style={{ padding: "4rem 0", textAlign: "center" }}>
        <h2>Article Not Found</h2>
        <p>The post you are looking for does not exist or has been shifted in the lab.</p>
        <Link to="/articles" style={{ color: "var(--primary-color, #ff4500)" }}>Back to Articles</Link>
      </div>
    );
  }

  return (
    <div className="ptm-container" style={{ padding: "3rem 1rem", maxWidth: "800px" }}>
      <Link to="/articles" style={{ color: "gray", textDecoration: "none", fontSize: "0.9rem" }}>
        &larr; Back to all articles
      </Link>
      
      <header style={{ margin: "2rem 0 1.5rem 0" }}>
        <p style={{ color: "var(--primary-color)", fontSize: "0.85rem", fontWeight: "bold", textTransform: "uppercase" }}>
          {article.date}
        </p>
        <h1 style={{ fontSize: "2.5rem", lineHeight: "1.2", marginBottom: "1rem" }}>{article.title}</h1>
      </header>

      <hr style={{ border: "0", borderTop: "1px solid #222", marginBottom: "2rem" }} />

      <div 
        className="ptm-article-body" 
        style={{ 
          fontSize: "1.15rem", 
          lineHeight: "1.7", 
          color: "#ccc",
          whiteSpace: "pre-line" // Keeps paragraph formatting from your data file
        }}
      >
        {article.content}
      </div>
    </div>
  );
}
