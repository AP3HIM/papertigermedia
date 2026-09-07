export default function FanMeter({ value }) {
  const ticketPrice = Math.round(15 + value * 0.6);

  return (
    <div className="ptm-fan-meter">
      <div className="ptm-fan-meter__label">
        <span>FAN SUPPORT</span>
        <span>{value}</span>
      </div>
      <div className="ptm-fan-meter__track">
        <div className="ptm-fan-meter__fill" style={{ width: `${value}%` }} />
      </div>
      <p className="ptm-fan-meter__ticket">Tickets: ${ticketPrice}</p>
    </div>
  );
}
