import { pct, rm } from "../format.js";


const STATUS_LABELS = {
  on_track: "On track",
  at_risk: "At risk",
  "n/a": "N/A",
};


function signedRm(value) {
  if (value == null) return "—";
  if (value === 0) return rm(0);

  const sign = value > 0 ? "+" : "-";
  return `${sign}${rm(Math.abs(value))}`;
}


export default function PacePanel({ pace }) {
  if (!pace) return null;

  const metrics = [
    ["MTD Revenue", rm(pace.mtd_revenue)],
    ["Elapsed Days", `${pace.elapsed_days} / ${pace.days_in_month}`],
    ["Projected Revenue", rm(pace.projected_revenue)],
    ["Monthly Target", rm(pace.target)],
    ["Variance", signedRm(pace.variance_amount)],
    ["Variance %", pct(pace.variance_pct)],
  ];

  return (
    <section className="panel pace-panel">
      <div className="pace-header">
        <div>
          <h2 className="pace-title">Pace to Target</h2>
          <p className="muted">
            Projected month-end performance based on completed sales
          </p>
        </div>

        <span className={`pace-status ${pace.status}`}>
          {STATUS_LABELS[pace.status] ?? "N/A"}
        </span>
      </div>

      <div className="pace-grid">
        {metrics.map(([label, value]) => (
          <div className="pace-metric" key={label}>
            <div className="pace-value">{value}</div>
            <div className="pace-label">{label}</div>
          </div>
        ))}
      </div>
    </section>
  );
}