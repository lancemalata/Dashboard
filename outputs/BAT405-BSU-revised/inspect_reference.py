from zipfile import ZipFile
from lxml import etree as E
from docx import Document
from pathlib import Path
import hashlib
p=Path(__file__).parent/'reference.docx'
z=ZipFile(p);ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
d=E.fromstring(z.read('word/document.xml'))
print('HASH',hashlib.sha256(p.read_bytes()).hexdigest())
print('SECTION',E.tostring(d.find('.//w:sectPr',ns)).decode())
for name in ['word/_rels/header2.xml.rels','word/_rels/header1.xml.rels','word/_rels/header3.xml.rels']:
 print(name,z.read(name).decode())
for i in [1,2,3]:
 x=E.fromstring(z.read(f'word/header{i}.xml'))
 print('HEADER',i,'shape attributes',[(el.tag,dict(el.attrib)) for el in x.iter() if E.QName(el).localname in ['shape','imagedata','anchor','extent','positionH','positionV']])
styles=E.fromstring(z.read('word/styles.xml'))
print('NORMAL',E.tostring(styles.xpath('//w:style[@w:styleId="Normal"]',namespaces=ns)[0]).decode())
print('SETTINGS',z.read('word/settings.xml').decode()[-2200:])
print('PARAGRAPH_FORMAT',[(i, E.tostring(el.find('w:pPr',ns)).decode() if el.find('w:pPr',ns) is not None else '') for i,el in enumerate(d.findall('w:body/w:p',ns)[:25])])
for name in z.namelist():
 if name.startswith('word/media/') and name.endswith(('.png','.jpeg','.jpg')):
  (p.parent/'qa'/Path(name).name).write_bytes(z.read(name))
