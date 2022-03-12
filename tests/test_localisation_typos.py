##########################
# Word seeker program. Finds all matches and prints where they were found
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
from ..data.bad_words import bad_words    # Dict with wrong_word : right_word. Bad versions are keys in the dict
import string
from ..test_classes.generic_test_class import FileOpener, DataCleaner, ResultsReporter


def test_find_bad_words(test_runner: object):
    filepath = f'{test_runner.full_path_to_mod}localisation\\'
    file_to_skip = f'{filepath}play_in_english_l_braz_por.yml'
    typo_list = []
    for filename in glob.iglob(filepath + '**/*.yml', recursive=True):        # Recursive opening of all yml files in folder and subfolders
        if filename == file_to_skip:
            continue
        text_file = FileOpener.open_text_file(filename)

        for symbol in text_file:
            if symbol in string.punctuation:
                text_file = text_file.replace(symbol, ' ')

        text_file = text_file.lower().split("\n")
        for line_index, line in enumerate(text_file):
            for word in line.split(' '):
                if word in bad_words.keys():
                    typo_list.append(f'File {filename} -- "{word}" in line {line_index + 1} - correct is "{bad_words.get(word)}"')

    ResultsReporter.report_results(results=typo_list, message="Typos were encountered. Check console output")
