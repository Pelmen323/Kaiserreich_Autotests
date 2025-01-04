##########################
# Test script to check if root can grant land is used in state scope
# By Pelmen, https://github.com/Pelmen323
##########################
import re

from test_classes.generic_test_class import ResultsReporter
from test_classes.events_class import Events


def test_effects_root_can_grant_land(test_runner: object):
    events = Events.get_all_events(test_runner=test_runner, lowercase=True, return_paths=False)
    results = []
    pattern_id = re.compile(r"^\tid = (\S+)", flags=re.MULTILINE)
    pattern_state = re.compile(r"(^(\t+)every_owned_state = \{.*?^\2\})", flags=re.DOTALL | re.MULTILINE)

    for event in events:
        if "root_can_grant_land" in event:
            event_id = pattern_id.findall(event)[0]
            pattern_matches = pattern_state.findall(event)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    if "root_can_grant_land" in match[0]:
                        results.append(event_id)

    ResultsReporter.report_results(results=results, message="Root can grant land is used in state scope. This will cause errors in log and will break the trigger.")
