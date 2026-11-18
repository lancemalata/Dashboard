# Program Chair Dashboard Review

Reviewed on 18 November 2026. Baseline source commit: `fd927ff`. This report describes the final single-page dashboard refinements prepared for the repository. No hosted deployment was performed.

## Overall assessment

The dashboard provides an appropriate academic and teaching-feedback overview for the BSIT Program Chair. Its five KPIs, three charts, semester and cohort filters, proposed targets, recorded academic difficulty alert, and SETE participation context support most of the evaluation questionnaire's design criteria. The supplied paper and the baseline dashboard use consistent default values and denominators.

The main gaps were how readily a chair could discover the KPI-detail interactions, distinguish observations from suggested actions, and identify a useful next step without opening several dialogs. The supplied dashboard PDF also has crowded print labels. These are presentation and decision-support gaps; they do not require another page or a sixth KPI.

This is a review of a simulated prototype. It does not establish readiness for confidential production records. Questionnaire agreement scores should come from the actual evaluator. No numerical ratings or completion percentage have been invented.

## Sources and evidence

- Supplied paper: `C:/Users/lance/Downloads/BAT405_Academic_Insights_BSU_Revised.docx`, especially Parts II, III and V. The document was read without modifying it.
- Supplied dashboard: `C:/Users/lance/Downloads/Academic Insights _ Program Chair Dashboard.pdf`. Its single page was rendered and visually inspected.
- Evaluation instrument: `C:/Users/lance/Downloads/BAT405_Analytics_Dashboard_Evaluation_Questionnaire_Revised.pdf`. Both pages and all 24 statements were inspected.
- Current application: [dashboard interface](../src/App.jsx), [calculations and simulated data](../src/data/dashboard.js), and [dashboard styles](../src/App.css).
- Verification: the existing calculation and server-rendering tests, additional tests for the new decision summaries, and the production build.

The questionnaire explicitly separates demonstrated behavior from proposed features. Source code and automated tests provide evidence, but they do not substitute for a live user demonstration, a usability rating or print-preview acceptance.

## Review against every questionnaire item

“Supported” means the reviewed content provides evidence for the statement. “Improved locally” means an identified weakness has a local implementation, with browser acceptance still outstanding. “Demo required” means behavior must be observed before a reviewer rates it as demonstrated.

| Item | Criterion in brief | Baseline finding | Local result and evidence |
| --- | --- | --- | --- |
| A1 | Purpose and intended user | Supported. The heading identifies academic performance, teaching effectiveness, Program Chair and BSIT/CICS. | The heading retains Program Chair and BSIT/CICS; KPI and chart titles identify the academic and teaching measures. |
| A2 | Important information easy to find | Supported. Five headline KPIs precede the charts. | Cards remain compact; counts and comparisons are available in their detail dialogs, while a priorities section surfaces follow-up. |
| A3 | Logical information order | Supported. Scope, summary metrics, academic outcomes and teaching feedback follow a coherent order. | Existing components remain. The new follow-up section connects summaries to a chair's tasks. |
| A4 | Recorded information distinguished from insights | Partially supported. Sample-data and descriptive-trend disclaimers exist, but the distinction is mostly implicit. | Improved locally. The reporting caption states scope, and the separate priorities section explicitly labels recommended actions. The simulated-data badge remains visible. |
| B1 | Five relevant KPI cards | Supported. Course passing, submission timeliness, evaluation coverage, mean feedback and academic difficulty are relevant to the paper's scope. | All five preserved; no extra KPI introduced. |
| B2 | Clear KPI labels | Supported. Labels and detailed definitions exist. | Detail-dialog counts clarify students, course outcomes, due sections and evaluations without replacing the original definitions. |
| B3 | Targets, periods and thresholds | Supported. Targets appear on cards and reporting scope appears above the charts. | Preserved. Prior-semester comparisons remain in the dialogs, using percentage points for rates and scale points for ratings. |
| B4 | Areas needing attention identified | Supported. Four default cards show review states, with threshold logic defined in code. | Cohort priorities make the academic concern more actionable while preserving existing warnings. |
| C1 | At least three suitable visualizations | Supported. Course pass-rate bars, a semester SETE trend and a dimension dot plot serve distinct comparisons. | All three preserved. |
| C2 | Chart titles, units and labels | Supported in content. Titles, count labels, scales and target explanations exist. Some print labels are too close. | Print spacing has been adjusted; a fresh browser print preview is required to confirm the result. |
| C3 | Trends and comparisons understandable | Supported. The time trend includes response counts and is explicitly descriptive. | Preserved. KPI dialogs provide prior-semester comparison context; no forecast has been added. |
| C4 | Readability and lack of clutter | Partially supported. The supplied PDF crowds the Year 4 count against the course target note and the dimension axis against its last row. | Print chart rows now allow content-driven height, with reserved axis and note spacing. Desktop, mobile and one-sheet print acceptance remain to be checked visually. |
| D1 | At least two interactive features presented | Both feature groups exist: coordinated filters and KPI-detail dialogs. The second is not immediately obvious in a static PDF. | Improved locally with card hover descriptions, explicit priority-detail buttons and a Focus Year control using the existing year-level filter. |
| D2 | Interaction purpose understandable | Filter labels are clear; the card-to-dialog action lacks a visible explanation. | Card hover descriptions and accessible labels explain their action. Priority buttons visibly name their focus/detail actions. |
| D3 | Interactions match user tasks | Supported by the design: term/cohort selection and KPI explanation fit chair review. | Guided cohort focus supports moving from an overall concern to the relevant year-level scope on the same page. |
| D4 | Controls update relevant information correctly when demonstrated | Calculation and rendering tests pass, but a static PDF cannot establish browser interaction correctness. | Demo required. Thirteen automated tests and the build pass; browser interaction verification was unavailable. Mark N/A if the evaluator has no demonstration, consistent with the form. |
| E1 | Understandable warning or alert | Supported. Academic-status and KPI review messages are present. | Preserved; the priorities section adds explicitly labeled review context. |
| E2 | Condition requiring attention explained | Supported. The default academic message states 63 of 420 students and the proposed difficulty threshold. | Cohort evidence now shows the selected focus's rates and student counts, without describing finalized outcomes as predictions. |
| E3 | Possible academic or teaching actions identifiable | Partially supported in a glance or printed view: actions exist primarily inside KPI dialogs. | Improved locally. Three compact follow-ups cover academic support, submission timeliness, and participation-aware teaching review. |
| E4 | Enough context to avoid unsupported conclusions | Supported. Formulas, item weights, sample counts, proposed benchmarks and interpretation notes are available. | Preserved. Submission evidence describes missed deadlines; its detail dialog clarifies that grades are finalized. Participation follow-up refers to the next evaluation window. |
| F1 | Avoid unnecessary confidential disclosure | Supported for the displayed synthetic prototype: no real student identities, faculty results or evaluation comments are displayed. | Preserved. This does not verify server-side permissions or security for a live deployment. |
| F2 | SETE participation and reporting context | Supported. The period, completed/eligible assignments and trend sample counts are shown. | Preserved and included in the new teaching-review summary. Evaluations are not relabeled as unique students. |
| F3 | SETE not treated as the sole teaching measure | Supported. The visible caution and detail interpretation reject using it alone for personnel conclusions. | Preserved. The concise context strip says to use SETE alongside other teaching evidence; the detail interpretation retains the fuller explanation. |
| F4 | Fair and responsible presentation | Supported for the prototype's stated scope: simulated data, proposed targets, no public faculty rankings and no predictive claim. | Preserved. The new priorities suggest human review and support rather than diagnoses, causal claims or automatic sanctions. |

## Local improvements made

1. Added supporting counts to the KPI detail dialogs while keeping cards limited to label, value, status and target. The default counts remain 1,848/2,100 passing course outcomes, 36/40 on-time due sections, 1,260/2,100 completed evaluation assignments, 1,260 completed evaluations for the mean, and 63/420 students with a finalized failed course.
2. Retained the full prior-semester comparison in each detail dialog. Rates use percentage points; ratings use points on the five-point scale. Missing history is explicitly unavailable.
3. Added hover descriptions to clickable KPI cards, explicit priority-detail buttons and a guided year-level focus control.
4. Added a compact Program Chair priorities section, calculated from the selected existing dataset. It separates suggested actions from the recorded outcomes and responds to the existing reporting filters.
5. Adjusted print spacing for the course-count/target-note collision and the dimension-row/axis collision visible in the supplied PDF. The existing 8.5-by-13-inch print size remains.
6. Restyled the priorities using the supplied UI reference: a red heading accent, rounded white cards, tinted icons and scope badges, prominent values, proposed targets and directional target gaps, recommended actions, and a View full analysis link. Values remain tied to the existing academic, submission and participation metrics. Cohort analysis opens the existing KPI dialog with that cohort selected, on the same application page.
7. Refined font weights without enlarging the established type scale, added relevant chart icons, enlarged KPI icons, thickened course pass-rate bars, shortened recommended actions, and expanded the filters and KPI row to use the available width. Repeated explanatory text was shortened at the user's request.

All five KPI cards, three charts, filters and detail dialogs were retained. Supporting text was streamlined at the user's request. No route, separate application page, additional KPI, new source dataset, fabricated course/faculty breakdown, login screen or predictive model was added. The supplied Word and PDF files were not edited.

## Why the additions matter to the Program Chair

The default aggregate academic difficulty is 15%, but the existing year-level data show Year 4 at 20 of 90 students, or 22.2%, with an 81.3% course pass rate. That is a useful review focus for advising and course-outcome validation. It does not identify the cause, a responsible faculty member or a future student outcome.

There are four due-section records that did not meet their submission deadline. The sample states that grades are finalized, so those records must not be presented as four currently unsubmitted sections.

The 4.20/5 mean SETE rating meets the proposed target, while only 60% of eligible evaluation assignments were completed. Those two facts must remain together. The next step is to understand participation barriers and use other teaching evidence; the sample does not justify treating a dimension above target as a poor faculty rating.

A cohort can warrant review even when the overall program rate meets its target. The new priority calculation evaluates the selected year-level rows, rather than letting a pooled average hide a smaller cohort's recorded difficulty. It never retrieves individual identities.

## Remaining limits and acceptance checks

The case-study overview is sufficient for demonstrating the selected five KPIs and most questionnaire design criteria. Operational use would additionally need authorized course/section detail, verified sources and reporting timestamps, source-quality checks, access controls and a documented follow-up process. Those are not implemented by adding a client-side filter or a visual login form. The paper already describes production controls and student-level prediction as future work.

For the current submission, keep the one-page dashboard and complete these acceptance checks:

- Change every academic-year/semester combination and every year-level option; confirm all counts, cards, priorities, chart values and trend scope update together.
- Select Focus Year from an overall priority, confirm the Year level selector and all other views follow it, then reset to the default scope.
- Open each KPI and each new detail button; close by button, Escape and backdrop; verify keyboard focus returns appropriately.
- Check at desktop and narrow mobile widths for clipping, horizontal overflow, unreadable labels and a sensible reading order.
- Print at 8.5 by 13 inches and inspect the actual browser preview for one-sheet pagination, complete legends and separated chart labels. One application page and one printed sheet are separate checks.
- Demonstrate these interactions to the evaluator before recording D4 as demonstrated. Do not fill in subjective agreement scores on the evaluator's behalf.
- Refresh the paper's dashboard illustration if the improved local version is used for the final submission. The supplied paper and PDFs continue to show the baseline design.

## Verification result

- `npm.cmd test`: 13 tests passed, including all 8 existing tests and new tests for cohort selection, coverage handling, timeliness interpretation, comparison direction/units and target-gap direction.
- `npm.cmd run build`: passed.
- `git diff --check`: passed.
- Existing five cards, three charts, filter groups, dialogs, participation cautions and menu-free single-page structure remain covered by the existing rendering test.
- The supplied dashboard PDF and both questionnaire pages were visually inspected.
- Live browser interactions, the updated responsive layout and the updated print pagination were not visually verified because the browser access host was unavailable. No deployment was performed.
