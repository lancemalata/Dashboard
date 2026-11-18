import { useRef, useState } from 'react'
import {
  dimensions,
  periods,
  kpis,
  summarize,
  getMetrics,
  getWarnings,
  selectRows,
  formatValue,
} from './data/dashboard.js'
import './App.css'

function Icon({ name, size = 20 }) {
  const paths = {
    grid: 'M3 3h7v7H3z M14 3h7v7h-7z M3 14h7v7H3z M14 14h7v7h-7z',
    book: 'M4 3h13a2 2 0 0 1 2 2v16H6a3 3 0 0 1-3-3V5a2 2 0 0 1 1-2 M3 17h16 M7 7h8 M7 10h6',
    cap: 'm2 9 10-5 10 5-10 5z M6 11v6q6 5 12 0v-6 M22 9v8',
    clock: 'M12 8v5l3 2 M22 12a10 10 0 1 1-20 0 10 10 0 0 1 20 0',
    message: 'M21 11a8 8 0 0 1-8 8H7l-5 3V11a9 9 0 0 1 19 0 M7 10h9 M7 14h5',
    star: 'm12 3 2.8 5.7 6.2.9-4.5 4.4 1.1 6.2-5.6-3-5.6 3 1.1-6.2L3 9.6l6.2-.9z',
    alert: 'm12 3 10 18H2z M12 9v5 M12 17v.1',
    arrow: 'M5 12h14 M14 7l5 5-5 5',
    info: 'M12 11v6 M12 7v.1 M22 12a10 10 0 1 1-20 0 10 10 0 0 1 20 0',
    print: 'M6 9V3h12v6 M6 17H3V9h18v8h-3 M6 14h12v7H6z M17 12h1',
    shield: 'm12 3 8 3v6c0 5-8 9-8 9s-8-4-8-9V6z m-4 9 3 3 5-5',
    close: 'm6 6 12 12 M6 18 18 6',
  }
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.7"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d={paths[name] || paths.info} />
    </svg>
  )
}

function PanelTitle({ number, title, subtitle, children }) {
  return (
    <div className="panel-title">
      <div>
        <span className="eyebrow">Visualization {number}</span>
        <h2>{title}</h2>
        <p>{subtitle}</p>
      </div>
      {children}
    </div>
  )
}

function App() {
  const [periodId, setPeriodId] = useState('2026-2027-1')
  const [yearLevel, setYearLevel] = useState('all')
  const [detail, setDetail] = useState(null)
  const dialogRef = useRef(null)
  const period = periods.find((item) => item.id === periodId)
  const rows = selectRows(period, yearLevel)
  const summary = summarize(rows)
  const metrics = getMetrics(summary)
  const warnings = getWarnings(metrics)
  const academicYear = period.year
  const scope = yearLevel === 'all' ? 'All year levels' : `Year ${yearLevel}`
  const trend = periods
    .filter((item) => item.order <= period.order)
    .map((item) => {
      const aggregate = summarize(selectRows(item, yearLevel))
      return {
        ...item,
        ...aggregate,
        meanRating: getMetrics(aggregate).meanRating,
      }
    })
  const detailKpi = kpis.find((item) => item.id === detail)
  const previousPeriod = periods.find((item) => item.order === period.order - 1)
  const previousMetrics = previousPeriod
    ? getMetrics(summarize(selectRows(previousPeriod, yearLevel)))
    : null

  function showDetails(id) {
    setDetail(id)
    dialogRef.current.showModal()
  }

  return (
    <div className="app-shell">
      <a className="skip-link" href="#main">
        Skip to dashboard
      </a>
      <div className="workspace">
        <main id="main">
          <div className="page-heading">
            <span className="university-mark">
              <Icon name="cap" size={31} />
            </span>
            <div>
              <div className="eyebrow">
                BATANGAS STATE UNIVERSITY · ARASOF NASUGBU
              </div>
              <h1>BatStateU Academic Insights</h1>
              <p>
                Academic performance &amp; teaching effectiveness{' '}
                <span>· Program Chair · BSIT / CICS</span>
              </p>
            </div>
            <div className="header-actions">
              <span className="sample-badge">Simulated data · Case study</span>
              <button
                className="button print-button"
                onClick={() => window.print()}
              >
                <Icon name="print" size={17} />
                Print dashboard
              </button>
            </div>
          </div>
          <section className="filter-bar" aria-label="Dashboard filters">
            <label>
              Academic year
              <select
                value={academicYear}
                onChange={(event) =>
                  setPeriodId(
                    periods
                      .filter((item) => item.year === event.target.value)
                      .at(-1).id,
                  )
                }
              >
                {[...new Set(periods.map((item) => item.year))].map((year) => (
                  <option key={year}>{year}</option>
                ))}
              </select>
            </label>
            <label>
              Semester
              <select
                value={periodId}
                onChange={(event) => setPeriodId(event.target.value)}
              >
                {periods
                  .filter((item) => item.year === academicYear)
                  .map((item) => (
                    <option key={item.id} value={item.id}>
                      {item.semester}
                    </option>
                  ))}
              </select>
            </label>
            <label>
              Year level
              <select
                value={yearLevel}
                onChange={(event) => setYearLevel(event.target.value)}
              >
                <option value="all">All year levels</option>
                {[1, 2, 3, 4].map((level) => (
                  <option key={level} value={level}>
                    Year {level}
                  </option>
                ))}
              </select>
            </label>
            <button
              type="button"
              className="reset-button"
              onClick={() => {
                setPeriodId('2026-2027-1')
                setYearLevel('all')
              }}
              disabled={periodId === '2026-2027-1' && yearLevel === 'all'}
            >
              Reset filters
            </button>
            <div
              className={`risk-summary ${metrics.difficultyRate > 10 ? 'risk-warning' : ''}`}
              role="status"
            >
              <span>ACADEMIC STATUS</span>
              <strong>
                <Icon
                  name={metrics.difficultyRate > 10 ? 'alert' : 'shield'}
                  size={16}
                />
                {metrics.difficultyRate > 10
                  ? 'Academic support review needed'
                  : 'Within proposed difficulty target'}
              </strong>
              <small>
                {summary.affected} of {summary.students} students have a
                finalized failed course · Target ≤ 10%
              </small>
            </div>
          </section>
          <section
            aria-label="Key performance indicators"
            className="kpi-grid"
            aria-live="polite"
          >
            {kpis.map((kpi) => {
              const value = metrics[kpi.id]
              const warning = warnings.some((item) => item.id === kpi.id)
              return (
                <button
                  key={kpi.id}
                  className="kpi-card"
                  onClick={() => showDetails(kpi.id)}
                  aria-label={`${kpi.label}: ${formatValue(value, kpi.unit)}. View calculation`}
                >
                  <div className="kpi-top">
                    <span
                      className={`kpi-icon ${warning ? 'needs-review' : ''}`}
                    >
                      <Icon name={kpi.icon} size={18} />
                    </span>
                  </div>
                  <h2>{kpi.label}</h2>
                  <div className="kpi-value">
                    {formatValue(value, kpi.unit)}
                    {kpi.unit === 'rating' && <small> / 5</small>}
                  </div>
                  <div className={`status ${warning ? 'warning' : 'healthy'}`}>
                    <span />
                    {value === null
                      ? 'Not available'
                      : warning
                        ? 'Needs review'
                        : 'Within target'}
                  </div>
                  <div className="kpi-target">
                    Target {kpi.targetLabel}
                  </div>
                </button>
              )
            })}
          </section>
          <div
            className="section-caption"
            role="status"
            aria-live="polite"
            aria-atomic="true"
          >
            <span>
              Showing {period.semester} · AY {period.year} · {scope} ·{' '}
              {summary.students} students
            </span>
            <span>
              Finalized scenario · Closed evaluation window · Proposed targets
            </span>
          </div>
          <div className="chart-grid">
            <section className="panel" id="academic">
              <PanelTitle
                number="01"
                title="Course pass rate"
                subtitle="By year level · finalized course outcomes"
              >
                <span className="unit-tag">%</span>
              </PanelTitle>
              <div
                className="bar-chart"
                role="img"
                aria-label={rows
                  .map(
                    (row) =>
                      `Year ${row.level}: ${((100 * row.passed) / row.outcomes).toFixed(1)} percent passed`,
                  )
                  .join('. ')}
              >
                {rows.map((row) => (
                  <div className="bar-row" key={row.level}>
                    <div className="bar-label">
                      <span>Year {row.level}</span>
                      <strong>
                        {((row.passed / row.outcomes) * 100).toFixed(1)}%
                      </strong>
                    </div>
                    <div className="bar-track">
                      <div
                        className={`bar-fill ${row.passed / row.outcomes < 0.9 ? 'below' : ''}`}
                        style={{
                          width: `${(row.passed / row.outcomes) * 100}%`,
                        }}
                      />
                      <span className="target-marker" />
                    </div>
                    <div className="bar-caption">
                      {row.passed.toLocaleString()} /{' '}
                      {row.outcomes.toLocaleString()} passed
                    </div>
                  </div>
                ))}
              </div>
              <div className="chart-note">
                <span className="legend-line" />
                Proposed target: 90% · Scale: 0–100%
              </div>
            </section>
            <section className="panel trend-panel" id="teaching">
              <PanelTitle
                number="02"
                title="Average SETE rating across semesters"
                subtitle="Overall item-weighted mean · through selected semester"
              />
              <div className="line-chart">
                <svg
                  viewBox="0 0 640 200"
                  preserveAspectRatio="none"
                  role="img"
                  aria-label={`Mean SETE rating trend for ${scope}. ${trend.map((point) => `${point.shortLabel}: ${point.meanRating.toFixed(2)} out of 5 from ${point.responses} evaluations`).join('. ')}`}
                >
                  {[1, 2, 3, 4, 5].map((tick) => (
                    <g key={tick}>
                      <line
                        x1="28"
                        x2="620"
                        y1={148 - (tick - 1) * 30}
                        y2={148 - (tick - 1) * 30}
                        stroke="#eceef1"
                      />
                    </g>
                  ))}
                  <line
                    className="trend-target"
                    x1="28"
                    x2="620"
                    y1="58"
                    y2="58"
                  >
                    <title>Proposed SETE target: 4.00 out of 5</title>
                  </line>
                  <polyline
                    fill="none"
                    stroke="#a92b3a"
                    strokeWidth="2.5"
                    points={trend
                      .map(
                        (point, i) =>
                          `${trend.length === 1 ? 324 : 60 + i * (528 / (trend.length - 1))},${148 - (point.meanRating - 1) * 30}`,
                      )
                      .join(' ')}
                  />
                  {trend.map((point, i) => {
                    const x =
                      trend.length === 1
                        ? 324
                        : 60 + i * (528 / (trend.length - 1))
                    const y = 148 - (point.meanRating - 1) * 30
                    return (
                      <g key={point.id}>
                        <circle
                          cx={x}
                          cy={y}
                          r={point.id === periodId ? 6 : 4}
                          fill="#a92b3a"
                          stroke={point.id === periodId ? '#fff' : 'none'}
                          strokeWidth="2"
                        >
                          <title>{`${point.shortLabel}: ${point.meanRating.toFixed(2)} / 5 · ${point.responses} completed evaluations`}</title>
                        </circle>
                      </g>
                    )
                  })}
                </svg>
                <div className="trend-labels" aria-hidden="true">
                  {[1, 2, 3, 4, 5].map((tick) => (
                    <span
                      key={tick}
                      className="axis-label"
                      style={{ top: `${(148 - (tick - 1) * 30) / 2}%` }}
                    >
                      {tick}
                    </span>
                  ))}
                  {trend.map((point, i) => {
                    const left = `${(trend.length === 1 ? 324 : 60 + i * (528 / (trend.length - 1))) / 6.4}%`
                    return (
                      <div key={point.id}>
                        <span
                          className="rating-label"
                          style={{
                            left,
                            top: `${(148 - (point.meanRating - 1) * 30) / 2}%`,
                          }}
                        >
                          {point.meanRating.toFixed(2)}
                        </span>
                        <span
                          className="period-label"
                          style={{ left, top: '82%' }}
                        >
                          {point.shortLabel}
                        </span>
                        <span
                          className="count-label"
                          style={{ left, top: '93%' }}
                        >
                          n = {point.responses.toLocaleString()}
                        </span>
                      </div>
                    )
                  })}
                </div>
              </div>
              <p className="chart-note">
                Scale: 1–5 · Dashed line: proposed target 4.00 · n = completed
                evaluations · Descriptive trend, not a forecast
              </p>
            </section>
            <section className="panel dimension-panel">
              <PanelTitle
                number="03"
                title="SETE ratings by evaluation dimension"
                subtitle="Dimension mean · dashed marker: proposed target 4.00"
              />
              <div
                className="dimension-chart"
                role="img"
                aria-label={dimensions
                  .map(
                    (dimension, i) =>
                      `${dimension.label}: ${summary.dimensionScores[i]?.toFixed(2) ?? 'not available'} out of 5`,
                  )
                  .join('. ')}
              >
                {dimensions.map((dimension, i) => (
                  <div className="dimension-row" key={dimension.id}>
                    <div className="dimension-label">
                      <span>{dimension.label}</span>
                      <strong>
                        {summary.dimensionScores[i]?.toFixed(2) ?? 'N/A'}
                        <small> / 5</small>
                      </strong>
                    </div>
                    <div className="dimension-track">
                      <span
                        className="dimension-point"
                        style={{
                          left: `${((summary.dimensionScores[i] - 1) / 4) * 100}%`,
                        }}
                      />
                    </div>
                    <small>
                      {dimension.items} statements · equal weight per item
                    </small>
                  </div>
                ))}
              </div>
              <div className="dimension-axis" aria-hidden="true">
                <span />{' '}
                <div>
                  {[1, 2, 3, 4, 5].map((tick) => (
                    <span key={tick} style={{ left: `${(tick - 1) * 25}%` }}>
                      {tick}
                    </span>
                  ))}
                </div>
                <span />
              </div>
              <div className="chart-note">
                Scale: 1–5 · Proposed target ≥ 4.00 ·{' '}
                {summary.responses.toLocaleString()} completed evaluations
              </div>
            </section>
          </div>
          <div className="context-strip">
            <span>
              <strong>
                {summary.responses.toLocaleString()} /{' '}
                {summary.eligible.toLocaleString()}
              </strong>{' '}
              completed / eligible evaluations
              {metrics.responseRate < 70 && (
                <b> · Low participation: interpret ratings cautiously.</b>
              )}
            </span>
            <span>
              SETE must not be the sole basis for personnel decisions. No real
              student or faculty records are shown.
            </span>
          </div>
          <footer>
            <span>
              <strong>Simulated data.</strong> · BAT 405 · Mendoza &amp; Malata
            </span>
            <span>
              Portal–SETE analytics integration is proposed · Targets are
              case-study benchmarks
            </span>
          </footer>
        </main>
      </div>
      <dialog
        ref={dialogRef}
        className="detail-dialog"
        aria-labelledby="kpi-detail-title"
        onClick={(event) => {
          if (event.target === event.currentTarget) dialogRef.current.close()
        }}
      >
        {detailKpi && (
          <>
            <div className="dialog-heading">
              <div>
                <span className="eyebrow">KPI DEFINITION</span>
                <h2 id="kpi-detail-title">{detailKpi.label}</h2>
              </div>
              <button
                className="icon-button"
                onClick={() => dialogRef.current.close()}
                aria-label="Close KPI details"
              >
                <Icon name="close" />
              </button>
            </div>
            <div className="dialog-body">
              <div className="dialog-metric">
                {formatValue(metrics[detailKpi.id], detailKpi.unit)}
                {detailKpi.unit === 'rating' && ' / 5'}
              </div>
              <p className="dialog-scope">
                {period.semester} · AY {period.year} · {scope}
              </p>
              <h3>Calculation</h3>
              <p>{detailKpi.formula}</p>
              <div className="calculation">{detailKpi.inputs(summary)}</div>
              <h3>Change from previous semester</h3>
              <p>
                {previousMetrics && metrics[detailKpi.id] !== null && previousMetrics[detailKpi.id] !== null
                  ? `${metrics[detailKpi.id] - previousMetrics[detailKpi.id] >= 0 ? '+' : '−'}${Math.abs(metrics[detailKpi.id] - previousMetrics[detailKpi.id]).toFixed(detailKpi.unit === 'rating' ? 2 : 1)} ${detailKpi.unit === 'rating' ? 'points' : 'percentage points'} vs ${previousPeriod.shortLabel}`
                  : 'No previous semester comparison available.'}
              </p>
              <h3>Proposed target</h3>
              <p>
                {detailKpi.targetLabel}. These are case-study benchmarks, not
                official university standards.
              </p>
              <h3>Management action</h3>
              <p>{detailKpi.action}</p>
              <h3>Interpretation</h3>
              <p>{detailKpi.context}</p>
              <p className="dialog-disclaimer">
                All data are simulated. Outcomes are finalized and the
                evaluation window is closed in this sample scenario. No
                prediction or personnel recommendation is produced.
              </p>
            </div>
            <div className="dialog-footer">
              <button
                className="button"
                onClick={() => dialogRef.current.close()}
              >
                Close details
              </button>
            </div>
          </>
        )}
      </dialog>
    </div>
  )
}

export default App
