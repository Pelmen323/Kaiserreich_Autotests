##########################
# The script analyzes the railways.txt file, if the line includes more or less provinces than specified - it throws error
# The error is very important as the game draws level 4 railways in half of the world if you provide less provinces than should
# By Pelmen, https://github.com/Pelmen323
##########################
from ..test_classes.generic_test_class import FileOpener, DataCleaner, ResultsReporter


def test_check_railways_file(test_runner: object) -> bool:
    filepath = f'{test_runner.full_path_to_mod}map\\railways.txt'
    results = []
    lines = FileOpener.open_text_file(filepath).split('\n')
    line_counter = 0

    for line in lines:
        line_counter += 1
        if line == '':
            continue
        elif line[3] != ' ':
            counter_of_provinces_in_line = line[2:4]
        else:
            counter_of_provinces_in_line = line[2]
        str_with_provinces = line[4:].strip()
        list_with_provinces = str_with_provinces.split()
        if int(counter_of_provinces_in_line) != len(list_with_provinces):
            results.append(f"Line {line_counter} - expected {counter_of_provinces_in_line} provinces, got {list_with_provinces}. Line: {line}")

    ResultsReporter.report_results(results=results, message="Issues in railway file were encountered. Check console output")
