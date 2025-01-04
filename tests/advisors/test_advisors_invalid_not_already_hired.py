##########################
# Test script to check for advisors having invalid not_already_hired_as lines
# By Pelmen, https://github.com/Pelmen323
##########################
from test_classes.characters_class import Advisors, Characters
from test_classes.generic_test_class import ResultsReporter


def test_advisors_invalid_not_already_hired(test_runner: object):
    advisors = Characters.get_all_advisors(test_runner=test_runner)
    results = []

    for advisor_code in advisors:
        adv = Advisors(adv=advisor_code)

        if adv.not_already_hired:
            if adv.slot not in adv.not_already_hired:
                results.append(f'{adv.token} - slot {adv.slot} - has "not already hired as" check for {adv.not_already_hired} slot')

    ResultsReporter.report_results(results=results, message="When checking advisors with not_already_hired_except_as trigger, at least one checked slot should be equal to the advisor slot")
