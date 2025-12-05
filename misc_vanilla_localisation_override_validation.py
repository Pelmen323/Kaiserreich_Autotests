##########################
# Find duplicated loc keys
# By Pelmen, https://github.com/Pelmen323
##########################
from test_classes.generic_test_class import ResultsReporter
from test_classes.localization_class import Localization
from fuzzywuzzy import fuzz


def test_localisation_override_check(test_runner: object):
    vanilla_keys = Localization.get_all_loc_keys(test_runner=test_runner, lowercase=False, fetch_from_vanilla=True)
    kr_override_keys = Localization.get_all_loc_keys(test_runner=test_runner, lowercase=False, include_only="replace")
    results = []

    for i in kr_override_keys:
        if i not in vanilla_keys:
            results.append(f'{i} key is not found in vanilla')

        else:
            vanilla_value = vanilla_keys[i]
            kr_value = kr_override_keys[i]
            if vanilla_value == kr_value:
                results.append(f'{i} key has the same value in vanilla')
            else:
                if fuzz.ratio(vanilla_value, kr_value) < 80:
                    results.append(f'KR and vanilla key {i} have < 80% match ratio')

    ResultsReporter.report_results(results=results, message="Bla.")
