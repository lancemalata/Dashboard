# Academic Insights

A BAT 405 Analytics Application case-study prototype for the BSIT Program Chair, CICS, Batangas State University – ARASOF Nasugbu. Prepared by Vince A. Mendoza and Ronel Lance Malata, section IT-BA-4101, for Noelyn M. De Jesus. Submission date: November 23, 2026.

All records are simulated aggregates. Portal–SETE analytics integration is proposed, not an existing connection. The application mark is an original symbol, not the university seal.

## Run locally

```sh
npm ci
npm run dev
```

Open the local URL printed by Vite. This is not a remotely accessible submission link.

```sh
npm test
npm run lint
npm run build
```

`npm test` checks the simulated dataset, formulas, weighted aggregation, thresholds, missing denominators, cohort filtering, and server-rendered dashboard requirements. It does not replace browser interaction or print checks.

## Dashboard scope

- Five KPI cards: course pass rate, on-time grade submission, SETE response rate, mean SETE rating, and academic difficulty rate.
- Three visualizations: pass rate by year level, overall mean SETE ratings across semesters, and selected-period SETE dimension scores.
- Two interactive feature groups: coordinated academic-year/semester/year-level filtering and KPI-detail dialogs.
- Compact review flags with management actions in the detail dialogs, plus participation context.
- A menu-free report layout: two charts above a full-width evaluation-dimension chart, with visible counts and targets.
- Long bond print styles requested at 8.5 × 13 inches; pagination and color output require print-preview verification.

The latest simulated scenario matches the paper: 88% pass rate, 90% on-time submission, 60% evaluation participation, 4.20/5 mean rating, and 15% academic difficulty. Earlier periods demonstrate historical comparisons and a no-alert state. A hypothetical finalized semester does not imply the real semester or evaluation window is closed.

## Project files

- [Parts I and II](docs/case-study-parts-i-ii.md): assessment, evidence and assumptions, KPI definitions, proposed thresholds, and sample calculations.
- [Part III](docs/case-study-part-iii.md): labeled component explanations, visualization choices, interactions, alerts, and proposed confidentiality controls.
- [Dashboard](src/App.jsx): one-page React interface.
- [Simulated data and calculations](src/data/dashboard.js): shared KPI definitions and aggregation logic.
- [Application mark](public/academic-insights.svg): original graduation-cap symbol.

## Verification and remaining work

The prototype includes no login, server-side authorization, real database, source-system APIs, faculty-level drill-down, or predictive model. Confidentiality controls discussed in the paper are production requirements. Do not load real records into this client-only demonstration.

Browser automation was unavailable during implementation. Check desktop/mobile layout, all filter combinations, dialog focus and Escape behavior, keyboard navigation, and long bond print pagination manually before submission. Final paper formatting, the colored dashboard page, a verified shareable link, and Parts IV and V remain outstanding.

Dependency installation reported five high-severity advisories in the inherited Vite/build-tool dependency tree. Dependency versions were not changed as part of the dashboard implementation; review the audit before hosting.
