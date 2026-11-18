import test from 'node:test'
import assert from 'node:assert/strict'
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
  getKpiComparison,
  getChairPriorities,
} from '../src/data/dashboard.js'

const paperPeriod = periods.find((period) => period.id === '2026-2027-1')

test('default reporting scenario reproduces the five paper examples', () => {
  const summary = summarize(paperPeriod.rows)
  assert.deepEqual(getMetrics(summary), {
    passRate: 88,
    onTimeRate: 90,
    responseRate: 60,
    meanRating: 4.2,
    difficultyRate: 15,
  })
  assert.equal(summary.points, 79380)
  assert.equal(summary.itemCount, 18900)
  assert.equal(summary.students, 420)
  assert.equal(summary.outcomes - summary.passed, 252)
  assert.equal(summary.responses, 1260)
})

test('every simulated cohort respects academic and evaluation count bounds', () => {
  for (const period of periods) {
    assert.equal(new Set(period.rows.map((row) => row.level)).size, 4)
    for (const row of period.rows) {
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
        assert.ok(
          Number.isInteger(row[key]) && row[key] >= 0,
          `${period.id}: ${key}`,
        )
      assert.ok(row.passed <= row.outcomes)
      assert.ok(row.affected <= row.students)
      assert.ok(row.affected <= row.outcomes - row.passed)
      assert.ok(row.outcomes - row.passed <= row.affected * 5)
      assert.ok(row.responses <= row.eligible)
      assert.ok(row.onTime <= row.sections)
      row.dimensionPoints.forEach((points, i) => {
        const count = row.responses * dimensions[i].items
        assert.ok(
          Number.isInteger(points) && points >= count && points <= count * 5,
        )
      })
    }
  }
})

test('year-level filtering recalculates all KPIs from only the selected cohort', () => {
  const period = paperPeriod
  const rows = selectRows(period, '4')
  assert.equal(rows.length, 1)
  assert.equal(rows[0].level, 4)
  const metrics = getMetrics(summarize(rows))
  assert.equal(metrics.passRate, (366 / 450) * 100)
  assert.equal(metrics.onTimeRate, 75)
  assert.equal(metrics.responseRate, (210 / 450) * 100)
  assert.equal(metrics.meanRating, 4.2)
  assert.equal(metrics.difficultyRate, (20 / 90) * 100)
  assert.equal(selectRows(period).length, 4)
})

test('aggregation uses underlying totals rather than averaging subgroup percentages or means', () => {
  const rows = [
    {
      students: 1,
      passed: 1,
      affected: 0,
      sections: 1,
      onTime: 1,
      responses: 1,
      outcomes: 1,
      eligible: 1,
      dimensionPoints: [30, 25, 20],
    },
    {
      students: 9,
      passed: 0,
      affected: 9,
      sections: 9,
      onTime: 0,
      responses: 9,
      outcomes: 9,
      eligible: 9,
      dimensionPoints: [54, 45, 36],
    },
  ]
  const summary = summarize(rows)
  const metrics = getMetrics(summary)
  assert.equal(metrics.passRate, 10)
  assert.equal(metrics.onTimeRate, 10)
  assert.equal(metrics.meanRating, 1.4)
  assert.deepEqual(summary.dimensionScores, [1.4, 1.4, 1.4])
})

test('threshold equality meets targets and unrounded breaches raise warnings', () => {
  const boundaries = {
    passRate: 90,
    onTimeRate: 95,
    responseRate: 70,
    meanRating: 4,
    difficultyRate: 10,
  }
  assert.equal(getWarnings(boundaries).length, 0)
  for (const kpi of kpis) {
    const value = kpi.target + (kpi.direction === 'below' ? 0.0001 : -0.0001)
    assert.deepEqual(
      getWarnings({ ...boundaries, [kpi.id]: value }).map((item) => item.id),
      [kpi.id],
    )
  }
})

test('missing denominators produce unavailable KPIs without performance warnings', () => {
  const metrics = getMetrics(summarize([]))
  assert.ok(Object.values(metrics).every((value) => value === null))
  assert.equal(getWarnings(metrics).length, 0)
  assert.equal(formatValue(null), 'N/A')
})

test('alerts change across periods and a good mean rating does not erase low participation', () => {
  assert.equal(getWarnings(getMetrics(summarize(periods[0].rows))).length, 0)
  const warnings = getWarnings(getMetrics(summarize(paperPeriod.rows)))
  assert.deepEqual(
    warnings.map((item) => item.id),
    ['passRate', 'onTimeRate', 'responseRate', 'difficultyRate'],
  )
  assert.equal(formatValue(4.2, 'rating'), '4.20')
})

test('chair priorities use the selected cohort counts and distinguish late records from missing grades', () => {
  const priorities = getChairPriorities(paperPeriod.rows)
  assert.equal(priorities[0].level, 4)
  assert.ok(priorities[0].evidence.includes('81.3%'))
  assert.ok(priorities[0].evidence.includes('20 of 90'))
  assert.ok(priorities[0].evidence.includes('22.2%'))
  assert.ok(priorities[1].evidence.includes('4 of 40'))
  assert.match(kpis.find((kpi) => kpi.id === 'onTimeRate').context, /all grades.*finalized/i)
  assert.ok(priorities[2].evidence.includes('1,260 / 2,100'))
  assert.ok(priorities[2].evidence.includes('60.0%'))

  const yearThree = getChairPriorities(selectRows(paperPeriod, '3'))
  assert.equal(yearThree[0].level, 3)
  assert.ok(yearThree[0].evidence.includes('17 of 100'))
  assert.ok(yearThree[1].evidence.includes('1 of 10'))
})

test('cohort review is not hidden by an overall academic rate within target', () => {
  const period = periods[1]
  assert.ok(getMetrics(summarize(period.rows)).difficultyRate < 10)
  const academic = getChairPriorities(period.rows)[0]
  assert.equal(academic.status, 'review')
  assert.equal(academic.level, 4)
  assert.ok(getChairPriorities(periods[0].rows).every((item) => item.status === 'within'))
})

test('missing coverage does not produce healthy chair priorities', () => {
  assert.deepEqual(getChairPriorities([]), [])
  const noCoverage = { level: 1, ...summarize([]) }
  assert.ok(getChairPriorities([noCoverage]).every((item) => item.status === 'unavailable'))
})

test('card comparisons respect metric direction, percentage-point units and missing history', () => {
  const pass = kpis.find((kpi) => kpi.id === 'passRate')
  const difficulty = kpis.find((kpi) => kpi.id === 'difficultyRate')
  const rating = kpis.find((kpi) => kpi.id === 'meanRating')
  assert.equal(getKpiComparison(pass, 88, 92.25).direction, 'declined')
  assert.equal(getKpiComparison(difficulty, 10, 15).direction, 'improved')
  assert.ok(getKpiComparison(pass, 88, 92.25).label.includes('4.3 pp'))
  assert.ok(getKpiComparison(rating, 4.2, 4.15).label.includes('0.05 points'))
  assert.equal(getKpiComparison(pass, 88, null).direction, 'unavailable')
  assert.equal(getKpiComparison(pass, null, 90).direction, 'unavailable')
  assert.equal(getKpiComparison(rating, 4.2, 4.200001).direction, 'unchanged')
  const summary = summarize(paperPeriod.rows)
  assert.ok(getKpiCount('difficultyRate', summary).includes('63 / 420 students'))
  assert.ok(getKpiCount('responseRate', summary).includes('1,260 / 2,100'))
})

test('priority metrics and target gaps use the same cohort and correct target direction', () => {
  const [academic, submission, teaching] = getChairPriorities(paperPeriod.rows)
  assert.equal(academic.metric.label, 'Academic difficulty rate')
  assert.ok(Math.abs(academic.metric.value - (20 / 90) * 100) < 1e-10)
  assert.ok(Math.abs(academic.metric.gap - ((20 / 90) * 100 - 10)) < 1e-10)
  assert.equal(academic.metric.gapDirection, 'above')
  assert.equal(submission.metric.value, 90)
  assert.equal(submission.metric.gap, 5)
  assert.equal(submission.metric.gapDirection, 'below')
  assert.equal(teaching.metric.value, 60)
  assert.equal(teaching.metric.gap, 10)
  assert.equal(teaching.metric.gapDirection, 'below')
  assert.ok(getChairPriorities(periods[0].rows).every((item) => item.metric.gap === 0))
  assert.ok(getChairPriorities([{ level: 1, ...summarize([]) }]).every((item) => item.metric.gap === null))
})

test('both academic years offer two semesters with separate cohort results', () => {
  for (const year of new Set(periods.map((period) => period.year))) {
    const terms = periods.filter((period) => period.year === year)
    assert.deepEqual(terms.map((period) => period.semester), ['First semester', 'Second semester'])
    assert.ok(terms[0].order < terms[1].order)
  }

  const secondSemester = periods.find((period) => period.id === '2026-2027-2')
  const summary = summarize(selectRows(secondSemester))
  assert.equal(summary.students, 420)
  assert.equal(summary.passed, 1925)
  assert.equal(summary.responses, 1560)
  assert.equal(getMetrics(summary).onTimeRate, 95)
  assert.notDeepEqual(getMetrics(summary), getMetrics(summarize(paperPeriod.rows)))

  const yearFour = getMetrics(summarize(selectRows(secondSemester, '4')))
  assert.equal(yearFour.passRate, (390 / 450) * 100)
  assert.equal(yearFour.responseRate, (300 / 450) * 100)
  assert.ok(getChairPriorities(secondSemester.rows).every((priority) => priority.metric.value !== null))
})
