##########################
# Test script to check for unused state flags
# If flag is not used via "has_state_flag" at least once, it will appear in test results
# Flags with values or variables (ROOT/THIS/FROM) should be added to false positives
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import pytest
import re
import os
from .imports.decorators import util_decorator_no_false_positives
from .imports.file_functions import open_text_file
FILEPATH = "C:\\Users\\VADIM\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\Kaiserreich Dev Build\\"


@pytest.mark.parametrize("filepath", [FILEPATH])
@util_decorator_no_false_positives
def test_check_retire_characters(filepath: str):
    results = {}
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            print(f'Skipping the file {filename}')
            print(ex)
            continue

        text_file_splitted = text_file.split('\n')
        for line in range(len(text_file_splitted)):
            current_line = text_file_splitted[line-1]
            if 'retire_character' in current_line:
                if 'effect_tooltip' not in current_line:
                    character_retires_in_line = re.findall('\t*retire_character.*', current_line)
                    if len(character_retires_in_line) > 0:
                        found_issue = character_retires_in_line[0].strip('\t').strip('}').strip()
                        results[f'{os.path.basename(filename)}, line {line}'] = found_issue

    if results != {}:
        print("Following characters should be retired with 'retire = yes'! Recheck them")
        for i in results.items():
            print(f'- [ ] {i}')
        print(f'{len(results)} times "retire_character" is used.')
        raise AssertionError("Characters retired with 'retire_character' were encountered, you should retire them with 'retire = yes'! Check console output")
