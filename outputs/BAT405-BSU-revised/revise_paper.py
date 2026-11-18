from pathlib import Path
from copy import deepcopy
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib, json, re
from lxml import etree as E
from PIL import Image, ImageDraw, ImageFont
from docx import Document
from docx.shared import Inches, Pt
from docx.shared import RGBColor
from decimal import Decimal, ROUND_HALF_UP
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

OUT=Path(__file__).parent
REF=OUT/'reference.docx'
assert hashlib.sha256(REF.read_bytes()).hexdigest()=='8f1dad3f9b18d8efde2c985be9b48da0e2eee99b1a9e6f829962d51151e66a11'
DATA=json.loads((OUT/'current-data.json').read_text(encoding='utf-8'))
LAST=DATA['periods'][-1];S=LAST['summary'];M=LAST['metrics']
assert [M[k] for k in ['passRate','onTimeRate','responseRate','meanRating','difficultyRate']]==[88,90,60,4.2,15]

# A code-drawn application symbol following the current dashboard's cap mark.
logo=Image.new('RGB',(300,300),'white');d=ImageDraw.Draw(logo)
d.rounded_rectangle((10,10,290,290),radius=60,fill='#982338')
d.line([(55,115),(150,70),(245,115),(150,160),(55,115)],fill='white',width=10)
d.line([(90,136),(90,207),(150,230),(210,207),(210,136)],fill='white',width=10)
d.line([(245,115),(245,215)],fill='white',width=10)
logo.save(OUT/'qa/app-logo.png')
watermark=Image.new('RGB',(900,491),'white');wd=ImageDraw.Draw(watermark)
wm_color='#c0a3ad'
wd.line([(270,205),(450,120),(630,205),(450,290),(270,205)],fill=wm_color,width=11)
wd.line([(340,238),(340,343),(450,385),(560,343),(560,238)],fill=wm_color,width=11)
wd.line([(630,205),(630,350)],fill=wm_color,width=11)
wm=BytesIO();watermark.save(wm,'JPEG',quality=95)

# Labeled mockup: same order, counts and visual encodings as the local app.
im=Image.new('RGB',(1800,1660),'#f5f6f9');draw=ImageDraw.Draw(im)
def font(n,b=False):return ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf' if b else 'C:/Windows/Fonts/arial.ttf',n)
def text(x,y,s,n=22,c='#303747',b=False):draw.text((x,y),s,font=font(n,b),fill=c)
def box(x,y,w,h,fill='#ffffff'):draw.rounded_rectangle((x,y,x+w,y+h),radius=14,fill=fill,outline='#dfe3eb',width=2)
text(45,25,'A  BatStateU Academic Insights',38,'#982338',True)
text(45,80,'Program Chair  /  BSIT  /  CICS  /  ARASOF Nasugbu  /  Simulated data',22)
box(35,130,1730,125)
text(55,148,'B  Academic year: 2026-2027   |   First semester   |   All year levels',24,b=True)
text(55,193,'Academic status: support review needed - 63 of 420 students have a finalized failed course.',23,'#895225')
labels=['Course pass rate','On-time grade submission','SETE response rate','Mean SETE rating','Academic difficulty rate']
values=['88.0%','90.0%','60.0%','4.20 / 5','15.0%']
targets=['Target >= 90%','Target >= 95%','Target >= 70%','Target >= 4.00 / 5','Target <= 10%']
for i in range(5):
 x=35+i*349;box(x,280,334,155)
 text(x+14,296,f'C{i+1}  {labels[i]}',18,b=True)
 text(x+14,330,values[i],39,'#292632',True)
 text(x+14,390,targets[i],18)
 text(x+14,414,'Within target' if i==3 else 'Needs review',15,'#32694d' if i==3 else '#895225')
box(35,465,845,445);box(900,465,865,445)
text(55,485,'D  Course pass rate by year level',27,b=True)
text(55,530,'Passed / finalized course outcomes  |  Scale 0-100%',19)
for i,row in enumerate(LAST['rows']):
 y=590+i*68;rate=row['passed']/row['outcomes']*100
 text(55,y,f'Year {row["level"]}',21);draw.rounded_rectangle((150,y+3,620,y+25),radius=5,fill='#edf0f3')
 draw.rounded_rectangle((150,y+3,150+470*rate/100,y+25),radius=5,fill='#a92b3a' if rate<90 else '#628578')
 draw.line((573,y-2,573,y+29),fill='#826a73',width=3)
 text(640,y,f'{rate:.1f}%',23,b=True);text(725,y,f'{row["passed"]}/{row["outcomes"]}',18)
text(55,872,'Dashed marker: proposed target 90%',19)
text(920,485,'E  Average SETE rating across semesters',27,b=True)
text(920,530,'Overall item-weighted mean  |  Scale 1-5',19)
for v in range(1,6):
 y=810-(v-1)*48;draw.line((970,y,1700,y),fill='#e3e6eb',width=2);text(932,y-12,str(v),18)
for x in range(970,1700,18):draw.line((x,666,x+9,666),fill='#826a73',width=2)
pts=[(1030+i*295,810-(p['metrics']['meanRating']-1)*48) for i,p in enumerate(DATA['periods'])]
draw.line(pts,fill='#a92b3a',width=4)
for (x,y),p in zip(pts,DATA['periods']):
 radius=9 if p['id']==LAST['id'] else 6
 draw.ellipse((x-radius,y-radius,x+radius,y+radius),fill='#a92b3a');text(x-28,y-35,f'{p["metrics"]["meanRating"]:.2f}',23,b=True)
 text(x-53,833,p['shortLabel'],20);text(x-53,864,f'n = {p["summary"]["responses"]:,}',18)
box(35,940,1730,455);text(55,960,'F  SETE ratings by evaluation dimension',27,b=True)
text(55,1003,'Dot plot  |  Scale 1-5  |  Dashed marker: proposed target 4.00',21)
for i,dim in enumerate(DATA['dimensions']):
 y=1085+i*90;text(55,y-5,dim['label'],20)
 text(55,y+23,f'{dim["items"]} statements - equal weight per item',17,'#687382')
 draw.line((660,y+12,1570,y+12),fill='#dfe4e8',width=4)
 draw.line((1342,y-6,1342,y+30),fill='#826a73',width=2)
 x=660+(S['dimensionScores'][i]-1)/4*910;draw.ellipse((x-8,y+4,x+8,y+20),fill='#a92b3a')
 score=Decimal(str(S['dimensionScores'][i])).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)
 text(1610,y-2,f'{score} / 5',24,b=True)
for v in range(1,6):text(652+(v-1)*227.5,1354,str(v),19)
box(35,1420,1730,160,'#eef1f6');text(55,1440,'G  1,260 / 2,100 completed / eligible evaluations',25,b=True)
text(55,1486,'Low participation: interpret ratings cautiously. SETE must not be the sole basis for personnel decisions.',21)
text(55,1530,'Simulated finalized scenario. Portal-SETE analytics integration is proposed. No real student or faculty records.',20)
text(45,1610,'Select KPI cards for formulas, management actions and previous-semester comparisons.',22)
im.save(OUT/'qa/current-dashboard-mockup.png')

old=Document(OUT.parent/'BAT405-case-study/BAT405_Academic_Insight_Case_Study.docx')

REPLACE={
'We propose Academic Insight as': 'We propose BatStateU Academic Insights as a one-page analytics dashboard for the BSIT Program Chair. It brings academic outcomes, grade-submission timeliness and student teaching feedback into one reporting view. Our purpose is to help the chair identify matters needing follow-up and plan academic support within CICS at the ARASOF Nasugbu Campus.',
'The Faculty Portal is included': 'The Faculty Portal is included in the case scenario, but we did not inspect a faculty account. Teaching assignments, class lists, grade records and submission timestamps are possible inputs to the proposed reporting layer. Their actual fields, reporting permissions, due dates and export options would need to be confirmed with the university. The on-time submission measure is an explicit design assumption, not an observed Faculty Portal capability.',
'We selected five KPIs': 'We selected five KPIs covering academic monitoring, grade-submission timeliness and teaching feedback. All targets are proposed case-study benchmarks, not official university standards. Each measure uses the selected semester and year-level scope. A missing or zero denominator produces an unavailable result rather than a zero performance score.',
'Objective and relevance: compare actual enrollment': 'Objective and relevance: monitor the share of finalized student-course outcomes that passed. This helps the chair identify cohorts requiring course-level review. Management action: examine the courses contributing to a lower rate and plan tutoring, assessment review or other learning support. This KPI counts course outcomes, not distinct students. Missing, incomplete and withdrawn records are excluded from its finalized pass/fail denominator.',
'Objective and relevance: monitor the share of graded': 'Objective and relevance: monitor whether complete section grades were submitted by the applicable deadline. Delayed submissions can affect academic monitoring and follow-up. Management action: review overdue sections and approved exceptions before contacting the responsible staff. The denominator includes only sections whose deadline has passed. A submission that is complete but late remains late even when all grades are later finalized.',
'Objective and relevance: show the share of enrolled': 'Objective and relevance: assess how much of the eligible teaching evaluation population is represented. Management action: check access and eligibility issues and interpret available ratings cautiously. One student may evaluate several courses, so this KPI counts evaluation assignments rather than unique respondents. In an open evaluation period, neutral reminders may be appropriate. The current sample is a hypothetical closed evaluation scenario.',
'Objective and relevance: summarize student perceptions': 'Objective and relevance: summarize student perceptions across the 15 evaluation criteria. Management action: discuss the dimension results with participation, course context and other teaching evidence. The calculation uses total valid item-score points divided by valid item responses. Equal item weights mean that the six-, five- and four-item dimensions must not simply be averaged as three equally weighted means.',
'Objective and relevance: show the coverage': 'Objective and relevance: identify the share of students with at least one finalized failed course who may need academic support. Management action: validate course outcomes and arrange confidential advising or learning support. Each student is counted once, even with several failed courses. The denominator includes students with at least one finalized pass/fail result. This describes recorded outcomes; it is not a prediction of future failure.',
'The sample workbook covers': 'The current local dashboard uses three simulated semesters: the first and second semesters of AY 2025–2026 and the first semester of AY 2026–2027. It defaults to the last period with all year levels selected. The figures are purpose-built application aggregates, not university records. The AY 2026–2027 sample is a hypothetical finalized scenario; it does not imply that the live semester or evaluation window shown in the screenshots has closed.',
'The dashboard rounds the risk rate': 'The latest sample has 420 students and 2,100 finalized course outcomes. Its 1,260 completed evaluations produce 18,900 scored items because each form has 15 items. Their total score is 79,380 points. The dashboard recalculates ratios from the underlying counts rather than averaging year-level percentages. The paper reports the same counts and definitions as the local dashboard.',
'Our first warning is': 'Our first warning is a course pass rate below 90%. The current sample is 88%, so its card displays Needs review. The chair should examine course and cohort outcomes before deciding what support is appropriate. A low aggregate rate does not establish its cause or identify a faculty member as responsible.',
'Our second warning is': 'Our second warning is an academic difficulty rate above 10%. In the sample, 63 of 420 students have at least one finalized failed course, or 15%. The academic-status message highlights this concern. This threshold applies to the selected program or year-level scope; it is separate from the passing rate, whose denominator counts course outcomes.',
'Other card warnings appear': 'Other card warnings appear below 95% on-time grade submission, below 70% SETE response or below a 4.00/5 mean rating. The latest sample therefore has four card warnings: passing, submission timing, participation and academic difficulty. The mean rating meets its target. We removed the separate review-flags strip because the card statuses and academic-status message already communicate the warnings. Threshold comparisons use unrounded values, and equality meets the target.',
'The dimension view gives': 'The dimension view provides a more useful discussion point than an overall score alone. In the sample, management of teaching and learning is 4.25, content knowledge, pedagogy and technology is 4.20, and commitment and transparency is 4.125, displayed as 4.13. All meet the proposed 4.00 benchmark. The relatively lower commitment score may prompt discussion, but it does not establish poor teaching, especially when response coverage is only 60%.',
'Our primary user is': 'Our primary user is the BSIT Program Chair. The layout starts with the reporting scope, filters and academic-status message, followed by five compact KPI cards. Academic outcomes come before the teaching trend, followed by teaching dimensions. This sequence supports a review from overall concerns to more specific teaching feedback. Figure 1 labels the current local dashboard design.',
'A. Reporting controls': 'A. The header identifies BatStateU Academic Insights, the Program Chair, BSIT/CICS and simulated data. B. Academic-year, semester and year-level filters update all cards, selected-term charts and participation counts. Reset filters returns to the default sample. College and program remain fixed because this local design covers BSIT within CICS; a broader implementation could add authorized college and department fields.',
'B1 to B5.': 'C1 to C5. The five cards show course pass rate, on-time grade submission, SETE response rate, mean SETE rating and academic difficulty rate. Each card shows its value, proposed target and status. Formulas, selected counts, management actions and prior-semester comparisons appear only when a card is selected. Rate changes use percentage points, while rating changes use scale points.',
'C. A line chart': 'D. Horizontal bars compare course passing rates across year levels on a 0–100% scale. Labels include passed and finalized outcome counts, and a marker identifies the proposed 90% target. The default rates are 92.0%, 90.0%, 87.0% and 81.3% for Years 1 through 4. A year-level filter narrows this view to the selected cohort.',
'D. Horizontal bars': 'E. A line chart shows the overall item-weighted mean SETE rating across the available semesters through the selected period. It uses a 1–5 scale and a dashed 4.00 target line. The default history is 4.06, 4.15 and 4.20, with 1,365, 1,495 and 1,260 completed evaluations. The selected semester has a larger point. Earlier periods remain as historical context, and the same year-level scope applies throughout. This is a descriptive trend, not a forecast.',
'E. A column chart': 'F. A horizontal dot plot compares the three selected-period evaluation dimensions on the same 1–5 scale. Dots show each score without implying that the rating is a filled quantity. The plot includes full dimension names, item counts, displayed scores and a dashed target marker at 4.00. The overall rating is weighted by item responses, not by giving each dimension equal weight.',
'F. The review section': 'G. The participation and interpretation strip shows completed and eligible evaluations, a low-participation message when appropriate, and the reminder that SETE must not be the sole basis for personnel decisions. The footer identifies simulated data and the proposed Portal–SETE analytics integration. The removed guide and review-flags sections are not part of this version.',
'The two main interactive features': 'The two main interactive features are coordinated reporting filters and click-to-open KPI details. Native dialogs can be closed using Close or Escape. The trend includes a native hover title on its points; the local version does not include the separate hosted version’s custom tooltips, chart-click navigation or CSV export. Print dashboard invokes the browser print layout. The accompanying labeled mockup follows the local design and is not a captured browser screenshot.',
'The hosted prototype currently': 'This report documents the local React dashboard, not the separate hosted prototype. The local address is localhost:5173 and is usable on the development computer. The same final version still needs publication to an instructor-accessible link. Automated tests, lint and the production build have passed; browser usability, keyboard operation and the dashboard’s actual print pagination still require acceptance checks.',
'Academic Insight for the Program Chair': 'BatStateU Academic Insights for the Program Chair | First semester AY 2026–2027 | Simulated finalized scenario',
'Figure 1.': 'Figure 1. Labeled mockup of the current local dashboard: identity (A), filters and academic status (B), five KPI cards (C1–C5), course pass-rate bars (D), semester SETE trend (E), dimension dot plot (F), and participation context (G). Values match the application dataset. Print this dashboard page in color.',
'We chose early identification': 'We chose early identification of academic difficulty because it gives the Program Chair a clear support decision: which students may need advising before the next semester’s outcomes are finalized. The current dashboard describes students with recorded finalized failures. It does not predict which individual student is likely to struggle in the future.',
'For a future model, we propose': 'For a future model, we propose defining the outcome as at least one finalized failed course in the next regular semester. This follows the type of academic concern shown by the descriptive difficulty KPI, but shifts the outcome to a future term. Staff would need to approve how incomplete, withdrawn and ungraded registrations are handled. Students without an observable next-term outcome must not automatically be labeled as having no difficulty.',
'The attendance variable is': 'Attendance is a proposed additional input, and its availability is not established by the screenshots. The dashboard contains only simulated semester and year-level aggregates, not individual predictor histories or future outcome labels. These records would need to be obtained through authorized sources; they cannot be inferred from the current totals.',
'Four aggregate semesters': 'Three aggregate semesters can demonstrate the dashboard, but cannot train and validate a student-level classifier. We have not fitted a model or measured predictive accuracy. The dashboard’s 63 students with finalized failures are descriptive sample counts, not model-generated predictions. The classifier remains a design proposal for this case study.',
'1. Data and calculation testing.': '1. Data and calculation testing. Reconcile students, course outcomes, section deadlines and completed evaluations by reporting period and year level. Check missing denominators, item weights, rounding and thresholds. In the default scenario, confirm 1,848/2,100 passing outcomes, 36/40 on-time sections, 1,260/2,100 completed evaluations, 79,380/18,900 rating points per item response and 63/420 students with finalized failures.',
'2. Functional and usability testing.': '2. Functional and usability testing. Ask a Program Chair or an appropriate reviewer to change the academic year, semester and year level, reset the filters, inspect a KPI and close its dialog with mouse and keyboard. Confirm that cards, charts, participation counts and warnings update together. Check desktop and mobile text, chart labels and one-page long-bond printing. The screen can scroll; the printed dashboard must be checked separately.',
'First, use the year-level risk view': 'First, use year-level academic outcomes to organize advising and learning support. The default sample shows a 15% academic difficulty rate, while Year 4 has an 81.3% course pass rate. After checking the underlying records, the chair could coordinate confidential advising and targeted course support. Later review should consider participation in that support and subsequent course outcomes.',
'Second, use semester and dimension': 'Second, use semester and dimension feedback to plan focused faculty development. The sample’s commitment and transparency score is 4.13, compared with 4.25 for teaching management. The chair could discuss consultation, feedback and assessment criteria, while accounting for 60% evaluation participation and other teaching evidence. A later score increase alone would not establish that a development activity caused an improvement.',
'Student group. (2026).': 'Mendoza, V. A., & Malata, R. L. (2026). Simulated semester and year-level aggregates for BatStateU Academic Insights [Application dataset, src/data/dashboard.js]. Three sample reporting periods; no actual university records.',
'Mendoza, V. A., & Malata, R. L. (2026). Academic Insight': 'Mendoza, V. A., & Malata, R. L. (2026). BatStateU Academic Insights [Local Program Chair dashboard prototype].',
'The dashboard uses synthetic semester': 'The paper and mockup describe the current local dashboard. The source repository is available below; an instructor-accessible link to this same version remains a deployment task.'
}
HEADINGS={'1 Enrollment achievement':'1 Course pass rate','2 Course pass rate':'2 On-time grade submission','3 Academic risk rate':'3 SETE response rate','4 Mean teaching evaluation':'4 Mean SETE rating','5 Evaluation participation':'5 Academic difficulty rate'}
HEADINGS['Sample results for the latest workbook term']='Sample results for the default reporting period'
REPLACE.update({
'Other card warnings appear':'Other card warnings appear below 95% on-time grade submission, below 70% SETE response or below a 4.00/5 mean rating. The latest sample has four card warnings: passing, submission timing, participation and academic difficulty. Its mean rating meets the target. Warnings are communicated through card statuses and the academic-status message, with management actions available in the KPI details. Comparisons use unrounded values, and equality meets the target.',
'F. The review section':'G. The participation and interpretation strip shows completed and eligible evaluations, a low-participation message when appropriate, and the reminder that SETE must not be the sole basis for personnel decisions. The footer identifies simulated data and the proposed Portal–SETE analytics integration.',
'The two main interactive features':'The two main interactive features are coordinated reporting filters and click-to-open KPI details. Native dialogs provide formulas, selected counts, management actions and interpretation notes, and can be closed using Close or Escape. The trend includes a native hover title on its points. Print dashboard invokes the browser print layout. Figure 1 is a labeled mockup of this design, rather than a captured browser screenshot.',
'The hosted prototype currently':'The local React prototype is available on the development computer at localhost:5173. Its source repository is linked above. Publication of the same final dashboard to an instructor-accessible address remains a submission task. Automated tests, lint and the production build have passed; browser usability, keyboard operation and the actual dashboard print pagination still require acceptance checks.',
'The dashboard uses synthetic semester':'The paper and mockup describe the current local dashboard. The source repository is linked above; publication of an instructor-accessible dashboard link remains a deployment task.',
'We propose Academic Insight as':'We propose BatStateU Academic Insights as a one-page dashboard for the BSIT Program Chair. It combines academic outcomes, grade-submission timeliness and teaching feedback to support academic assistance and instructional review within CICS at ARASOF Nasugbu.',
'The Student Portal screenshot shows':'The Student Portal screenshot shows enrollment status, subjects, grades, curriculum, registration documents, fees and student services. These entry points help students check records and complete transactions. The homepage does not establish how every linked service or administrative report works.',
'The Faculty Portal is included':'We did not inspect a Faculty Portal account. Teaching assignments, class lists, grade records, submission timestamps and deadlines are proposed reporting inputs whose availability and permissions need verification. On-time grade submission is a design assumption, not a personally observed capability.',
'The screenshots call the system':'The screenshots call the system Student Evaluation of Teachers or SET; this paper uses SETE to follow the assignment. The form has 15 five-star items, a maximum of 75 points and optional comments. Its dimensions are teaching and learning management (6 items), knowledge, pedagogy and technology (5), and commitment and transparency (4). Official verbal rating labels are not visible.',
'These responses can show':'SETE describes students’ experiences of instruction, feedback and assessment. It can suggest discussion or faculty development topics, but participation and course context are needed because student ratings do not capture every part of teaching effectiveness.',
'The screenshots do not establish':'The screenshots do not establish whether administrators already have trend reports, cohort alerts or combined summaries. We treat these as opportunities to validate, not verified defects. A portal link to SETE does not establish integrated analytics; our reporting layer is proposed.',
'The Program Chair would use':'The Program Chair could plan advising, course review and faculty support. The dean and authorized administrators could use approved summaries for resources, while faculty could review appropriately scoped teaching feedback. Students could benefit through support services without seeing other students’ records or confidential faculty results.'
})
for par in old.paragraphs:
 text_value=par.text
 if text_value in HEADINGS:par.text=HEADINGS[text_value]
 elif text_value=='Academic Insight':par.text='BatStateU Academic Insights'
 else:
  for prefix,value in REPLACE.items():
   if text_value.startswith(prefix):par.text=value;break

# Source-derived KPI table and exact calculations from the current local app.
for row,values in zip(old.tables[1].rows[1:],[
 ['Course pass rate','Passed finalized course outcomes / finalized pass/fail outcomes × 100','At least 90%'],
 ['On-time grade submission','Complete sections submitted by deadline / sections due × 100','At least 95%'],
 ['SETE response rate','Completed valid evaluations / eligible assignments × 100','At least 70%'],
 ['Mean SETE rating','Total valid item-score points / valid item responses','At least 4.00 / 5'],
 ['Academic difficulty rate','Students with a finalized failed course / students with finalized outcomes × 100','At most 10%']]):
 for cell,value in zip(row.cells,values):cell.text=value
for row,values in zip(old.tables[2].rows[1:],[
 ['Course pass rate','1,848 / 2,100 × 100','88.0%','Review'],
 ['On-time grade submission','36 / 40 × 100','90.0%','Review'],
 ['SETE response rate','1,260 / 2,100 × 100','60.0%','Review'],
 ['Mean SETE rating','79,380 / 18,900','4.20 / 5','Within target'],
 ['Academic difficulty rate','63 / 420 × 100','15.0%','Review']]):
 for cell,value in zip(row.cells,values):cell.text=value
old.tables[0].rows[-1].cells[0].text='Finalized pass/fail outcomes and students'
old.tables[0].rows[-1].cells[1].text='Calculate academic difficulty from distinct students with finalized failed courses.'
old.tables[0].rows[4].cells[0].text='Faculty assignments and submission records'
old.tables[0].rows[4].cells[1].text='Match evaluations; proposed grade timestamps and deadlines support timeliness monitoring.'

# Build in the supplied template so its institutional furniture remains native.
doc=Document(REF);body=doc.element.body
sect=deepcopy(body.sectPr)
for el in list(body):body.remove(el)
body.append(sect)
source_ns={'r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
for el in old.element.body:
 if el.tag==qn('w:sectPr'):continue
 clone=deepcopy(el)
 for sp in list(clone.iter(qn('w:sectPr'))):sp.getparent().remove(sp)
 # Empty section-break paragraphs are unnecessary in the all-portrait paper.
 if clone.tag==qn('w:p') and not ''.join(clone.itertext()).strip() and not list(clone.iter(qn('w:drawing'))):continue
 body.insert(len(body)-1,clone)
 # Resolve donor links; the separate hosted URL is intentionally not reused.
 for node in clone.iter():
  for attr in [qn('r:id'),qn('r:embed'),qn('r:link')]:
   rid=node.get(attr)
   if not rid:continue
   rel=old.part.rels.get(rid)
   if rel is None:continue
   if rel.reltype.endswith('/hyperlink'):
    target='https://github.com/lancemalata/Dashboard' if 'chatgpt.site' in rel.target_ref else rel.target_ref
    newrid=doc.part.relate_to(target,rel.reltype,is_external=True);node.set(attr,newrid)
    for tx in node.iter(qn('w:t')):
     if 'chatgpt.site' in (tx.text or ''):tx.text=target
   elif rel.reltype.endswith('/image'):
    # Donor cover and mockup are the only two body images.
    is_cover=len(rel.target_part.blob)<30000
    path=OUT/'qa'/('app-logo.png' if is_cover else 'current-dashboard-mockup.png')
    newrid,img=doc.part.get_or_add_image(str(path));node.set(attr,newrid)
    drawing=node
    while drawing is not None and drawing.tag!=qn('w:drawing'):drawing=drawing.getparent()
    if drawing is not None:
     width=Inches(1.25 if is_cover else 6.75)
     with Image.open(path) as pic:height=int(width*pic.height/pic.width)
     for extent in drawing.iter():
      if E.QName(extent).localname in ['extent','ext'] and 'cx' in extent.attrib:
       extent.set('cx',str(width));extent.set('cy',str(height))

# Portrait long bond, template side margins, and room for native letterhead.
s=doc.sections[0];s.page_width=Inches(8.5);s.page_height=Inches(13)
s.top_margin=Inches(1.85);s.bottom_margin=Inches(.75)
s.left_margin=s.right_margin=Inches(.7)

# Make mockup start on its own page (donor used a landscape section break).
for par in doc.paragraphs:
 t=par.text
 if t in ['Labeled Dashboard Mockup','Part IV Analytics Model Selection and Application']:
  par.paragraph_format.page_break_before=True
cover_end=next(j for j,p in enumerate(doc.paragraphs) if p.text=='Part I Existing System Assessment')
cover_nodes=set(par._p for par in doc.paragraphs[:cover_end])
for i,par in enumerate(list(doc.paragraphs)):
 t=par.text
 cover=par._p in cover_nodes
 if cover:
  par.alignment=1;par.paragraph_format.first_line_indent=Inches(0)
  par.paragraph_format.space_after=Pt(8)
 else:
  par.paragraph_format.line_spacing=1.1
  par.paragraph_format.space_after=Pt(5)
  if par.style.name.startswith('Heading'):
   par.paragraph_format.space_before=Pt(10);par.paragraph_format.keep_with_next=True
  elif t and not t.startswith(('Figure 1.','Dashboard','Academic Insight','BatStateU Academic Insights for','scikit-learn.','Retrieved','Mendoza,','Course handout.','Batangas State University portal','The paper and mockup')):
   par.alignment=3;par.paragraph_format.first_line_indent=Inches(.25)
 for run in par.runs:
  run.font.color.rgb=RGBColor(0,0,0)
  rp=run._r.get_or_add_rPr();rf=rp.find(qn('w:rFonts'))
  if rf is None:rf=OxmlElement('w:rFonts');rp.insert(0,rf)
  for key in list(rf.attrib):
   if 'Theme' in key:del rf.attrib[key]
  rf.set(qn('w:ascii'),'Times New Roman');rf.set(qn('w:hAnsi'),'Times New Roman')
  if not cover:run.font.size=Pt(14 if par.style.name=='Heading 1' else 12 if par.style.name=='Heading 2' else 11)
  if t=='BatStateU Academic Insights':run.font.size=Pt(19);run.bold=True
 # Remove redundant university text on the cover; native letterhead supplies it.
 if cover and t in ['Batangas State University','The National Engineering University','ARASOF Nasugbu Campus','College of Informatics and Computing Sciences']:
  par._element.getparent().remove(par._element)

# Replace old standalone link labels with the source repository, never a mismatched live site.
for par in doc.paragraphs:
 if 'not results from our workbook or prototype' in par.text:
  par.text=par.text.replace('not results from our workbook or prototype','not results from the application dataset or prototype')
 for tx in par._p.iter(qn('w:t')):
  if 'chatgpt.site' in (tx.text or ''):tx.text='https://github.com/lancemalata/Dashboard'
 if par.text.startswith('Dashboard link:'):par.runs[0].text='Dashboard source repository: '
 if par.text.startswith('Dashboard:'):par.runs[0].text='Source repository: '

source_table=Document(REF).tables[0]
for table in doc.tables:
 for row in table.rows:
  cant=OxmlElement('w:cantSplit');row._tr.get_or_add_trPr().append(cant)
  for cell in row.cells:
   for shd in list(cell._tc.get_or_add_tcPr().findall(qn('w:shd'))):shd.getparent().remove(shd)
   margins=cell._tc.get_or_add_tcPr().find(qn('w:tcMar'))
   if margins is not None:
    for m in margins:
     if E.QName(m).localname in ['top','bottom']:m.set(qn('w:w'),'45')
   for par in cell.paragraphs:
    par.paragraph_format.space_after=Pt(2);par.paragraph_format.line_spacing=1.0
    for run in par.runs:run.font.name='Times New Roman';run.font.size=Pt(10)
   borders=cell._tc.get_or_add_tcPr().find(qn('w:tcBorders'))
   if borders is not None:
    for border in borders:border.set(qn('w:color'),'000000')

doc.core_properties.title='BatStateU Academic Insights Case Study'
doc.core_properties.author='Vince A. Mendoza and Ronel Lance Malata'
doc.core_properties.subject='BAT 405 Analytics Application'
working=OUT/'working.docx';doc.save(working)

# Preserve untouched template parts byte-for-byte, replace only declared slots.
with ZipFile(working) as z:parts={n:z.read(n) for n in z.namelist()}
with ZipFile(REF) as ref:
 for name in ref.namelist():
  if name in ['word/document.xml','word/_rels/document.xml.rels','docProps/core.xml']:continue
  if name.startswith('word/media/'):
   if name=='word/media/image6.png':parts[name]=ref.read(name)
   continue
  # Styles, theme, numbering, custom XML, header XML and motto are retained.
  if name in parts:parts[name]=ref.read(name)
 for n in ['word/header1.xml','word/header2.xml','word/header3.xml']:
  parts[n]=ref.read('word/header2.xml')
  parts['word/_rels/'+Path(n).name+'.rels']=ref.read('word/_rels/header2.xml.rels')
 for n in ['word/footer1.xml','word/footer2.xml','word/footer3.xml']:parts[n]=ref.read('word/footer2.xml')
parts['word/media/image5.jpeg']=wm.getvalue()
# Strip unreferenced original body photos and their relationships.
rels=E.fromstring(parts['word/_rels/document.xml.rels'])
body_xml=E.fromstring(parts['word/document.xml'])
used={v for el in body_xml.iter() for k,v in el.attrib.items() if k.startswith('{'+source_ns['r']+'}')}
for rel in list(rels):
 if rel.get('Type','').endswith(('/image','/hyperlink')) and rel.get('Id') not in used:rels.remove(rel)
parts['word/_rels/document.xml.rels']=E.tostring(rels,xml_declaration=True,encoding='UTF-8',standalone=True)
media_used={'word/media/image5.jpeg','word/media/image6.png'}
for rel in rels:
 if rel.get('Type','').endswith('/image'):media_used.add('word/'+rel.get('Target'))
for name in list(parts):
 if name.startswith('word/media/') and name not in media_used:del parts[name]
settings=E.fromstring(parts['word/settings.xml']);uf=settings.find(qn('w:updateFields'))
if uf is None:uf=OxmlElement('w:updateFields');settings.append(uf)
uf.set(qn('w:val'),'true');parts['word/settings.xml']=E.tostring(settings,xml_declaration=True,encoding='UTF-8',standalone=True)
final=OUT/'BAT405_Academic_Insights_BSU_Revised.docx'
with ZipFile(final,'w',ZIP_DEFLATED) as z:
 for name,blob in parts.items():z.writestr(name,blob)
with ZipFile(REF) as z:
 for name in ['word/styles.xml','word/numbering.xml','word/theme/theme1.xml','word/media/image6.png']:
  if name in z.namelist():assert parts[name]==z.read(name),name
assert hashlib.sha256(REF.read_bytes()).hexdigest()=='8f1dad3f9b18d8efde2c985be9b48da0e2eee99b1a9e6f829962d51151e66a11'
print(final)
