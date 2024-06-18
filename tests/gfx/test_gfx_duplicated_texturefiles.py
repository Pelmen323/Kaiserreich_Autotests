##########################
# Test script to check if there are gfx that are defined more than once
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re

from ...test_classes.generic_test_class import (
    FileOpener,
    ResultsReporter,
)


def test_check_duplicated_gfx(test_runner: object):
    gfx_path = f'{test_runner.full_path_to_mod}interface\\'
    gfx_entities = []
    results = []

    # Get list of all image entities
    for filename in glob.iglob(gfx_path + '**/*.gfx', recursive=True):
        # if len([i for i in ["technology", "Technologies"] if i in filename]) > 0:
        #     continue
        if "portrait" not in filename:
            continue
        if "random" in filename:
            continue
        # if "companies" not in filename:
        #     continue
        text_file = FileOpener.open_text_file(filename, lowercase=True)
        if 'spritetype' in text_file:

            matches = re.findall(r'\tspritetype = \{.*?\}', text_file, flags=re.DOTALL | re.MULTILINE)
            if len(matches) > 0:
                for match in matches:
                    name = re.findall(r'name = (.*)', match)[0]
                    texturefile = re.findall(r'texturefile = (.*)', match)[0]
                    gfx_entities.append([name, texturefile])

    gfx_entities = [i for i in gfx_entities if "_shine" not in i[0]]
    # Duplication check
    gfx_texturefiles = [i[1] for i in gfx_entities]
    set_gfx_texturefiles = set(gfx_texturefiles)

    for i in set_gfx_texturefiles:
        if gfx_texturefiles.count(i) > 1:
            output_str = str([x[0] for x in gfx_entities if x[1] == i]).replace('"', '')
            results.append(f"{output_str} refer to the same texturefile {i}")

    results = sorted(results)
    ResultsReporter.report_results(results=results, message="Images with duplicated definitions/texturefiles are found. Check console output")
