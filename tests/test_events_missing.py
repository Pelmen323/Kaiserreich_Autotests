##########################
# Test script to check for missing events
# By Pelmen, https://github.com/Pelmen323
##########################
from ..test_classes.generic_test_class import FileOpener, DataCleaner, ResultsReporter
from ..test_classes.events_class import Events
import glob


def test_check_missing_events(test_runner: object):
# Part 1 - get list of all events
    events = Events.get_all_events_names(test_runner=test_runner)
    
# Part 2 - get triggered events
    triggered_events = Events.get_all_triggered_events_names(test_runner=test_runner)

# Part 3 - throw the error if entity is missing
    results = [i for i in triggered_events if events.count(i) == 0]
    results_to_exclude = []
    filepath = test_runner.full_path_to_mod
    
    # exclude commented events    
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        text_file_splitted = text_file.split('\n')[1:]
        for line in range(len(text_file_splitted)):
            current_line = text_file_splitted[line]
            for i in results:
                if i in current_line:
                    if '#' in current_line:
                        if current_line.strip('\t').index('#') == 0:
                            results_to_exclude.append(i)

    results = [i for i in results if i not in results_to_exclude]
    ResultsReporter.report_results(results=results, message="Missing triggered events were encountered. Check console output")
