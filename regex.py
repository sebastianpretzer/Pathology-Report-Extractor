import glob
import os
import re

import pathology_report


def load_text(pathname):
    with open(pathname, 'r') as myfile:
        data = myfile.read()

    return data


def get_regex_results(data):
    iter_results = re.finditer(
        '((\w*\s){1,3})(cancer|carcinoma|adenocarcinoma)', data.lower())

    results = [result.group(1).strip().replace(u'\xa0', u' ')
               for result in iter_results]
    print(results)


def regex_helper():
    with open('../Example Path Reports/6/google_text_0.txt', 'r') as myfile:
        data = myfile.read()  # .replace('\n', ' ')

    print(data)

    iter_results = re.finditer(
        '((\w*\s){0,3})(cancer|carcinoma|adenocarcinoma)', data.lower())

    results = [result.group().strip() for result in iter_results]

    print(results)


i = 0
print('%d:' % i)
get_regex_results(get_all_texts('Data/%d/' % i))
