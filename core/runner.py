class TestRunner:
    """
    Test class that contains full filepath to mod folder
    Initialized via fixture, accepts 2 args, both passed via pytest console:
    -username: pass via --username=my_username, it is system user name in which docs mod is located
    -mod_name: pass via --mod_name=my_modname

    Example: C:\\Users\\username\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\mod_name\\
    """
    def __init__(self, username: str, mod_name: str) -> None:
        self.username = username
        self.mod_name = mod_name
        self.full_path_to_mod = f"C:\\Users\\{username}\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\{mod_name}\\"
