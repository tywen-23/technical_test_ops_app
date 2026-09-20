# Sales KPI Dashboard

A full-stack sales performance dashboard for operations and finance teams. The application reports revenue, completed orders, average order value, target attainment, revenue breakdowns, and month-end performance projections.

## Key Features

- Filter sales by month, category, and channel
- View completed-sales revenue, order count, and average order value
- Compare revenue by category and channel
- Track monthly target attainment
- Project month-end revenue using the current sales pace
- Identify whether the selected month is on track or at risk
- Calculate the daily revenue required to recover an at-risk target
- Add and delete sales records

## Correctness Fixes

The original dashboard contained several KPI calculation issues. This implementation fixes:

1. **Refunded sales inclusion**
   Revenue, orders, AOV, category totals, and channel totals now use completed sales only.

2. **Percentage discount calculation**
   Net revenue is calculated as:

   ```text
   quantity × unit price × (1 - discount percentage / 100)
   ```

3. **Category aggregation**
   Revenue now accumulates all sales within each category instead of retaining only one row.

4. **Channel classification**
   `online` and `in_store` now use exact matching, preventing online revenue from being classified as in-store revenue.

5. **Target attainment**
   Target attainment now uses:

   ```text
   total completed revenue / monthly target × 100
   ```

   Missing and zero targets return N/A instead of causing invalid calculations.

## Pace to Target

For a selected month, the dashboard displays:

- Month-to-date completed-sales revenue
- Elapsed days and total days in the month
- Projected month-end revenue
- Monthly target
- Variance in RM and percentage
- On-track or at-risk status

Current-month projection:

```text
MTD revenue / elapsed days × days in month
```

Calculation rules:

- Past month: projection equals actual completed revenue
- Current month: projection uses elapsed days
- Future month: projection is N/A
- Calendar month lengths and leap years are supported
- The current date is evaluated in Malaysia time, UTC+8
- Missing targets and zero-day cases return N/A

## Innovation: Target Recovery Insight

When the current month is behind target, the dashboard converts the shortfall into an actionable daily goal:

```text
remaining target = max(target - MTD revenue, 0)
remaining days = days in month - elapsed days
required daily revenue = remaining target / remaining days
```

This helps the operations team understand:

- How much revenue remains
- How many recovery days are available
- How much revenue is required per day to reach the target

The calculation safely handles achieved targets, the final day of the month, and missing targets.

## Stack

| Layer | Technology |
|---|---|
| Frontend | React + Vite |
| Backend | Python + FastAPI |
| Database | PostgreSQL 16 |
| Runtime | Docker Compose |
| Tests | Python `unittest` |

## Running the Application

Requirements:

- Docker Desktop
- Docker Compose

From the project directory:

```bash
docker compose up --build
```

Open:

| Service | URL |
|---|---|
| Web application | http://localhost:5173 |
| API | http://localhost:8010 |
| API health check | http://localhost:8010/api/health |
| PostgreSQL | localhost:5442 |

The database is seeded automatically when it is empty.

## Running Tests

Run the backend test suite:

```bash
docker compose exec api python -m unittest discover -s tests -v
```

The tests cover:

- Percentage discounts
- Refunded-sale exclusion
- Category and channel aggregation
- Target attainment
- Missing targets
- Current, past, and future month projections
- Leap years
- Target recovery calculations
- Final-day division-by-zero protection

Build the frontend for production:

```bash
docker compose exec web npm run build
```

## API Reference

| Method | Path | Description |
|---|---|---|
| GET | `/api/health` | API health check |
| GET | `/api/summary?month=&category=&channel=` | KPI totals and breakdowns |
| GET | `/api/pace?month=YYYY-MM` | Pace-to-target and recovery metrics |
| GET | `/api/sales?month=&category=&channel=` | Filtered sales list |
| POST | `/api/sales` | Create a sale |
| DELETE | `/api/sales/{id}` | Delete a sale |
| GET | `/api/filters` | Available filter values |
| GET | `/api/targets` | Monthly targets |

## Project Structure

```text
backend/
  db.py                     Database queries and KPI calculations
  pace.py                   Pace and target recovery calculations
  main.py                   FastAPI application
  sales/routes.py           API routes
  tests/test_db.py          KPI regression tests
  tests/test_pace.py        Pace and recovery edge-case tests

frontend/
  src/App.jsx               Dashboard state and data loading
  src/api.js                API client
  src/components/
    PacePanel.jsx           Pace and recovery presentation
    KpiCards.jsx            KPI summary cards
    Breakdown.jsx           Category and channel breakdowns
    FilterBar.jsx           Dashboard filters
    AddSaleForm.jsx         Sale creation form
    SalesTable.jsx          Sales records table

docker-compose.yml          Database, API, and frontend services
```

## Design Decisions

- KPI calculations include only completed sales, while the sales table retains refunded records for visibility.
- Pace to Target uses the complete monthly company target and therefore depends on the selected month, not category or channel filters.
- The Pace panel is hidden for “All months” because monthly targets cannot be meaningfully combined into one attainment value.
- Target Recovery Insight applies to the current month, where remaining days can still support operational action.