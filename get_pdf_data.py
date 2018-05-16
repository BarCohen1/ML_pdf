from pdfminer.pdfdocument import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter  # process_pdf
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
import re

import ahocorasick
PROBLEM_SOLVING = 'problem solving'
TROUBLE = "troubleshooting"
PROBLEM = "problem"

def is_trouble_in(content):
    # maybe work with trie?
    for m in re.finditer(TROUBLE, content):
        # huristca trying to find problem\answer section after troubleshooting
        try:
            cur_trobule_section = content[m.end():(m.end()+2000)] # say 2000 chars?
            cur_trobule_section.index('problem') # found problem word
            print('troubleshooting + problem found', m.start(), m.end())
            return cur_trobule_section # section is suspect of being trouble-shooting
            # assume there is only one trouble shooting section
        except ValueError:
            continue
        except IndexError:
            break

def pdf_to_text(pdfname):

    rsrcmgr = PDFResourceManager()
    sio = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, sio, codec='utf-8', laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    try:
    # Extract text
        trouble_shoot_dict = set()
        fp = open("pdfs/"+pdfname, 'rb')
        # str_pdf = ""
        for page in PDFPage.get_pages(fp):
            interpreter.process_page(page)
        str_pdf = sio.getvalue()
        str_pdf = str(bytes(str_pdf, 'utf-8').decode('utf-8','ignore'))
        # str_pdf = str(str_pdf.replace('\r', '').replace('\n', '').replace('\f', '').lower())
        str_pdf = str(str_pdf.replace('\r', '').replace('\f', '').lower())
        shooting_section = is_trouble_in(str_pdf)
        # Cleanup
        device.close()
        sio.close()

    except:
        str_pdf = ''
        shooting_section = ''

    return str_pdf, shooting_section

def get_title(filename):
    from pdfminer.pdfparser import PDFParser
    from pdfminer.pdfdocument import PDFDocument

    fp = open(filename, 'rb')
    parser = PDFParser(fp)
    doc = PDFDocument(parser)
    print (doc.info)  # The "Info" metadata
    fp.close()