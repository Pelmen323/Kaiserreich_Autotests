##########################
# Test script to check for advisors having invalid ledger line
# By Pelmen, https://github.com/Pelmen323
##########################
from test_classes.characters_class import Advisors, Characters
from test_classes.generic_test_class import ResultsReporter


def test_check_advisors_invalid_ledger(test_runner: object):
    advisors = Characters.get_all_advisors(test_runner=test_runner)
    results = []

    for advisor_code in advisors:
        adv = Advisors(adv=advisor_code)

        if adv.has_not_already_hired:
            if adv.slot != adv.not_already_hired_slot:
                results.append((adv.token, f'Slot - {adv.slot}', f'Not already hired - {adv.not_already_hired_slot}'))

    ResultsReporter.report_results(results=results, message="Advisors with non-matching slot and `not_already_hired_except_as` slot encountered. Check console output")
