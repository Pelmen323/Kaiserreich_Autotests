##########################
# Test script to check for missing events
# Deprecated - CWTools can deal with missing events
# By Pelmen, https://github.com/Pelmen323
##########################
import glob

from test_classes.events_class import Events
from test_classes.generic_test_class import FileOpener, ResultsReporter


def test_events_missing(test_runner: object):
    events = Events.get_all_events_names(test_runner=test_runner, lowercase=True)
    triggered_events = Events.get_all_triggered_events_names(test_runner=test_runner, lowercase=True)
    results = [i for i in triggered_events if events.count(i) == 0]
    results_to_exclude = []
    filepath = test_runner.full_path_to_mod

    # exclude commented events
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)
        if "#" in text_file and "country_event =" in text_file:
            text_file_splitted = text_file.split('\n')[1:]
            for line in range(len(text_file_splitted)):
                current_line = text_file_splitted[line]
                if '#' in current_line:
                    for i in results:
                        if i in current_line and i not in results_to_exclude:
                            if current_line.strip('\t').index('#') == 0:
                                results_to_exclude.append(i)

    results = [i for i in results if i not in results_to_exclude]
    ResultsReporter.report_results(results=results, message="Missing triggered events were encountered.")
