from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml.ns import qn
from copy import deepcopy
import json

OUT=Path(__file__).parent
SOURCE=OUT.parent/'BAT405-BSU-revised/BAT405_Academic_Insights_BSU_Revised.docx'
turns=[
('VINCE', 'Purpose and primary user',
 'Good day po. I am Vince Mendoza, and with me is Ronel Lance Malata. Our proposed dashboard is BatStateU Academic Insights. We designed it for the BSIT Program Chair because this role needs to review academic outcomes and teaching feedback when planning support. As Business Analytics students, our goal is to connect each measure to a decision. The figures are simulated, and integration with the university systems is still proposed.'),
('RONEL', 'Why we chose pass rate and submission timeliness',
 'We selected five KPIs to cover academic operations and teaching feedback. First, course pass rate shows how many finalized course outcomes passed. Our sample is 88 percent, below the proposed 90 percent target. We chose it because it can guide course review and learning support. Second, on-time grade submission measures whether complete section grades arrived by their deadlines. The sample is 90 percent against a 95 percent target. This matters because the chair needs timely records for follow-up. These measures answer different questions: how students performed, and whether academic reporting was on time.'),
('VINCE', 'Why we read the two SETE indicators together',
 'For teaching feedback, we chose SETE response rate and mean SETE rating. Response rate shows how much of the eligible evaluation population is represented. Our sample is 60 percent, below the proposed 70 percent target. It counts student-course assignments, since one student may evaluate several courses. The mean rating is 4.20 out of 5, meeting our proposed 4.00 target. It combines the scores across all 15 items, giving each item equal weight. We show both KPIs because a favorable score still needs participation context. Maganda ang rating, pero we should ask whose feedback it represents.'),
('RONEL', 'Why academic difficulty is a separate KPI',
 'The fifth KPI is academic difficulty rate: students with at least one finalized failed course, counted once each. It is 15 percent, or 63 of 420 students, above our proposed 10 percent limit. Passing rate counts course outcomes, while this measure identifies how many individual students may need support. That makes it useful for advising. Together, the five KPIs cover outcomes, reporting timeliness, evaluation coverage, teaching perceptions and student support. All targets are case-study proposals, not official university standards. A warning starts a review; it does not automatically establish a cause.'),
('VINCE', 'Why the first chart uses horizontal bars',
 'We placed the KPI overview before the three charts so the chair can spot concerns first, then examine the details. The first chart compares passing rates by year level using horizontal bars. Bars are appropriate for comparing separate groups, and the horizontal layout leaves room for labels and counts. Rates allow comparison even when cohort sizes differ. The zero-to-100-percent scale and 90-percent target marker make the results easier to interpret. In our sample, Year 4 has the lowest rate at 81.3 percent, which suggests where course-level review could begin.'),
('RONEL', 'Why the semester chart uses a line',
 'The second chart uses a line because semesters have a chronological order. It helps us follow changes in the overall SETE rating over time. The sample moves from 4.06 to 4.15 to 4.20, on a clearly labeled one-to-five scale. We included evaluation counts because participation also changes, and a 4.00 target line for reference. The larger point identifies the selected semester. This is a descriptive trend, not a forecast. An increase in ratings alone does not prove that teaching caused better learning outcomes.'),
('VINCE', 'Why the dimension chart uses dots',
 'The third chart uses a horizontal dot plot to compare the three SETE dimensions: Management of Teaching and Learning; Content Knowledge, Pedagogy and Technology; and Commitment and Transparency. Dots make it easy to compare positions on the same rating scale, while horizontal labels keep the long names readable. The target marker helps identify areas for discussion. For example, commitment is about 4.13, compared with 4.25 for teaching management. Both meet the proposed target, but the difference can guide a conversation. Hindi ito automatic proof of poor teaching; other evidence still matters.'),
('RONEL', 'Filters, details and responsible decisions',
 'For interaction, we included academic-year, semester and year-level filters so the chair can narrow the reporting scope. Clicking a KPI opens its formula, sample counts and suggested management action. This keeps the cards simple while making calculations reviewable. The Needs review labels and academic-status message highlight threshold breaches. SETE should always be considered with participation, course context and other teaching evidence, never as the sole basis for personnel decisions. We use aggregate sample data without real student or faculty records. Our dashboard supports informed review and appropriate follow-up. The final decision still requires verification and human judgment. Thank you po.'),
]

doc=Document(SOURCE);body=doc.element.body;sect=deepcopy(body.sectPr)
for el in list(body):body.remove(el)
body.append(sect)
def add(text,size=11,bold=False,italic=False):
 p=doc.add_paragraph();p.paragraph_format.space_after=Pt(5)
 p.paragraph_format.line_spacing=1.08
 r=p.add_run(text);r.font.name='Times New Roman';r.font.size=Pt(size)
 r.font.color.rgb=RGBColor(0,0,0);r.bold=bold;r.italic=italic
 return p

p=add('BatStateU Academic Insights',16,True);p.alignment=1
p=add('Dashboard Presentation Script',13,True);p.alignment=1
p=add('Vince A. Mendoza and Ronel Lance Malata | About 6 minutes',10);p.alignment=1
p.paragraph_format.space_after=Pt(11)
for index,(speaker,cue,speech) in enumerate(turns):
 label=add(f'{speaker}  —  {cue}',11,True)
 if index==4:label.paragraph_format.page_break_before=True
 label.paragraph_format.keep_with_next=True
 label.paragraph_format.space_before=Pt(5)
 add(speech)

doc.core_properties.title='BatStateU Academic Insights Presentation Script'
doc.core_properties.author='Vince A. Mendoza and Ronel Lance Malata'
doc.core_properties.subject='BAT 405 two-person dashboard presentation'
final=OUT/'BAT405_Dashboard_Script_English_with_Tagalog.docx'
doc.save(final)
counts={name:sum(len(speech.split()) for speaker,_,speech in turns if speaker==name) for name in ['VINCE','RONEL']}
(OUT/'qa/english_script_check.json').write_text(json.dumps({'spoken_words':sum(counts.values()),'speaker_words':counts,'turns':len(turns)},indent=2),encoding='utf-8')
print(final)
print(counts)
