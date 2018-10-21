from time import time
from random import randint
from difflib import get_close_matches
from datetime import datetime


# appends current run date in 'datelog' file
def date_log():
    with open('datelog', 'a', encoding='cp1253') as datefile:
        datefile.write(str(datetime.now().replace(microsecond=0)) + '\n')


# reads a file and dumps content on a list of ints
# splitr defines the split character (if any)
# and column defines the column to append on the list column=0 -> 1st column
def file_to_list(filename, splitr='', column=0, char_thold=0, cast_to_int=False):

    with open(filename, 'r', encoding='cp1253') as processing_file:
        if splitr == '':
            if cast_to_int is False:
                return [str(line).strip('\n') for line in processing_file.readlines() if len(str(line).strip('\n')) > char_thold]
            elif cast_to_int is True:
                return [int(str(line).strip('\n')) for line in processing_file.readlines() if len(str(line).strip('\n')) > char_thold]
        else:
            if cast_to_int is False:
                return [str(line.split(str(splitr)[column])).strip('\n') for line in processing_file.readlines() if len(str(line)) > char_thold]
            elif cast_to_int is True:
                return [int(str(line.split(str(splitr))[column]).strip('\n')) for line in processing_file.readlines() if len(str(line)) > char_thold]


# writes a list to a given file
def list_to_file(filename, mode, alist):
    with open(filename, str(mode), encoding='cp1253') as processing_file:
        if isinstance(alist, str):
            processing_file.write(str(alist) + '\n')
        elif isinstance(alist, list):
            for i in range(len(alist)):
                processing_file.write(''.join(str(alist[i]).strip('[]\'')) + '\n')


# pretty much a useless function
def rand_file(no_of_files):
    return randint(1, no_of_files)


# inputs a list, returns a random number 0 <= number <= lenlist
def rand_word(inlist):
    word_index = randint(1, len(inlist))
    word = inlist[word_index - 1]
    return word, word_index


def used_checker():
    try:
        open(used_words, 'x')
    except FileExistsError:
        return False


# check for files
def file_checker(filename, filerange):
    for index in range(0, filerange):
        try:
            open(filename + str(index+1), 'r', encoding='cp1253')
        except FileNotFoundError:
            return False
    return index+1 == filerange


# return split boundaries
def file_boundaries(alist, filerange):
    if filerange == 1:
        startf = 0
        endf = len(alist)
    else:
        splitlines = len(alist) // filerange
        startf = [i*splitlines for i in range(0, filerange)]
        endf = [(i+1)*splitlines - 1 for i in range(0, filerange)]
    return startf, endf


# creates files with certain incremental name
def file_create(alist, outfile, startf, endf):
    strt = time()

    print("[x] One or more files are missing...\n")
    print("[*] Creating files...")
    print("[*] This may take a few moments...\n")

    for i in range(0, len(start)):
        file_splitter(alist, startf[i], endf[i], outfile + str(i+1))
        print('[*] File {0} of {1} created'.format(i+1, len(start)))

    print('\n[@] file creation execution time: {}s'.format(time() - strt))


def file_splitter(alist, startl, stopl, outfile):
    with open(outfile, '+w', encoding='cp1253') as edit:
        for line in range(startl, stopl):
            edit.write(alist[line] + '\n')


def alts(alist, word_in_alist, indx, usd_flname):
    alt = []
    alt_indx = []

    alt.append(get_close_matches(word_in_alist, alist[indx-5:indx+6], 10, 0.85))

    alt = [item for sublist in alt for item in sublist if item is not word_in_alist]

    for i in range(len(alt)):
        if alt[i] in alist:
            alt_indx.append(alist.index(alt[i])+1)

    alt_words_printable = []
    for i in range(len(alt_indx)):
        alt_words_printable.append(str(alt_indx[i]) + ' ' + str(random_file))

    lst_ch(len(alt), alt)
    list_to_file(usd_flname, 'a', alt_words_printable)
    return alts


# print alts on screen
def lst_ch(length, lst):
    if length:
        print('\nΆλλες {0} λέξεις της ίδιας ομάδας: {1}'.format(length, lst[0]))
        for i in range(1, length):
            print('\t\t\t\t\t\t\t\t {0}'.format(lst[i], ''.join(str(lst).strip('[]\''))))

    else:
        print('Δε βρέθηκαν παρόμοιες λέξεις...')


random_file = -1


if __name__ == '__main__':
    timestamp0 = time()

    # default filenames
    used_words = 'used_words'   # used words filename
    dic_filename = 'el_gr.dic'  # dictionary filename
    dic_split_filenames = 'dic_gr_part_'    # name of splitted files
    no_of_dic_split = 6     # initial file will get split in x pieces
    char_threshold = 2      # eliminate words equal to or less than x characters long from the dictionary

    date_log()
    used_checker()

    dictionary = file_to_list(dic_filename, char_thold=int(char_threshold))

    # check for files
    start, end = [], []
    if file_checker(dic_split_filenames, no_of_dic_split) is False:
        start, end = file_boundaries(dictionary, no_of_dic_split)
        file_create(dictionary, dic_split_filenames, start, end)
    else:
        start, end = file_boundaries(dictionary, no_of_dic_split)
        print("\n[*] All files found...\n\n")

    # pick random file
    random_file = rand_file(no_of_dic_split)

    # load random file to mem
    dic_file_list = file_to_list(str(dic_split_filenames) + str(random_file))

    # save used words of respective files to memory
    used_words_index = file_to_list(used_words, splitr=' ', column=0, cast_to_int=True)
    used_words_file = file_to_list(used_words, splitr=' ', column=1, cast_to_int=True)

    while True:
        word, word_indx = rand_word(dic_file_list)

        if word_indx in used_words_index and used_words_file[used_words_index.index(word_indx)] == random_file:
            continue
        else:
            used_words_index.append(word_indx)
            used_words_file.append(random_file)
            used_words_printable = [(str(used_words_index[i]) + ' ' + str(used_words_file[i]) + ' ') for i in range(len(used_words_file))]
            list_to_file(used_words, 'a', used_words_printable)
            break

    print('Random word: {}' .format(word))
    alts(dic_file_list, word, word_indx, used_words)
    print('\n\n[*] total execution time: {}s'.format(time() - timestamp0))
