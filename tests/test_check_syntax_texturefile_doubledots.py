##########################
# Test script to check if texturefile has >1 dot
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
from ..test_classes.generic_test_class import FileOpener, DataCleaner
import logging


def test_check_syntax_texturefile_doubledots(test_runner: object):
    filepath = test_runner.full_path_to_mod
    texturefiles = []
# Part 1 - get all idea tokens
    for filename in glob.iglob(filepath + '**/*.gfx', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'texturefile =' in text_file:
            pattern_matches = re.findall('texturefile = ".*\\..*\\..*"', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    texturefiles.append(match)

# Part 2 - throw the error any idea token is used twice
    results = texturefiles
    if results != []:
        logging.warning("Following texturepaths have more than 1 dot:")
        for i in results:
            logging.error(f"- [ ] {i}")
        logging.warning(f'{len(results)} issues found.')
        raise AssertionError("Texturepaths with more than 1 dot found! Check console output")
