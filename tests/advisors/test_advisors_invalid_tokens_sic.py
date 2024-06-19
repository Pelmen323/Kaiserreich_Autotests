##########################
# Test script to check for advisors that don't have _sic or _second_in_command in their SIC idea tokens
# By Pelmen, https://github.com/Pelmen323
##########################
import pytest
from test_classes.characters_class import Advisors, Characters
from test_classes.generic_test_class import ResultsReporter


@pytest.mark.kr_specific
def test_check_advisors_invalid_sic_tokens(test_runner: object):
    advisors = Characters.get_all_advisors(test_runner=test_runner)
    results = []

    for advisor_code in advisors:
        adv = Advisors(adv=advisor_code)

        if adv.sic_role:
            if "_sic" not in adv.token and "_second_in_command" not in adv.token:
                results.append(f"{adv.token} - missing '_sic' or '_second_in_command' in this SIC idea token")

    ResultsReporter.report_results(results=results, message="SIC idea tokens should contain _sic or _second_in_command")
