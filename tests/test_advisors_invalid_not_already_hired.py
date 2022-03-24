##########################
# Test script to check for advisors having invalid ledger line
# By Pelmen, https://github.com/Pelmen323
##########################
import re
from ..test_classes.generic_test_class import ResultsReporter
from ..test_classes.characters_class import Characters


def test_check_advisors_invalid_ledger(test_runner: object):
    advisors, paths = Characters.get_all_advisors(test_runner=test_runner, return_paths=True)
    results = []

    for adv in advisors:
        advisor_slot = re.findall('slot = (\\w*)', adv)
        not_already_hired_slot = re.findall('not_already_hired_except_as = (\\w*)', adv)
        advisor_name = re.findall('idea_token = (\\w*)', adv)

        if not_already_hired_slot != []:
            if advisor_slot != not_already_hired_slot:
                results.append((advisor_name, paths[adv], f'Slot - {advisor_slot}', f'Not already hired - {not_already_hired_slot}'))

    ResultsReporter.report_results(results=results, message="Advisors with non-matching slot and `not_already_hired_except_as` slot encountered. Check console output")
