import glob
import re

from ..test_classes.generic_test_class import FileOpener


class States:

    @classmethod
    def get_states_vps_dict(cls, test_runner, lowercase: bool = True) -> dict:
        """Parse all states files and return state - vp's dict

        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True.

        Returns:
            dict: state ids as keys and lists with VPs for those states as values
        """
        filepath_to_states = f'{test_runner.full_path_to_mod}history\\states'
        states_vp_dict = {}

        for filename in glob.iglob(filepath_to_states + '**/*.txt', recursive=True):
            text_file = FileOpener.open_text_file(filename, lowercase=lowercase)

            state_id = re.findall('	id = (\\d*)', text_file)[0]
            vp = re.findall('victory_points = \\{ (.*) \\}', text_file)
            vp_array = re.findall('state_victory_points = (\\d+)', text_file)
            victory_points_for_state = []

            if vp != []:
                for point in vp:
                    victory_points_for_state.append(point.split()[0])

            if vp_array != []:
                for point in vp_array:
                    victory_points_for_state.append(point)

            states_vp_dict[state_id] = victory_points_for_state

        return states_vp_dict

    @classmethod
    def get_states_provinces_dict(cls, test_runner, lowercase: bool = True) -> dict:
        """Parse all states files and return state - provinces dict

        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True.

        Returns:
            dict: state ids as keys and lists with provinces for those states as values
        """
        filepath_to_states = f'{test_runner.full_path_to_mod}history\\states'
        states_provinces_dict = {}

        for filename in glob.iglob(filepath_to_states + '**/*.txt', recursive=True):
            text_file = FileOpener.open_text_file(filename, lowercase=lowercase)

            state_id = re.findall('	id = (\\d*)', text_file)[0]
            provinces = re.findall('provinces = \\{\\n\\t*(.*?)\\n\\t\\}', text_file, flags=re.MULTILINE)[0].split()
            states_provinces_dict[state_id] = provinces

        return states_provinces_dict
