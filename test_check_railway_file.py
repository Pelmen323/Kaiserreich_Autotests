### By Pelmen323, https://github.com/Pelmen323
import pytest

def open_railways_file(filepath: str) -> str:
    try:
        with open(filepath, 'r') as raw_text_file:
            return raw_text_file.read()
    except Exception as ex:
        print("Unable to open railways file", ex)

@pytest.mark.parametrize("path_to_railway_file", 
    [("C:\\Users\\VADIM\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\Kaiserreich Dev Build\\map\\railways.txt")])
def test_check_railways_file(path_to_railway_file: str) -> bool:
    print("The railway file test is started! Opening the file...")
    lines = open_railways_file(path_to_railway_file).split('\n')
    line_counter = 0
    errors_list = []
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
            errors_list.append(f"Line {line_counter} - expected {counter_of_provinces_in_line} provinces, got {list_with_provinces}. Line: {line}")
    if errors_list != []:
        raise AssertionError(errors_list)
    print("The test is finished!")


if __name__ == '__main__':
    open_railways_file()
    input('Press any key to exit')
