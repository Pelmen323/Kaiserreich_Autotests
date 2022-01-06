##########################
# Word seeker program. Finds all matches and prints where they were found
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
from .bad_words import bad_words                                                                             # Dict with wrong_word : right_word. Bad versions are keys in the dict
import string
import pytest
PATH_TO_MOD = f"{os.environ.get('USERPROFILE')}\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\Kaiserreich Dev Build"
FILEPATH_LOCALIZATION = f"{PATH_TO_MOD}\\localisation\\"


@pytest.mark.parametrize("filepath", [(FILEPATH_LOCALIZATION)])
def test_find_bad_words(filepath: str):
    print("The test is started. Please wait...")
    typo_list = []
    for filename in glob.iglob(filepath + '**/*.yml', recursive=True):                                      # Recursive opening of all yml files in folder and subfolders
        if filename == f"{FILEPATH_LOCALIZATION}english\\play_in_english_l_braz_por.yml":
            continue
        try:
            with open(filename, 'r', encoding='utf-8-sig') as text_file:                                    # 'utf-8-sig' is mandatory for UTF-8 w/BOM
                text_file = text_file.read()
        except Exception as ex:
            print(f'Skipping the file {filename}')                                                              
            print(ex)
            continue
                                                                                                                    
        for i in text_file:                                                                                 # Remove all punctuation from the text
            if i in string.punctuation:
                text_file = text_file.replace(i, ' ')

        text_file = text_file.lower().split("\n")                                                           # Split the text by the lines
        for i, line in enumerate(text_file):                                                                # For line index and line text in enumerate(text) - returns line index and line contents
            for word in line.split(' '):                                                                    # For each word in splitted line (splitting by whitespaces)
                if word in bad_words.keys():
                    typo_list.append(f'File {filename} -- "{word}" in line {i+1} - correct is "{bad_words.get(word)}"')
    
    if typo_list != []:
        for error in typo_list:
            print(error)
        raise AssertionError("Typos were encountered! Check console output")
    print("The test is finished!")

if __name__=='__main__':
    test_find_bad_words(FILEPATH_LOCALIZATION)
    input('Press any key to exit')
