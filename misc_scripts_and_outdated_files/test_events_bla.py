##########################
# Test script to check for events with invalid title/desc
# By Pelmen, https://github.com/Pelmen323
##########################

from test_classes.events_class import Events, EventFactory
from test_classes.generic_test_class import ResultsReporter


def test_events_unsupported_title_desc(test_runner: object):
    results = []
    all_events = Events.get_all_events(test_runner=test_runner, lowercase=True)

    for i in all_events:
        e = EventFactory(i)
        if not e.is_triggered_only:
            results.append(e.token)

    ResultsReporter.report_results(results=results, message="Bla.")
