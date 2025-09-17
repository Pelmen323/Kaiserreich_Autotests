##########################
# Word seeker program. Finds all matches and prints where they were found
# By Pelmen, https://github.com/Pelmen323
##########################
from data.bad_words import bad_words  # Dict with wrong_word : right_word
from test_classes.generic_test_class import ResultsReporter
from test_classes.localization_class import Localization


def test_find_bad_words(test_runner: object):
    loc_keys = Localization.get_all_loc_keys(test_runner=test_runner)
    typo_list = []

    for key, value in loc_keys.items():
        for word in value.split(' '):
            if word in bad_words.keys():
                typo_list.append(f'Loc key {key} -- "{word}" - correct is "{bad_words.get(word)}"')

    ResultsReporter.report_results(results=typo_list, message="Typos were encountered.")
