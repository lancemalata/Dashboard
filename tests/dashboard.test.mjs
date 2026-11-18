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
} from '../src/data/dashboard.js'

test('default reporting scenario reproduces the five paper examples', () => {
  const summary = summarize(periods.at(-1).rows)
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
  const period = periods.at(-1)
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
  const warnings = getWarnings(getMetrics(summarize(periods.at(-1).rows)))
  assert.deepEqual(
    warnings.map((item) => item.id),
    ['passRate', 'onTimeRate', 'responseRate', 'difficultyRate'],
  )
  assert.equal(formatValue(4.2, 'rating'), '4.20')
})
