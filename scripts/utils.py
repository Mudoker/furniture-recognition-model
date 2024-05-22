import os
import importlib
import inspect

# Styling constants
BULLET_POINT = ">>>"


class Utils:
    @staticmethod  # Make get_file_path a static method
    def get_file_path():
        """Get the absolute path of the current file."""
        return os.path.abspath(__file__)

    @staticmethod  # Make get_file_dir a static method
    def get_file_dir():
        """Get the directory of the current file."""
        return os.path.dirname(Utils.get_file_path())  # Call static method directly

    @staticmethod
    def import_modules(module_list=[]):
        """Import modules with optional aliases into the caller's namespace."""

        core_modules = [
            ("os", None),
            ("sys", None),
            ("importlib", None),
            ("inspect", None),
            ("pandas", "pd"),
            ("numpy", "np"),
            ("matplotlib.pyplot", "plt"),
            ("seaborn", "sns"),
            ("tabulate", None),
            ("scripts.leon", "leon"),
            ("scripts.constants", "const"),
            ("scripts.styler", "styler"),
            ("tensorflow", "tf"),
        ]

        frame = inspect.currentframe().f_back  # Get the caller's frame

        module_list += core_modules  # Add core modules to the list

        for name, alias in module_list:
            try:
                module = importlib.import_module(name)
                if alias:  # Import with alias
                    frame.f_globals[alias] = importlib.__import__(
                        name, fromlist=[alias]
                    )
                    print(f"{BULLET_POINT} {name} imported as {alias}")
                else:
                    frame.f_globals[name] = module  # Import without alias
                    print(f"{BULLET_POINT} {name} imported")
            except ImportError as e:
                print(f"{BULLET_POINT} Error importing {name}: {e}")
