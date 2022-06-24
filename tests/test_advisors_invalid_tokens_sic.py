##########################
# Test script to check for advisors that don't have _sic or _second_in_command in their SIC idea tokens
# By Pelmen, https://github.com/Pelmen323
##########################
from ..test_classes.generic_test_class import ResultsReporter
from ..test_classes.characters_class import Characters, Advisors


def test_check_advisors_invalid_costs(test_runner: object):
    advisors = Characters.get_all_advisors(test_runner=test_runner)
    results = []

    for advisor_code in advisors:
        adv = Advisors(adv=advisor_code)

        # Idea token check
        if adv.token is None:
            results.append((advisor_code, "Missing advisor token"))

        if adv.sic_role:
            if "_sic" not in adv.token and "_second_in_command" not in adv.token:
                results.append((adv.token, "SIC - should have '_sic' or '_second_in_command' in idea token"))

    ResultsReporter.report_results(results=results, message="Advisors that don't have _sic or _second_in_command in their SIC idea tokens were encountered. Check console output")
