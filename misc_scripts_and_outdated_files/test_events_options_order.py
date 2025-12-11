##########################
# Test script to check for events with suspicious option name
# By Pelmen, https://github.com/Pelmen323
##########################
import re

from test_classes.events_class import Events
from test_classes.generic_test_class import ResultsReporter


def test_events_unsupported_title_desc(test_runner: object):
    results = []
    events = Events.get_all_events(test_runner=test_runner, lowercase=True, filepath_should_not_contain="Annexation")

    for event in events:
        event_id = re.findall(r"^\tid = (\S+)", event, flags=re.MULTILINE)[0]
        options = re.findall(r'(^\toption = \{.*?^\t\})', event, flags=re.DOTALL | re.MULTILINE)
        if len(options) > 1:
            if "after = {" not in event:
                if 'hidden = yes' not in event:
                    results.append(f'{event_id} has multiple options and no after block')
        # if len(options) > 0:
        #     option = options[0]
        #     i = 0
        #     try:
        #         option_name = re.findall(r'^\t\tname = (\S+)', option, flags=re.MULTILINE)[0]
        #     except Exception:
        #         if 'hidden = yes' not in event:
        #             results.append(f'Warning: {event_id} option {i+1} doesnt have option argument!')
        #         continue
        #     try:
        #         postfix = option_name[-2:]
        #         if '.' not in postfix:
        #             # Custom postfix detected, go away
        #             continue
        #         expected_postfix = expected_postfix_dict[i]
        #         if i == 0:
        #             if postfix != expected_postfix:
        #                 if postfix in expected_postfix_dict.values():
        #                     results.append(f'{option_name} - option {i+1} - postfix {postfix} doesnt match expected postfix {expected_postfix}')
        #     except Exception:
        #         print(option)
        #         raise

    ResultsReporter.report_results(results=results, message="Unexpected option name encountered")
