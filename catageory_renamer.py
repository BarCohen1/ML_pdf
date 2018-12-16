import pickle
import re

import os
import requests
import htmlParser

PATH = "C:/Users/Bar/PycharmProjects/pdf_parser/trouble/now"

ALL_ENTRIES = ["fitness", "kitchen", "babycare", "caraudio", "cellphone", "audio", "laundry", "homeappliance", "outdoorcooking", "phone", "office", "music", "personalcare", "lawnandgarden", "cellphone", "portablemedia"]
MAIN_URL = "manualsonline.com/manuals/mfg"
All_FILE_HITS = []
FileNamerHolder = []


class FileNamer:
    org_name = ""
    re_comp = ""
    re_serial = ""
    main_category = ""
    sub_category = ""
    found_url = ""
    real_prodcut_comp = ""

    def __str__(self):
        return self.main_category + " " + self.sub_category + " " + self.real_prodcut_comp + " "


    def __cmp__(self, other):
        return str(self.org_name) == str(other.org_name) and self.re_comp == other.re_comp and self.main_category == other.main_category and self.sub_category == other.sub_category and self.real_prodcut_comp == other.real_prodcut_comp


    def __init__(self, file_name, comp, serial):
        self.org_name = file_name
        self.re_comp = comp
        self.re_serial = serial




def get_all_file_names():
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(PATH) if isfile(join(PATH, f))]
    return onlyfiles


def parse_file_name(file_name):
    match = re.match(r"([0-9])?([a-z]+_[0-9a-z_]+)", file_name, re.I)
    if match and len(match.groups()) >= 2:
        match_groups = match.groups()
        full_name_list = match_groups[1].rsplit('_', 1)
        if (full_name_list) and len(full_name_list) == 2:
            comp = full_name_list[0]
            serial = full_name_list[1]

            return FileNamer(file_name, comp, serial)

def find_url(fileNamer : FileNamer):
    for entrie in ALL_ENTRIES:
        for reverse in range(4):
            if reverse == 0:
                cur_url = "http://" + entrie + "." + MAIN_URL + "/" + fileNamer.re_comp + "/" + fileNamer.re_serial + ".html"
            else: cur_url = "http://" + entrie + "." + MAIN_URL + "/" + fileNamer.re_comp + "/" + fileNamer.re_serial[:-reverse] + ".html"
            ret = requests.get(cur_url)
            if (ret.status_code == 200 and ret.url == cur_url):
                fileNamer.found_url = cur_url
                print("hit")
                return True
    return False

def find_category(curFileNamer):
    ret = requests.get(curFileNamer.found_url)
    htmlParser.parse_and_return_FileNamer(curFileNamer, ret.text)

def rename_file(fileNamer):
    src = "C:/Users/Bar/PycharmProjects/pdf_parser/trouble/working_dir/"
    dst = fileNamer.main_category + "א" + fileNamer.sub_category + "א" + fileNamer.real_prodcut_comp + "א" + fileNamer.re_serial + ".txt"
    if fileNamer.org_name in os.listdir(src):
        try:
            os.rename(src + fileNamer.org_name, src + dst[:-4])
        except:
            print("damn")

    # ycharmProjects / pdf_parser / trouble / working_dir / "
    # src = "C:/Users/Bar/PycharmProjects/pdf_parser/trouble/working_dir/"
    # try:
    #      os.rename(src + fileNamer, src + fileNamer[:-4])
    # except:
    #      print("damn")


def find_all_file_categories(all_file_names):

    file_counter = 0
    total_hits = 0
    for file_name in all_file_names:
        file_counter += 1
        print("trying "+ str(file_counter) + "/" + str(len(all_file_names)))
        curFileNamer = parse_file_name(file_name)
        if curFileNamer:
            if find_url(curFileNamer):
                All_FILE_HITS.append(file_name)
                find_category(curFileNamer)
                if curFileNamer.main_category != "" and curFileNamer.sub_category != "":
                    total_hits += 1
                    FileNamerHolder.append(curFileNamer)

    print("total number of files iterated over: " + str(file_counter))
    print("total hits inc html parsing got: " + str(total_hits))


def write_all_found_hits_into_file():
    print("writing...")
    with open('all_file_hits.txt', 'w') as f:
        for item in All_FILE_HITS:
            f.write("%s\n" % item)

def read_hit_files():
    hit_files_names = []
    with open('all_file_hits.txt', 'r') as f:
        line = f.readline()
        while line:
            hit_files_names.append(line)
            line = f.readline()
    return hit_files_names

def dump_to_pickle():
    print("dumping total " + str(len(FileNamerHolder)) + "classes to pickle")
    with open("FileNamersClassTotal.pkl", 'wb') as f:
        pickle.dump(FileNamerHolder, f)

def read_from_pickle():
    pickle_off = open("FileNamersClassTotal.pkl", "rb")
    global FileNamerHolder
    FileNamerHolder = pickle.load(pickle_off)



if __name__ == '__main__':
    # start from zero
    # read_from_pickle()
    # all_file_names = get_all_file_names()
    # find_all_file_categories(all_file_names)
    # dump_to_pickle()

    # just rename from pickle
    read_from_pickle()
    # filenames = get_all_file_names()
    for filenamer in FileNamerHolder:
    # for filed in filenames:
        rename_file(filenamer)

    # read_from_pickle()
    # for fileName in FileNamerHolder:
    #     for fileName2 in FileNamerHolder:
    #         if fileName is not fileName2 and str(fileName) == str(fileName2):
    #             print("damn damn")
    #
    #


