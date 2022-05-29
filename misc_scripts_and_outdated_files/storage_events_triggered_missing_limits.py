##########################
# Test script to check if "is_triggered_only = yes" events are triggered from somewhere
# If they not - they'll never be triggered
# By Pelmen, https://github.com/Pelmen323
##########################
import re
from ..test_classes.generic_test_class import DataCleaner, ResultsReporter
from ..test_classes.events_class import Events
FALSE_POSITIVES = ['ace_promoted.1', 'ace_promoted.2', 'ace_died.1',
                   'ace_killed_by_ace.1', 'ace_killed_other_ace.1',
                   'aces_killed_each_other.1', 'nuke_dropped.0']


def test_check_triggered_events(test_runner: object):
    results = []
    # 1. Get all events code
    all_events, paths = Events.get_all_events(test_runner=test_runner, lowercase=True, return_paths=True)

    # 2. Get the "triggered only events"
    for event in all_events:
        if "is_triggered_only = yes" not in event:
            if 'trigger = {' in event:
                trigger_part = re.findall("^\\ttrigger = (\\{.*?^\\t\\})", event, flags=re.DOTALL | re.MULTILINE)
                if len(trigger_part) > 0:
                    if '\ttag =' not in trigger_part[0] and '\toriginal_tag =' not in trigger_part[0]:
                        print(trigger_part[0])
                        pattern_matches = re.findall('id = .*', event)
                        event_id = pattern_matches[0].strip('\t').strip()                   # Only first match is taken
                        if '#' in event_id:
                            event_id = event_id[:event_id.index('#')].strip()               # Clean up comments
                        event_id = event_id[5:].strip()                                     # Remove "id =" part
                        results.append((event_id, paths[event]))

    ResultsReporter.report_results(results=results, message="Those events have 'is_triggered_only = yes' attr but are never triggered from outside. Check console output")
