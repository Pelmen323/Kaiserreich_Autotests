##########################
# Test script to check if there are opinion modifiers that are not used via "modifier = xx"
# By Pelmen, https://github.com/Pelmen323
##########################
from ..test_classes.generic_test_class import ResultsReporter
from ..test_classes.ideas_class import Ideas
FILES_TO_SKIP = ["00 Generic ideas.txt", '01 Army Spirits.txt', '01 Air Spirits.txt', '01 Navy Spirits.txt']
FALSE_POSITIVES = ('hai_foreign_control_dummy', 'empowered_trade_unions_sic', 'empowered_executive_sic', 'empowered_legislative_sic')


def test_check_ideas_missing(test_runner: object):
    # 1. Get list of all ideas
    defined_ideas = Ideas.get_all_ideas_names(test_runner=test_runner, lowercase=True, return_paths=False, include_country_ideas=True, include_manufacturers=True, include_characters_tokens=True, include_laws=True, include_army_spirits=True)

    # 2. Get dict of ideas usages:
    used_ideas, paths = Ideas.get_all_used_ideas(test_runner=test_runner, lowercase=True, return_paths=True)

    # 3. Report the results:
    results = [i for i in used_ideas if i not in defined_ideas and "var:" not in i and i not in FALSE_POSITIVES]
    ResultsReporter.report_results(results=results, paths=paths, message="Missing ideas were encountered. Check console output")
