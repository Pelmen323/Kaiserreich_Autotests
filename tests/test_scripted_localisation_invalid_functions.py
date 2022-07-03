##########################
# Test script to check for various loc syntax issues
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re

from ..data.scripted_localisation_functions import \
    scripted_localisation_functions
from ..test_classes.generic_test_class import FileOpener, ResultsReporter
from ..test_classes.scripted_loc_class import Scripted_localisation


def test_check_unsupported_scripted_loc(test_runner: object):
    filepath = f'{test_runner.full_path_to_mod}localisation\\'
    custom_scripted_loc = Scripted_localisation.get_scripted_loc_names(test_runner=test_runner, lowercase=True)
    test_data_list = [i.lower() for i in scripted_localisation_functions]
    results = {}
    for filename in glob.iglob(filepath + '**/*.yml', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        text_file_splitted = text_file.lower().split('\n')[1:]
        for line in range(len(text_file_splitted)):
            current_line = text_file_splitted[line]
            current_line_number = line + 2

            if "[" in current_line:                                                             # 1. Get all scripted loc usages in yml files
                scripted_loc_pattern = re.findall("\\[.*?\\]", current_line)
                if len(scripted_loc_pattern) > 0:
                    for func in scripted_loc_pattern:
                        func = func[1:-1]                                                       # 2. Cut brackets ( [ ] )                    
                        if func[0] != "?" and func[0] != "!":                                   # 3. Variables (?) and gui (!) - ignore those instances                      
                            if "." in func:                                                     # 4. Scoping - cut it
                                func = func[func.rindex(".", ) + 1:]
                            if func not in test_data_list and func not in custom_scripted_loc:  # 5. Check if func is present in vanilla scripted loc and in custom scripted loc
                                results[f'{os.path.basename(filename)}, line {current_line_number}'] = func

    ResultsReporter.report_results(results=results, message="Unsupported scripted loc functions were found. Check console output")
