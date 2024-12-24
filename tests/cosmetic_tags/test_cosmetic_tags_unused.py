##########################
# Test script to check for unused cosmetic tags via any of possible ways:
# - cosmetic.txt
# - country flag files .tga
# - has_cosmetic_tag trigger
# - localisation
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import logging
import os
import re
from pathlib import Path

from test_classes.generic_test_class import FileOpener, ResultsReporter


def test_cosmetic_tags_unused(test_runner: object):
    filepath = test_runner.full_path_to_mod
    cosmetic_tags = {}
    paths = {}
    # 1. get the dict of all cosmetic tags
    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if "set_cosmetic_tag =" in text_file:
            pattern_matches = re.findall(r"set_cosmetic_tag = ([^ \n\t]+)", text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    cosmetic_tags[match] = 0
                    paths[match] = os.path.basename(filename)

    # 2. count the number of tag occurrences
    logging.debug(f"{len(cosmetic_tags)} set cosmetic tags were found")
    assert len(cosmetic_tags) > 0, "cosmetic_tags must not be empty"

    # Usage in country colors
    filepath_cosmetic = Path(test_runner.full_path_to_mod) / "common" / "countries" / "cosmetic.txt"
    text_file = FileOpener.open_text_file(filepath_cosmetic)
    not_encountered_cosmetic_tags = [i for i in cosmetic_tags.keys() if cosmetic_tags[i] == 0]

    for flag in not_encountered_cosmetic_tags:
        if f"{flag} =" in text_file:
            cosmetic_tags[flag] += 1

    # Usage in tga flags
    country_flags = []
    path_to_flags = str(Path(test_runner.full_path_to_mod) / "gfx" / "flags" / "**/*.tga")

    for filename in glob.iglob(path_to_flags, recursive=True):
        country_flags.append(os.path.basename(filename.lower())[:-4])

    for flag in not_encountered_cosmetic_tags:
        if flag in country_flags:
            cosmetic_tags[flag] += 1
        else:
            for i in [
                "_social_democrat",
                "_social_liberal",
                "_market_liberal",
                "_social_conservative",
                "_authoritarian_democrat",
                "_paternal_autocrat",
                "_national_populist",
                "_radical_socialist",
                "_syndicalist",
                "_totalist",
            ]:
                if flag + i in country_flags:
                    cosmetic_tags[flag] += 1

    # Usage via has_cosmetic_tag
    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename)
        not_encountered_cosmetic_tags = [i for i in cosmetic_tags.keys() if cosmetic_tags[i] == 0]

        if "has_cosmetic_tag =" in text_file:
            all_matches = re.findall(r"has_cosmetic_tag = [^ \n\t]*", text_file)
            for flag in not_encountered_cosmetic_tags:
                cosmetic_tags[flag] += all_matches.count(f"has_cosmetic_tag = {flag}")

    # Usage in loc
    for filename in glob.iglob(filepath + "**/*.yml", recursive=True):
        text_file = FileOpener.open_text_file(filename)
        not_encountered_cosmetic_tags = [i for i in cosmetic_tags.keys() if cosmetic_tags[i] == 0]

        for flag in not_encountered_cosmetic_tags:
            if f"{flag}:" in text_file:
                cosmetic_tags[flag] += 1

        for i in [
            "_social_democrat:",
            "_social_liberal:",
            "_market_liberal:",
            "_social_conservative:",
            "_authoritarian_democrat:",
            "_paternal_autocrat:",
            "_national_populist:",
            "_radical_socialist:",
            "_syndicalist:",
            "_totalist:",
        ]:
            if i in text_file:
                for flag in not_encountered_cosmetic_tags:
                    if flag + i in text_file:
                        cosmetic_tags[flag] += 1

    # 4. throw the error if tag is not used
    results = [i for i in cosmetic_tags if cosmetic_tags[i] == 0]
    ResultsReporter.report_results(
        results=results, paths=paths, message="Unused cosmetic tags were encountered - they are not used in cosmetic.txt, country flag .tga, has_cosmetic_tag trigger or localisation."
    )
