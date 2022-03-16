##########################
# Test script to check for advisors that have incorrect costs
# By Pelmen, https://github.com/Pelmen323
##########################
import re
from ..test_classes.generic_test_class import FileOpener, DataCleaner, ResultsReporter
from ..test_classes.characters_class import Characters
import re


def test_check_advisors_invalid_costs(test_runner: object):
    advisors = Characters.get_all_advisors(test_runner=test_runner, lowercase=True)
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
    )
            
    for adv in advisors:
        specialist_role = False
        expert_role = False
        genius_role = False
        theorist_role = False
        spec_role = False
        hc_role = False
        specialist_role = adv.count('_1') > 0
        expert_role = adv.count('_2') > 0
        genius_role = adv.count('_3') > 0
        theorist_role = adv.count('slot = theorist') > 0       
        hc_role = adv.count('slot = high_command') > 0
        advisor_name = re.findall('idea_token = .*', adv)

        
        if specialist_role:
            if 'cost =' in adv: 
                if 'cost = 50' not in adv:
                    results.append((advisor_name, "Specialist level - should cost 50"))
                    
        elif expert_role:
            if 'cost =' in adv: 
                if 'cost = 100' not in adv:
                    results.append((advisor_name, "Expert level - should cost 100"))
                    
        elif genius_role:
            if 'cost =' in adv: 
                if 'cost = 200' not in adv:
                    results.append((advisor_name, "Genius level - should cost 200"))
                    
        elif theorist_role:
            for role in special_theorists:
                if role in adv:
                    spec_role = True
            
            if spec_role:
                if 'cost = 150' not in adv:
                    results.append((advisor_name, "Special theorist - should cost 150"))

            elif 'cost = 100' not in adv and 'cost =' in adv:
                    results.append((advisor_name, "Non-special theorist - should cost 100"))
     
    if results != []:           
        ResultsReporter.report_results(results=results, message="Non-conventional advisor cost (should be 50, 100 or 200 for military advisors, 150 for doctrine theorists and 100 for other theorists) encountered. Check console output")
