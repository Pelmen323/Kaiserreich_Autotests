##########################
# Test script to check for duplicated characters
# By Pelmen, https://github.com/Pelmen323
##########################
import re
import pytest

from test_classes.characters_class import Characters
from test_classes.generic_test_class import ResultsReporter

FALSE_POSITIVES = (
    'abdallah_ibn_mitab_ibn_abd_al_aziz_al_rashid',
    'abdallah_ibn_talal_al_rashid',
    'saud_al_subhan',
    'muhammad_ibn_talil_al_rashid',
    'clement_attlee',
    'hugh_gaitskell',
    'luigi_gasparotto',
    'reform_council',
    'united_states_congress',
    'john_anderson',
    'army_reform_group',
    'army_council',
    'ma_liang',
    'saud_bin_abd_al_aziz',
    'assorted_leaders',
    'theory_of_action',
)


@pytest.mark.smoke
@pytest.mark.kr_specific
def test_check_duplicated_characters(test_runner: object):
    characters, paths = Characters.get_all_characters(test_runner=test_runner, return_paths=True)
    character_names = []
    character_names_full_data = []

    for char in characters:
        char_name = re.findall(r'^\t(.+) =', char)[0]
        char_name_short = char_name[4:]
        character_names.append(char_name_short)
        character_names_full_data.append((char_name_short, char_name, paths[char]))

    results = sorted([character_names_full_data[i] for i, value in enumerate(character_names) if character_names.count(value) > 1 and value not in FALSE_POSITIVES])

    ResultsReporter.report_results(results=results, message="Duplicated characters were encountered. Having the same character defined in multiple places is odd at least. If thins is expected, notify @Pelmen to update test exceptions")
