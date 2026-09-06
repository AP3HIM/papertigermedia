import "./SectionHeader.css";

export default function SectionHeader({ eyebrow, title, subtitle }) {
  return (
    <div className="ptm-section-header">
      {eyebrow && <p className="ptm-section-header__eyebrow">{eyebrow}</p>}
      <h2 className="ptm-section-header__title">{title}</h2>
      {subtitle && <p className="ptm-section-header__subtitle">{subtitle}</p>}
    </div>
  );
}
