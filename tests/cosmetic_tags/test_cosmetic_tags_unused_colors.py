##########################
# Test script to check for unused cosmetic tag colors
# This means that the color is defined but not used anywhere
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import logging
import re
from pathlib import Path

from test_classes.generic_test_class import (
    DataCleaner,
    FileOpener,
    ResultsReporter,
)

FALSE_POSITIVES = ["cro_habsburg"]


def test_cosmetic_tags_unused_colors(test_runner: object):
    filepath = test_runner.full_path_to_mod
    filepath_cosmetic = Path(test_runner.full_path_to_mod) / "common" / "countries" / "cosmetic.txt"
    cosmetic_tags = {}
    # 1. get the dict of all cosmetic tags
    text_file = FileOpener.open_text_file(filepath_cosmetic)
    pattern_matches = re.findall(r"^(\S+) = \{", text_file, flags=re.MULTILINE)
    for match in pattern_matches:
        cosmetic_tags[match] = 0

    # 2. count the number of tag occurrences
    logging.debug(f"{len(cosmetic_tags)} cosmetic tags colors were found")
    assert len(cosmetic_tags) > 0, "cosmetic_tags must not be empty"
    cosmetic_tags = DataCleaner.clear_false_positives(input_iter=cosmetic_tags, false_positives=FALSE_POSITIVES)

    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if "set_cosmetic_tag =" in text_file:
            not_encountered_cosmetic_tags = [i for i in cosmetic_tags.keys() if cosmetic_tags[i] == 0]
            for flag in not_encountered_cosmetic_tags:
                cosmetic_tags[flag] += text_file.count(f"set_cosmetic_tag = {flag}")

    # 3. throw the error if tag is not used
    results = [i for i in cosmetic_tags if cosmetic_tags[i] == 0]
    ResultsReporter.report_results(results=results, message="Unused cosmetic tags colors were encountered. Assign them with set_cosmetic_tag")
