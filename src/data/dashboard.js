// Entirely simulated aggregates. No personal records or real faculty ratings.
export const dimensions = [
  {
    id: 'management',
    label: 'Management of Teaching and Learning',
    short: 'Management',
    items: 6,
    color: '#a92b3a',
  },
  {
    id: 'knowledge',
    label: 'Content Knowledge, Pedagogy and Technology',
    short: 'Knowledge',
    items: 5,
    color: '#446d83',
    dash: '6 3',
  },
  {
    id: 'commitment',
    label: 'Commitment and Transparency',
    short: 'Commitment',
    items: 4,
    color: '#97815c',
    dash: '2 3',
  },
]

function makeRows(tuples, means) {
  return tuples.map(
    ([students, passed, affected, sections, onTime, responses], i) => ({
      level: i + 1,
      students,
      passed,
      affected,
      sections,
      onTime,
      responses,
      outcomes: students * 5,
      eligible: students * 5,
      dimensionPoints: dimensions.map((dimension, j) =>
        Math.round(responses * dimension.items * means[j]),
      ),
    }),
  )
}

export const periods = [
  {
    id: '2025-2026-1',
    year: '2025-2026',
    semester: 'First semester',
    shortLabel: '25–26 · S1',
    order: 1,
    rows: makeRows(
      [
        [110, 510, 10, 10, 10, 385],
        [100, 460, 10, 10, 10, 350],
        [90, 414, 9, 8, 8, 315],
        [90, 414, 9, 8, 8, 315],
      ],
      [4.1, 4.06, 4.0],
    ),
  },
  {
    id: '2025-2026-2',
    year: '2025-2026',
    semester: 'Second semester',
    shortLabel: '25–26 · S2',
    order: 2,
    rows: makeRows(
      [
        [115, 535, 10, 12, 12, 430],
        [105, 485, 10, 10, 10, 390],
        [95, 435, 10, 10, 10, 355],
        [85, 390, 9, 8, 8, 320],
      ],
      [4.2, 4.14, 4.08],
    ),
  },
  {
    id: '2026-2027-1',
    year: '2026-2027',
    semester: 'First semester',
    shortLabel: '26–27 · S1',
    order: 3,
    rows: makeRows(
      [
        [120, 552, 12, 12, 12, 420],
        [110, 495, 14, 10, 9, 350],
        [100, 435, 17, 10, 9, 280],
        [90, 366, 20, 8, 6, 210],
      ],
      [4.25, 4.2, 4.125],
    ),
  },
]

export function selectRows(period, yearLevel = 'all') {
  return period.rows.filter(
    (row) => yearLevel === 'all' || row.level === Number(yearLevel),
  )
}

const divide = (numerator, denominator) =>
  denominator > 0 ? numerator / denominator : null
const percent = (numerator, denominator) =>
  denominator > 0 ? (numerator / denominator) * 100 : null

export function summarize(rows) {
  const summary = rows.reduce(
    (total, row) => {
      for (const key of [
        'students',
        'passed',
        'affected',
        'sections',
        'onTime',
        'responses',
        'outcomes',
        'eligible',
      ])
        total[key] += row[key]
      row.dimensionPoints.forEach((points, i) => {
        total.dimensionPoints[i] += points
      })
      return total
    },
    {
      students: 0,
      passed: 0,
      affected: 0,
      sections: 0,
      onTime: 0,
      responses: 0,
      outcomes: 0,
      eligible: 0,
      dimensionPoints: [0, 0, 0],
    },
  )
  summary.itemCount = summary.responses * 15
  summary.points = summary.dimensionPoints.reduce((a, b) => a + b, 0)
  summary.dimensionScores = summary.dimensionPoints.map((points, i) =>
    divide(points, summary.responses * dimensions[i].items),
  )
  return summary
}

export function getMetrics(summary) {
  return {
    passRate: percent(summary.passed, summary.outcomes),
    onTimeRate: percent(summary.onTime, summary.sections),
    responseRate: percent(summary.responses, summary.eligible),
    meanRating: divide(summary.points, summary.itemCount),
    difficultyRate: percent(summary.affected, summary.students),
  }
}

export const formatValue = (value, unit = 'percent') =>
  value === null
    ? 'N/A'
    : `${value.toFixed(unit === 'rating' ? 2 : 1)}${unit === 'rating' ? '' : '%'}`
const n = (value) => value.toLocaleString('en-US')

export const kpis = [
  {
    id: 'passRate',
    label: 'Course pass rate',
    icon: 'cap',
    unit: 'percent',
    target: 90,
    targetLabel: '≥ 90%',
    direction: 'above',
    formula:
      'Passed student–course enrollments ÷ enrollments with finalized pass/fail outcomes × 100.',
    inputs: (s) => `${n(s.passed)} ÷ ${n(s.outcomes)} × 100`,
    title: 'Course outcomes need attention',
    action:
      'Review course and year-level outcomes; plan appropriate academic support.',
    context:
      'Counts course outcomes, not unique students. Missing, incomplete and withdrawn records are excluded and must be disclosed in a production report.',
  },
  {
    id: 'onTimeRate',
    label: 'On-time grade submission',
    icon: 'clock',
    unit: 'percent',
    target: 95,
    targetLabel: '≥ 95%',
    direction: 'above',
    formula:
      'Sections with complete final grades submitted by the applicable deadline ÷ sections whose deadline has passed × 100.',
    inputs: (s) => `${n(s.onTime)} ÷ ${n(s.sections)} × 100`,
    title: 'Grade submission needs follow-up',
    action:
      'Check overdue sections and approved deadline exceptions before follow-up.',
    context:
      'A complete submission after the deadline remains late. All grades in this scenario are now finalized; the timeliness record is retained.',
  },
  {
    id: 'responseRate',
    label: 'SETE response rate',
    icon: 'message',
    unit: 'percent',
    target: 70,
    targetLabel: '≥ 70%',
    direction: 'above',
    formula:
      'Completed valid evaluations ÷ eligible student–course evaluation assignments × 100.',
    inputs: (s) => `${n(s.responses)} ÷ ${n(s.eligible)} × 100`,
    title: 'Evaluation participation is low',
    action:
      'Review access and eligibility issues; interpret the available feedback cautiously.',
    context:
      'A student can evaluate several courses. This counts evaluation assignments, not distinct students. The evaluation window is closed in this scenario; open windows should say participation in progress.',
  },
  {
    id: 'meanRating',
    label: 'Mean SETE rating',
    icon: 'star',
    unit: 'rating',
    target: 4,
    targetLabel: '≥ 4.00 / 5',
    direction: 'above',
    formula:
      'Total valid item-score points ÷ valid item responses in completed fifteen-item evaluations.',
    inputs: (s) => `${n(s.points)} points ÷ ${n(s.itemCount)} item responses`,
    title: 'Teaching feedback warrants review',
    action:
      'Discuss dimension results, participation and supporting evidence with the faculty member.',
    context:
      'All fifteen items have equal weight. The dimensions have six, five and four items. A rating is student perception, not a complete measure of effectiveness; do not use it alone for personnel decisions.',
  },
  {
    id: 'difficultyRate',
    label: 'Academic difficulty rate',
    icon: 'alert',
    unit: 'percent',
    target: 10,
    targetLabel: '≤ 10%',
    direction: 'below',
    formula:
      'Distinct students with at least one finalized failed course ÷ students with at least one finalized pass/fail outcome × 100.',
    inputs: (s) => `${n(s.affected)} ÷ ${n(s.students)} × 100`,
    title: 'Academic support may be needed',
    action:
      'Validate failed-course records and arrange confidential advising or learning support.',
    context:
      'Each student is counted once. This describes recorded academic outcomes; it is not a prediction of future failure or a judgment of student ability.',
  },
]

export function getWarnings(metrics) {
  return kpis.filter(
    (kpi) =>
      metrics[kpi.id] !== null &&
      (kpi.direction === 'below'
        ? metrics[kpi.id] > kpi.target
        : metrics[kpi.id] < kpi.target),
  )
}

export function getKpiCount(id, summary) {
  const counts = {
    passRate: `${n(summary.passed)} / ${n(summary.outcomes)} course outcomes passed`,
    onTimeRate: `${n(summary.onTime)} / ${n(summary.sections)} due sections on time`,
    responseRate: `${n(summary.responses)} / ${n(summary.eligible)} evaluations completed`,
    meanRating: `${n(summary.responses)} completed evaluations`,
    difficultyRate: `${n(summary.affected)} / ${n(summary.students)} students with failed courses`,
  }
  return counts[id]
}

export function getKpiComparison(kpi, current, previous) {
  if (current == null || previous == null)
    return { label: 'No prior-semester comparison', direction: 'unavailable' }

  const difference = current - previous
  const digits = kpi.unit === 'rating' ? 2 : 1
  const magnitude = Math.abs(difference).toFixed(digits)
  if (Number(magnitude) === 0)
    return { label: 'No displayed change vs prior semester', direction: 'unchanged' }

  const improved = kpi.direction === 'below' ? difference < 0 : difference > 0
  return {
    label: `${difference > 0 ? '+' : '−'}${magnitude} ${kpi.unit === 'rating' ? 'points' : 'pp'} vs prior semester`,
    direction: improved ? 'improved' : 'declined',
  }
}

export function getChairPriorities(rows) {
  if (rows.length === 0) return []

  const summary = summarize(rows)
  const metrics = getMetrics(summary)
  const target = Object.fromEntries(kpis.map((kpi) => [kpi.id, kpi.target]))
  const academicConcerns = rows
    .map((row) => ({ row, metrics: getMetrics(summarize([row])) }))
    .filter(({ metrics: value }) =>
      (value.passRate !== null && value.passRate < target.passRate) ||
      (value.difficultyRate !== null && value.difficultyRate > target.difficultyRate),
    )
    .sort((a, b) =>
      (b.metrics.difficultyRate ?? -1) - (a.metrics.difficultyRate ?? -1) ||
      (a.metrics.passRate ?? 101) - (b.metrics.passRate ?? 101),
    )
  const focus = academicConcerns[0]
  const academicAvailable = metrics.passRate !== null && metrics.difficultyRate !== null
  const submissionAvailable = metrics.onTimeRate !== null
  const teachingAvailable = metrics.responseRate !== null && metrics.meanRating !== null
  const lowParticipation = metrics.responseRate !== null && metrics.responseRate < target.responseRate
  const lowRating = metrics.meanRating !== null && metrics.meanRating < target.meanRating
  const academicDetail = focus && focus.metrics.difficultyRate <= target.difficultyRate ? 'passRate' : 'difficultyRate'
  const teachingDetail = lowRating && !lowParticipation ? 'meanRating' : 'responseRate'

  function priorityMetric(id, values) {
    const kpi = kpis.find((item) => item.id === id)
    const value = values[id]
    return {
      label: kpi.label,
      value,
      unit: kpi.unit,
      targetLabel: kpi.targetLabel,
      gap: value === null ? null : Math.max(0,
        kpi.direction === 'below' ? value - kpi.target : kpi.target - value,
      ),
      gapDirection: kpi.direction === 'below' ? 'above' : 'below',
    }
  }

  return [
    {
      id: 'academic',
      icon: 'alert',
      metric: priorityMetric(academicDetail, focus?.metrics ?? metrics),
      status: !academicAvailable ? 'unavailable' : focus ? 'review' : 'within',
      title: focus ? `Review Year ${focus.row.level} academic outcomes` : 'Academic outcomes',
      evidence: focus
        ? `${formatValue(focus.metrics.passRate)} course pass rate; ${n(focus.row.affected)} of ${n(focus.row.students)} students have a finalized failed course (${formatValue(focus.metrics.difficultyRate)}).`
        : academicAvailable
          ? `All selected year levels meet both proposed academic targets; ${n(summary.affected)} of ${n(summary.students)} students have a finalized failed course.`
          : 'Finalized academic coverage is unavailable for the selected scope.',
      action: focus
        ? 'Validate outcomes and coordinate confidential student advising.'
        : academicAvailable
          ? 'Monitor outcomes and provide support as needed.'
          : 'Verify academic data before review.',
      level: focus?.row.level ?? null,
      detail: academicDetail,
    },
    {
      id: 'submission',
      icon: 'clock',
      metric: priorityMetric('onTimeRate', metrics),
      status: !submissionAvailable ? 'unavailable' : metrics.onTimeRate < target.onTimeRate ? 'review' : 'within',
      title: 'Grade-submission timeliness',
      evidence: submissionAvailable
        ? `${n(summary.sections - summary.onTime)} of ${n(summary.sections)} due sections did not meet the submission deadline.`
        : 'No due-section denominator is available.',
      action: 'Check submission times and approved deadline exceptions.',
      detail: 'onTimeRate',
    },
    {
      id: 'teaching',
      icon: 'message',
      metric: priorityMetric(teachingDetail, metrics),
      status: !teachingAvailable ? 'unavailable' : lowParticipation || lowRating ? 'review' : 'within',
      title: 'Teaching feedback and participation',
      evidence: `${n(summary.responses)} / ${n(summary.eligible)} evaluations completed (${formatValue(metrics.responseRate)}); mean SETE ${formatValue(metrics.meanRating, 'rating')} / 5.`,
      action: lowParticipation
        ? 'Address participation barriers before the next evaluation window.'
        : 'Review faculty feedback alongside other teaching evidence.',
      detail: teachingDetail,
    },
  ]
}
