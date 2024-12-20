import os


class TestRunner:
    """
    Test class that contains the full filepath to the mod folder.
    - Locally: Constructed using `--username` and `--mod_name`.
    - In CI: Use a direct `repo_path` argument.
    """
    def __init__(self, username: str = None, mod_name: str = None, repo_path: str = None) -> None:
        # If repo_path is provided, use it (for CI)
        if repo_path:
            self.full_path_to_mod = os.path.abspath(repo_path)
        else:
            # Fallback to local paths if no repo_path is provided
            self.username = username
            self.mod_name = mod_name

            if os.name == "nt":
                self.full_path_to_mod = f"C:\\Users\\{username}\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\{mod_name}\\"
            elif os.name == "posix":
                self.full_path_to_mod = f"/Users/{username}/Documents/Paradox Interactive/Hearts of Iron IV/mod/{mod_name}/"

        # Normalize the path for cross-platform consistency
        self.full_path_to_mod = os.path.normpath(self.full_path_to_mod)

        # Ensure the path exists
        if not os.path.exists(self.full_path_to_mod):
            raise FileNotFoundError(f"The specified mod path does not exist: {self.full_path_to_mod}")
