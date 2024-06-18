##########################
# Test script to check for unused cosmetic tags
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import logging
import os
import re

from ...test_classes.generic_test_class import FileOpener, ResultsReporter


def test_check_cosmetic_tags_unused(test_runner: object):
    filepath = test_runner.full_path_to_mod
    cosmetic_tags = {}
    paths = {}
# Part 1 - get the dict of all cosmetic tags
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'set_cosmetic_tag =' in text_file:
            pattern_matches = re.findall('set_cosmetic_tag = \\b\\w*\\b', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[19:].strip().strip('}').strip()
                    cosmetic_tags[match] = 0
                    paths[match] = os.path.basename(filename)

# Part 2 - count the number of tag occurrences
    logging.debug(f'{len(cosmetic_tags)} set cosmetic tags were found')
    # Usage directly
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)
        not_encountered_cosmetic_tags = [i for i in cosmetic_tags.keys() if cosmetic_tags[i] == 0]

        if 'has_cosmetic_tag =' in text_file:
            for flag in not_encountered_cosmetic_tags:
                cosmetic_tags[flag] += text_file.count(f'has_cosmetic_tag = {flag}')

    # Usage in loc
    for filename in glob.iglob(filepath + '**/*.yml', recursive=True):
        text_file = FileOpener.open_text_file(filename)
        not_encountered_cosmetic_tags = [i for i in cosmetic_tags.keys() if cosmetic_tags[i] == 0]

        for flag in not_encountered_cosmetic_tags:
            if f'{flag}:' in text_file:
                cosmetic_tags[flag] += 1
            if f'{flag}_social_democrat:' in text_file:
                cosmetic_tags[flag] += 1
            if f'{flag}_social_liberal:' in text_file:
                cosmetic_tags[flag] += 1
            if f'{flag}_market_liberal:' in text_file:
                cosmetic_tags[flag] += 1
            if f'{flag}_social_conservative:' in text_file:
                cosmetic_tags[flag] += 1
            if f'{flag}_authoritarian_democrat:' in text_file:
                cosmetic_tags[flag] += 1
            if f'{flag}_paternal_autocrat:' in text_file:
                cosmetic_tags[flag] += 1
            if f'{flag}_national_populist:' in text_file:
                cosmetic_tags[flag] += 1
            if f'{flag}_radical_socialist:' in text_file:
                cosmetic_tags[flag] += 1
            if f'{flag}_syndicalist:' in text_file:
                cosmetic_tags[flag] += 1
            if f'{flag}_totalist:' in text_file:
                cosmetic_tags[flag] += 1

    # Usage in country colors
    filepath_cosmetic = f'{test_runner.full_path_to_mod}common\\countries\\cosmetic.txt'
    text_file = FileOpener.open_text_file(filepath_cosmetic)

    for flag in not_encountered_cosmetic_tags:
        not_encountered_cosmetic_tags = [i for i in cosmetic_tags.keys() if cosmetic_tags[i] == 0]
        if f'{flag} =' in text_file:
            cosmetic_tags[flag] += 1

    # Usage in flags
    country_flags = []
    path_to_flags = f'{test_runner.full_path_to_mod}gfx\\flags\\'

    for filename in glob.iglob(path_to_flags + '**/*.tga', recursive=True):
        country_flags.append(os.path.basename(filename.lower())[:-4])

    for flag in country_flags:
        not_encountered_cosmetic_tags = [i for i in cosmetic_tags.keys() if cosmetic_tags[i] == 0]
        for remaining_flag in not_encountered_cosmetic_tags:
            if flag in remaining_flag:
                cosmetic_tags[remaining_flag] += 1


# Part 4 - throw the error if tag is not used
    results = [i for i in cosmetic_tags if cosmetic_tags[i] == 0]
    ResultsReporter.report_results(results=results, paths=paths, message="Unused cosmetic tags were encountered. Check console output")
