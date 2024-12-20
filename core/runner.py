import os


class TestRunner:
    """
    Test class that contains the full filepath to the mod folder.
    Automatically ensures filepaths are properly formatted for cross-platform compatibility.
    """
    def __init__(self, username: str = None, mod_name: str = None, repo_path: str = None) -> None:
        # If a direct repo path is provided (for CI), use it
        if repo_path:
            self.full_path_to_mod = os.path.abspath(repo_path)
        else:
            # Otherwise, construct the path from username and mod_name
            if os.name == "nt":
                self.full_path_to_mod = f"C:\\Users\\{username}\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\{mod_name}\\"
            elif os.name == "posix":
                self.full_path_to_mod = f"/Users/{username}/Documents/Paradox Interactive/Hearts of Iron IV/mod/{mod_name}/"

        # Normalize the path for cross-platform consistency
        self.full_path_to_mod = self.ensure_trailing_slash(os.path.normpath(self.full_path_to_mod))

    @staticmethod
    def ensure_trailing_slash(filepath: str) -> str:
        """
        Ensure the filepath ends with a slash (either '/' or '\\') for compatibility with glob and other operations.
        """
        if not filepath.endswith(('/', '\\')):
            filepath += os.sep  # Add the appropriate separator for the current OS
        return filepath
