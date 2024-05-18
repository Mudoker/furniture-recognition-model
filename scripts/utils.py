import os
import importlib
import inspect

BULLET_POINT = ">>>"


class Utils:
    VALID_ENVIRONMENTS = ["dev", "gcolab", "kaggle"]

    def __init__(self):
        self._env = "dev"  # Use a private attribute

    @property
    def env(self):
        """Get the current environment."""
        return self._env

    @env.setter
    def env(self, new_env):
        """Set the environment, validating the input."""
        if new_env not in self.VALID_ENVIRONMENTS:
            raise ValueError(
                f"Invalid environment: {new_env}. Choose from: {', '.join(self.VALID_ENVIRONMENTS)}"
            )
        self._env = new_env
        print(f"{BULLET_POINT} Environment set to {new_env}")

    @env.getter
    def env(self):
        """Get the current environment."""
        return self._env

    @staticmethod  # Make get_file_path a static method
    def get_file_path():
        """Get the absolute path of the current file."""
        return os.path.abspath(__file__)

    @staticmethod  # Make get_file_dir a static method
    def get_file_dir():
        """Get the directory of the current file."""
        return os.path.dirname(Utils.get_file_path())  # Call static method directly

    @staticmethod
    def import_modules(module_list):
        """Import modules with optional aliases into the caller's namespace."""
        frame = inspect.currentframe().f_back  # Get the caller's frame
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
