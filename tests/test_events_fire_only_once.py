##########################
# Test script to check if events that are fired only once are having fire_only_once = yes flag
# By Pelmen, https://github.com/Pelmen323
##########################
import re
import glob
import pytest

from ..test_classes.events_class import Events
from ..test_classes.generic_test_class import ResultsReporter, FileOpener


@pytest.mark.skip(reason="For manual execution only due to huge number of results")
def test_events_fire_only_once(test_runner: object):
    filepath_on_actions = f'{test_runner.full_path_to_mod}\\common\\on_actions\\'
    fire_only_once_events_id = []
    # 1. Get all events code
    all_events = Events.get_all_events(test_runner=test_runner, lowercase=True)
    all_triggered_events = Events.get_all_triggered_events_names(test_runner=test_runner, lowercase=True, return_duplicates=True)     # Returns a list with all events triggered in files with duplicates
    results = {}

    # 2. Get the "triggered only events that are fired once"
    for event in all_events:
        if "fire_only_once = yes" in event and "is_triggered_only = yes" in event:
            pattern_matches = re.findall('id = .*', event)
            event_id = pattern_matches[0].strip('\t').strip()                   # Only first match is taken
            if '#' in event_id:
                event_id = event_id[:event_id.index('#')].strip()               # Clean up comments
            event_id = event_id[5:].strip()                                     # Remove "id =" part
            fire_only_once_events_id.append(event_id)

    # 3. Limit events to only those that are triggered somewhere once
    for i in fire_only_once_events_id:
        if i in all_triggered_events:
            if all_triggered_events.count(i) == 1:
                results[i] = 0

    # 4. Exclude events from on_actions
    for filename in glob.iglob(filepath_on_actions + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename)

        for i in results.keys():
            pattern = i + "\\b"
            pattern_matches = re.findall(pattern, text_file)
            if len(pattern_matches) > 0:
                results[i] += 1

    cleaned_results = [i for i in results.keys() if results[i] == 0]
    ResultsReporter.report_results(results=cleaned_results, message="Those events are fired only once but have 'fire_only_once' line. Check console output")
