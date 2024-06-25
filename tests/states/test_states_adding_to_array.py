##########################
# Test script to check for states that are incorrectly added to arrays
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re
import logging

from test_classes.generic_test_class import FileOpener, ResultsReporter


def test_states_adding_to_array(test_runner: object):
    filepath = test_runner.full_path_to_mod
    results = []
    paths = {}

    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        if "history" in filename:
            continue
        text_file = FileOpener.open_text_file(filename)
        if "add_to_array" in text_file or "add_to_temp_array" in text_file:
            pattern_matches = re.findall(r"\n([^\n]*?\n[^\n]*?)(add_to_array = \{.*?= \b([^\}]*)\b.*?\})", text_file, flags=re.DOTALL | re.MULTILINE)
            pattern_matches += re.findall(r"\n([^\n]*?\n[^\n]*?)(add_to_temp_array = \{.*?= \b([^\}]*)\b.*?\})", text_file, flags=re.DOTALL | re.MULTILINE)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    prefix = match[0]
                    body = match[1]
                    target = match[2]
                    # Don't check arrays with index
                    if "index" in body:
                        continue

                    # 1. Check if ID is used
                    if '.id' in target:
                        continue

                    # 1.1 Narrow down search only to arrays with states
                    try:
                        int(target)
                    except Exception:
                        continue

                    # 2. Check if target state is somewhere in prefix
                    if f'{target} = ' + '{' in prefix:
                        continue
                    # 3. Foolproof for some values
                    elif int(target) < 10:
                        logging.error(f'Double-check {body} array - it may target state using invalid syntax')
                    # 3 Report the issue
                    else:
                        results.append(body)
                        paths[body] = os.path.basename(filename)

    ResultsReporter.report_results(results=results, paths=paths, message="Invalid state adding to array encountered. Use state.id instead")
