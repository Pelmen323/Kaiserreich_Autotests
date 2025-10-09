import glob
import os
import re
from pathlib import Path

from test_classes.generic_test_class import FileOpener


class GFX:
    @classmethod
    def get_code(cls, test_runner, lowercase: bool = True, return_paths: bool = False) -> list[str]:
        """Parse all files return the list with all vars
        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True.
            return_paths (bool, optional): defines if vars code is returned with dict that contains their filenames. Defaults to False.

        Returns:
            if return_paths - tuple[list, dict]: list with vars and dict with filenames
            else - list: list with vars code
        """
        filepath = str(Path(test_runner.full_path_to_mod) / "interface") + "/"
        gfx_entities = []
        paths = {}
        if lowercase:
            pattern = re.compile(r"\tspritetype = \{.*?\}", flags=re.MULTILINE | re.DOTALL)
        else:
            pattern = re.compile(r"\t[s|S]priteType = \{.*?\}", flags=re.MULTILINE | re.DOTALL)

        for filename in glob.iglob(filepath + "**/*.gfx", recursive=True):
            text_file = FileOpener.open_text_file(filename, lowercase=lowercase)
            if "texturefile =" in text_file or "textureFile =" in text_file:
                pattern_matches = re.findall(pattern, text_file)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        gfx_entities.append(match)
                        paths[match] = os.path.basename(filename)

        if return_paths:
            return (gfx_entities, paths)
        else:
            return gfx_entities


class GFXFactory:
    def __init__(self, gfx: str) -> None:
        # Decision properties
        self.name = re.findall(r'name = "(.*?)"', gfx)[0]
        try:
            self.texturefile = re.findall(r'texturefile = "(.*?)"', gfx)[0]
        except IndexError:
            try:
                self.texturefile = re.findall(r'textureFile = "(.*?)"', gfx)[0]
            except IndexError:
                print(self.name)
                raise
