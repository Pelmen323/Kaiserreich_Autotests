##########################
# Test script to check for decisions that are targeted but don't have targets (this means that every tag will e checked daily)
# By Pelmen, https://github.com/Pelmen323
##########################
from test_classes.decisions_class import Decisions, DecisionsFactory
from test_classes.generic_test_class import ResultsReporter

FALSE_POSITIVES = ['ast_demand_claimed_territory',
                   'gbr_demand_england',
                   'gbr_demand_colonies',
                   ]


def test_check_decisions_targeted(test_runner: object):
    decisions, paths = Decisions.get_all_decisions(test_runner=test_runner, lowercase=True, return_paths=True)
    results = []

    for i in decisions:
        decision = DecisionsFactory(dec=i)
        if decision.token in FALSE_POSITIVES:
            continue

        if decision.target_root_trigger or decision.target_trigger:
            if not decision.targets and not decision.target_array and "always = no" not in i and "annexation" not in i:
                results.append(f'{decision.token}, {paths[i]} - The decision has target_root_trigger/target_trigger but targets are not defined')

    ResultsReporter.report_results(results=results, message="Decisions with target_root_trigger/target_trigger but no targets defined found. This means every country will be checked daily. Check console output")
