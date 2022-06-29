##########################
# Test script to check for events with missing pics
# By Pelmen, https://github.com/Pelmen323
##########################
import re

import pytest

from ..test_classes.events_class import Events
from ..test_classes.generic_test_class import ResultsReporter


@pytest.mark.skip(reason="Disabled for now")
def test_check_missing_pics_events(test_runner: object):
    results = []
    events_code = Events.get_all_events(test_runner=test_runner, lowercase=True)

    for event in events_code:
        if "hidden = yes" not in event:
            if "picture =" not in event:
                pattern_matches = re.findall('id = .*', event)
                event_id = pattern_matches[0].strip('\t').strip()                   # Only first match is taken
                if '#' in event_id:
                    event_id = event_id[:event_id.index('#')].strip()               # Clean up comments
                event_id = event_id[5:].strip()                                     # Remove "id =" part
                results.append(event_id)

    ResultsReporter.report_results(results=results, message="Events with no pictures were encountered. Check console output")
