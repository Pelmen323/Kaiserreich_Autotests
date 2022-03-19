##########################
# Test script to check for sic having invalid traits
# By Pelmen, https://github.com/Pelmen323
##########################
import re
from ..test_classes.generic_test_class import FileOpener, DataCleaner, ResultsReporter
from ..test_classes.characters_class import Characters


def test_check_advisors_sic_invalid_traits(test_runner: object):
    advisors, paths = Characters.get_all_advisors_with_paths(test_runner=test_runner, lowercase=True)
    advisor_traits = Characters.get_all_sic_traits(test_runner=test_runner, lowercase=True)
    results = []
    print(advisor_traits)        
    for adv in advisors:
        if adv.count('slot = second_in_command') > 0:
            try:
                advisor_name = re.findall('idea_token = (\w*)', adv)[0]
            except:
                results.append((adv, paths[adv], f'Missing idea_token'))
            invalid_trait_syntax = len(re.findall('traits = \\{\\n', adv)) > 0
            one_trait = re.findall('traits = \{ (\w*) \}', adv)
            two_traits = re.findall('traits = \{ (\w*) (\w*) \}', adv)
            if invalid_trait_syntax:
                 results.append((advisor_name, paths[adv], f'This SIC trait syntax is multiline - single-line syntax is strongly recommended'))
            elif one_trait != []:
                if 'second_in_command_trait' not in one_trait:
                    results.append((advisor_name, paths[adv], f'This SIC is missing second_in_command_trait trait'))
            elif two_traits != []:
                if 'second_in_command_trait' not in two_traits[0]:
                    results.append((advisor_name, paths[adv], f'This SIC is missing second_in_command_trait trait'))
                for trait in two_traits[0]:
                    if trait not in advisor_traits:
                        results.append((advisor_name, paths[adv], f'Invalid SIC trait encountered - {trait}'))

    if results != []:
        ResultsReporter.report_results(results=results, message="SIC without second_in_command_trait trait encountered. Check console output")
