##########################
# Test script to check for characters have already hired lines if having > 1 advisors roles
# By Pelmen, https://github.com/Pelmen323
##########################
import re
import glob
import os

from ..test_classes.characters_class import Characters
from ..test_classes.generic_test_class import FileOpener, ResultsReporter

FALSE_POSITIVES = ['eth_', 'gbr_', 'asy_malik_qambar', 'can_john_bracken', 'can_robert_manion', 'sic_giovanni_messe',
                   'syr_sami_al_hinawi', 'irq_rashid_al_gaylani', 'irq_hashim_al_alawi', 'xsm_ma_hushan',
                   'chi_dai_chunfeng', 'gxc_chen_jiongming', 'qie_liu_menggeng', 'leb_fuad_chehab']                     # convert to list if more added here


def test_check_characters_already_hired(test_runner: object):
    filepath = test_runner.full_path_to_mod
    characters, paths = Characters.get_all_characters(test_runner=test_runner, return_paths=True)
    raw_char_ids = Characters.get_all_characters_names(test_runner=test_runner)
    char_ids = []
    results = []

    ### 1. Chars that have country leader role
    for char in characters:
        if 'country_leader = {' in char:
            char_id = re.findall(r'^\t([^\t]*?) = \{', char)[0]
            char_ids.append(char_id)

    ### 2. Chars that get country leader role during the game
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if "add_country_leader_role = {" in text_file:
            target_code_block = re.findall(r'[^\{]*\{[^\{]*\{[^\{]*add_country_leader_role = {[^\n]*\n[^\n]*', text_file, flags=re.DOTALL | re.MULTILINE)
            for t in target_code_block:
                for c in raw_char_ids:
                    if c in t and c not in char_ids:
                        char_ids.append(c)

    ### 3. Chars that get military role during the game
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        for i in ["add_corps_commander_role", "add_field_marshal_role", "add_naval_commander_role"]:
            if i + " = {" in text_file:
                pattern = r'[^\{]*\{[^\{]*\{[^\{]*' + i + r' = {[^\n]*\n[^\n]*'
                target_code_block = re.findall(pattern, text_file, flags=re.DOTALL | re.MULTILINE)
                for t in target_code_block:
                    for c in char_ids:
                        if c in t and f'{c} - {i} - {os.path.basename(filename)}' not in results:
                            results.append(f'{c} - {i} - {os.path.basename(filename)}')

    ResultsReporter.report_results(results=results, message="Issues with 'not_already_hired_except_as' lines were encountered. Check console output")
