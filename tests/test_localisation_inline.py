import glob
import re
import os
import py
import pytest
from ..test_classes.modifiers_loc_class import Modifiers
from ..test_classes.generic_test_class import FileOpener, ResultsReporter, DataCleaner
FILES_TO_SKIP = []#['localisation', 'game_rules', 'names', 'names_ships', 'names_divsions']
LINES_TO_SKIP = ['log =', 'division_template', 'gfx', '19', '18', 'transfer_ship =', '_desc',
                 'waking the tiger', 'together for victory', 'la resistance', 'man the guns',
                 'no step back', 'death or dishonor', 'window_name = ', '[', '#']


list_of_filepaths_to_check = [
    "common\\scripted_localisation\\",
    # "events\\",
]


@pytest.mark.parametrize("filepath_to_check", list_of_filepaths_to_check)
def test_loc_references_to_keys(test_runner: object, filepath_to_check):
    filepath_test = f'{test_runner.full_path_to_mod}{filepath_to_check}'
    results = []
    paths = {}

    for filename in glob.iglob(filepath_test + '**/*.txt', recursive=True):
        if DataCleaner.skip_files(files_to_skip=FILES_TO_SKIP, filename=filename):
            continue
        text_file = FileOpener.open_text_file(filename)

        text_file_splitted = text_file.split('\n')[1:]
        for line in range(len(text_file_splitted)):
            current_line = text_file_splitted[line]
            pattern_matches = re.findall('".*"', current_line)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    if len([i for i in LINES_TO_SKIP if i in current_line]) == 0:
                        if len(match) > 7:
                            results.append(match)
                            paths[match] = os.path.basename(filename)

    ResultsReporter.report_results(results=results, paths=paths, message="Inline loc has been encountered. Check console output")
