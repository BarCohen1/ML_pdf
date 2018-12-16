import csv
import time
from pdfminer.pdfdocument import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter  # process_pdf
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
import re
import tabula
import os
PROBLEM_SOLVING = 'problem solving'
TROUBLE = "troubleshooting"
PROBLEM = "problem"
# problems = []
# solutions = []
# both = set()
total_errs = 0

Namers = []




class Namer:
    main_category = ""
    sub_category = ""
    comp = ""
    id = ""
    problems = set()
    solutions = set()
    both = set()

    def __init__(self, fileName):
        self.parse_fileName(fileName)

    def parse_fileName(self, fileName):
        self.main_category, self.sub_category , self.comp, self.id = fileName.split("א")



def find_By_g(curNamer, txt):
    r5 = r"(^no\s.*)"
    r6 = r"(^problem:\s.+)"
    r7 = r"(^.*cannot\s.+)"
    r8 = r"(^.*does not work\s.+)"
    r9 = r"(^i\s.*)"
    r10 = r"(^.*do not\s.+)"
    r1 = r"^[g,•,-]\s(.+)"
    r2 = r"^\d.\s+(.+)"
    r3 = r"^\(cid:[\d]*\)\s+(.+)"

    for i in [r1,r2,r3,r5,r6,r7,r8,r9,r10]:
        matches = re.finditer(i, txt, re.MULTILINE)
        for matchNum, match in enumerate(matches):
            if len(match.groups()) >= 1 and len(match.group(1))> 8:
                # print('***********************************')
                if i in [r5,r6,r7,r8,r9]:
                    # print('found prob ' + match.group(0))
                    curNamer.problems.add(match.group(0))
                elif i in [r10]:
                    # print('found prob or solution ' + match.group(0))
                    curNamer.both.add(match.group(0))
                else:
                    curNamer.solutions.add(match.group(1))
                    # print('found sol ' + match.group(0))


    # matches = re.finditer(r2, txt, re.MULTILINE)
    # for matchNum, match in enumerate(matches):
    #     print('***********************************')
    #     if len(match.groups()) >= 1:
    #         probs.append(match.group(1))
    #         print('found prob ' + match.group(1))
    #
    #     if len(match.groups()) >= 2:
    #         sols.append(match.group(2))
    #         print('found sols ' + match.group(2))

def is_trouble_in(content):
    """using a simple regex to get the pdf troubleshooting segment"""
    # maybe work with trie?
    cur_trobule_section = ""
    for m in re.finditer(TROUBLE, content):
        # huristca trying to find problem\answer section after troubleshooting
        cur_trobule_section = ""
        try:
            cur_trobule_section = content[m.end():(m.end()+3000)] # say 2000 chars?
            problem_index = cur_trobule_section.index('problem') # found problem word
            #cur_trobule_section = cur_trobule_section[m.start():(m.end()+3000)]

            print('troubleshooting + problem found', problem_index, m.end()+2000)
            return cur_trobule_section # section is suspect of being trouble-shooting
            # assume there is only one trouble shooting section
        except ValueError: # got a bad value
            continue
        except IndexError: # we reached the end of the file
            return cur_trobule_section

def create_csv(name):
    # given a matrix with lists of author, pdf title and top 15 terms, create csv according to name param
    with open(name, 'w',  encoding="utf-8") as csvfile: # creating appropriate csv
        filewriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        if name == "problems":
            filewriter.writerow(["category", "sub category", "company", "product id", "problem"])
        elif name == "solutions":
            filewriter.writerow(["category", "sub category", "company", "product id", "solution"])
        else :
            filewriter.writerow(["category", "sub category", "company", "product id", "both"])

        # for row in matrix: # write rows to csv
        for namer in Namers:
            if name == "problems":
                for problem in namer.problems:
                    filewriter.writerow([namer.main_category, namer.sub_category , namer.comp, namer.id, problem])
            elif name == "solutions": # solutions
                for solution in namer.solutions:
                    filewriter.writerow([namer.main_category, namer.sub_category , namer.comp, namer.id, solution])
            else:
                for unknown in namer.both:
                    filewriter.writerow([namer.main_category, namer.sub_category, namer.comp, namer.id, unknown])



def pdf_to_text(pdfname):
    """ main fucntion of this file. attempts to take a pdf file path, turn it into python string while also trying to find
    the troubleshooting segment of that pdf, returns string values in either case (when failing, returns empty string)"""
    rsrcmgr = PDFResourceManager()
    sio = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, sio, codec='utf-8', laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    shooting_section = ""
    try:
    # Extract text
        trouble_shoot_dict = set()
        start_time = time.time()
        fp = open("pdfs/batch4/"+pdfname, 'rb')
        # str_pdf = ""
        for page in PDFPage.get_pages(fp):
            interpreter.process_page(page)
            elapsed_time = time.time() - start_time
            print(elapsed_time)
            if elapsed_time >= 60:
                print('running for too long, exiting this file')
                raise Exception

        str_pdf = sio.getvalue()
        str_pdf = str(bytes(str_pdf, 'utf-8').decode('utf-8','ignore'))
        # str_pdf = str(str_pdf.replace('\r', '').replace('\n', '').replace('\f', '').lower())
        str_pdf = str(str_pdf.replace('\r', '').replace('\f', '').lower())
        shooting_section = is_trouble_in(str_pdf)
        if shooting_section:
        # Cleanup
            device.close()
            sio.close()
            print('returning shooting')
            return shooting_section
        print('return none')

    except:
        print('execption in pdf parse')
        if shooting_section:
            print('returning shooting_section')
            return shooting_section
        else:
            return ""

def iter_over_folder(encoding):
    directory = "C:/Users/Bar/PycharmProjects/pdf_parser/trouble/renamed/"
    for filename in os.listdir(directory):
            try:
                f = open(directory+filename, 'r')
                txt = f.read()
                # txt.replace('\n', ' ')
                find_By_g(filename, txt)
            except:
                global total_errs
                total_errs+=1
                continue
# for encoding in ["ascii" , "cp862", "utf_8" , "utf_16", "", "cp424", "cp856" , "cp1255", "iso8859_8"]:
iter_over_folder("")
print(total_errs)
# create_csv("problems")
# create_csv("solutions")
# create_csv("both")

# print(len(both))
# print(len(problems))
# print(len(solutions))
