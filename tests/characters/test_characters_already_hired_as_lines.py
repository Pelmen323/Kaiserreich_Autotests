##########################
# Test script to check for characters have already hired lines if having > 1 advisors roles
# By Pelmen, https://github.com/Pelmen323
##########################
import re

from test_classes.characters_class import Characters
from test_classes.generic_test_class import ResultsReporter

FALSE_POSITIVES = ['eth_', 'gbr_', 'asy_malik_qambar', 'can_john_bracken', 'can_robert_manion', 'sic_giovanni_messe',
                   'syr_sami_al_hinawi', 'irq_rashid_al_gaylani', 'irq_hashim_al_alawi', 'xsm_ma_hushan',
                   'chi_dai_chunfeng', 'gxc_chen_jiongming', 'qie_liu_menggeng', 'leb_fuad_chehab', 'chi_lixingshe',
                   'ukr_symon_petliura', 'spa_augusto_barcia_trelles', 'spa_manuel_azana_diaz', 'spa_niceto_alcala_zamora']


def test_check_characters_already_hired(test_runner: object):
    characters, paths = Characters.get_all_characters(test_runner=test_runner, return_paths=True)
    results = []

    for char in characters:
        char_name = re.findall('name = (.*)', char)[0]
        one_advisor_role = char.count('advisor = {') == 1
        two_advisor_roles = char.count('advisor = {') == 2
        three_advisor_roles = char.count('advisor = {') == 3
        sic_status = char.count('slot = second_in_command')
        not_already_hired_status = char.count('not_already_hired_except_as')

        if [i for i in FALSE_POSITIVES if i in char_name]:
            continue
        if one_advisor_role:
            if not_already_hired_status > 0:
                results.append((char_name, paths[char], "Character has 1 advisor role and has 'not_already_hired_except_as' line"))

        elif two_advisor_roles:
            if sic_status == 0:
                if not_already_hired_status < 2:
                    results.append((char_name, paths[char], "Character has 2 advisor roles but doesn't have 2 'not_already_hired_except_as' lines"))

            if sic_status == 1:
                if not_already_hired_status < 1:
                    results.append((char_name, paths[char], "Character has 2 advisor roles (including 1 sic role) but doesn't have 1 'not_already_hired_except_as' lines"))

        elif three_advisor_roles:
            if sic_status == 0:
                if not_already_hired_status < 3:
                    results.append((char_name, paths[char], "Character has 3 advisor roles but doesn't have 3 'not_already_hired_except_as' lines"))

            if sic_status == 1:
                if not_already_hired_status < 2:
                    results.append((char_name, paths[char], "Character has 3 advisor roles (including 1 sic role) but doesn't have 2 'not_already_hired_except_as' lines"))

        if sic_status > 1:
            results.append((char_name, paths[char], "Character has > 1 sic roles"))

    ResultsReporter.report_results(results=results, message="Issues with 'not_already_hired_except_as' lines were encountered. Check console output")
