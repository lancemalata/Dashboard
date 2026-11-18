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
  getKpiCount,
  getChairPriorities,
} from './data/dashboard.js'
import './App.css'

function Icon({ name, size = 20, strokeWidth = 1.7 }) {
  const paths = {
    grid: 'M3 3h7v7H3z M14 3h7v7h-7z M3 14h7v7H3z M14 14h7v7h-7z',
    book: 'M4 3h13a2 2 0 0 1 2 2v16H6a3 3 0 0 1-3-3V5a2 2 0 0 1 1-2 M3 17h16 M7 7h8 M7 10h6',
    cap: 'm2 9 10-5 10 5-10 5z M6 11v6q6 5 12 0v-6 M22 9v8',
    trend: 'M3 3v18h18 M7 14l4-4 4 3 6-7 M17 6h4v4',
    checklist: 'M9 4H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2h-4 M9 2h6v4H9z m-3 10 1 1 2-2 M12 12h5 m-11 5 1 1 2-2 M12 17h5',
    clock: 'M12 8v5l3 2 M22 12a10 10 0 1 1-20 0 10 10 0 0 1 20 0',
    message: 'M21 11a8 8 0 0 1-8 8H7l-5 3V11a9 9 0 0 1 19 0 M7 10h9 M7 14h5',
    star: 'm12 3 2.8 5.7 6.2.9-4.5 4.4 1.1 6.2-5.6-3-5.6 3 1.1-6.2L3 9.6l6.2-.9z',
    alert: 'm12 3 10 18H2z M12 9v5 M12 17v.1',
    arrow: 'M5 12h14 M14 7l5 5-5 5',
    info: 'M12 11v6 M12 7v.1 M22 12a10 10 0 1 1-20 0 10 10 0 0 1 20 0',
    print: 'M6 9V3h12v6 M6 17H3V9h18v8h-3 M6 14h12v7H6z M17 12h1',
    shield: 'm12 3 8 3v6c0 5-8 9-8 9s-8-4-8-9V6z m-4 9 3 3 5-5',
    close: 'm6 6 12 12 M6 18 18 6',
    reload: 'M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8 M21 3v5h-5',
    bell: 'M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9 M10 21a2 2 0 0 0 4 0',
  }
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={strokeWidth}
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d={paths[name] || paths.info} />
    </svg>
  )
}

function PanelTitle({ icon, title, subtitle, children }) {
  return (
    <div className="panel-title">
      <div className="panel-heading">
        <span className="panel-heading-icon" aria-hidden="true">
          <Icon name={icon} size={22} />
        </span>
        <div>
          <h2>{title}</h2>
          <p>{subtitle}</p>
        </div>
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
  const priorities = getChairPriorities(rows)
  const reviewPriorityCount = priorities.filter((priority) => priority.status === 'review').length
  const priorityReviewLabel = `${reviewPriorityCount} ${reviewPriorityCount === 1 ? 'priority needs' : 'priorities need'} review`

  function showDetails(id) {
    setDetail(id)
    dialogRef.current.showModal()
  }

  function showPriorityDetails(priority) {
    if (priority.level) setYearLevel(String(priority.level))
    showDetails(priority.detail)
  }

  return (
    <div className="app-shell">
      <a className="skip-link" href="#main">
        Skip to dashboard
      </a>
      <header className="brand-header">
        <div className="brand-header-inner">
          <a className="chairview-brand" href="#main" aria-label="ChairView dashboard">
            <img src="/chairview-logo.png" width="54" height="54" alt="" />
            <span>
              <strong>ChairView</strong>
              <span>Academic Analytics Dashboard</span>
            </span>
          </a>
          <div className="brand-context">
            <span className="brand-period">A.Y. {academicYear}</span>
            <a
              className="brand-notifications"
              href="#chair-priorities"
              aria-label={`${priorityReviewLabel}. View Program Chair priorities`}
              title={priorityReviewLabel}
            >
              <Icon name="bell" size={23} />
              <span
                className={`notification-badge${reviewPriorityCount === 0 ? ' is-clear' : ''}`}
                aria-hidden="true"
              >
                {reviewPriorityCount}
              </span>
            </a>
            <div className="brand-role">
              <span className="brand-avatar" aria-hidden="true">PC</span>
              <div>
                <strong>Program Chair</strong>
                <span>BS Information Technology</span>
              </div>
            </div>
          </div>
        </div>
      </header>
      <div className="workspace">
        <main id="main">
          <div className="page-heading">
            <div>
              <div className="eyebrow">
                BATANGAS STATE UNIVERSITY · ARASOF NASUGBU
              </div>
              <h1>Academic Analytics Overview</h1>
              <p>Program Chair · BSIT / CICS</p>
            </div>
          </div>
          <div className="report-toolbar">
            <div
              className="section-caption"
              role="status"
              aria-live="polite"
              aria-atomic="true"
            >
              <span>
                <strong>{period.semester} · AY {period.year}</strong> · {scope} ·{' '}
                {summary.students} students
              </span>
            </div>
            <div className="report-actions">
              <span className="sample-badge">Simulated data</span>
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
              <Icon name="reload" size={17} />
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
                  ? 'Academic support needed'
                  : 'Within proposed difficulty target'}
              </strong>
              <small>
                {summary.affected} of {summary.students} students with failed
                courses · Target ≤ 10%
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
                  title="View calculation, interpretation and recommended action"
                >
                  <div className="kpi-top">
                    <span
                      className={`kpi-icon ${warning ? 'needs-review' : ''}`}
                    >
                      <Icon name={kpi.icon} size={21} />
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
          <section className="chair-priorities" id="chair-priorities" aria-labelledby="chair-priorities-title">
            <div className="priority-heading">
              <div>
                <h2 id="chair-priorities-title">Program Chair priorities</h2>
                <p className="priority-period">
                  {priorityReviewLabel}
                </p>
              </div>
            </div>
            <ul className="priority-list">
              {priorities.map((priority) => (
                <li key={priority.id} className={`priority-item priority-${priority.status}`}>
                  <div className="priority-title">
                    <span className="priority-icon"><Icon name={priority.icon} size={21} /></span>
                    <h3>{priority.title}</h3>
                    <span className="priority-scope">{priority.level ? `Year ${priority.level}` : scope}</span>
                  </div>
                  <div className="priority-metric">
                    <strong>{formatValue(priority.metric.value, priority.metric.unit)}
                      {priority.metric.unit === 'rating' && <small> / 5</small>}
                    </strong>
                    <span>{priority.metric.label}</span>
                  </div>
                  <div className="priority-target">
                    <span>Target {priority.metric.targetLabel}</span>
                    <strong>
                      {priority.metric.gap === null ? 'Gap N/A' : priority.metric.gap > 0
                        ? `Gap ${priority.metric.gap.toFixed(priority.metric.unit === 'rating' ? 2 : 1)} ${priority.metric.unit === 'rating' ? 'points' : 'pp'} ${priority.metric.gapDirection}`
                        : 'Target met'}
                    </strong>
                  </div>
                  <p className="priority-evidence">
                    <strong>{priority.status === 'review' ? 'Review needed' : priority.status === 'within' ? 'Within target' : 'Not available'}</strong>
                    {' · '}{priority.evidence}
                  </p>
                  <div className="priority-action">
                    <strong>Recommended action</strong>
                    <p>{priority.action}</p>
                  </div>
                  <div className="priority-controls">
                    <button type="button" onClick={() => showPriorityDetails(priority)}
                      aria-label={`View full analysis for ${priority.metric.label}, ${priority.level ? `Year ${priority.level}` : scope}`}>
                      View full analysis <Icon name="arrow" size={14} />
                    </button>
                    {priority.level && yearLevel === 'all' && (
                      <button type="button" className="priority-focus" onClick={() => setYearLevel(String(priority.level))}>
                        Focus Year {priority.level} <Icon name="arrow" size={13} />
                      </button>
                    )}
                  </div>
                </li>
              ))}
            </ul>
          </section>
          <div className="chart-grid">
            <section className="panel" id="academic">
              <PanelTitle
                icon="cap"
                title="Course pass rate"
                subtitle="By year level"
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
                icon="trend"
                title="Average SETE rating across semesters"
                subtitle="Item-weighted mean through selected semester"
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
                Scale: 1–5 · Dashed line: target 4.00 · n = completed evaluations
              </p>
            </section>
            <section className="panel dimension-panel">
              <PanelTitle
                icon="checklist"
                title="SETE ratings by evaluation dimension"
                subtitle="Mean scores from completed evaluations"
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
                    <small title="Each statement has equal weight within its dimension">
                      {dimension.items} statements
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
              {metrics.responseRate < 70
                ? <b>Low participation: interpret SETE ratings cautiously.</b>
                : 'SETE ratings reflect completed evaluations.'}
            </span>
            <span>
              Use SETE alongside other teaching evidence.
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
              <p>{getKpiCount(detailKpi.id, summary)}</p>
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
