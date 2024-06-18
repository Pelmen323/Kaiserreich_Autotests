##########################
# Test script to check if doctrines are used in 'add_tech_bonus' expression - with NSB they have separate syntax
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re

from ..data.doctrine_categories import doctrine_categories
from ..test_classes.generic_test_class import FileOpener, ResultsReporter


def test_check_outdated_doctrine_bonus_syntax(test_runner: object):
    filepath = test_runner.full_path_to_mod
    results = []
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        # Get all doctrine reductions form files
        if 'add_doctrine_cost_reduction =' in text_file:
            cost_reduction_strings = re.findall(r'add_doctrine_cost_reduction = \{(.*?\})', text_file, flags=re.DOTALL | re.MULTILINE)
            for i in cost_reduction_strings:
                categories_used = re.findall(r'category = (.*?)\n', i)
                for category_used in categories_used:
                    if category_used not in doctrine_categories:
                        results.append(f"{filename} - encountered cost reduction with invalid category {category_used}")

    ResultsReporter.report_results(results=results, message="Outdated doctrine bonus syntax was found. Check console output")
