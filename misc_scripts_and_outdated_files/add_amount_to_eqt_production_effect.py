import re
import os
import glob
from pathlib import Path
from test_classes.generic_test_class import FileOpener

INPUT_FILE_PATH = 'C:\\Users\\' + os.getlogin() + '\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\Kaiserreich Dev Build\\'


def main():

    filepath = str(Path(INPUT_FILE_PATH)) + "/"

    for i in ['\t', '\t\t', '\t\t\t', '\t\t\t\t', '\t\t\t\t\t']:
        for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
            text_file = FileOpener.open_text_file(filename, lowercase=False)
            input_file_repl = text_file
            override = False
            pattern = r'^' + i + r'tadd_equipment_production = \{.*?^' + i + r'\}'
            matches = re.findall(pattern=pattern, string=text_file, flags=re.DOTALL | re.MULTILINE)

            if len(matches) > 0:
                for match in matches:
                    if 'amount' not in match and "ship" in match:
                        override = True
                        input_file_repl = input_file_repl.replace(match, match[:-3] + '\n\t' + i + 'amount = 1\n' + i + '}')

            if override:
                with open(filename, 'w', encoding='utf-8') as text_file_write:
                    text_file_write.write(input_file_repl)


if __name__ == '__main__':
    main()
