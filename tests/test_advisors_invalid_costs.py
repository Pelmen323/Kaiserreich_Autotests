##########################
# Test script to check for advisors that have incorrect costs
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

        # Costs checks #
        # Costs check - military
        if adv.specialist_lvl:
            if adv.cost != 50:
                results.append((adv.token, f"Specialist level - should cost 50, but got {adv.cost}"))

        elif adv.expert_lvl:
            if adv.cost != 100:
                results.append((adv.token, f"Expert level - should cost 100, but got {adv.cost}"))

        elif adv.genius_lvl:
            if adv.cost != 200:
                results.append((adv.token, f"Genius level - should cost 200, but got {adv.cost}"))

        # Costs check - theorists
        elif adv.theorist_role:
            if adv.special_theorist:
                if adv.cost != 150:
                    results.append((adv.token, f"Special theorist - should cost 150, but got {adv.cost}"))
            else:
                if adv.cost != 100:
                    results.append((adv.token, f"Non-special theorist - should cost 100, but got {adv.cost}"))

        # Costs check - SIC
        elif adv.sic_role:
            if adv.cost != 0:
                results.append((adv.token, f"SIC - should have 'cost = 0' line, but got {adv.cost}"))
            if adv.sic_has_correct_removal_cost is False:
                results.append((adv.token, "SIC - should have 'removal_cost = -1' line"))

        # Unknown role check
        if adv.unknown_role:
            results.append((adv.token, "Unknown advisor type"))

    ResultsReporter.report_results(results=results, message="Issues with advisors were encountered. Check console output")