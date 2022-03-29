##########################
# Test script to check for duplicated characters
# By Pelmen, https://github.com/Pelmen323
##########################
import re
from ..test_classes.generic_test_class import ResultsReporter
from ..test_classes.characters_class import Characters
FALSE_POSITIVES = (
    'abdallah_ibn_mitab_ibn_abd_al_aziz_al_rashid',
    'abdallah_ibn_talal_al_rashid',
    'clement_attlee',
    'hugh_gaitskell',
    'george_v',
    'saud_al_subhan',
    'muhammad_ibn_talil_al_rashid',
    'parliament',
    'augusto_barcia_trelles',
    'dolores_ibarruri_gomez',
    'juan_iii',
    'national_congress',
)


def test_check_duplicated_characters(test_runner: object):
    characters, paths = Characters.get_all_characters(test_runner=test_runner, return_paths=True)
    character_names = []
    character_names_full_data = []

    for char in characters:
        char_name = re.findall('^\\t(.+) =', char)[0]
        char_name_short = char_name[4:]
        character_names.append(char_name_short)
        character_names_full_data.append((char_name_short, char_name, paths[char]))

    results = sorted([character_names_full_data[i] for i, value in enumerate(character_names) if character_names.count(value) > 1 and value not in FALSE_POSITIVES])

    ResultsReporter.report_results(results=results, message="Duplicated characters were encountered. Check console output")
