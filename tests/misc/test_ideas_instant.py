##########################
# Test script to check if equipment modifiers have instant application
# By Pelmen, https://github.com/Pelmen323
##########################
from test_classes.generic_test_class import ResultsReporter
from test_classes.ideas_class import Ideas
import re


def test_ideas_instant_yes(test_runner: object):
    results = []
    ideas, paths = Ideas.get_all_ideas(
        test_runner=test_runner, lowercase=True, return_paths=True, include_country_ideas=True, include_manufacturers=False, include_laws=True, include_army_spirits=True
    )
    for idea in ideas:
        if "equipment_bonus = {" in idea:
            if "instant = yes" not in idea:
                idea_name = re.findall(r"^\t\t(.*?) =", idea, re.MULTILINE)[0]
                results.append(f"{paths[idea]} - {idea_name} - has equipment bonus that is not applied instantly")

    # 2. throw the error if those combinations are encountered
    ResultsReporter.report_results(results=results, message="Equipment bonuses without instant = yes were encountered.")
