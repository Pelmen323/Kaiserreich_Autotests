##########################
# Find duplicated loc keys
# By Pelmen, https://github.com/Pelmen323
##########################
from pathlib import Path
import glob
import re
import pytest


from test_classes.generic_test_class import ResultsReporter
from test_classes.localization_class import Localization
from test_classes.generic_test_class import FileOpener


@pytest.mark.skip("Resource-heavy test - only manual execution")
def test_find_unused_keys(test_runner: object):
    exceptions = [
        "guide",                        # Country intro
        "country_intro_",
        "social_democrat",              # Political parties
        "market_liberal",
        "social_liberal",
        "social_conservative",
        "authoritarian_democrat",
        "paternal_autocrat",
        "national_populist",
        "radical_socialist",
        "syndicalist",
        "totalist",
        "_ADJ",                         # Tag loc
        "_DEF",
        "_NOT",
        "OTT_Population_",              # OTT GUI bs
        "ottoman_province",
        "mitteleuropa_",                # MIE
        "_card",                        # GER cardgame
        "PARTY",
        "_GUI",
        "_MIO",
        "_sp_",                         # special projects loc
        "_blocked",                     # various custom cost TTs
        "_tooltip",
        "_spirit",                      # army spirirts
        "_governorate",                 # Puppet loc
    ]

    filepath_techs = str(Path(test_runner.full_path_to_mod) / "common" / "technologies") + "/"
    techs = []
    for filename in glob.iglob(filepath_techs + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename, lowercase=False)
        pattern_matches = re.findall(r"^\t([^\t\@]+?) =", text_file, flags=re.DOTALL | re.MULTILINE)
        if len(pattern_matches) > 0:
            for match in pattern_matches:
                techs.append(match)

    filepath = str(Path(test_runner.full_path_to_mod) / "localisation" / "english" / "KR_country_specific") + "/"
    filepath_common = str(Path(test_runner.full_path_to_mod) / "common") + "/"
    filepath_events = str(Path(test_runner.full_path_to_mod) / "events") + "/"
    filepath_gui = str(Path(test_runner.full_path_to_mod) / "interface" / "kaiserreich") + "/"
    input_map = {filepath_common: '.txt', filepath_events: '.txt', filepath_gui: '.gui'}
    results = []
    for filename in glob.iglob(filepath + "**/*.yml", recursive=True):
        print(filename)
        loc_keys = Localization.get_all_loc_keys(test_runner=test_runner, lowercase=False, return_keys_from_specific_file=filename)
        loc_keys_dict = {i: 0 for i in loc_keys if not any([x for x in exceptions if x in i])}
        loc_file = FileOpener.open_text_file(filename, lowercase=False)
        # Remove keys that are used in loc itself
        for k in loc_keys_dict:
            if f'${k}$' in loc_file:
                loc_keys_dict[k] += 1

        # Remove keys that are used in techs
        for k in loc_keys_dict:
            for t in techs:
                if t in k:
                    loc_keys_dict[k] += 1
                    continue

        for filepath2 in input_map:
            extension = input_map[filepath2]
            for filename2 in glob.iglob(filepath2 + "**/*" + extension, recursive=True):
                text_file = FileOpener.open_text_file(filename2, lowercase=False)
                trimmed_dict = {kk for kk in loc_keys_dict if loc_keys_dict[kk] == 0}
                for k in trimmed_dict:
                    if k in text_file:
                        loc_keys_dict[k] += 1
                    elif "national_focus" in filename2:
                        if "_desc" in k and k[:-5] in text_file:
                            loc_keys_dict[k] += 1
                    elif "ideas" in filename2:
                        if "_desc" in k and k[:-5] in text_file:
                            loc_keys_dict[k] += 1
                    elif "characters" in filename2:
                        if "_desc" in k and k[:-5] in text_file:
                            loc_keys_dict[k] += 1
                    elif "decision" in filename2:
                        if "_desc" in k and k[:-5] in text_file:
                            loc_keys_dict[k] += 1

        for key in loc_keys_dict:
            if loc_keys_dict[key] == 0:
                results.append(key)

    ResultsReporter.report_results(results=results, message="Duplicated loc keys were encountered.")
