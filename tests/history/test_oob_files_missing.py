##########################
# Test script to detect missing oob files
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import logging
import os
import re
from pathlib import Path

from test_classes.generic_test_class import (
    FileOpener,
    ResultsReporter,
)


def test_oob_files_missing(test_runner: object):
    filepath = test_runner.full_path_to_mod
    path_to_oob_files = str(Path(test_runner.full_path_to_mod) / "history" / "units") + "/"
    oob_files = {}
    pattern = re.compile(r"^[^#]+oob = ([^ \t\n#]*)", flags=re.MULTILINE)

    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if "oob =" in text_file:
            pattern_matches = re.findall(pattern, text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    oob_files[match.strip('"')] = 0

    logging.debug(f"{len(oob_files)} unique usages of oob files found")
    for filename in glob.iglob(path_to_oob_files + "**/*.txt", recursive=True):
        for oob in oob_files:
            if oob == os.path.basename(filename.lower())[:-4]:
                oob_files[oob] += 1

    results = [i for i in oob_files if oob_files[i] == 0]
    ResultsReporter.report_results(results=results, message="Missing oob files were found.")
