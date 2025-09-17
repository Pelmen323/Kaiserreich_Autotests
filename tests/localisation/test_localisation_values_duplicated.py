##########################
# Find duplicated loc keys
# By Pelmen, https://github.com/Pelmen323
##########################
from test_classes.generic_test_class import ResultsReporter
from test_classes.localization_class import Localization
import pytest

FALSE_POSITIVES_STATE = ["Georgia", "Maine", "Morava", "Santa Cruz"]
FALSE_POSITIVES_VP = ["Birmingham", "Charleston", "Concepcion", "Dover", "Frankfurt", 'Ganzhou',
                      'Georgetown', 'Kochi', 'La Paz', 'León', 'Mafikeng', 'Malaga', 'Mérida', 'Newcastle',
                      'Petropavlovsk', 'Port Arthur', 'San Juan', 'Santarém', 'Concepción', 'Mogilev']

list_of_filepaths = [
    ["localisation\\english\\KR_common\\00 Map States l_english.yml", FALSE_POSITIVES_STATE],
    ["localisation\\english\\KR_common\\00 Map Victory Points l_english.yml", FALSE_POSITIVES_VP]
]


@pytest.mark.parametrize("filepath", list_of_filepaths)
def test_find_duplicated_keys(test_runner: object, filepath):
    loc_dict = Localization.get_all_loc_keys(test_runner=test_runner, lowercase=False, return_keys_from_specific_file=f'{test_runner.full_path_to_mod}{filepath[0]}')
    false_positives_iter = filepath[1]

    duplicated_values = {i: loc_dict[i][1:-1] for i in loc_dict if list(loc_dict.values()).count(loc_dict[i]) > 1}
    duplicated_values = sorted(duplicated_values.items(), key=lambda x: x[1])

    if false_positives_iter is not None:
        duplicated_values = [i for i in duplicated_values if i[1] not in false_positives_iter]

    ResultsReporter.report_results(results=duplicated_values, message="Duplicated loc values were encountered.")
