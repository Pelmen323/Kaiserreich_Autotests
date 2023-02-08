##########################
# Test script to check if specific pattern is used that can be replaced with scripted effect (in KR there are scripted effects that should be used instead)
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re

from ..test_classes.generic_test_class import FileOpener, ResultsReporter
from ..test_classes.events_class import Events


def test_check_root_can_grant_land_in_state_scope(test_runner: object):
    events = Events.get_all_events(test_runner=test_runner, lowercase=True, return_paths=False)
    results = []
    key_string = "root_can_grant_land"
    pattern = '(^(\\t+)every_owned_state = \\{.*?^\\2\\})'

    for event in events:
        if key_string in event:
            event_id = re.findall('^\\tid = ([^ \\n\\t]+)', event, flags=re.MULTILINE)[0]
            pattern_matches = re.findall(pattern, event, flags=re.DOTALL | re.MULTILINE)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    if key_string in match[0]:
                        results.append(event_id)

    ResultsReporter.report_results(results=results, message="Root can grant land is used in state scope. This will cause errors in log and will break the trigger.")
