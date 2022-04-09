##########################
# Test script to check for advisors having invalid ledger line
# By Pelmen, https://github.com/Pelmen323
##########################
from ..test_classes.generic_test_class import ResultsReporter
from ..test_classes.characters_class import Characters, Advisors


def test_check_advisors_invalid_ledger(test_runner: object):
    advisors = Characters.get_all_advisors(test_runner=test_runner)
    army_hc_advisor_traits = Characters.get_hc_specified_advisor_traits(test_runner=test_runner, trait_type="army", lowercase=True)
    navy_hc_advisor_traits = Characters.get_hc_specified_advisor_traits(test_runner=test_runner, trait_type="navy", lowercase=True)
    air_hc_advisor_traits = Characters.get_hc_specified_advisor_traits(test_runner=test_runner, trait_type="air", lowercase=True)
    results = []

    for advisor_code in advisors:
        adv = Advisors(adv=advisor_code)
        # Ledger checks #
        if not adv.hc_role and not adv.theorist_role:
            if adv.has_ledger_slot:
                results.append((adv.token, "Ledger slot is not needed here"))

        else:
            if "KR_council_of_theorists" in advisor_code:
                if "ledger = military" not in advisor_code:
                    results.append((adv.token, "Ledger slot 'military' is required here"))

            if len(adv.traits) == 1:
                found_trait = ''.join(adv.traits)
                if found_trait in army_hc_advisor_traits:
                    if adv.ledger_slot != "army":
                        results.append((adv.token, "Ledger slot 'army' is required here"))
                elif found_trait in navy_hc_advisor_traits:
                    if adv.ledger_slot != "navy":
                        results.append((adv.token, "Ledger slot 'navy' is required here"))
                elif found_trait in air_hc_advisor_traits:
                    if adv.ledger_slot != "air":
                        results.append((adv.token, "Ledger slot 'air' is required here"))

            if not adv.has_ledger_slot:
                results.append((adv.token, "Ledger slot is required here"))

    ResultsReporter.report_results(results=results, message="Missing/excessive ledger line encountered. Check console output")
