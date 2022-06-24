##########################
# By Pelmen, https://github.com/Pelmen323
# Only to be run via pytest due to relative imports errors
##########################
import re
import copy
from ..test_classes.generic_test_class import FileOpener
from ..test_classes.characters_class import Characters, Advisors
import logging


def test_replace_char_raw_names_with_keys(test_runner: object):
    """Function to:
    1. Check all characters and detect if their names are raw str
    2. Replace raw str with leys
    3. Print key: str pairs that should be added to loc files

    Args:
        test_runner (_type_): test runner obj that contains filepath
    """
    path_to_character_files = f'{test_runner.full_path_to_mod}common\\characters\\'
    lines_to_replace = {}
    advisors = Characters.get_all_advisors(test_runner=test_runner, lowercase=False)

    for advisor_code in advisors:
        adv = Advisors(adv=advisor_code)

        if adv.sic_role:
            if "_sic" not in adv.token and "_second_in_command" not in adv.token:
                # advisor_code_copy = copy.copy(advisor_code)
                x = f'idea_token = {adv.token}'
                y = f'idea_token = {adv.token}_sic'
                to_replace = advisor_code
                to_replace_with = advisor_code.replace(x, y)
                lines_to_replace[to_replace] = to_replace_with

    # Replace name lines with newly generated ones
    FileOpener.replace_all_keys_in_file_with_values(path_to_files=path_to_character_files, dict_with_strings_to_replace=lines_to_replace, lowercase=False)
    for key, value in lines_to_replace.items():
        print(f'{key} - replaced with {value}')
