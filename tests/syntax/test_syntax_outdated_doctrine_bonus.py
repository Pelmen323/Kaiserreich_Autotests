##########################
# Test script to check if doctrines are used in 'add_tech_bonus' expression - with NSB they have separate syntax
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re

from ...data.doctrine_categories import combined_doctrines_list
from ...test_classes.generic_test_class import FileOpener, ResultsReporter


def test_check_outdated_doctrine_bonus_syntax(test_runner: object):
    filepath = test_runner.full_path_to_mod
    all_tech_bonuses = []
    results = []
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

# Get all tech bonuses from mod files
        if 'add_tech_bonus =' in text_file:
            tech_bonuses_in_file = re.findall('add_tech_bonus = \\{(.*?\\})', text_file, flags=re.DOTALL | re.MULTILINE)
            if len(tech_bonuses_in_file) > 0:
                for expression in tech_bonuses_in_file:
                    all_tech_bonuses.append(expression)

# Verify if doctrines/doctrine categories are used in the tech files
    trimmed_expression = expression.replace('\t', '').replace('\n', '  ')
    for expression in all_tech_bonuses:
        for tech_name in combined_doctrines_list:
            if f'category = {tech_name}' in expression:
                results.append(f"{tech_name} doctrine/doctrine category is used in the following expression: \n{trimmed_expression}")
            if f'technology = {tech_name}' in expression:
                results.append(f"{tech_name} doctrine/doctrine category is used in the following expression: \n{trimmed_expression}")

    ResultsReporter.report_results(results=results, message="Outdated doctrine bonus syntax was found. Check console output")
