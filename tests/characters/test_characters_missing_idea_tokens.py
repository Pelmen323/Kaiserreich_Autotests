##########################
# Test script to check if activate/deactivate advisors use non-existing tokens
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re
import logging

from test_classes.generic_test_class import (
    DataCleaner,
    FileOpener,
    ResultsReporter,
)

FALSE_POSITIVES = ("empowered_trade_unions_sic", "empowered_executive_sic", "empowered_legislative_sic")


def test_characters_missing_idea_tokens(test_runner: object):
    filepath = test_runner.full_path_to_mod
    idea_tokens = {}
    paths = {}
    # 1. Get all used idea tokens
    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename)

        for i in ["activate_advisor", "deactivate_advisor"]:
            pattern = i + r" = (\S*)"
            if i in text_file:
                pattern_matches = re.findall(pattern, text_file)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        idea_tokens[match] = 0
                        paths[match] = os.path.basename(filename)

    # 2. Find what idea tokens are used
    idea_tokens = DataCleaner.clear_false_positives(input_iter=idea_tokens, false_positives=FALSE_POSITIVES)
    logging.debug(f"{len(idea_tokens)} tokens encountered")
    assert len(idea_tokens) > 0, "idea_tokens must not be empty"

    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename)

        not_encountered_tokens = [i for i in idea_tokens.keys() if idea_tokens[i] == 0]
        if not_encountered_tokens == []:
            break

        if "idea_token" in text_file:
            all_matches = re.findall(r"idea_token = \S*", text_file)
            for token in not_encountered_tokens:
                if f"idea_token = {token}" in all_matches:
                    idea_tokens[token] += 1

    results = [i for i in idea_tokens.keys() if idea_tokens[i] == 0]
    ResultsReporter.report_results(results=results, paths=paths, message="Advisors activation with missing idea tokens were encountered.")
