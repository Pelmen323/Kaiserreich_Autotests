from .generic_test_class import FileOpener


class Modifiers:

    @classmethod
    def get_all_modifiers(cls, path: str, lowercase: bool = True) -> dict:
        """Parse all files in common/characters and return the list with all characters code

        Args:
            test_runner (_type_): test runner obj
            path (str): Path to file where modifiers are located
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True.

        Returns:
            list: list with characters code
        """
        if path == "Vanilla":
            filepath_to_modifiers = "C:\\SteamLibrary\\steamapps\\common\\Hearts of Iron IV\\localisation\\english\\modifiers_l_english.yml"
        else:
            filepath_to_modifiers = path
        modifiers_dict = {}

        if lowercase:
            text_file = FileOpener.open_text_file(filepath_to_modifiers)
        else:
            text_file = FileOpener.open_text_file(filepath_to_modifiers, lowercase=False)

        text_file_splitted = text_file.split('\n')[1:]
        for line in range(len(text_file_splitted)):
            current_line = text_file_splitted[line-1]
            if ':' in current_line:
                try:
                    value = current_line[:current_line.index(":")].strip()
                    key = current_line[current_line.index('"'):].strip('"')
                    modifiers_dict[key] = value
                except Exception as ex:
                    print(current_line)

        return modifiers_dict
