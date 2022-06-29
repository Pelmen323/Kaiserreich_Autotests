##########################
# Test script to check if "is_triggered_only = yes" events are triggered from somewhere
# If they not - they'll never be triggered
# By Pelmen, https://github.com/Pelmen323
##########################
import re

from ..test_classes.events_class import Events
from ..test_classes.generic_test_class import DataCleaner, ResultsReporter

FALSE_POSITIVES = ['ace_promoted.1', 'ace_promoted.2', 'ace_died.1',
                   'ace_killed_by_ace.1', 'ace_killed_other_ace.1',
                   'aces_killed_each_other.1', 'nuke_dropped.0']


def test_check_triggered_events(test_runner: object):
    all_events = []
    triggered_events_id = dict()
    invoked_events_id = []
    # 1. Get all events code
    all_events = Events.get_all_events(test_runner=test_runner, lowercase=True)

    # 2. Get the "triggered only events"
    for event in all_events:
        if "is_triggered_only = yes" in event:
            pattern_matches = re.findall('id = .*', event)
            event_id = pattern_matches[0].strip('\t').strip()                   # Only first match is taken
            if '#' in event_id:
                event_id = event_id[:event_id.index('#')].strip()               # Clean up comments
            event_id = event_id[5:].strip()                                     # Remove "id =" part
            triggered_events_id[event_id] = 0                                   # Default value is set to zero

    # 3. Get all events triggered in files
    triggered_events_id = DataCleaner.clear_false_positives(input_iter=triggered_events_id, false_positives=FALSE_POSITIVES)
    invoked_events_id = Events.get_all_triggered_events_names(test_runner=test_runner, lowercase=True)

    # 4. Check if events are used
    for event in invoked_events_id:
        if event in triggered_events_id.keys():
            triggered_events_id[event] += 1

    results = [i for i in triggered_events_id.keys() if triggered_events_id[i] == 0]
    ResultsReporter.report_results(results=results, message="Those events have 'is_triggered_only = yes' attr but are never triggered from outside. Check console output")
