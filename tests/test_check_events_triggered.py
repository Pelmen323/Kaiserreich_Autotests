##########################
# Test script to check if "is_triggered_only = yes" events are triggered from somewhere
# If they not - they'll never be triggered
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
from ..test_classes.generic_test_class import TestClass
import logging
FALSE_POSITIVES = ['ace_promoted.1', 'ace_promoted.2', 'ace_died.1',
                   'ace_killed_by_ace.1', 'ace_killed_other_ace.1',
                   'aces_killed_each_other.1', 'nuke_dropped.0']


def test_check_triggered_events(test_runner: object):
    test = TestClass()
    filepath_events = f'{test_runner.full_path_to_mod}events\\'
    filepath_global = test_runner.full_path_to_mod
    filepath_history = f'{test_runner.full_path_to_mod}history\\'
    all_events = []
    triggered_events_id = dict()
    invoked_events_id = []

    for filename in glob.iglob(filepath_events + '**/*.txt', recursive=True):
        text_file = test.open_text_file(filename).lower()

    # 1. Get list of all events in events files
        pattern_matches = re.findall('((?<=\n)country_event = \\{.*\n(.|\n*?)*\n\\})', text_file)
        if len(pattern_matches) > 0:
            for match in pattern_matches:
                match = match[0]                                            # Counter empty capture groups
                all_events.append(match)

    # 2. Get the "triggered only events"
    for event in all_events:
        if "is_triggered_only = yes" in event:
            pattern_matches = re.findall('id = .*', event)
            event_id = pattern_matches[0].strip('\t').strip()                   # Only first match is taken
            if '#' in event_id:
                event_id = event_id[:event_id.index('#')].strip()               # Clean up comments
            event_id = event_id[5:].strip()                                     # Remove "id =" part
            triggered_events_id[event_id] = 0                                   # Default value is set to zero

    # 3. Time to roll out - NO HISTORY FILES HERE
    triggered_events_id = test.clear_false_positives_dict(input_dict=triggered_events_id, false_positives=FALSE_POSITIVES)
    for filename in glob.iglob(filepath_global + '**/*.txt', recursive=True):
        if '\\history\\' in filename:
            continue
        text_file = test.open_text_file(filename).lower()

        if "country_event =" in text_file:
            # 3.0 One-liners w/o brackets
            pattern_matches = re.findall('([\t| ]country_event = ((?!\\{).)*\n)', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[0]
                    match = match[16:].strip().strip('}').strip().strip('}').strip()
                    if '#' in match:
                        match = match[:match.index('#')].strip().strip('}').strip()    # Clean up comments
                    invoked_events_id.append(match)

            # 3.1 One-liners with brackets
            pattern_matches = re.findall('[\t| ]country_event = \\{.*\\}', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    event_id_match = re.findall('id = [a-zA-Z0-9\\._]*', match)
                    match = ''.join(event_id_match)[4:].strip()
                    invoked_events_id.append(match)

            # 3.2 Multiliners
            pattern_matches = re.findall('([\t| ]country_event = \\{((?!\\}).)*\n(.|\n*?)*\n\t*\\})', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    if '' in match:
                        match = match[0]                                            # Counter empty capture groups
                    event_id_match = re.findall('id = [a-zA-Z0-9\\._]*', match)
                    match = ''.join(event_id_match)[4:].strip()
                    invoked_events_id.append(match)

    for filename in glob.iglob(filepath_history + '**/*.txt', recursive=True):
        text_file = test.open_text_file(filename).lower()

        if "country_event =" in text_file:
            # 4.0 One-liners w/o brackets
            pattern_matches = re.findall('(country_event = ((?!\\{).)*\n)', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[0]
                    match = match[16:].strip().strip('}').strip().strip('}').strip()
                    if '#' in match:
                        match = match[:match.index('#')].strip().strip('}').strip()    # Clean up comments
                    invoked_events_id.append(match)

            # 4.1 One-liners with brackets
            pattern_matches = re.findall('country_event = \\{.*\\}', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    event_id_match = re.findall('id = [a-zA-Z0-9\\._]*', match)
                    match = ''.join(event_id_match)[4:].strip()
                    invoked_events_id.append(match)

            # 4.2 Multiliners
            pattern_matches = re.findall('(country_event = \\{((?!\\}).)*\n(.|\n*?)*\n\t*\\})', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    if '' in match:
                        match = match[0]                                            # Counter empty capture groups
                    event_id_match = re.findall('id = [a-zA-Z0-9\\._]*', match)
                    match = ''.join(event_id_match)[4:].strip()
                    invoked_events_id.append(match)

    for event in invoked_events_id:
        if event in triggered_events_id.keys():
            triggered_events_id[event] += 1

    results = [i for i in triggered_events_id.keys() if triggered_events_id[i] == 0]
    if results != []:
        logging.warning("Following events have 'is_triggered_only = yes' attr but are never triggered from outside:")
        for i in results:
            logging.error(f'- [ ] {i}')
        logging.warning(f"{len(results)} 'is_triggered_only = yes' events are not triggered from somewhere.")
        raise AssertionError("Following events have 'is_triggered_only = yes' attr but are not triggered! Check console output")
