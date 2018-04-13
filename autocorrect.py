import os
import glob
import re
import collections
from time import gmtime, strftime

import spellchecker


def load_word_model():
    compile_text('./GDC/', './autocorrect-reference.txt')

    word_model = spellchecker.train(open('/usr/share/dict/words').read())
    real_words = set(word_model)

    combined_model = spellchecker.train(
        open('./medical-words.txt').read(), model=word_model)
    combined_words = set(combined_model)

    texts = ['./autocorrect-reference.txt']
    combined_model = spellchecker.train_from_files(texts, combined_model)

    return combined_model, combined_words


def get_folders(pathname):
    return [x[0] for x in os.walk(pathname)]


def get_pdf_path(pathname):
    return glob.glob(pathname + '/*.pdf')


def check_text_file(filename):
    temp_text_file = filename.replace('.pdf', '.txt')
    return os.path.isfile(temp_text_file)


def check_edited_text_file(filename):
    temp_text_file = filename.replace('.pdf', '-EDITED.txt')
    return os.path.isfile(temp_text_file)


def compile_text(datapath, destpath):
    text = ''
    total_folders = len(get_folders(datapath))
    for i, folder in enumerate(get_folders(datapath)):
        pdf_path_list = get_pdf_path(folder)
        if len(pdf_path_list) == 1:
            if check_text_file(pdf_path_list[0]):
                temp_text = open(pdf_path_list[0].replace('.pdf', '.txt'), "r")
                text = text + temp_text.read() + '\n'
                temp_text.close()
    final_text = open(destpath, 'w')
    final_text.write(text)
    final_text.close()


def correct_word(word, real_words, model):
    suggestions = spellchecker.suggestions(
        word, real_words, short_circuit=False)
    best = spellchecker.best(word, suggestions, word_model=model)
    #print('Word: ' + word)
    #print('Suggestions: ' + str(suggestions))
    #print('Best: ' + str(best))
    return best


def correct_document(pathname, model, dict_words):
    text_file = open(pathname, 'r')
    text = text_file.read()
    text_file.close()
    words = text.split()
    words_count = collections.Counter(words)
    for word in words:
        word = word.rstrip(',.:')
        if len(word) > 3 and len(word) < 10 and re.search('[A-z]', word) and '---' not in word:
            if word not in list(dict_words) and words_count[word] < 2:
                fixed_word = correct_word(word, dict_words, model)
                if 'NO SUGGESTION' not in fixed_word and word.lower() not in fixed_word.lower():
                    # print(word)
                    # print(fixed_word)
                    text = text.replace(word, fixed_word)
    final_text = open(pathname.replace('.txt', '-EDITED.txt'), 'w')
    final_text.write(text)
    final_text.close()


def autocorrect(pathname):
    model, dict_words = load_word_model()
    total_folders = len(get_folders(pathname))
    for i, folder in enumerate(get_folders(pathname)):
        pdf_path_list = get_pdf_path(folder)
        if len(pdf_path_list) == 1:
            print(str(i) + '/' + str(total_folders) + ' - ' + strftime("%H:%M:%S", gmtime()) +
                  ' - ' + pdf_path_list[0])
            if check_text_file(pdf_path_list[0]) and not check_edited_text_file(pdf_path_list[0]):
                correct_document(pdf_path_list[0].replace(
                    '.pdf', '.txt'), model, dict_words)


##model, words = load_word_model()
#correct_word('lymph', words, model)
#correct_document('./GDC/1d1ed8c6-e859-47d4-ad91-cd00c98f63bd/TCGA-20-1684.3ce61823-9e89-424f-9ce2-a8987420b2a9.txt', model, dict_words)
autocorrect('./GDC/')
