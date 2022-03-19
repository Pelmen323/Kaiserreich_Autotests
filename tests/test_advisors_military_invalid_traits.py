##########################
# Test script to check for military having invalid traits
# By Pelmen, https://github.com/Pelmen323
##########################
import re
from ..test_classes.generic_test_class import FileOpener, DataCleaner, ResultsReporter
from ..test_classes.characters_class import Characters


def test_check_advisors_military_invalid_traits(test_runner: object):
    advisors, paths = Characters.get_all_advisors_with_paths(test_runner=test_runner, lowercase=True)
    advisor_traits = Characters.get_all_military_traits(test_runner=test_runner, lowercase=True)
    results = []
    print(advisor_traits)        
    for adv in advisors:
        if adv.count('slot = theorist') > 0 or adv.count('slot = high_command') > 0 or adv.count('slot = army_chief') > 0 or adv.count('slot = air_chief') > 0 or adv.count('slot = navy_chief') > 0:
            try:
                advisor_name = re.findall('idea_token = (\w*)', adv)[0]
            except:
                results.append((adv, paths[adv], f'Missing idea_token'))
            invalid_trait_syntax = len(re.findall('traits = \\{\\n', adv)) > 0
            one_trait = re.findall('traits = \{ (\w*) \}', adv)
            if invalid_trait_syntax:
                 results.append((advisor_name, paths[adv], f'This advisor trait syntax is multiline - single-line syntax is strongly recommended'))
            elif one_trait != []:
                if one_trait[0] not in advisor_traits:
                    results.append((advisor_name, paths[adv], f'Invalid military trait encountered - {one_trait[0]}'))
            else:
                results.append((advisor_name, paths[adv], f'This advisor has <1 or >1 traits'))

    if results != []:
        ResultsReporter.report_results(results=results, message="Military advisors with invalid traits encountered. Check console output")
