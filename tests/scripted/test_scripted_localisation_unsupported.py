##########################
# Test script to check for various loc syntax issues
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re
from pathlib import Path

from data.scripted_localisation_functions import \
    scripted_localisation_functions
from test_classes.generic_test_class import FileOpener, ResultsReporter
from test_classes.scripted_loc_class import ScriptedLocalisation


def test_scripted_loc_unsupported(test_runner: object):
    filepath = str(Path(test_runner.full_path_to_mod) / "localisation") + "/"
    custom_scripted_loc = set(ScriptedLocalisation.get_all_scripted_loc_names(test_runner=test_runner))
    vanilla_scripted_loc = {i.lower() for i in scripted_localisation_functions}
    scripted_loc_pattern = re.compile(r"\[.*?\]")
    results = []

    for filename in glob.iglob(filepath + '**/*.yml', recursive=True):
        text_file = FileOpener.open_text_file(filename)
        if '[' not in text_file:
            continue

        for line in text_file.splitlines():
            if line.lstrip().startswith('#'):                       # Skip non- loc keys
                continue

            scripted_loc_matches = scripted_loc_pattern.findall(line)
            for match in scripted_loc_matches:
                match = match[1:-1]                                 # Cut brackets
                if match[0] not in ["?", "!", "("]:                 # Variables (?, () and gui (!) - ignore
                    if "$" not in match:                            # Reference to a variable - ignore
                        if "." in match:
                            match = match.rsplit(".", 1)[1]         # Cut all scoping
                        if match not in custom_scripted_loc and match not in vanilla_scripted_loc:
                            results.append(f'{match} - {os.path.basename(filename)}')

    ResultsReporter.report_results(results=results, message="Unsupported scripted loc functions were found.")
