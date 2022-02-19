##########################
# Test script to check if doctrines are used in 'add_tech_bonus' expression - with NSB they have separate syntax
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
import os
from ..data.doctrine_categories import combined_doctrines_list
from ..test_classes.generic_test_class import TestClass
import logging


def test_check_outdated_doctrine_bonus_syntax(test_runner: object):
    test = TestClass()
    filepath = test_runner.full_path_to_mod
    all_tech_bonuses = []
    results = []
    paths = {}
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = test.open_text_file(filename)

# Get all tech bonuses from mod files
        if 'add_tech_bonus =' in text_file:
            tech_bonuses_in_file = re.findall('add_tech_bonus = \\{[ \\w\r\n\t=.]*\\}', text_file)
            if len(tech_bonuses_in_file) > 0:
                for expression in tech_bonuses_in_file:
                    all_tech_bonuses.append(expression)
                    paths[expression] = os.path.basename(filename)

# Verify if doctrines/doctrine categories are used in the tech files
    for expression in all_tech_bonuses:
        for tech_name in combined_doctrines_list:
            if f'category = {tech_name}' in expression:
                results.append(f'{tech_name} doctrine/doctrine category is used in the following expression: \n{expression}')
            if f'technology = {tech_name}' in expression:
                results.append(f'{tech_name} doctrine/doctrine category is used in the following expression: \n{expression}')

    if results != []:
        for i in results:
            logging.error(f"- [ ] {i}, - '{paths[i]}'")
        logging.warning(f'{len(results)} times wrong doctrine syntax is used!')
        raise AssertionError("'Outdated doctrine bonus syntax encountered! Check console output")
