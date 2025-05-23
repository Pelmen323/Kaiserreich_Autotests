import glob
import re
import os
from charset_normalizer import detect

from core.runner import TestRunner
from test_classes.generic_test_class import DataCleaner, FileOpener
from test_classes.localization_class import Localization
from test_classes.characters_class import Characters, Advisors

FILES_TO_SKIP = ['\\localisation', 'interface', 'gfx', 'map', 'common\\units', 'names', 'states', '00_construction_scripted_effects', 'UI_scripted_localisation', 'technologies', 'occupation_laws', 'KR intro screen scripted loc', 'MIT scripted_loc', 'special_projects']


def detect_encoding(filename):
    with open(filename, 'rb') as f:
        raw_data = f.read()
        return detect(raw_data)['encoding']


def format_events(username, mod_name):
    test_runner = TestRunner(username, mod_name)
    results_dict = {}

    filepath_to_events = f'{test_runner.full_path_to_mod}events\\'
    events = []

    for filename in glob.iglob(filepath_to_events + '**/*.txt', recursive=True):
        if '\\categories' in filename:
            continue
        text_file = FileOpener.open_text_file(filename, lowercase=False)
        pattern_matches = re.findall('^country_event = \\{(.*?)^\\}', text_file, flags=re.DOTALL | re.MULTILINE)
        if len(pattern_matches) > 0:
            for match in pattern_matches:
                events.append(match)

    # 1. Remove AI chance from events with only one option
    for event in events:
        if event.count("option = {") == 1 and event.count("ai_chance") == 1:
            ai_will_do_line = re.findall("\\t*ai_chance = \\{[^}]*?\\}\n", string=event, flags=re.MULTILINE | re.DOTALL)[0]
            results_dict[event] = event.replace(ai_will_do_line, "")
        # https://github.com/Kaiserreich/Kaiserreich-4-Development/pull/8597
        # if "immediate = {" in event:
        #     immediate_line = re.findall("immediate = \\{.*", string=event)[0]
        #     # One liner
        #     if "}" in immediate_line:
        #         immediate_code = re.findall("immediate = \\{.*\\}", string=event)[0]
        #         if "immediate = { hidden_effect = {" not in immediate_code:
        #             immediate_code_new = immediate_code.replace("immediate = {", "immediate = { hidden_effect = {") + " }"
        #             results_dict[event] = event.replace(immediate_code, immediate_code_new)
        #     # Multiple lines
        #     else:
        #         immediate_code = re.findall("(immediate = \\{[^\n]*\n)(.*?^\\t\\})\n", string=event, flags=re.MULTILINE | re.DOTALL)[0]
        #         if "hidden_effect = {" not in immediate_code[1]:
        #             immediate_code_new = immediate_code[0] + "\t\thidden_effect = {\n\t" + immediate_code[1].replace('\n', '\n\t') + "\n\t}"
        #             results_dict[event] = event.replace(immediate_code[0]+immediate_code[1], immediate_code_new)

    # 2. Apply changes
    for filename in glob.iglob(test_runner.full_path_to_mod + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename, lowercase=False)
        for i in results_dict:
            if i in text_file:
                text_file = FileOpener.open_text_file(filename, lowercase=False)
                text_file_new = text_file.replace(i, results_dict[i])
                with open(filename, 'w', encoding="utf-8") as text_file_write:
                    text_file_write.write(text_file_new)


def replace_string(filename, pattern, replace_with, encoding="utf-8", flag=None):
    text_file = FileOpener.open_text_file(filename, lowercase=False)
    if flag is None:
        text_file_fixed = re.sub(pattern=pattern, repl=replace_with, string=text_file)
    else:
        text_file_fixed = re.sub(pattern=pattern, repl=replace_with, string=text_file, flags=flag)

    with open(filename, 'w', encoding=encoding) as text_file_write:
        text_file_write.write(text_file_fixed)


def format_filenames_strategic_regions(username, mod_name):
    """Rename strategic regions files to match the scheme "ID - Region loc key.txt". Requested by Alpinia, December 2022

    Args:
        username (_type_): windows username
        mod_name (_type_): mod folder name
    """
    test_runner = TestRunner(username, mod_name)
    filepath_to_strategic_regions_loc = f'{test_runner.full_path_to_mod}localisation\\english\\KR_common\\00 Strategic Regions l_english.yml'
    filepath_to_strategic_regions_code = f'{test_runner.full_path_to_mod}map\\strategicregions'

    text_file = FileOpener.open_text_file(filepath_to_strategic_regions_loc, lowercase=False)
    strategic_regions_loc = {}
    for line in text_file.split("\n")[1:-1]:
        region_id = line.split(':')[0].split("_")[1]
        region_name = line.split(':')[1].strip().strip('"')
        strategic_regions_loc[region_id] = region_name

    for filename in glob.iglob(filepath_to_strategic_regions_code + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename, lowercase=False)
        current_region_id = re.findall("id[ ]*=[ ]*(.*)", text_file)[0]
        expected_filename = f'{current_region_id} - {strategic_regions_loc[current_region_id]}.txt'
        if os.path.basename(filename) != expected_filename:
            os.rename(filename, f'{filepath_to_strategic_regions_code}\\{expected_filename}')


def format_filenames_states(username, mod_name):
    """Rename states files to match the scheme "ID - State loc key.txt". Requested by Alpinia, December 2022

    Args:
        username (_type_): windows username
        mod_name (_type_): mod folder name
    """
    test_runner = TestRunner(username, mod_name)
    filepath_to_states_loc = f'{test_runner.full_path_to_mod}localisation\\english\\KR_common\\00 Map States l_english.yml'
    filepath_to_states_code = f'{test_runner.full_path_to_mod}history\\states'
    loc_keys = Localization.get_all_loc_keys(test_runner=test_runner, lowercase=False)

    text_file = FileOpener.open_text_file(filepath_to_states_loc, lowercase=False)
    states_loc = {}
    target_lines = re.findall("STATE_\\d+: .*", text_file)
    for line in target_lines:
        state_id = line.split(':')[0].split("_")[1]
        state_name = line.split(':')[1].strip().strip('"')
        if "$" in state_name:
            state_name = loc_keys[state_name.strip("$")].strip('"')
        states_loc[state_id] = state_name

    for filename in glob.iglob(filepath_to_states_code + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename, lowercase=False)
        current_region_id = re.findall("id[ ]*=[ ]*(\\d*)", text_file)[0]
        expected_filename = f'{current_region_id} - {states_loc[current_region_id]}.txt'
        if os.path.basename(filename) != expected_filename:
            os.rename(filename, f'{filepath_to_states_code}\\{expected_filename}')


def format_logging_events(username, mod_name):
    """Add logging to events

    Args:
        username (_type_): windows username
        mod_name (_type_): mod folder name
    """
    test_runner = TestRunner(username, mod_name)
    filepath_to_events = f'{test_runner.full_path_to_mod}events\\'
    files_to_skip = ['Pilot', 'LaR', 'Nuke', ' - Vanilla']
    false_positives = []
    options_event_logging_args = {
        "country_event": "[GetLogInfo]",
        "state_event": "[GetLogInfo]",
        "unit_leader_event": "[GetLogInfo]",
    }

    # 1. Event logging - options
    for event_type, logging in options_event_logging_args.items():
        for filename in glob.iglob(filepath_to_events + '**/*.txt', recursive=True):
            if DataCleaner.skip_files(files_to_skip=files_to_skip, filename=filename):
                continue

            text_file = FileOpener.open_text_file(filename, lowercase=False)
            pattern_event = '^' + event_type + ' = \\{(.*?)^\\}'
            pattern_matches = re.findall(pattern_event, text_file, flags=re.DOTALL | re.MULTILINE)
            if len(pattern_matches) > 0:
                dict_with_str_to_replace_event = dict()
                for event in pattern_matches:
                    try:
                        event_id = re.findall('^\\tid = (\\S+)', event, flags=re.MULTILINE)[0]
                    except IndexError:
                        print(event)
                        raise

                    hidden_event = "donotlog" in event
                    if event_id in false_positives or hidden_event:
                        continue

                    options = re.findall('(^\\toption = \\{.*?^\\t\\})', event, flags=re.DOTALL | re.MULTILINE)

                    for index, option in enumerate(options):
                        dict_with_str_to_replace_option = dict()
                        has_any_logging = "log =" in option
                        has_data_logging = 'log = "KR_Event_Logging' in option
                        option_name = re.findall('^\\t\\tname = (\\S+)', option, flags=re.MULTILINE)[0] if '\n\t\tname = ' in option and '\n\t\tname = "' not in option else index + 1
                        expected_logging_line = 'log = "' + logging + ': event ' + event_id + ' option ' + str(option_name) + '"'
                        has_valid_logging = expected_logging_line in option

                        if not has_valid_logging:
                            if has_any_logging and not has_data_logging:
                                str_to_replace = re.findall('log =.*', option)[0]
                                dict_with_str_to_replace_option[option] = option.replace(str_to_replace, expected_logging_line)
                            if has_any_logging and has_data_logging:
                                if option.count("log =") == 1:
                                    x = re.findall('^\\toption = .*', option, flags=re.MULTILINE)[0]
                                    dict_with_str_to_replace_option[option] = option.replace(x, f'{x}\n\t\t{expected_logging_line}')
                                else:
                                    str_to_replace = re.findall('log = \\"(?!KR_Event_Logging).*', option)[0]
                                    dict_with_str_to_replace_option[option] = option.replace(str_to_replace, expected_logging_line)
                            if not has_any_logging:
                                x = re.findall('^\\toption = .*', option, flags=re.MULTILINE)[0]
                                dict_with_str_to_replace_option[option] = option.replace(x, f'{x}\n\t\t{expected_logging_line}')

                        for key, value in dict_with_str_to_replace_option.items():
                            dict_with_str_to_replace_event[event] = event.replace(key, value) if event not in dict_with_str_to_replace_event.keys() else dict_with_str_to_replace_event[event].replace(key, value)

                for key, value in dict_with_str_to_replace_event.items():
                    text_file = text_file.replace(key, value)
                with open(filename, 'w', encoding="utf-8") as text_file_write:
                    text_file_write.write(text_file)

    for filename in glob.iglob(filepath_to_events + '**/*.txt', recursive=True):
        if DataCleaner.skip_files(files_to_skip=files_to_skip, filename=filename):
            continue

        text_file = FileOpener.open_text_file(filename, lowercase=False)
        pattern_matches = re.findall('^country_event = \\{(.*?)^\\}', text_file, flags=re.DOTALL | re.MULTILINE)
        if len(pattern_matches) > 0:
            for event in pattern_matches:
                event_id = re.findall('^\\tid = (\\S+)', event, flags=re.MULTILINE)[0]

                hidden_event = "donotlog" in event
                if event_id in false_positives or hidden_event:
                    continue

                options = re.findall('(^\\toption = \\{.*?^\\t\\})', event, flags=re.DOTALL | re.MULTILINE)

                for index, option in enumerate(options):
                    if 'log = "[GetLogInfo]: event ' + event_id not in option:
                        print(f'{event_id}, option {index} - missing logging')

    # 2. Event logging - immediate
    for filename in glob.iglob(filepath_to_events + '**/*.txt', recursive=True):
        if DataCleaner.skip_files(files_to_skip=files_to_skip, filename=filename):
            continue

        text_file = FileOpener.open_text_file(filename, lowercase=False)
        pattern_matches = re.findall('^news_event = \\{(.*?)^\\}', text_file, flags=re.DOTALL | re.MULTILINE)
        if len(pattern_matches) > 0:
            dict_with_str_to_replace = dict()
            for event in pattern_matches:
                event_id = re.findall('^\\tid = (\\S+)', event, flags=re.MULTILINE)[0]
                if event_id in false_positives:
                    continue

                hidden_event = "hidden = yes" in event or "donotlog" in event
                has_any_logging = "immediate = { log =" in event
                has_data_logging = 'immediate = { log = "KR_Event_Logging' in event
                expected_logging_line = 'immediate = { log = "[GetLogInfo]: event ' + event_id + '" }'
                has_valid_logging = expected_logging_line in event

                if not has_valid_logging and not hidden_event:
                    if has_any_logging and not has_data_logging:
                        str_to_replace = re.findall('immediate = \\{ log =.*', event)[0]
                        dict_with_str_to_replace[event] = event.replace(str_to_replace, expected_logging_line)
                    if not has_any_logging:
                        x = re.findall('^\\tid = .*', event, flags=re.MULTILINE)[0]
                        dict_with_str_to_replace[event] = event.replace(x, f'{x}\n\t{expected_logging_line}')

            for key, value in dict_with_str_to_replace.items():
                text_file = text_file.replace(key, value)
            with open(filename, 'w', encoding="utf-8") as text_file_write:
                text_file_write.write(text_file)


def format_logging_decisions(username, mod_name):
    """Add logging to decisions

    Args:
        username (_type_): windows username
        mod_name (_type_): mod folder name
    """
    test_runner = TestRunner(username, mod_name)
    filepath_to_decisions = f'{test_runner.full_path_to_mod}common\\decisions\\'

    for filename in glob.iglob(filepath_to_decisions + '**/*.txt', recursive=True):
        if '\\categories' in filename or "Generic decisions" in filename:
            continue
        text_file = FileOpener.open_text_file(filename, lowercase=False)
        pattern_matches = re.findall('^\\t[^\\t#]+ = \\{.*?^\\t\\}', text_file, flags=re.MULTILINE | re.DOTALL)
        if len(pattern_matches) > 0:
            dict_with_str_to_replace = dict()
            for dec in pattern_matches:
                dec_id = re.findall('^\\t([^\t]+) = \\{', dec, flags=re.MULTILINE)[0]

                donotlog = "donotlog" in dec
                if donotlog:
                    continue

                cancel_effect = re.findall('(\\t+)cancel_effect = \\{([^\\n]*|.*?^\\1)\\}', dec, flags=re.DOTALL | re.MULTILINE)[0][1] if 'cancel_effect =' in dec else False
                complete_effect = re.findall('(\\t+)complete_effect = \\{([^\\n]*|.*?^\\1)\\}', dec, flags=re.DOTALL | re.MULTILINE)[0][1] if 'complete_effect =' in dec else False
                remove_effect = re.findall('(\\t+)remove_effect = \\{([^\\n]*|.*?^\\1)\\}', dec, flags=re.DOTALL | re.MULTILINE)[0][1] if 'remove_effect =' in dec else False
                timeout_effect = re.findall('(\\t+)timeout_effect = \\{([^\\n]*|.*?^\\1)\\}', dec, flags=re.DOTALL | re.MULTILINE)[0][1] if 'timeout_effect =' in dec else False
                is_targeted = "FROM" in dec or "state_target = yes" in dec or "target_trigger" in dec or "target_root_trigger" in dec
                target_line = "[GetLogFrom]" if is_targeted else ""
                expected_logging_line_cancel = f'log = "[GetLogRoot]{target_line}: Decision cancel {dec_id}"'
                expected_logging_line_complete = f'log = "[GetLogRoot]{target_line}: Decision complete {dec_id}"'
                expected_logging_line_remove = f'log = "[GetLogRoot]{target_line}: Decision remove {dec_id}"'
                expected_logging_line_timeout = f'log = "[GetLogRoot]{target_line}: Decision timeout {dec_id}"'
                has_any_logging_cancel = 'cancel_effect = {\n\t\t\tlog' in dec
                has_any_logging_complete = 'complete_effect = {\n\t\t\tlog' in dec
                has_any_logging_remove = 'remove_effect = {\n\t\t\tlog' in dec
                has_any_logging_timeout = 'timeout_effect = {\n\t\t\tlog' in dec
                fixed_decision_code = dec

                if cancel_effect:
                    if expected_logging_line_cancel not in cancel_effect:
                        if has_any_logging_cancel:
                            str_to_replace_cancel = re.findall('cancel_effect = \\{.*\\n\\t+log =.*', dec)[0]
                            fixed_decision_code = fixed_decision_code.replace(str_to_replace_cancel, 'cancel_effect = {\n\t\t\t' + expected_logging_line_cancel)

                        if not has_any_logging_cancel:
                            str_to_replace_cancel = re.findall('cancel_effect = \\{', dec)[0]
                            fixed_decision_code = fixed_decision_code.replace(str_to_replace_cancel, 'cancel_effect = {\n\t\t\t' + expected_logging_line_cancel)

                if complete_effect:
                    if expected_logging_line_complete not in complete_effect:
                        if has_any_logging_complete:
                            str_to_replace_complete = re.findall('complete_effect = \\{.*\\n\\t+log =.*', dec)[0]
                            fixed_decision_code = fixed_decision_code.replace(str_to_replace_complete, 'complete_effect = {\n\t\t\t' + expected_logging_line_complete)

                        if not has_any_logging_complete:
                            str_to_replace_complete = re.findall('complete_effect = \\{', dec)[0]
                            fixed_decision_code = fixed_decision_code.replace(str_to_replace_complete, 'complete_effect = {\n\t\t\t' + expected_logging_line_complete)

                if remove_effect:
                    if expected_logging_line_remove not in remove_effect:
                        if has_any_logging_remove:
                            str_to_replace_remove = re.findall('remove_effect = \\{.*\\n\\t+log =.*', dec)[0]
                            fixed_decision_code = fixed_decision_code.replace(str_to_replace_remove, 'remove_effect = {\n\t\t\t' + expected_logging_line_remove)

                        if not has_any_logging_remove:
                            str_to_replace_remove = re.findall('remove_effect = \\{', dec)[0]
                            fixed_decision_code = fixed_decision_code.replace(str_to_replace_remove, 'remove_effect = {\n\t\t\t' + expected_logging_line_remove)

                if timeout_effect:
                    if expected_logging_line_timeout not in timeout_effect:
                        if has_any_logging_timeout:
                            str_to_replace_timeout = re.findall('timeout_effect = \\{.*\\n\\t+log =.*', dec)[0]
                            fixed_decision_code = fixed_decision_code.replace(str_to_replace_timeout, 'timeout_effect = {\n\t\t\t' + expected_logging_line_timeout)

                        if not has_any_logging_timeout:
                            str_to_replace_timeout = re.findall('timeout_effect = \\{', dec)[0]
                            fixed_decision_code = fixed_decision_code.replace(str_to_replace_timeout, 'timeout_effect = {\n\t\t\t' + expected_logging_line_timeout)

                if fixed_decision_code != dec:
                    dict_with_str_to_replace[dec] = fixed_decision_code

            for key, value in dict_with_str_to_replace.items():
                text_file = text_file.replace(key, value)
            with open(filename, 'w', encoding="utf-8") as text_file_write:
                text_file_write.write(text_file)


def format_logging_focuses(username, mod_name):
    """Add logging to focuses

    Args:
        username (_type_): windows username
        mod_name (_type_): mod folder name
    """
    test_runner = TestRunner(username, mod_name)
    filepath_to_focuses = f'{test_runner.full_path_to_mod}common\\national_focus\\'

    # Regular focus
    for filename in glob.iglob(filepath_to_focuses + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename, lowercase=False)
        pattern_matches = re.findall('^\\tfocus = \\{.*?^\\t\\}', text_file, flags=re.MULTILINE | re.DOTALL)
        if len(pattern_matches) > 0:
            dict_with_str_to_replace = dict()
            for focus in pattern_matches:
                try:
                    focus_id = re.findall('^\\t\\tid = (\S+)', focus, flags=re.MULTILINE)[0]

                    select_effect = re.findall('(\\t+)select_effect = \\{([^\\n]*|.*?^\\1)\\}', focus, flags=re.DOTALL | re.MULTILINE)[0][1] if 'select_effect =' in focus else False
                    complete_effect = re.findall('(\\t+)completion_reward = \\{([^\\n]*|.*?^\\1)\\}', focus, flags=re.DOTALL | re.MULTILINE)[0][1] if 'completion_reward =' in focus else False

                    expected_logging_line_select = f'log = "[GetLogRoot]: Select Focus {focus_id}"'
                    expected_logging_line_complete = f'log = "[GetLogRoot]: Focus Completed {focus_id}"'

                    has_any_logging_select = 'select_effect = {\n\t\t\tlog' in focus
                    has_any_logging_complete = 'completion_reward = {\n\t\t\tlog' in focus

                    fixed_focus_code = focus
                except IndexError:
                    print(focus)
                    raise

                if select_effect:
                    if expected_logging_line_select not in select_effect:
                        if has_any_logging_select:
                            str_to_replace_select = re.findall('select_effect = \\{.*\\n\\t+log =.*', focus)[0]
                            fixed_focus_code = fixed_focus_code.replace(str_to_replace_select, 'select_effect = {\n\t\t\t' + expected_logging_line_select)

                        if not has_any_logging_select:
                            str_to_replace_select = re.findall('select_effect = \\{', focus)[0]
                            fixed_focus_code = fixed_focus_code.replace(str_to_replace_select, 'select_effect = {\n\t\t\t' + expected_logging_line_select)

                if complete_effect:
                    if expected_logging_line_complete not in complete_effect:
                        if has_any_logging_complete:
                            str_to_replace_complete = re.findall('completion_reward = \\{.*\\n\\t+log =.*', focus)[0]
                            fixed_focus_code = fixed_focus_code.replace(str_to_replace_complete, 'completion_reward = {\n\t\t\t' + expected_logging_line_complete)

                        if not has_any_logging_complete:
                            str_to_replace_complete = re.findall('completion_reward = \\{', focus)[0]
                            fixed_focus_code = fixed_focus_code.replace(str_to_replace_complete, 'completion_reward = {\n\t\t\t' + expected_logging_line_complete)

                if fixed_focus_code != focus:
                    dict_with_str_to_replace[focus] = fixed_focus_code

            for key, value in dict_with_str_to_replace.items():
                text_file = text_file.replace(key, value)
            with open(filename, 'w', encoding="utf-8") as text_file_write:
                text_file_write.write(text_file)

    # Shared focus
    for filename in glob.iglob(filepath_to_focuses + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename, lowercase=False)
        pattern_matches = re.findall('^shared_focus = \\{.*?^\\}', text_file, flags=re.MULTILINE | re.DOTALL)
        if len(pattern_matches) > 0:
            dict_with_str_to_replace = dict()
            for focus in pattern_matches:
                focus_id = re.findall('^\\tid = (\S+)', focus, flags=re.MULTILINE)[0]

                select_effect = re.findall('(\\t+)select_effect = \\{([^\\n]*|.*?^\\1)\\}', focus, flags=re.DOTALL | re.MULTILINE)[0][1] if 'select_effect =' in focus else False
                complete_effect = re.findall('(\\t+)completion_reward = \\{([^\\n]*|.*?^\\1)\\}', focus, flags=re.DOTALL | re.MULTILINE)[0][1] if 'completion_reward =' in focus else False

                expected_logging_line_select = f'log = "[GetLogRoot]: Select Focus {focus_id}"'
                expected_logging_line_complete = f'log = "[GetLogRoot]: Focus Completed {focus_id}"'

                has_any_logging_select = 'select_effect = {\n\t\tlog' in focus
                has_any_logging_complete = 'completion_reward = {\n\t\tlog' in focus

                fixed_focus_code = focus

                if select_effect:
                    if expected_logging_line_select not in select_effect:
                        if has_any_logging_select:
                            str_to_replace_select = re.findall('select_effect = \\{.*\\n\\t+log =.*', focus)[0]
                            fixed_focus_code = fixed_focus_code.replace(str_to_replace_select, 'select_effect = {\n\t\t' + expected_logging_line_select)

                        if not has_any_logging_select:
                            str_to_replace_select = re.findall('select_effect = \\{', focus)[0]
                            fixed_focus_code = fixed_focus_code.replace(str_to_replace_select, 'select_effect = {\n\t\t' + expected_logging_line_select)

                if complete_effect:
                    if expected_logging_line_complete not in complete_effect:
                        if has_any_logging_complete:
                            str_to_replace_complete = re.findall('completion_reward = \\{.*\\n\\t+log =.*', focus)[0]
                            fixed_focus_code = fixed_focus_code.replace(str_to_replace_complete, 'completion_reward = {\n\t\t' + expected_logging_line_complete)

                        if not has_any_logging_complete:
                            str_to_replace_complete = re.findall('completion_reward = \\{', focus)[0]
                            fixed_focus_code = fixed_focus_code.replace(str_to_replace_complete, 'completion_reward = {\n\t\t' + expected_logging_line_complete)

                if fixed_focus_code != focus:
                    dict_with_str_to_replace[focus] = fixed_focus_code

            for key, value in dict_with_str_to_replace.items():
                text_file = text_file.replace(key, value)
            with open(filename, 'w', encoding="utf-8") as text_file_write:
                text_file_write.write(text_file)


def format_characters(username, mod_name):
    """Add logging to focuses

    Args:
        username (_type_): windows username
        mod_name (_type_): mod folder name
    """
    test_runner = TestRunner(username, mod_name)
    filepath = test_runner.full_path_to_mod
    advisors = Characters.get_all_advisors(test_runner=test_runner, lowercase=False, return_paths=False)
    adv_link_dict = {}
    for adv in advisors:
        try:
            tab = re.findall(r'\n(\t*?)slot =', adv)[0]
        except Exception:
            print(adv)
            raise
        a = Advisors(adv)
        slot = f"{tab}slot = {a.slot}\n" if a.slot else ""
        idea_token = f"{tab}idea_token = {a.token}\n" if a.token else ""
        name = f"{tab}name = {a.name}\n" if a.name else ""
        desc = f"{tab}desc = {a.desc}\n" if a.desc else ""
        ledger = f"{tab}ledger = {a.ledger_slot}\n" if a.ledger_slot else ""
        traits = f"{tab}traits = {{ {' '.join([i for i in a.traits])} }}\n" if a.traits_line else ""
        modifier = f"{tab}modifier = {a.modifier}\n" if a.modifier else ""
        research_bonus = f"{tab}research_bonus = {a.research_bonus}\n" if a.research_bonus else ""
        allowed = f"{tab}allowed = {a.allowed}\n" if a.allowed else ""
        available = f"{tab}available = {a.available}\n" if a.available else ""
        visible = f"{tab}visible = {a.visible}\n" if a.visible else ""
        cost = f"{tab}cost = {a.cost}\n" if a.cost else ""
        can_be_fired = f"{tab}can_be_fired = {a.can_be_fired}\n" if a.can_be_fired else ""
        on_add = f"{tab}on_add = {a.on_add}\n" if a.on_add else ""
        on_remove = f"{tab}on_remove = {a.on_remove}\n" if a.on_remove else ""
        ai_will_do = f"{tab}ai_will_do = {a.ai_will_do}\n" if a.ai_will_do else ""

        new_str = f'\n{name}{slot}{idea_token}{desc}{ledger}{allowed}{available}{visible}{traits}{modifier}{research_bonus}{cost}{can_be_fired}{on_add}{on_remove}{ai_will_do}'
        adv_link_dict[adv] = new_str

    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename, lowercase=False)
        if "characters" in filename or "add_advisor_role = {" in text_file:
            file_encoding = detect_encoding(filename)
            text_file_new = text_file
            override = False
            if "advisor" in text_file:
                for adv in adv_link_dict.keys():
                    if adv in text_file:
                        text_file_new = text_file_new.replace(adv, adv_link_dict[adv])
                        override = True

            if override:
                with open(filename, 'w', encoding=file_encoding) as text_file_write:
                    text_file_write.write(text_file_new)


def apply_formatting(filename, encoding="utf-8"):
    replace_string(filename=filename, pattern='(?<=[\\w_\\"=\\{\\}])  (?=[\\w_\\"=\\{\\}])', replace_with=' ', encoding=encoding)  # Remove any doublespaces
    replace_string(filename=filename, pattern='=\\b', replace_with='= ', encoding=encoding)                     # Add spaces between symbol and =
    replace_string(filename=filename, pattern='\\b=', replace_with=' =', encoding=encoding)                     # Add spaces between symbol and =
    replace_string(filename=filename, pattern='=\\{', replace_with='= {', encoding=encoding)                    # Add spaces between symbol and =
    replace_string(filename=filename, pattern='[ \\t]{1,}\\n', replace_with='\\n', encoding=encoding)           # Remove trailing whitespaces
    replace_string(filename=filename, pattern='\\{(?=[\\w_\\"=])', replace_with='{ ', encoding=encoding)        # Add spaces between symbol and {
    replace_string(filename=filename, pattern='(?<=[\\w_\\"=])\\}', replace_with=' }', encoding=encoding)       # Add spaces between symbol and }
    replace_string(filename=filename, pattern='(?<=[^\\n])\\Z', replace_with='\\n', encoding=encoding)          # Add last line if file is missing
    replace_string(filename=filename, pattern='(?<=^)    ', replace_with='\\t', encoding=encoding, flag=re.MULTILINE)  # Fix cases of using spaces
    replace_string(filename=filename, pattern='(?<=\\t)        ', replace_with='\\t\\t', encoding=encoding, flag=re.MULTILINE)  # Fix cases of using spaces
    replace_string(filename=filename, pattern='(?<=\\t)        ', replace_with='\\t\\t', encoding=encoding, flag=re.MULTILINE)  # Fix cases of using spaces
    replace_string(filename=filename, pattern='(?<=\\t)    ', replace_with='\\t', encoding=encoding, flag=re.MULTILINE)  # Fix cases of using spaces
    replace_string(filename=filename, pattern='(?<=\\t)    ', replace_with='\\t', encoding=encoding, flag=re.MULTILINE)  # Fix cases of using spaces
    replace_string(filename=filename, pattern='^$\\n{2,}', replace_with='\\n', encoding=encoding, flag=re.MULTILINE)          # Add last line if file is missing
    replace_string(filename=filename, pattern='\\{	(?=\\w)', replace_with='{ ', encoding=encoding, flag=re.MULTILINE)          # \t -> space
    replace_string(filename=filename, pattern='=	(?=\\w)', replace_with='= ', encoding=encoding, flag=re.MULTILINE)          # \t -> space
    replace_string(filename=filename, pattern='(?<=\\w)	\\}', replace_with=' }', encoding=encoding, flag=re.MULTILINE)          # \t -> space
    replace_string(filename=filename, pattern='(?<=\\w)	=', replace_with=' =', encoding=encoding, flag=re.MULTILINE)            # \t -> space

    replace_string(filename=filename, pattern='.*immediate = \\{ log = \\"\\[GetDateText\\]: \\[Root.GetName\\]: event.*\\n', replace_with='', encoding=encoding)       # outdated logging
    # replace_string(filename=filename, pattern='.*log = \\"\\[GetLogInfo\\]:.*\\n', replace_with='', encoding=encoding)       # outdated logging

    replace_string(filename=filename, pattern='limit = \\{\\n\\t+(has_template = .*?)\\n\\t+\\}', replace_with='limit = { \\1 }', encoding=encoding)
    replace_string(filename=filename, pattern='set_technology = \\{\\n\\t+(.+?)\\n\\t+\\}', replace_with='set_technology = { \\1 }', encoding=encoding)
    replace_string(filename=filename, pattern='delete_unit_template_and_units = \\{[^}]*?\\n\\t+(division_template = \".*?\").*\\n\\t+(disband = \\w+).*\\n\\t+\\}', replace_with='delete_unit_template_and_units = { \\1 \\2 }', encoding=encoding)
    replace_string(filename=filename, pattern='delete_unit_template_and_units = \\{[^}]*?\\n\\t+(division_template = \".*?\").*\\n\\t+\\}', replace_with='delete_unit_template_and_units = { \\1 }', encoding=encoding)
    replace_string(filename=filename, pattern='target_array = allies', replace_with='target_array = faction_members', encoding=encoding)
    replace_string(filename=filename, pattern='activate_targeted_decision = \\{\\n\\t+(target = .*?)\\n\\t+(decision = .*?)\\n\\t+\\}', replace_with='activate_targeted_decision = { \\1 \\2 }', encoding=encoding, flag=re.MULTILINE)
    replace_string(filename=filename, pattern='activate_targeted_decision = \\{\\n\\t+(decision = .*?)\\n\\t+(target = .*?)\\n\\t+\\}', replace_with='activate_targeted_decision = { \\2 \\1 }', encoding=encoding, flag=re.MULTILINE)
    replace_string(filename=filename, pattern='remove_targeted_decision = \\{\\n\\t+(target = .*?)\\n\\t+(decision = .*?)\\n\\t+\\}', replace_with='remove_targeted_decision = { \\1 \\2 }', encoding=encoding, flag=re.MULTILINE)
    replace_string(filename=filename, pattern='remove_targeted_decision = \\{\\n\\t+(decision = .*?)\\n\\t+(target = .*?)\\n\\t+\\}', replace_with='remove_targeted_decision = { \\2 \\1 }', encoding=encoding, flag=re.MULTILINE)
    replace_string(filename=filename, pattern='has_game_rule = \\{\\n\\t+(rule = .*?)\\n\\t+(option = .*?)\\n\\t+\\}', replace_with='has_game_rule = { \\1 \\2 }', encoding=encoding, flag=re.MULTILINE)
    replace_string(filename=filename, pattern='has_game_rule = \\{\\n\\t+(option = .*?)\\n\\t+(rule = .*?)\\n\\t+\\}', replace_with='has_game_rule = { \\2 \\1 }', encoding=encoding, flag=re.MULTILINE)

    replace_string(filename=filename, pattern='ai_chance = \\{\\n\\t+(base = [\\d\\.]+).*\\n\\t+\\}', replace_with='ai_chance = { \\1 }', encoding=encoding, flag=re.MULTILINE)
    replace_string(filename=filename, pattern='ai_chance = \\{\\n\\t+(factor = [\\d\\.]+).*\\n\\t+\\}', replace_with='ai_chance = { \\1 }', encoding=encoding, flag=re.MULTILINE)
    replace_string(filename=filename, pattern='ai_will_do = \\{\\n\\t+(base = [\\d\\.]+).*\\n\\t+\\}', replace_with='ai_will_do = { \\1 }', encoding=encoding, flag=re.MULTILINE)
    replace_string(filename=filename, pattern='ai_will_do = \\{\\n\\t+(factor = [\\d\\.]+).*\\n\\t+\\}', replace_with='ai_will_do = { \\1 }', encoding=encoding, flag=re.MULTILINE)

    replace_string(filename=filename, pattern='(?<!^)country_event = \\{\\n\\t+id = ([^ #]*?)\\n\\t+\\}', replace_with='country_event = \\1', encoding=encoding, flag=re.MULTILINE)                                                                  # base
    replace_string(filename=filename, pattern='(?<!^)country_event = \\{.*?(#.*?)\\n\\t+id = ([^ #]*?)\\n\\t+\\}', replace_with='country_event = \\2 \\1', encoding=encoding, flag=re.MULTILINE)                                                     # With comments
    replace_string(filename=filename, pattern='(?<!^)country_event = \\{\\n\\t+id = ([^ #]*?)[ \\t]*?(#.*?)\\n\\t+\\}', replace_with='country_event = \\1 \\2', encoding=encoding, flag=re.MULTILINE)                                                # With comments

    replace_string(filename=filename, pattern='(?<!^)set_province_name = \\{\\n\\t+(id = [^ #]*?)\\n\\t+(name = [^ #]*?)\\n\\t+\\}', replace_with='set_province_name = { \\1 \\2 }', encoding=encoding, flag=re.MULTILINE)
    replace_string(filename=filename, pattern='(?<!^)set_province_name = \\{\\n\\t+(name = [^ #]*?)\\n\\t+(id = [^ #]*?)\\n\\t+\\}', replace_with='set_province_name = { \\2 \\1 }', encoding=encoding, flag=re.MULTILINE)

    replace_string(filename=filename, pattern='(?<!^)country_event = \\{\\n\\t+(id = [^ #]*?)\\n\\t+(days = [^ #]*?)\\n\\t+\\}', replace_with='country_event = { \\1 \\2 }', encoding=encoding, flag=re.MULTILINE)                                   # base
    replace_string(filename=filename, pattern='(?<!^)country_event = \\{\\n\\t+(id = [^ #]*?)\\n\\t+(months = [^ #]*?)\\n\\t+\\}', replace_with='country_event = { \\1 \\2 }', encoding=encoding, flag=re.MULTILINE)                                 # months
    replace_string(filename=filename, pattern='(?<!^)country_event = \\{\\n\\t+(id = [^ #]*?)\\n\\t+(days = [^ #]*?)\\n\\t+(random_days = [^ #]*?)\\n\\t+\\}', replace_with='country_event = { \\1 \\2 \\3 }', encoding=encoding, flag=re.MULTILINE)  # with random_days
    replace_string(filename=filename, pattern='(?<!^)country_event = \\{\\n\\t+(id = [^ #]*?)\\n\\t+(random_days = [^ #]*?)\\n\\t+(days = [^ #]*?)\\n\\t+\\}', replace_with='country_event = { \\1 \\3 \\2 }', encoding=encoding, flag=re.MULTILINE)  # with random_days
    replace_string(filename=filename, pattern='(?<!^)country_event = \\{\\n\\t+(id = [^ #]*?)\\n\\t+(hours = [^ #]*?)\\n\\t+\\}', replace_with='country_event = { \\1 \\2 }', encoding=encoding, flag=re.MULTILINE)                                  # with hours
    replace_string(filename=filename, pattern='(?<!^)country_event = \\{\\n\\t+(id = [^ #]*?)\\n\\t+(hours = [^ #]*?)\\n\\t+(random_hours = [^ #]*?)\\n\\t+\\}', replace_with='country_event = { \\1 \\2 \\3 }', encoding=encoding, flag=re.MULTILINE)  # with hours and random_hours
    replace_string(filename=filename, pattern='(?<!^)country_event = \\{\\n\\t+(id = [^ #]*?)\\n\\t+(random_hours = [^ #]*?)\\n\\t+(hours = [^ #]*?)\\n\\t+\\}', replace_with='country_event = { \\1 \\3 \\2 }', encoding=encoding, flag=re.MULTILINE)  # with hours and random_hours
    replace_string(filename=filename, pattern='(?<!^)country_event = \\{\\n\\t+(id = [^ #]*?)\\n\\t+(days = [^ #]*?)\\n\\t+(random_hours = [^ #]*?)\\n\\t+\\}', replace_with='country_event = { \\1 \\3 \\2 }', encoding=encoding, flag=re.MULTILINE)   # with days and random_hours

    replace_string(filename=filename, pattern='(?<!^)country_event = \\{.*?(#.*?)\\n\\t+(id = [^ #]*?)\\n\\t+(days = [^ #]*?)\\n\\t+\\}', replace_with='country_event = { \\2 \\3 } \\1', encoding=encoding, flag=re.MULTILINE)                      # With comments
    replace_string(filename=filename, pattern='(?<!^)country_event = \\{.*?(#.*?)\\n\\t+(id = [^ #]*?)\\n\\t+(random_days = [^ #]*?)\\n\\t+\\}', replace_with='country_event = { \\2 \\3 } \\1', encoding=encoding, flag=re.MULTILINE)               # With comments
    replace_string(filename=filename, pattern='(?<!^)country_event = \\{.*?(#.*?)\\n\\t+(id = [^ #]*?)\\n\\t+(hours = [^ #]*?)\\n\\t+\\}', replace_with='country_event = { \\2 \\3 } \\1', encoding=encoding, flag=re.MULTILINE)                     # With comments
    replace_string(filename=filename, pattern='(?<!^)country_event = \\{.*?(#.*?)\\n\\t+(id = [^ #]*?)\\n\\t+(random_hours = [^ #]*?)\\n\\t+\\}', replace_with='country_event = { \\2 \\3 } \\1', encoding=encoding, flag=re.MULTILINE)              # With comments
    replace_string(filename=filename, pattern='(?<!^)country_event = \\{.*?(#.*?)\\n\\t+(id = [^ #]*?)\\n\\t+(days = [^ #]*?)\\n\\t+(random_days = [^ #]*?)\\n\\t+\\}', replace_with='country_event = { \\2 \\3 \\4 } \\1', encoding=encoding, flag=re.MULTILINE)                      # With comments

    replace_string(filename=filename, pattern='(?<!^)country_event = \\{\\n\\t+(id = [^ #]*?) .*?(#.*?)\\n\\t+(days = [^ #]*?)\\n\\t+\\}', replace_with='country_event = { \\1 \\3 } \\2', encoding=encoding, flag=re.MULTILINE)                                        # With comments on id line
    replace_string(filename=filename, pattern='(?<!^)country_event = \\{\\n\\t+(id = [^ #]*?) .*?(#.*?)\\n\\t+(days = [^ #]*?)\\n\\t+(random_days = [^ #]*?)\\n\\t+\\}', replace_with='country_event = { \\1 \\3 \\4 } \\2', encoding=encoding, flag=re.MULTILINE)      # With comments on id line
    replace_string(filename=filename, pattern='(?<!^)country_event = \\{\\n\\t+(id = [^ #]*?) .*?(#.*?)\\n\\t+(hours = [^ #]*?)\\n\\t+\\}', replace_with='country_event = { \\1 \\3 } \\2', encoding=encoding, flag=re.MULTILINE)                                       # With comments on id line
    replace_string(filename=filename, pattern='(?<!^)country_event = \\{\\n\\t+(id = [^ #]*?) .*?(#.*?)\\n\\t+(hours = [^ #]*?)\\n\\t+(random_hours = [^ #]*?)\\n\\t+\\}', replace_with='country_event = { \\1 \\3 \\4 } \\2', encoding=encoding, flag=re.MULTILINE)    # With comments on id line
    replace_string(filename=filename, pattern='(?<!^)country_event = \\{\\n\\t+(id = [^ #]*?) (days = [^ #]*?)\\n\\t+\\}', replace_with='country_event = { \\1 \\2 }', encoding=encoding, flag=re.MULTILINE)                                         # id and days on the same line
    replace_string(filename=filename, pattern='(?<!^)country_event = \\{\\n\\t+(id = [^ #]*?) (days = [^ #]*?) .*?(#.*?)\\n\\t+\\}', replace_with='country_event = { \\1 \\2 } \\3', encoding=encoding, flag=re.MULTILINE)                           # id and days and comments on the same line

    replace_string(filename=filename, pattern='(?<!^)transfer_ship = \\{\\n\\t+(prefer_name = [^#]*?)\\n\\t+(type = [^ #]*?)\\n\\t+(target = [^ #]*?)\\n\\t+\\}', replace_with='transfer_ship = { \\1 \\2 \\3 }', encoding=encoding, flag=re.MULTILINE)          # transfer ship w prefered name
    replace_string(filename=filename, pattern='(?<!^)transfer_ship = \\{\\n\\t+(type = [^ #]*?)\\n\\t+(target = [^ #]*?)\\n\\t+\\}', replace_with='transfer_ship = { \\1 \\2 }', encoding=encoding, flag=re.MULTILINE)                                           # transfer ship w/o prefered name

    # replace_string(filename=filename,
    #                pattern='random_owned_controlled_state = \\{\\n(\\t+)limit = \\{\\n(\\1.*\\n)*?\\1\\}\\n(\\1.*\\n)*?\\t+add_building_construction = \\{\\n\\t+type = industrial_complex\\n\\t+level = 1(\\n\\1.*\\n)*?\\t+\\}\\n\\t+\\}',
    #                replace_with='add_one_random_civilian_factory = yes', encoding=encoding, flag=re.MULTILINE)                           # Factory format


def apply_formatting_loc(filename, encoding="utf-8-sig"):
    replace_string(filename=filename, pattern='[ \\t]{1,}\\n', replace_with='\\n', encoding=encoding)           # Remove trailing whitespaces
    replace_string(filename=filename, pattern='\\{(?=[\\w_\\"=])', replace_with='{ ', encoding=encoding)        # Add spaces between symbol and {
    replace_string(filename=filename, pattern='(?<=[\\w_\\"=])\\}', replace_with=' }', encoding=encoding)       # Add spaces between symbol and }
    replace_string(filename=filename, pattern='(?<=[^\\n])\\Z', replace_with='\\n', encoding=encoding)          # Add last line if file is missing
    replace_string(filename=filename, pattern=':[0-9] ', replace_with=': ', encoding=encoding)                      # Purge version control
    replace_string(filename=filename, pattern='^$\\n{2,}', replace_with='\\n', encoding=encoding, flag=re.MULTILINE)          # Add last line if file is missing
    replace_string(filename=filename, pattern='^([^ #\\n]+?:) ', replace_with=' \\1 ', encoding=encoding, flag=re.MULTILINE)  # Add whitespace if the line doesn't start with


def apply_formatting_characters(filename, encoding="utf-8"):
    replace_string(filename=filename, pattern='\\t*ai_will_do = \\{ factor = 1 \\}.*\n', replace_with='', encoding=encoding)                  # Delete ai factors from characters files
    replace_string(filename=filename, pattern='\\t*ai_will_do = \\{.*\\n\\t*factor = 1\\n\\t*\\}.*\n', replace_with='', encoding=encoding)  # Delete ai factors from characters files


def format_kaiserreich(username, mod_name):
    runner = TestRunner(username, mod_name)
    filepath_common = f'{runner.full_path_to_mod}common\\'
    filepath_history = f'{runner.full_path_to_mod}history\\'
    filepath_events = f'{runner.full_path_to_mod}events\\'
    filepath_loc = f'{runner.full_path_to_mod}localisation\\'
    filepath_characters = f'{runner.full_path_to_mod}common\\characters\\'
    filepath_unit_names_divisions = f'{runner.full_path_to_mod}common\\units\\names_divisions\\'
    filepath_unit_names_ships = f'{runner.full_path_to_mod}common\\units\\names_ships\\'
    print(filepath_common)
    for filename in glob.iglob(filepath_common + '**/*.txt', recursive=True):
        if DataCleaner.skip_files(files_to_skip=FILES_TO_SKIP, filename=filename):
            continue
        apply_formatting(filename=filename)

    for filename in glob.iglob(filepath_history + '**/*.txt', recursive=True):
        if DataCleaner.skip_files(files_to_skip=FILES_TO_SKIP, filename=filename):
            continue
        apply_formatting(filename=filename, encoding="utf-8")

    for filename in glob.iglob(filepath_events + '**/*.txt', recursive=True):
        apply_formatting(filename=filename, encoding="utf-8")

    for filename in glob.iglob(filepath_unit_names_divisions + '**/*.txt', recursive=True):
        apply_formatting(filename=filename, encoding="utf-8")

    for filename in glob.iglob(filepath_unit_names_ships + '**/*.txt', recursive=True):
        apply_formatting(filename=filename, encoding="utf-8")

    for filename in glob.iglob(filepath_loc + '**/*.yml', recursive=True):
        apply_formatting_loc(filename=filename, encoding="utf-8-sig")

    for filename in glob.iglob(filepath_characters + '**/*.txt', recursive=True):
        apply_formatting_characters(filename=filename)

    format_events(username=username, mod_name=mod_name)


if __name__ == '__main__':
    format_kaiserreich(username="VADIM", mod_name="Kaiserreich Dev Build")
    # format_filenames_strategic_regions(username="VADIM", mod_name="Kaiserreich Dev Build")
    # format_filenames_states(username="VADIM", mod_name="Kaiserreich Dev Build")
    format_logging_events(username="VADIM", mod_name="Kaiserreich Dev Build")
    format_logging_decisions(username="VADIM", mod_name="Kaiserreich Dev Build")
    format_logging_focuses(username="VADIM", mod_name="Kaiserreich Dev Build")
    format_characters(username="VADIM", mod_name="Kaiserreich Dev Build")
