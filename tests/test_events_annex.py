##########################
# Test script to check if annex events have recheck_annex
# By Pelmen, https://github.com/Pelmen323
##########################
import re

from ..test_classes.generic_test_class import ResultsReporter
from ..test_classes.events_class import Events


def test_check_annex_events_have_recheck_annex(test_runner: object):
    events = Events.get_all_events(test_runner=test_runner, lowercase=True, return_paths=False)
    results = []
    key_string = "recheck_annexations"
    pattern = r'(^(\t+)option = \{.*?^\2\})'

    for event in events:
        event_id = re.findall('^\\tid = ([^ \\n\\t]+)', event, flags=re.MULTILINE)[0]
        if "annex" in event_id:
            pattern_matches = re.findall(pattern, event, flags=re.DOTALL | re.MULTILINE)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    if key_string not in match[0] and "annex.occupation" not in match[0]:
                        option_id = re.findall(r'^\t\tname = ([^ \n\t]+)', match[0], flags=re.MULTILINE)
                        results.append(f'{event_id} - {str(option_id)[1:-1]}')

    ResultsReporter.report_results(results=results, message="The annex event option doesn't have the recheck_annexations.")
