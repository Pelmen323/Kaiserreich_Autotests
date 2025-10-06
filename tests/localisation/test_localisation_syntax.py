##########################
# Test script to check for various loc syntax issues
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
from pathlib import Path

from test_classes.generic_test_class import FileOpener, ResultsReporter
from test_classes.localization_class import Localization


def test_check_localisation_files_syntax(test_runner: object):
    filepath = str(Path(test_runner.full_path_to_mod) / "localisation") + "/"
    colors = Localization.get_all_colors(test_runner)
    results = []
    for filename in glob.iglob(filepath + "**/*.yml", recursive=True):
        if "Ukraine" in filename:
            continue
        text_file = FileOpener.open_text_file(filename, lowercase=False)

        text_file_splitted = text_file.split("\n")[1:]
        for line in range(len(text_file_splitted)):
            current_line = text_file_splitted[line]
            if "#" not in current_line and [i for i in ["", " ", "l_english:"] if i == current_line] == []:
                if "§" in current_line and "desc_end" not in current_line:
                    if current_line.count("§") % 2 != 0:
                        results.append(f"{os.path.basename(filename)}, line {line+2}, colors - Number of '§' symbols is not even - {current_line.count('§')}")
                    elif current_line.count("§") != current_line.count("§!") * 2:
                        results.append(
                            f"{os.path.basename(filename)}, line {line+2}, colors - Not enough §! symbols - expected {int(current_line.count('§') / 2)} but got - {current_line.count('§!')}"
                        )
                    else:
                        try:
                            for ind, s in enumerate(current_line):
                                current_color = current_line[ind + 1]
                                if s == "§" and current_color not in colors and current_color not in ["!", "[", "$"]:
                                    results.append(f"{os.path.basename(filename)}, line {line+2}, colors - Unsupported color {current_line[ind+1]}")
                        except Exception:
                            continue

    ResultsReporter.report_results(results=results, message="Loc syntax issues were found.")
