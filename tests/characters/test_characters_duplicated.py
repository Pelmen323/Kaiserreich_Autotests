##########################
# Test script to check for duplicated characters
# By Pelmen, https://github.com/Pelmen323
##########################
import re
import pytest

from test_classes.characters_class import Characters
from test_classes.generic_test_class import ResultsReporter

FALSE_POSITIVES = (
    "abdallah_ibn_mitab_ibn_abd_al_aziz_al_rashid",     # Intentional
    "abdallah_ibn_talal_al_rashid",                     # Intentional
    "muhammad_ibn_talil_al_rashid",                     # Intentional
    "saud_al_subhan",                                   # Intentional
    "saud_bin_abd_al_aziz",                             # Intentional
    "hugh_gaitskell",                                   # Intentional
    "chen_yi",                                          # Different people
    "dai_jitao",                                        # Different people
    "john_anderson",                                    # Different people
    "ma_liang",                                         # Different people
    "army_reform_group",                                # Generic
    "army_council",                                     # Generic
    "assorted_leaders",                                 # Generic
    "reform_council",                                   # Generic
    "theory_of_action",                                 # Generic
    "united_states_congress",                           # Generic
    "henri_tanguy",                                     # Intentional
)


@pytest.mark.smoke
@pytest.mark.kr_specific
def test_characters_duplicated(test_runner: object):
    characters, paths = Characters.get_all_characters(test_runner=test_runner, return_paths=True)
    character_names = []
    character_names_full_data = []

    for char in characters:
        char_name = re.findall(r"^\t(.+) =", char)[0]
        char_name_short = char_name[4:]
        character_names.append(char_name_short)
        character_names_full_data.append((char_name_short, char_name, paths[char]))

    results = sorted([character_names_full_data[i] for i, value in enumerate(character_names) if character_names.count(value) > 1 and value not in FALSE_POSITIVES])

    ResultsReporter.report_results(results=results, message="Duplicated characters were encountered")
