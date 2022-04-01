##########################
# Test script to check for advisors that have incorrect costs
# By Pelmen, https://github.com/Pelmen323
##########################
import re
from ..test_classes.generic_test_class import ResultsReporter
from ..test_classes.characters_class import Characters


def test_check_advisors_invalid_costs(test_runner: object):
    advisors = Characters.get_all_advisors(test_runner=test_runner)
    results = []
    special_theorists = (
        'kr_mobile_warfare_expert',
        'kr_superior_firepower_expert',
        'kr_grand_battle_plan_expert',
        'kr_mass_assault_expert',
        'kr_victory_through_airpower',
        'kr_close_air_support_proponent',
        'kr_assault_aviation',
        'kr_naval_aviation_pioneer',
        'kr_grand_fleet_proponent',
        'kr_submarine_specialist',
        'fra_atomic_pair',
    )

    for adv in advisors:
        military_role = any([adv.count('slot = army_chief') == 1, adv.count('slot = navy_chief') == 1, adv.count('slot = air_chief') == 1, adv.count('slot = high_command') == 1, adv.count('slot = theorist') == 1])
        specialist_role = False
        expert_role = False
        genius_role = False
        theorist_role = False
        spec_role = False
        sic_role = False
        political_role = False
        specialist_role = adv.count('_1') == 1
        expert_role = adv.count('_2') == 1
        genius_role = adv.count('_3') == 1
        theorist_role = adv.count('slot = theorist') == 1
        sic_role = adv.count('slot = second_in_command') == 1
        political_role = adv.count('slot = political_advisor') == 1
        defined_cost = adv.count('cost =') > 0

        try:
            advisor_name = re.findall('idea_token = (.+)', adv)[0]
        except IndexError:
            results.append((adv, "Missing advisor token"))

        if specialist_role:
            if defined_cost:
                if 'cost = 50' not in adv:
                    results.append((advisor_name, "Specialist level - should cost 50"))

        elif expert_role:
            if defined_cost:
                if 'cost = 100' not in adv:
                    results.append((advisor_name, "Expert level - should cost 100"))
            else:
                results.append((advisor_name, "Expert level - should cost 100"))

        elif genius_role:
            if defined_cost:
                if 'cost = 200' not in adv:
                    results.append((advisor_name, "Genius level - should cost 200"))
            else:
                results.append((advisor_name, "Genius level - should cost 200"))

        elif theorist_role:
            for role in special_theorists:
                if role in adv:
                    spec_role = True

            if spec_role:
                if defined_cost:
                    if 'cost = 150' not in adv:
                        results.append((advisor_name, "Special theorist - should cost 150"))
                else:
                    results.append((advisor_name, "Special theorist - should cost 150"))

            else:
                if defined_cost:
                    if 'cost = 100' not in adv:
                        results.append((advisor_name, "Non-special theorist - should cost 100"))

        elif sic_role:
            if "cost = 0" not in adv:
                results.append((advisor_name, "SIC - should have 'cost = 0' line"))
            if "removal_cost = -1" not in adv:
                results.append((advisor_name, "SIC - should have 'removal_cost = -1' line"))

        elif political_role or military_role:
            continue

        else:
            results.append((advisor_name, "Unknown advisor type"))

    ResultsReporter.report_results(results=results, message="Non-conventional advisor cost (should be 50, 100 or 200 for military advisors, 150 for doctrine theorists and 100 for other theorists) encountered. Check console output")
