##########################
# Test script to check for advisors that have incorrect costs
# By Pelmen, https://github.com/Pelmen323
##########################
from ..test_classes.characters_class import Advisors, Characters
from ..test_classes.generic_test_class import ResultsReporter

FALSE_POSITIVES_TOKENS = ["pol_andrzej_wierbicki", "pol_henryk_ehrlich", "csa_eleanor_roosevelt", "nee_", "shx_"]
FALSE_POSITIVES_TRAITS = ["kr_plodding_bureaucrat"]


def test_check_advisors_invalid_costs(test_runner: object):
    advisors = Characters.get_all_advisors(test_runner=test_runner)
    results = []

    for advisor_code in advisors:
        adv = Advisors(adv=advisor_code)

        # Idea token check
        if adv.token is None:
            results.append((advisor_code, "Missing advisor token"))

        # Exclude advisors that have tokens included in false positives
        if [i for i in FALSE_POSITIVES_TOKENS if i in adv.token]:
            continue

        # Exclude advisors that have traits included in false positives
        if [i for i in FALSE_POSITIVES_TRAITS if i in adv.traits]:
            continue

        # Costs check - military
        if adv.military_role and not adv.theorist_role:
            if adv.military_trait_lvl == "specialist" and adv.cost != 50:
                results.append((adv.token, f"Specialist level - should cost 50, but got {adv.cost}"))
            elif adv.military_trait_lvl == "expert" and adv.cost != 100:
                results.append((adv.token, f"Expert level - should cost 100, but got {adv.cost}"))
            elif adv.military_trait_lvl == "genius" and adv.cost != 200:
                results.append((adv.token, f"Genius level - should cost 200, but got {adv.cost}"))
            elif adv.military_trait_lvl is None:
                results.append((adv.token, f"Unknown advisor level - got {adv.cost} cost"))

        # Costs check - theorists
        elif adv.theorist_role:
            if adv.special_theorist and adv.cost != 150:
                results.append((adv.token, f"Special theorist - should cost 150, but got {adv.cost}"))
            elif not adv.special_theorist and adv.cost != 100:
                results.append((adv.token, f"Non-special theorist - should cost 100, but got {adv.cost}"))

        # Costs check - SIC
        elif adv.sic_role:
            if adv.cost != 0:
                results.append((adv.token, f"SIC - should have 'cost = 0' line, but got {adv.cost}"))
            elif adv.sic_has_correct_removal_cost is False:
                results.append((adv.token, "SIC - should have 'can_be_fired = no' line"))

        # Costs check - political advisor
        elif adv.political_role:
            if adv.cost != 150 and adv.cost != 0:
                results.append((adv.token, f"Political advisor - should cost 150, but got {adv.cost}"))

        # Unknown role check
        elif adv.unknown_role:
            results.append((adv.token, "Unknown advisor type"))

    ResultsReporter.report_results(results=results, message="Issues with advisors were encountered. Check console output")
