##########################
# Find duplicated loc keys
# By Pelmen, https://github.com/Pelmen323
##########################
from ..test_classes.generic_test_class import ResultsReporter
from ..test_classes.localization_class import Localization
import pytest

list_of_filepaths = [
    "localisation\\KR_common\\00_Map_States_l_english.yml",
    "localisation\\KR_common\\00_Map_Victory_Points_l_english.yml",
]

@pytest.mark.parametrize("filepath", list_of_filepaths)
def test_find_duplicated_keys(test_runner: object, filepath):
    loc_dict = Localization.get_all_loc_keys(test_runner=test_runner, lowercase=False, return_keys_from_specific_file=f'{test_runner.full_path_to_mod}{filepath}')
 
    duplicated_values = {i: loc_dict[i] for i in loc_dict if list(loc_dict.values()).count(loc_dict[i]) > 1}
    duplicated_values = sorted(duplicated_values.items(), key=lambda x: x[1])

    ResultsReporter.report_results(results=duplicated_values, message="Duplicated loc values were encountered. Check console output")
