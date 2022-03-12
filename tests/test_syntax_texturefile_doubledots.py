##########################
# Test script to check if texturefile has >1 dot
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
from ..test_classes.generic_test_class import FileOpener, DataCleaner, ResultsReporter


def test_check_syntax_texturefile_doubledots(test_runner: object):
    filepath = test_runner.full_path_to_mod
    results = []
# Part 1 - get all idea tokens
    for filename in glob.iglob(filepath + '**/*.gfx', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'texturefile =' in text_file:
            pattern_matches = re.findall('texturefile = ".*\\..*\\..*"', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    results.append(match)

# Part 2 - throw the error any idea token is used twice
    ResultsReporter.report_results(results=results, message="Texturepaths with more than 1 dot were encountered. Check console output")
