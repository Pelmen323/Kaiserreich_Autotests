##########################
# Test script to check for advisors having invalid ledger line
# By Pelmen, https://github.com/Pelmen323
##########################
import re
from ..test_classes.generic_test_class import FileOpener, DataCleaner, ResultsReporter
from ..test_classes.characters_class import Characters


def test_check_advisors_invalid_ledger(test_runner: object):
    advisors = Characters.get_all_advisors(test_runner=test_runner)
    results = []
            
    for adv in advisors:
        theorist_role = False
        hc_role = False
        theorist_role = adv.count('slot = theorist') > 0       
        hc_role = adv.count('slot = high_command') > 0
        advisor_name = re.findall('idea_token = .*', adv)

        if not theorist_role and not hc_role:
            if 'ledger =' in adv:
                results.append((advisor_name, "Ledger slot is not needed here"))
                
        if theorist_role or hc_role:
            if 'ledger =' not in adv:
                results.append((advisor_name, "Ledger slot is required here"))
     
    if results != []:           
        ResultsReporter.report_results(results=results, message="Missing/excessive ledger line encountered. Check console output")
