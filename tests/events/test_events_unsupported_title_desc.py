##########################
# Test script to check for events with invalid title/desc
# By Pelmen, https://github.com/Pelmen323
##########################
import re
import pytest

from test_classes.events_class import Events
from test_classes.generic_test_class import ResultsReporter

input_list = ["title", "desc"]


@pytest.mark.parametrize("line", input_list)
def test_events_unsupported_title_desc(test_runner: object, line: str):
    results = []
    events_code = Events.get_all_events(test_runner=test_runner, lowercase=True)

    pattern_1 = r"^\t" + line + r" = \{"
    pattern_2 = r"^\t" + line + r" = \w"
    pattern_id = re.compile(r"^\tid = (\S+)", flags=re.MULTILINE)

    for event in events_code:
        pattern_1_in_file = len(re.findall(pattern_1, event, flags=re.MULTILINE)) > 0
        pattern_2_in_file = len(re.findall(pattern_2, event, flags=re.MULTILINE)) > 0

        if pattern_1_in_file and pattern_2_in_file:
            event_id = pattern_id.findall(event)[0]
            results.append(f"{event_id}, {line}")

    ResultsReporter.report_results(results=results, message=f"Invalid combinations of {line} were encountered.")
