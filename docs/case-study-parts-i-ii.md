# Enhancing the University Student and Faculty Portal Through Analytics and Decision Support

## Case study scope

**Course:** BAT 405 — Analytics Application  
**Institution:** Batangas State University – ARASOF Nasugbu  
**Proposed application:** Academic Insights  
**Primary dashboard user:** Program Chair  
**College and program scope:** College of Informatics and Computing Sciences (CICS), BS Information Technology (BSIT)  
**Group members:** Vince A. Mendoza and Ronel Lance Malata  
**Instructor:** Noelyn M. De Jesus  
**Section:** IT-BA-4101  
**Submission date:** November 23, 2026

This case study proposes an analytics dashboard to help a Program Chair monitor academic outcomes, the timeliness of grade submission, and student feedback on teaching. It combines selected information from the Student and Faculty Portal and the teaching evaluation system in a proposed reporting layer. Its purpose is to support academic assistance and instructional improvement through information that can be interpreted in context.

The researcher confirmed that CICS at the selected campus has only BSIT under it. This proposal therefore covers BSIT within CICS, rather than comparisons among multiple programs in the college. The dashboard can compare year levels, sections, courses, and reporting periods within that scope.

### Evidence and assumptions

The assessment draws on the supplied assignment brief, the student researcher's experience using the Student Portal, and three supplied screenshots: the Student Portal home page, the student teaching evaluation list, and an evaluation form. No interviews with university administrators, Faculty Portal inspection, database access, or actual reporting extracts have been conducted for this draft.

The student researcher has not personally encountered reporting difficulties in the Student Portal. The reporting opportunities below are therefore analytical design proposals and assumptions to validate, rather than problems reported from personal use.

The screenshots call the evaluation system **Student Evaluation of Teachers (SET)**, while the assignment uses **Student Evaluation of Teaching Effectiveness (SETE)**. This paper uses SETE to follow the assignment and describes the SET screens as the available reference. The exact institutional terminology and its relationship to the assignment's system name should be confirmed before final submission.

Faculty Portal functions and administrative reporting capabilities discussed below are explicit working assumptions. Reporting gaps are opportunities to investigate, not verified defects. An entry point from the Student Portal to teaching evaluations does not establish that their data are already integrated for analytics. All dashboard data will be simulated and labeled accordingly; no numerical example represents actual university, student, or faculty performance.

## Part I Existing System Assessment

### 1 Primary functions of the Student and Faculty Portal

The Student Portal provides students with access to their academic records and university services. The supplied home-page screenshot shows links for a Certificate of Registration, Student ID, subjects, grades, all grades, curriculum, assessment of fees, payments, scholarships, liabilities, and subjects to complete. It also displays enrollment information for a selected academic year and semester. These functions support students in checking their registration, academic progress, and financial obligations.

The screenshot also shows notices and service entry points, including the collegiate calendar, downloads, student support and feedback, e-counseling, teaching evaluations, registration, and student record updates. A visible link establishes the availability of an entry point; the complete behavior of every linked service has not been verified. The portal therefore provides evidence of student-facing transactions and access to information, but its home page alone does not establish the capabilities of administrative reports.

For this proposal, the Faculty Portal is assumed to allow faculty members to view teaching assignments and class lists and submit course grades. It is further assumed that authorized administrators can obtain enrollment summaries and grade-submission status reports. These functions would provide useful inputs for academic monitoring, but the available fields, export options, submission timestamps, and reporting permissions require confirmation. The proposal does not claim that these capabilities were personally observed.

### 2 Contribution of SETE to teaching performance evaluation

The supplied evaluation list presents assigned subjects and instructors, an evaluation period, an evaluation completion count, and an Evaluate button. The form contains fifteen statements with five selectable stars per statement, a total score out of 75, and an optional comments field. The numerical star choices are visible, but official verbal rating labels and performance interpretation bands are not established by the screenshots.

The visible statements are organized into three dimensions:

| Evaluation dimension | Number of statements | Areas represented in the supplied form |
| --- | ---: | --- |
| Management of Teaching and Learning | 6 | Punctuality, expectations, learning time, learning activities, independent learning, and constructive feedback |
| Content Knowledge, Pedagogy and Technology | 5 | Subject knowledge, clarity, relevance, learning resources, and assessment alignment |
| Commitment and Transparency | 4 | Learner differences, consultation support, feedback, and transparent assessment criteria |

SETE can provide structured information about students' perceptions of teaching practices and areas where support may be helpful. For example, a recurring concern about the timeliness of feedback may justify discussing assessment turnaround with the faculty member. Dimension-level summaries can make such patterns easier to examine than a single overall rating.

These responses represent students' reported experiences. They do not, by themselves, establish the cause of a learning outcome or provide a complete judgment of teaching effectiveness. Their interpretation should account for participation, class context, the evaluation instrument, and other evidence.

### 3 Potential data collected from the systems

The following data categories could support the proposal. The availability of a category does not imply that the researchers have access to its records.

| Data category | Potential source | Proposed analytical use | Evidence status |
| --- | --- | --- | --- |
| Student program, year level, and enrollment status | Student Portal or registration records | Define the program population and compare year levels | Enrollment and academic information are visible; export fields require confirmation |
| Academic year, semester, subject, and class section | Student and Faculty Portal | Group academic results and match the correct reporting period | Period and subject information are visible; shared identifiers require confirmation |
| Final course grade and grade status | Portal academic records | Calculate course pass rate and identify students with failed courses | Grade links are visible; grading rules and extracts require confirmation |
| Faculty teaching assignment and class roster | Faculty Portal | Identify sections and the eligible evaluation population | Assumed Faculty Portal capability |
| Grade-submission timestamp and applicable deadline | Faculty Portal and academic administration | Measure submission timeliness | Assumed data availability |
| Evaluation eligibility and completion status | SETE | Calculate participation using eligible student–course evaluation assignments | Evaluation assignments and completion counts are visible; administrative extracts require confirmation |
| Item scores and evaluation dimensions | SETE | Summarize student feedback overall and by dimension | Rating controls, statements, and dimensions are visible; stored values require confirmation |
| Optional evaluation comments | SETE | Support confidential qualitative review of recurring concerns | Comment field is visible; access and handling procedures require confirmation |

The proposed integration would match program, subject, section, faculty assignment, and reporting period using validated identifiers. Student identity should not be attached to evaluation response content in the analytical output. Participation checking and anonymized response analysis would need separate handling under institution-approved procedures.

### 4 Reporting limitations and opportunities for improvement

The available Student Portal screenshot focuses on individual records and service access. It does not show a Program Chair dashboard. Similarly, the supplied SETE screens show how a student evaluates assigned instructors, rather than how an administrator analyzes results. These observations support proposing an administrative analytics view; they do not prove that equivalent reporting is absent elsewhere.

Four opportunities should be investigated before implementation:

1. **Consolidating information.** If portal records and SETE reports are reviewed separately, the Program Chair may need to reconcile periods and class assignments manually. A proposed reporting layer could present aligned summaries without replacing either source system.
2. **Comparing periods and groups.** If existing reports provide limited historical comparisons, semester trends and year-level breakdowns could help the chair decide where to investigate academic concerns. Comparisons would need consistent definitions and an unchanged or mapped evaluation instrument.
3. **Showing evidence behind ratings.** A mean SETE score becomes more useful when displayed with completed and eligible evaluation counts. Participation and dimension-level results could help the chair distinguish a possible teaching improvement opportunity from weak or incomplete evidence.
4. **Making follow-up visible.** Proposed threshold alerts could direct attention to low participation, delayed grade submission, or elevated academic difficulty. Each alert should identify the relevant period, denominator, and suggested review action rather than issue an automatic judgment.

Before data integration, the university would need to validate whether submission timestamps, historical reports, consistent identifiers, and approved exports already exist. Incomplete grades, duplicate records, withdrawn enrollments, and late data updates must be handled explicitly to prevent misleading summaries.

### 5 Stakeholders and decisions

| Stakeholder | Decisions supported by the proposed information |
| --- | --- |
| Program Chair, the primary dashboard user | Prioritize academic support, follow up grade-submission delays, review evaluation participation, and discuss faculty development needs |
| Dean and authorized academic administrators | Assess program-level patterns and allocate resources for advising and instructional support |
| Faculty members | Review feedback for their own classes and improve learning activities, assessment practices, and feedback delivery |
| Registrar or authorized records personnel | Validate enrollment and grade records and resolve submission or completeness issues |
| Authorized quality assurance or evaluation personnel | Check evaluation coverage, instrument consistency, and responsible interpretation of results |
| Students | Receive appropriately targeted academic support and contribute feedback; this does not imply access to confidential faculty or other students' records |
| ICT and system administrators | Maintain approved data access, integration reliability, and technical controls without assuming unrestricted access to evaluation content |

Access should follow responsibility. A Program Chair's proposed access should be limited to the program they oversee. Broader access for other roles would require separate authorization rather than a freely selectable dashboard role.

## Part II KPI Identification and Design

### 1 Measurement scope and common rules

The proposal uses five KPIs covering academic operations and teaching feedback. All targets and thresholds below are initial design proposals for the case study, not official Batangas State University standards. They require consultation with authorized university personnel and comparison with an approved historical baseline before operational use.

Each KPI must display its academic year, semester, program scope, and reporting cutoff. A zero denominator produces **Not available**, not zero performance. Records with missing values must not be silently treated as passing, failing, submitted on time, or completed. Where the denominator excludes incomplete records, the dashboard should show the excluded count or a completeness notice.

For academic outcomes, the reporting period should use finalized grades as of a stated cutoff. A current semester with incomplete grades should be labeled provisional. An apparent improvement caused by unsubmitted grades must not be interpreted as a real improvement.

### 2 Proposed KPI matrix

| KPI | Objective | Formula | Proposed target | Management action |
| --- | --- | --- | --- | --- |
| 1 Course pass rate | Monitor successful course completion | Passed student–course enrollments ÷ student–course enrollments with finalized pass/fail outcomes × 100 | At least 90% | Review lower-performing courses and year levels, check record completeness, and arrange suitable academic support |
| 2 On-time grade submission rate | Support timely availability of academic results | Class sections with complete final grades submitted by their applicable deadline ÷ class sections whose final-grade deadline has passed × 100 | At least 95% | Follow up outstanding sections, verify deadline exceptions, and address submission or workflow problems |
| 3 SETE response rate | Assess evaluation coverage | Completed valid evaluations ÷ eligible student–course evaluation assignments × 100 | At least 70% | Check eligibility records and access issues and send approved general participation reminders without pressuring students to give favorable ratings |
| 4 Mean SETE rating | Summarize students' reported teaching experiences | Sum of valid item scores in completed evaluations ÷ number of valid item scores in those evaluations | At least 4.00 out of 5 | Review dimension results, participation, and supporting evidence with the faculty member before considering development support |
| 5 Academic difficulty rate | Monitor the share of students with at least one failed course | Distinct students with at least one finalized failed course ÷ distinct students with at least one finalized pass/fail course outcome × 100 | At most 10% | Validate the records, offer confidential advising or learning support, and examine recurring course-level concerns |

### 3 Relevance and calculation details

**KPI 1 Course pass rate.** This indicator supports the proposed academic monitoring objective by showing the proportion of finalized course outcomes that are passes. Its unit is a student–course enrollment: a student taking several courses contributes several outcomes. Pass or fail status must use the university's verified grading rules. Withdrawn, incomplete, pending, and other non-final statuses are excluded from this denominator and reported separately. A pass rate should prompt investigation of student support needs; it should not encourage changing grading standards to reach a target.

**KPI 2 On-time grade submission rate.** Timely submission supports students' access to results and administrators' ability to review academic progress. A section counts as on time only when its complete required final-grade submission is recorded by its approved deadline. A partial submission does not qualify. Approved deadline extensions must be reflected in the applicable deadline, while sections not yet due are excluded. A record of later submission remains late for this KPI. If reliable submission history and timestamps are unavailable, the indicator must remain unavailable until those inputs can be verified.

**KPI 3 SETE response rate.** This indicator supports responsible use of teaching feedback by making evaluation coverage visible. Its denominator counts eligible student–course evaluation assignments, not unique students: one student may be eligible to evaluate several classes. Eligibility should use a documented evaluation-period roster and withdrawal policy. Only one valid completed response per eligible assignment is counted. Drafts, abandoned evaluations, and duplicate submissions are excluded. The rate is provisional while the evaluation window remains open and final only after the approved closing cutoff.

**KPI 4 Mean SETE rating.** This indicator summarizes reported teaching experiences while dimension-level views retain information about specific practices. The prototype proposes numerical scores from 1 to 5, consistent with the visible five-star controls, subject to confirmation of the official stored scale. It uses completed evaluations with all fifteen required items answered. Incomplete evaluation records are excluded and counted separately. The overall mean is computed from item-score totals and item counts, not an unweighted average of class or faculty means. Because the dimensions contain six, five, and four items, this method gives each item equal weight; it does not give each dimension equal weight. Dimension summaries should also be shown, and comparisons require a consistent instrument. Any official weighting scheme, if later provided, must replace this provisional calculation consistently.

**KPI 5 Academic difficulty rate.** This indicator supports student assistance by showing how many students have at least one finalized failed course. Each student appears once in the numerator and denominator, regardless of the number of courses taken. Students with no finalized pass/fail outcomes are excluded and reported separately. A student with both finalized and pending outcomes is included using the available finalized outcomes, so the result remains provisional until grade coverage is complete. This is a retrospective measure of recorded academic difficulty, not a prediction of future failure and not a label of a student's ability. It complements course pass rate because failures may be concentrated among a smaller group or distributed across many students.

### 4 Warning thresholds and management response

The dashboard should compare unrounded values with the thresholds, then round the displayed numbers. Equality with a target meets that target. A warning is a request for human review, not an automatic sanction.

| Warning condition | Meaning for the proposed dashboard | Suggested response |
| --- | --- | --- |
| Course pass rate below 90% | Finalized course outcomes fall below the proposed benchmark | Check missing grades and course context; discuss appropriate tutoring or academic support |
| On-time grade submission below 95% | Submission timeliness falls below the proposed benchmark | Identify overdue sections and verify approved exceptions before follow-up |
| SETE response rate below 70% | Evaluation coverage is below the proposed benchmark | Display a low-participation notice; investigate access and eligibility issues and interpret ratings cautiously |
| Mean SETE rating below 4.00 out of 5 | Reported experiences may warrant closer review | Examine dimension scores, response counts, context, and other evidence with the faculty member |
| Academic difficulty rate above 10% | More students have failed courses than the proposed benchmark allows | Validate student-level counts and offer confidential assistance |

For an open evaluation window, a low-participation message should say **Participation in progress**, rather than imply that a final deadline was missed. Likewise, unfinished academic records should display a provisional-data notice. A KPI with no valid denominator must show unavailable data and must not produce a performance warning.

At faculty or class level, the design proposes suppressing rating details when there are fewer than five completed evaluations. This is a preliminary small-group protection rule, not an institutional policy or a guarantee of anonymity. The university must approve an appropriate minimum, assess whether overlapping filters or exports could reveal small groups, and apply the rule consistently. A suppressed result must not be treated as a low rating. Even where the minimum is met, a low response rate must remain visible.

### 5 Responsible interpretation of SETE results

SETE should inform professional discussion and instructional improvement alongside other available evidence. It should not serve as the sole measure of teaching effectiveness or automatically determine promotion, discipline, teaching assignments, or other personnel decisions.

The Program Chair should first examine response counts and coverage. A high average based on limited participation does not establish that the results represent the full class. Similarly, a lower average may need further investigation rather than an immediate conclusion about teaching quality. The dashboard should display completed and eligible counts beside the response rate and disclose incomplete or suppressed results.

Interpretation should also consider class size, course difficulty, teaching modality, assessment demands, student expectations, and changes to the evaluation instrument. Responses may reflect selection effects or non-teaching factors; students who respond may have different experiences from those who do not. Differences between faculty members or semesters should therefore not be treated as precise rankings without checking comparability and uncertainty.

Dimension-level patterns and confidential review of relevant comments can guide a constructive conversation. The chair should compare these patterns with other authorized evidence, such as peer observation, course materials, assessment alignment, and the faculty member's explanation. Academic outcomes can provide context, but an association between grades and ratings does not prove that one caused the other.

Evaluation content should be accessible only to authorized recipients. Public dashboards and the case-study prototype should contain no real student identities, faculty ratings, identifiable comments, or individual response records. In a future operational system, authentication, server-side authorization, secure storage, access logging, and approved retention procedures would be required. A visual role label or filter alone does not enforce confidentiality.

### 6 Illustrative calculations for dashboard design

The following values are an internally consistent simulated reporting scenario for a single program and semester. They are not findings about Batangas State University and are not a historical baseline. In this example, all 420 students have finalized outcomes for five courses each, the relevant grade deadlines have passed, and the evaluation window is closed.

| KPI | Simulated inputs | Calculated result | Proposed status |
| --- | --- | --- | --- |
| Course pass rate | 1,848 passed enrollments out of 2,100 finalized outcomes | 88.00% | Review below-target pass rate |
| On-time grade submission rate | 36 on-time sections out of 40 sections due | 90.00% | Follow up submission timeliness |
| SETE response rate | 1,260 completed evaluations out of 2,100 eligible assignments | 60.00% | Low participation; interpret ratings cautiously |
| Mean SETE rating | 79,380 total item-score points across 18,900 valid item responses | 4.20 out of 5 | Meets proposed rating target, with low-participation caution |
| Academic difficulty rate | 63 distinct students with at least one failed course out of 420 students | 15.00% | Review need for academic support |

The 1,260 completed evaluations each contain fifteen valid item responses, giving 18,900 responses in total. The course outcomes include 252 failed enrollments, distributed among the 63 students with at least one failed course. Of the 40 sections due, the four not submitted on time may have been submitted later; a finalized reporting dataset can therefore contain all grades while still recording a submission-timeliness concern.

The example illustrates why indicators must be read together. A mean rating above its proposed target does not remove the concern created by a 60% evaluation response rate. Similarly, a course pass rate and a student-level difficulty rate answer different questions and should retain their separate denominators.

## Sources and items to confirm

This draft uses the supplied **BAT 405 Case Study.docx** assignment brief and the three user-supplied screenshots described under Evidence and assumptions. Faculty Portal features, proposed data integration, KPI targets, warning rules, and the numerical scenario are assumptions or design proposals. No official university performance targets or administrative reporting specifications were supplied.

The researcher has confirmed the college and program scope, author name, instructor, section, and submission date recorded above. Items still requiring institutional confirmation include official evaluation terminology and rating scale, grading rules, grade-submission deadlines, and any permitted information about existing administrative reports. Any observation added later should be attributed to its actual source rather than presented as a verified system-wide fact.

## Assignment requirements and remaining work

The supplied activity is a two-student case study analysis and system design task worth 100 points. Programming is not required. The current draft covers Parts I and II; it is not yet the complete submission.

| Assignment component | Required content | Current status |
| --- | --- | --- |
| Part I Existing System Assessment, 15 points | System functions, SETE contribution, at least five data types, reporting opportunities, and stakeholder decisions | Drafted above |
| Part II KPI Identification and Design, 25 points | Five KPIs with objective, formula, target, and management action; relevance; at least two warning thresholds; responsible interpretation of SETE | Drafted above |
| Part III Analytics Dashboard and Decision-Support Design, 25 points | One-page labeled dashboard for a selected primary user, five KPI cards, three visualizations, two interactive features, at least one alert, and component explanations addressing confidentiality | Prototype implemented; explanation drafted in case-study-part-iii.md; browser, print, and submission-link verification remain pending |
| Part IV Analytics Model Selection and Application, 25 points | One analytical problem and intended decision, analytics category, technique, at least four input variables, expected output, seven workflow steps, and two justified evaluation metrics; bias discussion if SETE is used predictively | Pending |
| Part V System Evaluation and Recommendations, 10 points | Three types of testing, privacy and fairness concerns, appropriate SETE interpretation, and two specific improvement recommendations | Pending |

The final package must include a cover page with the application logo, application name, and group members' names; the paper on long bond paper; one colored dashboard page; and a dashboard link. The assignment lists November 9–15 for the analytics dashboard, November 16–22 for evaluation and documentation, and November 23 for submission of the printed document and dashboard link. The researcher confirmed the submission year as 2026. A shareable dashboard link still needs to be prepared and checked before submission.
