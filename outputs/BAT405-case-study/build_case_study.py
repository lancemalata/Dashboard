from pathlib import Path
import json, textwrap
from PIL import Image, ImageDraw, ImageFont
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION_START, WD_ORIENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

OUT=Path(__file__).parent
ROOT=OUT.parent.parent
URL='https://academic-insight-bat405-vince.formalpuffin8.chatgpt.site'
W=json.loads((ROOT/'sites/academic-insight/src/data/workbook.json').read_text(encoding='utf-8-sig'))
FONT='C:/Windows/Fonts/arial.ttf'
BOLD='C:/Windows/Fonts/arialbd.ttf'
def font(n,b=False): return ImageFont.truetype(BOLD if b else FONT,n)
im=Image.new('RGB',(2100,1240),'#f3f5f8'); draw=ImageDraw.Draw(im)
def text(x,y,s,n=22,c='#303747',b=False): draw.text((x,y),s,font=font(n,b),fill=c)
def box(x,y,w,h,fill='#ffffff'): draw.rounded_rectangle((x,y,x+w,y+h),radius=16,fill=fill,outline='#dfe3eb',width=2)
text(55,25,'Academic Insight',40,'#891c32',True)
text(55,80,'PROGRAM CHAIR  /  BSIT  /  CICS  /  ARASOF NASUGBU',20)
text(1570,38,'SYNTHETIC DATA',23,'#891c32',True)
box(45,130,2010,80)
text(70,151,'A   Academic year: 2025-2026     |     Semester: Second     |     All year levels',24,b=True)
text(1680,155,'Export CSV   /   Print',21)
labels=['Enrollment achievement','Course pass rate','Academic risk rate','Mean teaching evaluation','Evaluation participation']
values=['96.0%','88.0%','9.0%','4.20 / 5','80.0%']
targets=['Target >= 95%','Target >= 90%','Target <= 10%','Target >= 4.00 / 5','Target >= 70%']
for i in range(5):
    x=45+i*405;box(x,235,390,185)
    text(x+18,252,f'B{i+1}  {labels[i]}',19,b=True)
    text(x+18,290,values[i],48,'#891c32',True)
    text(x+18,365,targets[i],20)
for x in [45,725,1405]:box(x,448,650,475)
text(65,465,'C   Teaching feedback over time',25,b=True)
text(65,505,'Mean rating / 5  |  Hover or select a point',19)
for val in range(1,6):
    yy=825-(val-1)*64;draw.line((115,yy,650,yy),fill='#e5e8ed',width=2);text(80,yy-12,str(val),18)
pts=[(155+i*150,825-(v-1)*64) for i,v in enumerate([3.9,4,4.1,4.2])]
draw.line(pts,fill='#922b42',width=5)
for i,((x,y),v) in enumerate(zip(pts,[3.9,4,4.1,4.2])):
    draw.ellipse((x-7,y-7,x+7,y+7),fill='#922b42');text(x-25,y-34,f'{v:.2f}',18,b=True)
    text(x-45,850,['24-25 S1','24-25 S2','25-26 S1','25-26 S2'][i],17)
text(745,465,'D   Evaluation dimensions',25,b=True)
text(745,505,'Selected term  |  1,920 completed forms',19)
for i,(label,score,n) in enumerate([('Teaching and learning management',4.1,6),('Knowledge, pedagogy and technology',4.2,5),('Commitment and transparency',4.35,4)]):
    yy=570+i*105;text(750,yy,label,20);text(1280,yy,f'{score:.2f}',22,b=True)
    draw.rounded_rectangle((750,yy+36,1335,yy+52),radius=6,fill='#eee8ed')
    draw.rounded_rectangle((750,yy+36,750+585*score/5,yy+52),radius=6,fill=['#94596b','#b07b8b','#cfabba'][i])
    draw.line((1218,yy+29,1218,yy+59),fill='#66534a',width=2)
    text(750,yy+61,f'{n} criteria per form',17)
text(1425,465,'E   Academic risk by year level',25,b=True)
text(1425,505,'Flagged / enrolled  |  Select a bar for context',19)
for tick in [0,5,10,15,20,25]:
    yy=825-tick*10;draw.line((1470,yy,2010,yy),fill='#e5e8ed',width=2);text(1425,yy-10,f'{tick}%',16)
for i,(a,b) in enumerate([(15,140),(12,125),(9,115),(7,100)]):
    rate=a/b*100;x=1510+i*130;yy=825-rate*10
    draw.rounded_rectangle((x,yy,x+58,825),radius=6,fill='#b86a39' if rate>10 else '#71968d')
    text(x-2,yy-30,f'{rate:.1f}%',19,b=True);text(x-1,850,f'Year {i+1}',18);text(x-1,880,f'{a}/{b}',17)
box(45,950,2010,170,'#fffaf2');text(65,970,'F   Priorities for review',26,b=True)
text(65,1018,'Course pass rate: 88.0% is below the proposed 90% target.',23)
text(65,1061,'Year 1: 15 of 140 students flagged (10.7%). Review advising needs above the 10% threshold.',23)
text(55,1152,'G   Aggregate sample data only. Portal-SETE analytics integration is proposed.',22)
text(55,1192,'Teaching ratings require participation, course context and other evidence. Do not use SETE alone for personnel decisions.',19)
im.save(OUT/'qa/dashboard_mockup.png')
logo=Image.new('RGB',(240,240),'white');d=ImageDraw.Draw(logo)
d.rounded_rectangle((10,10,230,230),radius=48,fill='#891c32')
d.line([(45,82),(120,47),(195,82),(120,117),(45,82)],fill='white',width=9)
for x,y in [(80,120),(120,140),(160,120)]:d.line((x,y,x,180),fill='white',width=9)
d.line((58,199,182,199),fill='white',width=9);logo.save(OUT/'qa/logo.png')

doc=Document();sec=doc.sections[0]
def setup(s,landscape=False):
    s.orientation=WD_ORIENT.LANDSCAPE if landscape else WD_ORIENT.PORTRAIT
    s.page_width=Inches(13 if landscape else 8.5);s.page_height=Inches(8.5 if landscape else 13)
    s.top_margin=Inches(.8);s.bottom_margin=Inches(.75);s.left_margin=s.right_margin=Inches(.85)
setup(sec)
normal=doc.styles['Normal'];normal.font.name='Times New Roman';normal.font.size=Pt(11)
normal.paragraph_format.line_spacing=1.08;normal.paragraph_format.space_after=Pt(6)
for name,size in [('Title',23),('Heading 1',16),('Heading 2',12)]:
    st=doc.styles[name];st.font.name='Times New Roman';st.font.size=Pt(size);st.font.color.rgb=RGBColor(0,0,0)
    st.paragraph_format.space_before=Pt(9);st.paragraph_format.space_after=Pt(5)
doc.core_properties.author='Vince A. Mendoza and Ronel Lance Malata'
doc.core_properties.title='Academic Insight Case Study'
def p(t,style=None):
    after_table=doc.element.body[-2].tag==qn('w:tbl') if len(doc.element.body)>1 else False
    par=doc.add_paragraph(t,style)
    if after_table:par.paragraph_format.space_before=Pt(6)
    return par
def h(t):doc.add_heading(t,2)
def page(title):
    heading=doc.add_heading(title,1);heading.paragraph_format.page_break_before=True
def table(headers,rows,widths):
    t=doc.add_table(rows=1,cols=len(headers));t.autofit=False
    for c,w in zip(t.columns,widths):c.width=Inches(w)
    for i,s in enumerate(headers):t.rows[0].cells[i].text=s
    for row in rows:
        for c,s in zip(t.add_row().cells,row):c.text=str(s)
    for ri,row in enumerate(t.rows):
        for i,c in enumerate(row.cells):
            c.width=Inches(widths[i]);c.vertical_alignment=1
            tcPr=c._tc.get_or_add_tcPr();b=OxmlElement('w:tcBorders')
            for side in ['top','left','bottom','right']:
                e=OxmlElement('w:'+side);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4');e.set(qn('w:color'),'D9D9D9');b.append(e)
            tcPr.append(b);shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'E8EDF2' if ri==0 else ('F5F7F9' if ri%2==0 else 'FFFFFF'));tcPr.append(shade)
            margins=OxmlElement('w:tcMar')
            for side in ['top','left','bottom','right']:
                e=OxmlElement('w:'+side);e.set(qn('w:w'),'90');e.set(qn('w:type'),'dxa');margins.append(e)
            tcPr.append(margins)
            for par in c.paragraphs:
                par.paragraph_format.space_after=Pt(3);par.paragraph_format.line_spacing=1.05
                for r in par.runs:r.font.size=Pt(10);r.bold=ri==0
        cant=OxmlElement('w:cantSplit');row._tr.get_or_add_trPr().append(cant)
    repeat=OxmlElement('w:tblHeader');t.rows[0]._tr.get_or_add_trPr().append(repeat)
    return t
def link(label,url):
    par=doc.add_paragraph();r=par.add_run(label+' ')
    rel=par.part.relate_to(url,'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink',is_external=True)
    el=OxmlElement('w:hyperlink');el.set(qn('r:id'),rel);run=OxmlElement('w:r');tx=OxmlElement('w:t');tx.text=url;run.append(tx);el.append(run);par._p.append(el)

# Cover
for s in ['Batangas State University','The National Engineering University','ARASOF Nasugbu Campus','College of Informatics and Computing Sciences']:
    a=p(s);a.alignment=1
p('')
a=p('');a.alignment=1;a.add_run().add_picture(str(OUT/'qa/logo.png'),width=Inches(1))
a=p('Academic Insight','Title');a.alignment=1
a=p('Enhancing the University Student and Faculty Portal\nThrough Analytics and Decision Support');a.alignment=1;a.runs[0].bold=True;a.runs[0].font.size=Pt(15)
a=p('Integrated Case Study\nBAT 405 Analytics Application');a.alignment=1
p('')
for s in ['Submitted by','Vince A. Mendoza','Ronel Lance Malata','BS Information Technology','Business Analytics','IT-BA-4101','','Submitted to','Noelyn M. De Jesus','','November 23, 2026']:
    a=p(s);a.alignment=1

page('Part I Existing System Assessment')
p('We propose Academic Insight as a one-page dashboard for the BSIT Program Chair. It brings academic outcomes and student teaching feedback into one reporting view so that the chair can identify concerns and decide what needs follow-up. Our proposal focuses on academic support and teaching improvement within CICS at the ARASOF Nasugbu Campus.')
h('Current portal functions')
p('The Student Portal screenshot shows enrollment status, academic year and semester, subjects, grades, curriculum, a Certificate of Registration, fee assessment, payments and student services. Students can use these entry points to check academic records and complete university transactions. The screenshot shows navigation to these functions; it does not show every process behind them.')
p('The Faculty Portal is included in the case scenario, but we did not inspect a faculty account. For our proposed design, teaching assignments, class lists and submitted grades would be possible faculty-side inputs. Their exact fields, reporting permissions and export options would need to be confirmed with the university.')
h('How teaching evaluations contribute')
p('The screenshots call the system Student Evaluation of Teachers or SET, while the assignment uses Student Evaluation of Teaching Effectiveness or SETE. We use SETE in the discussion to follow the assignment. The observed form has 15 items with five selectable stars per item, a maximum total of 75 points, and an optional comments field. It covers teaching and learning management (6 items), content knowledge, pedagogy and technology (5), and commitment and transparency (4). The visible form does not establish official verbal labels for each star value.')
p('These responses can show how students experience instruction, feedback and assessment. They can help identify topics for discussion or faculty development. They should be read with participation and course context because student ratings do not capture every part of teaching effectiveness.')
h('Data available or needed for the proposal')
table(['Data type','Use in the proposed solution'],[
('Enrollment counts and program or year level','Monitor enrollment against planned intake and compare cohorts.'),
('Academic year and semester','Align source records and compare reporting periods.'),
('Course registrations and grade outcomes','Calculate passing rates using graded course registrations.'),
('Teaching assignments and faculty identifiers','Match eligible course evaluations; verify availability and restrict access.'),
('Evaluation eligibility and completion counts','Calculate participation without confusing assignments with unique students.'),
('Item scores and evaluation dimensions','Calculate weighted teaching feedback summaries.'),
('Academic support flags','Identify advising needs after agreeing on a documented flagging rule.')],[2.15,4.65])
h('Reporting opportunities and stakeholders')
p('The screenshots do not establish whether administrators already have trend reports, cohort alerts or combined academic and evaluation summaries. We therefore treat these as opportunities to validate, rather than confirmed defects. A portal link to SETE does not prove that the systems are already integrated for analytics. Our reporting layer is a proposed enhancement.')
p('The Program Chair would use the dashboard to plan advising, course review and faculty support. The dean and authorized administrators could use approved summaries for resource allocation. Faculty could use appropriately scoped feedback for instructional improvement. Students would benefit through support services and clearer follow-up, without receiving access to other students’ records or confidential faculty results.')

page('Part II KPI Identification and Design')
p('We selected five KPIs that cover academic operations and teaching feedback. All targets below are proposed case-study benchmarks. They are not presented as official Batangas State University standards. Each measure uses the selected semester, and missing or zero denominators are shown as unavailable rather than as a zero performance score.')
table(['KPI','Formula','Proposed target'],[
('Enrollment achievement','Enrolled students / target enrollment × 100','At least 95%'),
('Course pass rate','Passed registrations / graded registrations × 100','At least 90%'),
('Academic risk rate','Flagged students / enrolled students × 100','At most 10%'),
('Mean teaching evaluation','Total rating points / total scored criteria','At least 4.00 / 5'),
('Evaluation participation','Completed evaluations / eligible assignments × 100','At least 70%')],[1.85,3.65,1.3])
h('1 Enrollment achievement')
p('Objective and relevance: compare actual enrollment with the program’s planned intake. This helps the chair review whether expected enrollment and available sections are reasonably aligned. Management action: check intake and retention patterns before changing recruitment plans or section capacity. A result above 100% would mean enrollment exceeded the planning target; it would not automatically mean that capacity is adequate.')
h('2 Course pass rate')
p('Objective and relevance: monitor the share of graded course registrations with passing outcomes. A decrease can prompt a closer review of courses and learning support. Management action: identify the courses contributing to the result, examine assessment and course context, and arrange tutoring or curriculum review where appropriate. This KPI counts course registrations, not distinct students.')
h('3 Academic risk rate')
p('Objective and relevance: show the share of enrolled students already flagged for possible academic support. Management action: validate the flags and arrange confidential advising. The workbook contains synthetic risk counts but does not define how students were flagged. We therefore do not describe these counts as failed-course totals or model predictions. A real implementation must document the criteria, reporting date and responsible reviewer before using the indicator.')
h('4 Mean teaching evaluation')
p('Objective and relevance: summarize student perceptions across the 15 evaluation criteria. Management action: examine the dimension results with participation, course context and other teaching evidence. The overall score uses total points divided by scored criteria. Since the dimensions contain 6, 5 and 4 items, simply averaging their three means would give the dimensions equal weight and would not match our equal-item scoring assumption.')
h('5 Evaluation participation')
p('Objective and relevance: show the coverage of eligible teaching evaluation assignments. Management action: check access and eligibility issues and, during an open evaluation period, use neutral reminders. One student can evaluate several courses, so completed assignments must not be reported as the number of individual students who responded. A high response rate also does not prove that responses are free of bias.')

page('KPI Calculations and Interpretation')
h('Sample results for the latest workbook term')
p('The sample workbook covers four semesters from AY 2024–2025 to AY 2025–2026. The dashboard defaults to the second semester of AY 2025–2026. These historical sample periods are separate from the AY 2026–2027 evaluation window shown in the screenshots. All figures in the following table are synthetic.')
table(['KPI','Selected term calculation','Result','Target status'],[
('Enrollment achievement','480 / 500 × 100','96.0%','Within target'),
('Course pass rate','2,112 / 2,400 × 100','88.0%','Review'),
('Academic risk rate','43 / 480 × 100','8.9583%','Within target'),
('Mean teaching evaluation','120,960 / 28,800','4.20 / 5','Within target'),
('Evaluation participation','1,920 / 2,400 × 100','80.0%','Within target')],[1.8,2.5,1.2,1.3])
p('The dashboard rounds the risk rate to 9.0%, but its warning logic uses the unrounded value. The 28,800 scored criteria equal 1,920 completed forms multiplied by 15 items. We do not add completed form counts across the three dimensions because the same evaluation form contains all three.')
h('Warning thresholds and management intervention')
p('Our first warning is a course pass rate below 90%. The latest sample is 88%, so the chair should review course-level results and identify where learning support may be useful. The dashboard does not establish the cause of the lower rate; that requires further review.')
p('Our second warning is a year-level academic risk rate above 10%. In the latest sample, Year 1 has 15 flagged students out of 140 enrolled, or 10.7%. This triggers an advising review even though the overall program rate is below 10%. Looking only at the program average would hide this cohort concern. A rate equal to 10% meets the proposed threshold.')
p('Other card warnings appear when enrollment achievement falls below 95%, participation falls below 70%, or the mean rating falls below 4.00. These are prompts for verification and discussion. The dashboard does not automatically impose an intervention or make a personnel decision.')
h('Responsible interpretation of SETE')
p('We would check participation, valid response counts, the evaluation criteria and differences in course context before interpreting a score. A result based on limited feedback should not be treated as equally representative of the full class. Nonresponse, course difficulty and students’ expectations may affect the feedback, so a rating change should lead to questions rather than an immediate conclusion about a faculty member.')
p('The dimension view gives a more useful starting point than a single overall score. In the latest sample, management of teaching and learning is 4.10, knowledge, pedagogy and technology is 4.20, and commitment and transparency is 4.35. All meet our proposed 4.00 benchmark. The relatively lower management score could still be discussed as a development opportunity, but it does not establish poor teaching.')
p('SETE should be considered alongside classroom observation, assessment design, course materials and other appropriate evidence. We would avoid public faculty rankings and prevent small groups or evaluation comments from identifying student respondents. Evaluation results should not automatically determine promotion, discipline or other personnel outcomes.')

page('Part III Dashboard and Decision Support Design')
h('Primary user and reporting scope')
p('Our primary user is the BSIT Program Chair. The dashboard keeps the selected reporting period, five KPI values and review priorities visible in a single overview. Enrollment and academic outcomes appear with teaching feedback so the chair can decide whether to examine course support, advising needs or instructional practices. The following page provides a labeled mockup of that layout.')
h('Dashboard components')
p('A. Reporting controls identify the academic year and semester. Changing either updates the five KPI cards, selected-term charts, warnings and CSV export. BSIT and CICS are fixed scope labels because the supplied workbook has no other college, department or program records. A broader version could add authorized college and department filters after those fields are available.')
p('B1 to B5. The five cards show the selected-term value, proposed target, target status and change from the preceding sample semester. Selecting a card opens its objective, formula, calculation inputs and suggested management action. Rate comparisons use percentage points; teaching score comparisons use points on the five-point scale.')
p('C. A line chart presents mean teaching evaluation across all four sample semesters. A line makes changes over time easy to follow without treating the semesters as unrelated categories. Hovering or focusing a point shows the rating and participation. Selecting a point changes the reporting term. The full history remains visible for comparison even when a different academic year is selected.')
p('D. Horizontal bars compare the three teaching evaluation dimensions in the selected term. The bars share a 0–5 axis and a proposed 4.00 target marker. Hover details provide the score, completed forms and scored criteria. The instrument’s response values are five-point ratings; the zero baseline is a chart display choice, not an additional response option.')
p('E. A column chart compares academic risk rates across year levels. Each label also identifies the flagged and enrolled counts. This lets the chair compare differently sized cohorts without mistaking a larger count for a higher rate. Selecting a bar opens the advising context.')
p('F. The review section names threshold breaches and gives a suggested next action. The latest sample flags the 88% pass rate and Year 1’s 10.7% risk rate. G. A short footer identifies the synthetic data and proposed integration and reminds users to interpret teaching feedback responsibly.')
h('Interactive features and confidentiality')
p('The two main interactive features are coordinated period filtering and detail-on-demand through cards and charts. Hover tooltips and keyboard focus provide quick context. CSV export supports further review, while print styles provide a long-bond output. The accompanying mockup is a labeled design view, not a screenshot of a verified browser session.')
p('The prototype uses aggregate synthetic data and contains no real student identities or faculty evaluation responses. Production access would require authentication and server-enforced permissions for the chair’s program. Faculty detail and comments would need tighter restrictions, minimum response-count rules and an access log. A filter in the browser is not a security control.')
link('Dashboard link:',URL)
p('The hosted prototype currently has owner-only access. Access for the instructor must be arranged before submitting the link. Automated calculation and render checks, lint and the production build passed; browser interaction, responsive appearance and print pagination remain to be verified.')

land=doc.add_section(WD_SECTION_START.NEW_PAGE);setup(land,True)
doc.add_heading('Labeled Dashboard Mockup',1)
p('Academic Insight for the Program Chair   |   Second semester AY 2025–2026   |   Synthetic data')
pic=doc.add_paragraph();pic.alignment=1;pic.add_run().add_picture(str(OUT/'qa/dashboard_mockup.png'),width=Inches(9.25))
p('Figure 1. One-page design showing filters (A), five KPI cards (B1–B5), three visualizations (C–E), review alerts (F) and interpretation notes (G). Values match the supplied workbook. This mockup is suitable for the colored dashboard page.')
portrait=doc.add_section(WD_SECTION_START.NEW_PAGE);setup(portrait)
doc.add_heading('Part IV Analytics Model Selection and Application',1)
h('Problem and intended decision')
p('We chose early identification of academic difficulty because it gives the Program Chair a clear support decision: which students may need advising before the next semester’s outcomes are finalized. The current dashboard shows recorded synthetic flags by year level. It cannot tell us which individual student is likely to struggle in a future term.')
p('For a future model, we propose defining the outcome as at least one finalized failed course in the next regular semester. This is a proposed modeling definition, not the undefined risk rule in the supplied workbook. The university would need to approve how incomplete, withdrawn and ungraded registrations are handled. Students with no observable next-term outcome should not automatically be labeled as having no difficulty.')
h('Analytics approach and technique')
p('The approach is predictive analytics, using a regularized logistic regression classifier. It would estimate a probability for the agreed next-term outcome using information available before that term begins. Logistic regression is an established classification method; the scikit-learn documentation describes its regularized implementation (scikit-learn, n.d.-a). We prefer a simple baseline that can be checked and explained before considering a more complex model.')
p('The output would be a probability from 0 to 1 and an advising-review flag based on a threshold chosen with academic staff. The threshold would reflect validation results and available advising capacity. It would not be a passing-grade cutoff, a diagnosis or an automatic decision about enrollment.')
h('Proposed input variables')
table(['Input available before prediction','Meaning and preparation'],[
('Prior-term grade average','Use the verified institutional grade scale and state whether lower or higher values indicate better performance.'),
('Prior failed-course count','Count finalized failed courses from the preceding term; exclude unresolved results using the agreed policy.'),
('Prior completion ratio','Completed units / attempted units, with a consistent definition of completion and withdrawal.'),
('Prior attendance rate','Attended sessions / scheduled sessions, only where attendance is reliable and authorized for this use.')],[2.3,4.5])
p('The attendance variable is a proposed additional input. Its availability is not established by the portal screenshots. None of these individual predictors or future outcome labels is available in the aggregate sample workbook. They would have to be obtained from appropriately authorized records; we would not infer them from the semester totals.')
h('Feasibility and limits')
p('Four aggregate semesters are enough to demonstrate a dashboard, but not to train and validate this student-level classifier. We have not fitted a model or measured predictive accuracy. The dashboard’s 43 flagged students are sample source counts, not model-generated predictions. The model remains a design proposal for this case study.')
p('SETE is not a predictor in our proposed student-risk model. This avoids using faculty feedback as a shortcut for individual student performance. If it were used in another model, nonresponse, course context and possible evaluation bias would need separate analysis, and predictions must never automatically determine faculty personnel outcomes.')

page('Analytics Modeling Workflow and Evaluation')
h('Seven major steps')
steps=[
('1 Define the problem and decision','Agree on the next-term outcome, prediction date and advising process. Decide who reviews the flags and what support can be offered.'),
('2 Collect and authorize the data','Obtain de-identified student records across several terms, with approved access and a stable identifier for longitudinal matching. Record the source and reporting date of each field.'),
('3 Check data quality and labels','Review missing grades, duplicate registrations, inconsistent attendance and changing course codes. Apply the agreed outcome definition and retain clear reasons for exclusions.'),
('4 Explore and prepare the inputs','Examine outcome prevalence and cohort coverage. Separate earlier training terms from later validation and test terms. Fit preprocessing only on training data, and keep information recorded after the prediction date out of the inputs.'),
('5 Train a baseline and classifier','Compare a simple baseline with regularized logistic regression. Examine whether the model adds useful information and whether the inputs are meaningful. Avoid including identifiers as predictive features.'),
('6 Validate and choose a threshold','Use validation results to balance missed students and unnecessary outreach. Choose the threshold before looking at the final test results. Review performance across year levels and other appropriate cohorts.'),
('7 Evaluate and monitor','Test on a held-out later term and report errors, recall and precision. Academic staff should review the flags before a pilot. After deployment, monitor data changes, error patterns and whether advising actually helps students.')]
for title,body in steps:h(title);p(body)
p('Our time-based evaluation is intended to imitate the real decision: using past information to support a later term. The scikit-learn cross-validation guidance explains why testing on future observations matters for time-ordered data (scikit-learn, n.d.-b). A real evaluation should also account for repeated student records and prevent outcome information from leaking across the prediction cutoff.')
h('Two evaluation metrics')
p('Recall = TP / (TP + FN). Here, TP means students correctly flagged who later meet the agreed difficulty outcome, and FN means students missed by the model who later meet it. Recall matters because a missed student may lose an opportunity for early support (scikit-learn, n.d.-c).')
p('Precision = TP / (TP + FP). FP means students flagged who do not later meet the defined outcome. Precision helps the chair judge how much outreach is directed toward students who meet that outcome, which matters when advising capacity is limited (scikit-learn, n.d.-d). A false positive should lead to respectful review, not punishment.')
p('For illustration only, if a test set had 30 TP, 10 FN and 20 FP, recall would be 75% and precision would be 60%. These numbers explain the formulas; they are not results from our workbook or prototype. Both metrics should be reported with the threshold, sample size and outcome prevalence. If a denominator is zero, the metric needs an explicit undefined-value policy rather than a misleading score.')

page('Part V System Evaluation and Recommendations')
h('Three types of testing before implementation')
p('1. Data and calculation testing. Reconcile totals across the term, semester summary, dimension and year-level tables. Check join keys, missing denominators, item weights, rounding and boundary values. For example, the three dimension point totals should equal the overall point total, and a year-level risk rate exactly equal to 10% should not trigger an above-10% warning.')
p('2. Functional and usability testing. Ask a Program Chair or an appropriate reviewer to carry out common tasks: change the semester, inspect a KPI, interpret a warning, use hover or keyboard details, export a CSV and print the page. Check that all selected-term outputs stay synchronized and that text and chart labels remain readable on desktop and mobile. Confirm that the long-bond printout fits and retains useful color contrast.')
p('3. Security and access testing. Verify that users can retrieve only the programs and faculty records allowed by their role, including through direct data requests and exports. Test whether small response groups or comments can reveal identities. Check access logging and restrictions on saved or downloaded reports. These production controls are requirements, not features established by the client-only prototype.')
h('Privacy and fairness')
p('We would keep identifying records separate from published summaries and provide only the minimum detail needed for each role. Faculty evaluation results and comments should not be displayed in a public ranking. Small groups require a documented suppression rule because removing names alone may not prevent identification. The university would also need an agreed retention and export policy.')
p('Academic flags need review because errors, missing records and different student circumstances can affect who appears in the list. A predictive system should be checked for uneven error rates and should allow staff to correct inaccurate information. Its purpose is to offer support, not to deny a student an opportunity automatically.')
p('For SETE, we would show response coverage with the rating, explain the criteria and consider course context before making comparisons. Faculty should have an opportunity to discuss the results with other evidence. A numerical target can organize a review, but it does not replace professional judgment.')
h('Two recommendations')
p('First, use the year-level risk view to organize advising and learning support. In our sample, Year 1 exceeds the proposed 10% threshold even when the program average does not. After validating the flags, the chair could coordinate confidential outreach and later review participation in support activities and subsequent course outcomes.')
p('Second, use semester and dimension feedback to plan focused faculty development. A lower management-of-teaching score could lead to a discussion of learning activities, expectations or feedback practices. The chair should compare later results with participation and other evidence instead of treating a rating increase alone as proof that an activity worked.')
h('Implementation recommendation')
p('We recommend starting with a limited aggregate reporting pilot and agreed KPI definitions. The current dashboard demonstrates the reporting design with synthetic data. A live implementation would require approved data access, verified source fields, secure role-based reporting and completed user testing. Student-risk prediction should follow only when suitable longitudinal data and an approved support process are available.')

page('References')
p('Course handout. (n.d.). BAT 405 Analytics Application: Integrated case study activity. Enhancing the University Student and Faculty Portal Through Analytics and Decision Support. Supplied assignment document.')
p('Student group. (2026). BAT405_AcademicInsight_Synthetic_PowerBI_Data.xlsx [Synthetic workbook]. Tables used: Terms, SemesterSummary, SETDimensions, YearLevelRisk and ReadMe.')
p('Batangas State University portal reference screens. (2026, November 18). Student Portal homepage, Student Evaluation of Teachers list, and evaluation form [Three screenshots supplied for the case study].')
for label,url in [
('scikit-learn. (n.d.-a). LogisticRegression.', 'https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html'),
('scikit-learn. (n.d.-b). Cross-validation: Evaluating estimator performance.', 'https://scikit-learn.org/stable/modules/cross_validation.html'),
('scikit-learn. (n.d.-c). recall_score.', 'https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html'),
('scikit-learn. (n.d.-d). precision_score.', 'https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html')]:
    p(label);link('Retrieved November 18, 2026, from',url)
h('Project output')
p('Mendoza, V. A., & Malata, R. L. (2026). Academic Insight [Program Chair dashboard prototype].')
link('Dashboard:',URL)
p('The dashboard uses synthetic semester aggregates. Its hosted access is private at the time this document was prepared.')

for section in doc.sections:section.footer_distance=Inches(.3)
footer=doc.sections[0].footer.paragraphs[0];footer.alignment=2
run=footer.add_run();fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');run._r.addnext(fld)
for element in list(doc.styles.element.iter(qn('w:pBdr'))):element.getparent().remove(element)
for element in list(doc.element.iter(qn('w:pBdr'))):element.getparent().remove(element)
doc.save(OUT/'BAT405_Academic_Insight_Case_Study.docx')
print(OUT/'BAT405_Academic_Insight_Case_Study.docx')
