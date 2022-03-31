import glob
import os
from ..test_classes.modifiers_loc_class import Modifiers
from ..test_classes.generic_test_class import FileOpener, ResultsReporter


def test_loc_references_to_keys(test_runner: object):
    filepath = test_runner.full_path_to_mod
    results = Modifiers.get_all_modifiers(path="Vanilla", lowercase=False)
    results_kr = Modifiers.get_all_modifiers(path=f"{test_runner.full_path_to_mod}localisation\\replace\\KR_Vanilla_Override_l_english.yml", lowercase=False)
    results.update(results_kr)
    lines_to_report = []

    for filename in glob.iglob(filepath + '**/*.yml', recursive=True):
        if 'KR_Vanilla_Override_l_english.yml' in filename:
            continue
        text_file = FileOpener.open_text_file(filename, lowercase=False)

        for key, value in results.items():
            if value == "REMOVE_IDEA":
                continue
            if f'{key}:' in text_file:
                lines_to_report.append((f"{key}: - can be replaced with {value} - {os.path.basename(filename)}"))

            if ':' in key:
                if f'{key}' in text_file:
                    lines_to_report.append((f"{key} - can be replaced with {value} - {os.path.basename(filename)}"))

    ResultsReporter.report_results(results=sorted(lines_to_report),  message="Lines that can be replaced with modifiers variables were encountered. Check console output")
