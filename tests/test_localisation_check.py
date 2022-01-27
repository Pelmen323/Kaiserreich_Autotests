##########################
# Word seeker program. Finds all matches and prints where they were found
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
from .imports.bad_words import bad_words    # Dict with wrong_word : right_word. Bad versions are keys in the dict
from .imports.file_functions import open_text_file
import string


def test_find_bad_words(test_runner: object):
    filepath = f'{test_runner.full_path_to_mod}localisation\\'
    file_to_skip = f'{filepath}english\\play_in_english_l_braz_por.yml'
    typo_list = []
    for filename in glob.iglob(filepath + '**/*.yml', recursive=True):        # Recursive opening of all yml files in folder and subfolders
        if filename == file_to_skip:
            continue
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            print(f'Skipping the file {filename}')
            print(ex)
            continue

        for symbol in text_file:
            if symbol in string.punctuation:
                text_file = text_file.replace(symbol, ' ')

        text_file = text_file.lower().split("\n")
        for line_index, line in enumerate(text_file):
            for word in line.split(' '):
                if word in bad_words.keys():
                    typo_list.append(f'File {filename} -- "{word}" in line {line_index + 1} - correct is "{bad_words.get(word)}"')

    if typo_list != []:
        for i in typo_list:
            print(f'- [ ] {i}')
        print(f'{len(typo_list)} localisation issues found.')
        raise AssertionError("Typos were encountered! Check console output")
