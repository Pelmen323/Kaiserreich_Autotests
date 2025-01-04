##########################
# Test script to check for characters to have already hired lines if having > 1 advisors roles
# By Pelmen, https://github.com/Pelmen323
##########################
import re

from test_classes.characters_class import Characters, Advisors
from test_classes.generic_test_class import ResultsReporter

FALSE_POSITIVES = (
    "rus_mikhail_frunze",
    "rus_pavel_petrov",
    "rus_nikolay_kuznetsov",
    "rus_aleksandr_lapchinsky",
    "rus_vasily_khripin",
)


def test_characters_already_hired(test_runner: object):
    characters, paths = Characters.get_all_characters(test_runner=test_runner, return_paths=True)
    results = []

    for char in characters:
        char_name = re.findall(r"^\t(.+) =", char)[0]
        advisor_status = char.count("\tadvisor = {")
        sic_status = char.count("slot = second_in_command")
        not_already_hired_status = char.count("not_already_hired_except_as")
        instanced = "instance" in char

        if char_name in FALSE_POSITIVES:
            continue

        if not instanced:

            if advisor_status > 1 and sic_status == 0:
                if not_already_hired_status < advisor_status:
                    results.append(f"{char_name} - {paths[char]} - character has {advisor_status} advisor roles and {not_already_hired_status} 'not_already_hired_except_as' lines")

            elif sic_status > 1:
                results.append(f"{char_name} - {paths[char]} - character has > 1 sic roles")

    advisors = Characters.get_all_advisors(test_runner=test_runner)
    for advisor_code in advisors:
        adv = Advisors(adv=advisor_code)
        if adv.not_already_hired:
            if adv.not_already_hired != adv.slot:
                results.append(f"{adv.token} - not_already_hired_as line value {adv.not_already_hired} doesnt match advisor slot {adv.slot}")

    ResultsReporter.report_results(results=results, message="Characters with insufficient number of 'not_already_hired' lines found. Generally you'd want characters to be able to take only one slot at the time.")
