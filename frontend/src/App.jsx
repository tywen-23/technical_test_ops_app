import React, { useCallback, useEffect, useState } from "react";
import * as api from "./api.js";
import FilterBar from "./components/FilterBar.jsx";
import KpiCards from "./components/KpiCards.jsx";
import Breakdown from "./components/Breakdown.jsx";
import AddSaleForm from "./components/AddSaleForm.jsx";
import SalesTable from "./components/SalesTable.jsx";
import PacePanel from "./components/PacePanel.jsx";

function currentMonth() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}`;
}

export default function App() {
  const [filters, setFilters] = useState({ month: currentMonth(), category: "", channel: "" });
  const [options, setOptions] = useState({ categories: [], channels: [], months: [] });
  const [summary, setSummary] = useState(null);
  const [sales, setSales] = useState([]);
  const [error, setError] = useState(null);
  const [pace, setPace] = useState(null);

  const load = useCallback(async () => {
    try {
      setError(null);
      const paceRequest = filters.month
        ? api.getPace(filters.month)
        : Promise.resolve(null);

      const [s, list, paceData] = await Promise.all([
        api.getSummary(filters),
        api.getSales(filters),
        paceRequest,
      ]);

      setSummary(s);
      setSales(list);
      setPace(paceData);
    } catch (e) {
      setError(String(e.message || e));
    }
  }, [filters]);

  useEffect(() => {
    load();
  }, [load]);

  useEffect(() => {
    api.getFilters().then(setOptions).catch(() => {});
  }, []);

  return (
    <div className="app">
      <header className="app-header">
        <h1>Sales KPI Dashboard</h1>
        <p className="subtitle">Ops finance overview · all amounts in RM</p>
      </header>

      {error && <div className="error">API error: {error}</div>}

      <FilterBar filters={filters} options={options} onChange={setFilters} />

      {summary && <KpiCards summary={summary} />}

      {pace && <PacePanel pace={pace} />}

      {summary && (
        <div className="grid-2">
          <Breakdown title="Revenue by Category" rows={summary.by_category} labelKey="category" />
          <Breakdown title="Revenue by Channel" rows={summary.by_channel} labelKey="channel" />
        </div>
      )}

      <AddSaleForm options={options} onCreated={load} />

      <SalesTable sales={sales} onDeleted={load} />
    </div>
  );
}
