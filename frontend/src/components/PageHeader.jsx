import "./PageHeader.css";

export default function PageHeader({ eyebrow, title, blurb }) {
  return (
    <div className="ptm-page-header">
      <div className="ptm-container">
        {eyebrow && <p className="ptm-page-header__eyebrow">{eyebrow}</p>}
        <h1 className="ptm-page-header__title">{title}</h1>
        {blurb && <p className="ptm-page-header__blurb">{blurb}</p>}
      </div>
    </div>
  );
}
