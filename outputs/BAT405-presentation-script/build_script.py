from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml.ns import qn
from copy import deepcopy
import json

OUT=Path(__file__).parent
SOURCE=OUT.parent/'BAT405-BSU-revised/BAT405_Academic_Insights_BSU_Revised.docx'
turns=[
('VINCE', 'Introduction',
 'Good day po. Ako po si Vince Mendoza, at kasama ko si Ronel Lance Malata. Ang ginawa namin ay BatStateU Academic Insights, isang proposed dashboard para sa BSIT Program Chair. Bilang Business Analytics students, gusto naming maipakita kung paano magagamit ang academic data at teaching evaluations para malaman kung saan kailangan ng follow-up at support. Sample data lang po ang figures dito, at proposed pa ang integration sa university systems.'),
('RONEL', 'Academic indicators',
 'Dito sa taas, may five KPI cards. Una, ang course pass rate ay 88 percent, below sa proposed target na 90 percent. Course results ang binibilang dito, hindi individual students. Ang on-time grade submission naman ay 90 percent, below sa 95 percent target. Then, ang academic difficulty rate ay 15 percent. Ibig sabihin, 63 out of 420 students ang may at least one finalized failed course sa sample. Ito ang puwedeng maging basis para mag-review ng records at magplano ng advising.'),
('VINCE', 'Teaching evaluations',
 'Para naman sa teaching feedback, ang SETE response rate ay 60 percent. Meaning, 60 percent ng eligible evaluation assignments ang completed, hindi ito bilang ng unique students. Ang mean SETE rating ay 4.20 out of 5, which meets our proposed 4.00 target. Pero kahit okay ang rating, kailangan pa ring tingnan ang participation at course context. Hindi sapat ang SETE score lang para husgahan ang teaching performance ng faculty.'),
('RONEL', 'Three visualizations',
 'Sa graphs naman, una ang bar chart ng pass rate per year level para madaling mag-compare. Sa sample, Year 4 ang may pinakamababang pass rate, kaya puwedeng doon magsimula ang course review. Pangalawa, ang line chart ay para makita ang pagbabago ng SETE ratings across semesters. Pangatlo, ang dot plot ay nagko-compare ng three evaluation dimensions: teaching management; knowledge, pedagogy and technology; at commitment and transparency. Makikita rin ang target markers bilang reference.'),
('VINCE', 'Quick demonstration',
 'Puwede nating baguhin ang academic year, semester, at year level. Sabay na mag-a-update ang cards at charts ayon sa selected scope. Kapag klinick naman ang isang KPI card, lalabas ang formula, actual sample counts, at suggested management action. Yung Needs review status at academic-status message ang nagsisilbing warnings kapag hindi na-meet ang proposed targets.'),
('RONEL', 'Closing',
 'So, ang purpose ng dashboard ay tulungan ang Program Chair na makita kung ano ang dapat i-review, gaya ng academic support, delayed grade submissions, o evaluation participation. Descriptive po ang current dashboard; hindi pa ito predictive model. Wala rin pong real student or faculty records na ipinapakita. Ang next step sa actual implementation ay i-validate ang data, permissions, at findings bago gumawa ng decisions. Thank you po.'),
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
p=add('Taglish Presentation Script',13,True);p.alignment=1
p=add('Vince A. Mendoza and Ronel Lance Malata | About 4 minutes',10);p.alignment=1
p.paragraph_format.space_after=Pt(11)
for speaker,cue,speech in turns:
 label=add(f'{speaker}  —  {cue}',11,True)
 label.paragraph_format.keep_with_next=True
 label.paragraph_format.space_before=Pt(5)
 add(speech)

doc.core_properties.title='BatStateU Academic Insights Taglish Presentation Script'
doc.core_properties.author='Vince A. Mendoza and Ronel Lance Malata'
doc.core_properties.subject='BAT 405 two-person dashboard presentation'
final=OUT/'BAT405_Taglish_Dashboard_Script_Vince_and_Ronel.docx'
doc.save(final)
counts={name:sum(len(speech.split()) for speaker,_,speech in turns if speaker==name) for name in ['VINCE','RONEL']}
(OUT/'qa/script_check.json').write_text(json.dumps({'spoken_words':sum(counts.values()),'speaker_words':counts,'turns':len(turns)},indent=2),encoding='utf-8')
print(final)
print(counts)
