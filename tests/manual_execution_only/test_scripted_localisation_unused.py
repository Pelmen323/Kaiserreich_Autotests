##########################
# Test script to check if scripted loc is unused
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import pytest

from test_classes.generic_test_class import FileOpener, ResultsReporter
from test_classes.scripted_loc_class import ScriptedLocalisation


@pytest.mark.skip("Costly and low-prio test")
def test_scripted_localisation_unused(test_runner: object):
    scripted_loc = set(ScriptedLocalisation.get_all_scripted_loc_names(test_runner=test_runner))
    filepath = test_runner.full_path_to_mod

    for _ in ['txt', 'gui', 'yml']:
        for filename in glob.iglob(filepath + '**/*.' + _, recursive=True):
            if not scripted_loc:
                break

            text_file = FileOpener.open_text_file(filename)
            for i in tuple(scripted_loc):
                if i in text_file:
                    scripted_loc.remove(i)

    results = sorted(scripted_loc)
    ResultsReporter.report_results(results=results, message="Unused scripted loc was found.")
