# Part III Analytics Dashboard and Decision Support Design

## Purpose and primary user

Academic Insights is a proposed analytics dashboard for the Program Chair of BS Information Technology under the College of Informatics and Computing Sciences at Batangas State University – ARASOF Nasugbu. It brings selected academic indicators and student teaching feedback into a common reporting view. The intended decisions concern academic support, timely grade submission, evaluation participation, and constructive discussion of teaching practices.

The dashboard is a system-design prototype implemented in the repository's existing React and Vite project. Programming is optional in the activity; the interactive prototype supplies the labeled dashboard mockup requested in the brief. It uses only simulated program aggregates. No connection to the university's systems, official administrative reports, real student records, or actual faculty ratings is implemented or claimed. The supplied student screens label the evaluation process SET; this case study follows the assignment's SETE terminology.

## Dashboard structure and component labels

The dashboard presents the primary user's role and program scope, followed by filters, an academic-status summary, and five KPI cards. A visible footer identifies the simulated data and proposed integration. There is no sidebar or navigation menu. The cards appear before detailed charts so the Program Chair can first identify indicators requiring review. Each card shows its value, proposed target, and a written status. Targets are initial case-study benchmarks, not university standards. Selecting a card opens its formula, numerical inputs, management action, and interpretation notes.

| Dashboard label | Component | Information and intended use |
| --- | --- | --- |
| Academic year, Semester, Year level | Interactive filter controls | Select a simulated reporting period and year-level cohort; recompute the cards, charts, alerts, and participation counts |
| BSIT / CICS in the header | Fixed scope label | BS Information Technology within CICS; avoids implying comparisons among multiple programs when the researcher confirms BSIT is the college's only program |
| KPI 1 | Course pass rate | Passed student–course enrollments divided by finalized pass/fail course outcomes; helps prioritize review of academic outcomes |
| KPI 2 | On-time grade submission | Complete section submissions by their applicable deadlines divided by sections due; supports follow-up of submission delays |
| KPI 3 | SETE response rate | Completed valid evaluations divided by eligible student–course evaluation assignments; shows coverage and supports cautious interpretation |
| KPI 4 | Mean SETE rating | Sum of valid item-score points divided by valid item responses; summarizes student perceptions with contextual qualifications |
| KPI 5 | Academic difficulty rate | Distinct students with at least one failed course divided by students with finalized outcomes; supports confidential academic assistance |
| Visualization 01 | Course pass rate by year level | Horizontal bars and numerical percentages with a proposed 90% reference marker; compares academic outcomes within BSIT |
| Visualization 02 | Average SETE rating across semesters | Overall item-weighted mean across available semesters, with numerical ratings and completed evaluation counts; displays descriptive patterns rather than predictions |
| Visualization 03 | SETE ratings by evaluation dimension | Horizontal dot plot for three dimension means on a 1–5 scale, with a proposed target marker at 4.00 |
| Priorities for review | Warning mechanism | Text-based flags for KPIs that breach the proposed thresholds, each paired with a suggested review action |
| Participation and confidentiality context | Compact information strip | Completed and eligible evaluation counts, a participation explanation, and a reminder that SETE must not determine personnel decisions by itself |

The screen design uses a concise, scrollable white dashboard with subtle burgundy accents, targeting approximately two desktop viewport heights. Five compact KPI cards and a short warning strip precede two side-by-side charts for course outcomes and semester ratings. A full-width dimension dot plot follows. Essential counts and participation context remain visible; formulas and longer explanations are available in dialogs or a collapsed dashboard guide. No navigation menu is included. Narrow screens stack the same charts naturally. Exact screen height depends on viewport and zoom and remains subject to visual verification; the assignment's one-page dashboard remains a separate print-layout requirement.

## Choice of three visualizations

**Visualization 01 Course pass rate by year level.** Horizontal bars make year-level comparisons straightforward. The chart shows the pass percentage and the passed/total course-outcome count for each included year level. Its scale spans 0–100%, and a reference marker identifies the proposed 90% target. The chair can use this comparison to decide where course-level investigation and academic assistance may be appropriate. A lower pass rate does not establish that a faculty member caused the outcome.

**Visualization 02 Average SETE rating across semesters.** A single line chart shows the overall mean SETE rating across the available semesters on a 1–5 scale. It computes each mean from the underlying item-score totals and response counts rather than averaging subgroup means. Visible point labels provide the ratings; each semester also displays n, its completed evaluation count. Period labels identify the academic year and semester; for example, 25–26 · S1 means the first semester of AY 2025–2026. Selecting an earlier reporting period removes later periods from the trend, and selecting a year level applies that cohort scope across the historical periods. Earlier academic years remain as historical context. The chart's accessible description also supplies the values and counts. Changes are descriptive and require contextual review; they are not forecasts or proof of improved learning.

**Visualization 03 SETE evaluation dimensions.** A horizontal dot plot compares the selected period's three dimension averages on a 1–5 display scale, with a dashed reference marker at the proposed 4.00 target. Dots show location on the rating scale rather than implying that the entire scale is a filled quantity. The display identifies the full dimension names, scores, number of statements, and total completed evaluations. The six-, five-, and four-item dimensions follow the supplied form. Each item has equal weight in the provisional calculation, meaning the overall rating is not a simple average of the three dimension means. Once an official instrument or weighting rule is provided, the calculation and explanation should be updated together.

## Readability and usability choices

The revised visual direction takes structural inspiration from [AcaVision](https://acavision.vercel.app/), inspected through its public page markup and styles. The application retains its own name, graduation-cap mark, BSU burgundy accents, dataset, five KPI definitions, and three evaluation dimensions. The final design uses compact headers, KPI cards, and charts instead of a large introduction or reading-guide panel. Additional explanation is available on demand. Each KPI also displays a neutral comparison with the immediately preceding sample semester for the same year-level scope. Percentage changes are expressed in percentage points, while rating differences use scale points; no earlier-period comparison appears when none is available. These comparisons describe the samples and do not establish causes. The reference is a design reference, not a source of university performance data. Its visual rendering could not be inspected through the available browser tools.

The interface uses a clean white report canvas, a slim header with a restrained burgundy rule, compact KPI cards, and larger chart areas with balanced emphasis on academic outcomes and teaching feedback. Dark secondary text, larger screen labels, generous chart padding, and consistent spacing establish a clear hierarchy. The screen layout grows naturally with its content rather than compressing charts to a fixed viewport height. Trend labels use CSS-sized text outside the scalable SVG drawing so they retain normal proportions. KPI formulas remain in the detail dialogs rather than taking space inside the cards; chart counts, bars, and ratings occupy separate columns to prevent label collisions. The original application symbol remains distinct from the official university seal. These choices apply usability principles; they are design decisions rather than a completed usability study or accessibility certification.

The review uses [Jakob Nielsen's ten heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/) as design guidance, not certification.

| Heuristic area | Application or limit |
| --- | --- |
| 1 Status | Active scope and changing counts remain visible. |
| 2 Familiar language | Academic terms have contextual explanations. |
| 3 Control | Reset filters and close dialogs. |
| 4 Consistency | Repeated labels, targets, controls, and chart patterns. |
| 5 Prevention | Semester choices follow the selected academic year. |
| 6 Recognition | Targets stay visible; details explain calculations. |
| 7 Efficiency | Filters update together; details open from cards or warnings. |
| 8 Focus | Large charts; supplementary help stays collapsed. |
| 9 Recovery | Unavailable calculations avoid false scores; live-source error recovery remains future work. |
| 10 Help | Collapsed task guidance and KPI interpretation dialogs. |

The interface prioritizes readable content on small or zoomed viewports. It does not hide or clip information merely to force a single-screen fit. Visual layout, keyboard interaction, zoom behavior, and print output still require browser acceptance testing.

## Two interactive features

**Feature 1 Coordinated filtering.** Academic-year and semester controls select the reporting period. Only semesters included in the simulated dataset are offered for a given year. A year-level control allows the chair to inspect all BSIT year levels or a single year level. All five KPI cards, the selected-period charts, participation counts, and warning conditions are recalculated from the selected scope. The historical trend uses the same year-level scope and includes periods up to the selected semester. Because this case study has one college and one program, the header's college/program scope remains fixed rather than offering meaningless alternatives. A future authorized multi-college system could add scoped college or department filters.

**Feature 2 KPI detail inspection.** Selecting a KPI card or a warning opens a labeled dialog. It explains the formula, shows the selected aggregate inputs, identifies the proposed target, and suggests a management action. It also provides the qualifications needed to interpret that KPI. This makes the calculation reviewable without exposing personal records. The dialog can be closed using its Close controls or the Escape key through the browser's native dialog behavior. Keyboard, focus, and visual checks remain part of acceptance testing rather than being assumed to pass.

## Warning mechanism and example decisions

Warnings use the same proposed thresholds as Part II: pass rate below 90%, on-time submission below 95%, SETE response below 70%, mean SETE rating below 4.00/5, or academic difficulty above 10%. Comparisons use unrounded values, so equality with a target meets the target. Where a KPI has no denominator, the calculation returns unavailable data rather than a performance warning.

The default simulated scenario matches the examples in Part II: 88% pass rate, 90% on-time submission, 60% SETE response, a 4.20/5 mean rating, and 15% academic difficulty. It produces four review flags. Although the mean rating meets its proposed target, the low-participation message remains visible. The Program Chair should investigate participation or access concerns before treating the rating as representative, check academic record completeness, and offer suitable student support.

This is a hypothetical finalized reporting scenario, not a claim that the real first semester of AY 2026–2027 has finished or that its evaluation window has closed. The supplied evaluation screenshot shows an open evaluation period; it is interface evidence, not the source of the prototype's completion status or sample results. In an operational dashboard, finalized/provisional status and the reporting cutoff must come from verified source records. An open evaluation period should display participation in progress, and incomplete grades should generate a completeness notice. The current prototype does not implement live cutoff or workflow tracking.

No real faculty members are ranked or linked to the sample scores. The warning actions request investigation and support; they do not prescribe sanctions or declare a cause for academic outcomes.

## Proposed confidentiality and access controls

The prototype protects real identities by including no actual student or faculty records, evaluation comments, or individual responses. Its Program Chair label communicates the intended audience; it is not an implemented login or permission system. All bundled simulated aggregates are accessible to someone who can open the prototype.

A real deployment would require institution-approved authentication and server-side authorization limiting a Program Chair to the program they oversee. Student identities should be separated from evaluation content. Participation checks should not permit the chair to connect an individual student's identity with their ratings. Faculty-level summaries should be available only to authorized recipients, while identifiable comments and academic support records require more restrictive handling.

Part II proposes suppressing class or faculty rating details below five completed evaluations, subject to institutional approval. The current view contains only program/year-level aggregates with larger sample counts and does not implement faculty-level access or suppression. A production design would also need to prevent disclosure through overlapping filters and exports, secure data transmission and storage, record authorized access, and apply approved retention procedures. These are requirements for the proposed operational solution, not completed prototype features.

## Relationship to existing systems and submission output

The proposed reporting layer would obtain institution-approved extracts or APIs from portal academic records and SETE. It would validate academic year, semester, class section, and program identifiers before aggregation. Source-system transactions would continue in their existing systems. The prototype demonstrates how aligned summaries could support decisions; it does not establish that the integration or the assumed Faculty Portal reporting capabilities already exist.

The screen view is deliberately scrollable. The Print dashboard control invokes a separate compact browser print layout. Print styles request one long bond page, 8.5 × 13 inches, and retain the five cards, three charts, filters, alerts, and confidentiality context. Actual pagination must be checked in print preview before submission, using the correct paper size and color settings. Browser headers and footers may need to be disabled. No final colored page or verified print artifact is claimed by this draft.

The labeled prototype and this explanation address the Part III design requirements. The final submission still needs its checked colored dashboard page and a verified shareable dashboard link; a local development URL is not a link that an instructor can access remotely. Parts IV and V and the final formatted paper remain separate work.
