import test from 'node:test'
import assert from 'node:assert/strict'
import { createServer } from 'vite'
import { createElement } from 'react'
import { renderToString } from 'react-dom/server'

test('dashboard renders the required five cards, three charts, filters and contextual alerts', async () => {
  const server = await createServer({
    server: { middlewareMode: true },
    appType: 'custom',
  })
  try {
    // Vite transforms JSX while React remains an external Node dependency.
    const { default: App } = await server.ssrLoadModule('/src/App.jsx')
    const html = renderToString(createElement(App))
    assert.equal((html.match(/class="kpi-card"/g) || []).length, 5)
    assert.equal((html.match(/Visualization /g) || []).length, 3)
    assert.equal((html.match(/<select/g) || []).length, 3)
    assert.equal((html.match(/class="alert-row"/g) || []).length, 4)
    for (const value of ['88.0%', '90.0%', '60.0%', '4.20', '15.0%'])
      assert.ok(html.includes(value))
    assert.ok(html.includes('Program Chair'))
    assert.ok(html.includes('Simulated data.'))
    assert.ok(html.includes('integration is proposed'))
    assert.ok(
      html.includes('must not be the sole basis for personnel decisions'),
    )
    assert.ok(html.includes('completed / eligible evaluations'))
    assert.ok(html.includes('<dialog'))
    assert.ok(!html.includes('<aside'))
    assert.ok(!html.includes('<nav'))
    assert.ok(!html.includes('class="sidebar"'))
    assert.ok(html.includes('Academic support review needed'))
    assert.ok(html.includes('Average SETE rating across semesters'))
    assert.ok(html.includes('n = '))
    assert.ok(html.includes('Reset filters'))
    assert.ok(html.includes('Simulated data · Case study'))
    assert.ok(html.includes('Details'))
    assert.ok(html.includes('aria-atomic="true"'))
    assert.ok(html.includes('aria-labelledby="kpi-detail-title"'))
  } finally {
    await server.close()
  }
})
