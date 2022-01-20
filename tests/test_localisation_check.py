##########################
# Word seeker program. Finds all matches and prints where they were found
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
from .imports.bad_words import bad_words    # Dict with wrong_word : right_word. Bad versions are keys in the dict
from .imports.file_functions import open_text_file
import string
import pytest
from timeit import default_timer as timer
PATH_TO_MOD = "C:\\Users\\VADIM\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\Kaiserreich Dev Build"
FILEPATH_LOCALIZATION = f"{PATH_TO_MOD}\\localisation\\"


@pytest.mark.parametrize("filepath", [(FILEPATH_LOCALIZATION)])
def test_find_bad_words(filepath: str):
    print("The test is started. Please wait...")
    start = timer()
    typo_list = []
    for filename in glob.iglob(filepath + '**/*.yml', recursive=True):        # Recursive opening of all yml files in folder and subfolders
        if filename == f"{FILEPATH_LOCALIZATION}english\\play_in_english_l_braz_por.yml":
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
        for error in typo_list:
            print(error)
        raise AssertionError("Typos were encountered! Check console output")
    end = timer()
    print(f"The test is finished in {end-start} seconds!")
