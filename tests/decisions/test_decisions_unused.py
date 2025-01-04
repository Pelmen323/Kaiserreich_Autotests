##########################
# Test script to check if decisions are unused
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re

from test_classes.decisions_class import Decisions, DecisionsFactory
from test_classes.generic_test_class import ResultsReporter, FileOpener


def test_decisions_unused(test_runner: object):
    filepath = test_runner.full_path_to_mod
    results = []
    decisions = Decisions.get_all_decisions(test_runner=test_runner, lowercase=True, return_paths=False)
    manual_decisions = {}
    manual_missions = {}

    for i in decisions:
        decision = DecisionsFactory(dec=i)
        if decision.allowed:
            if "always = no" in decision.allowed and not decision.mission_subtype:
                manual_decisions[decision.token] = 0
            elif "always = no" in decision.allowed and decision.mission_subtype:
                manual_missions[decision.token] = 0

    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if "activate_targeted_decision =" in text_file:
            manual_decisions = {key: value for key, value in manual_decisions.items() if value == 0}
            all_matches = re.findall(r'activate_targeted_decision = [^\n\t]*', text_file)
            for decision in manual_decisions:
                for match in all_matches:
                    if f"decision = {decision}" in match:
                        manual_decisions[decision] += 1

        if "activate_mission =" in text_file:
            manual_missions = {key: value for key, value in manual_missions.items() if value == 0}
            all_matches = re.findall(r'activate_mission = \S*', text_file)
            for mission in manual_missions:
                if f"activate_mission = {mission}" in all_matches:
                    manual_missions[mission] += 1

    results = [key for key in manual_decisions.keys() if manual_decisions[key] == 0]
    results += [key for key in manual_missions.keys() if manual_missions[key] == 0]

    ResultsReporter.report_results(results=results, message="Unused decisions/missions were encountered. They are designed to be manually activated with activate_targeted_decision/activate_mission but never are")
