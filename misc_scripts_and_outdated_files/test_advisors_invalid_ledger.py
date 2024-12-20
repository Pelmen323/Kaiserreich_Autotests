##########################
# Test script to check for advisors having invalid ledger line
# By Pelmen, https://github.com/Pelmen323
##########################
import pytest
from data.advisor_traits import (
    air_theorists_traits,
    army_theorists_traits,
    navy_theorists_traits,
)
from test_classes.characters_class import Advisors, Characters
from test_classes.generic_test_class import ResultsReporter


@pytest.mark.skip("No way to differentiate between different HC traits")
@pytest.mark.kr_specific
def test_advisors_invalid_ledger(test_runner: object):
    advisors = Characters.get_all_advisors(test_runner=test_runner)
    army_hc_advisor_traits = Characters.get_hc_specified_advisor_traits(test_runner=test_runner, trait_type="army", lowercase=True)
    navy_hc_advisor_traits = Characters.get_hc_specified_advisor_traits(test_runner=test_runner, trait_type="navy", lowercase=True)
    air_hc_advisor_traits = Characters.get_hc_specified_advisor_traits(test_runner=test_runner, trait_type="air", lowercase=True)
    results = []

    for advisor_code in advisors:
        adv = Advisors(adv=advisor_code)
        # 1. Ledger line is needed only for "high_command" and "theorist" roles
        if not adv.hc_role and not adv.theorist_role:
            if adv.has_ledger_slot:
                results.append(f"{adv.token} - Ledger line is not needed here")

        else:
            # 2. Checks for high command advisor traits
            if adv.hc_role:
                found_trait = ''.join(adv.traits)
                if found_trait in army_hc_advisor_traits:
                    if adv.ledger_slot != "army":
                        results.append(f"{adv.token} - Ledger slot 'army' is required here, found trait - {found_trait}")
                elif found_trait in navy_hc_advisor_traits:
                    if adv.ledger_slot != "navy":
                        results.append(f"{adv.token} - Ledger slot 'navy' is required here, found trait - {found_trait}")
                elif found_trait in air_hc_advisor_traits:
                    if adv.ledger_slot != "air":
                        results.append(f"{adv.token} - Ledger slot 'air' is required here, found trait - {found_trait}")

            # 3. Checks for theorist command advisor traits
            elif adv.theorist_role:
                found_trait = ''.join(adv.traits)
                if found_trait in army_theorists_traits:
                    if adv.ledger_slot != "army":
                        results.append(f"{adv.token} - Ledger slot 'army' is required here, found trait - {found_trait}")
                elif found_trait in navy_theorists_traits:
                    if adv.ledger_slot != "navy":
                        results.append(f"{adv.token} - Ledger slot 'navy' is required here, found trait - {found_trait}")
                elif found_trait in air_theorists_traits:
                    if adv.ledger_slot != "air":
                        results.append(f"{adv.token} - Ledger slot 'air' is required here, found trait - {found_trait}")

            # 4. All high command and theorist advisors should have ledgers
            if not adv.has_ledger_slot and adv.token is not None:
                results.append(f"{adv.token} - Ledger line is required here")

    ResultsReporter.report_results(results=results, message="Missing/excessive ledger line encountered. Ledger line is needed only for high_command and theorist roles.")
