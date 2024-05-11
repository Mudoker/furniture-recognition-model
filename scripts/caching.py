import os
import json

class Caching:

    def __init__(self, path):
        self.CACHE_FOLDER = "../../cache"
        self.CACHE_SUB_FOLDER = os.path.join(self.CACHE_FOLDER, path)
        self.check_cache_folder_exists()

    def check_cache_folder_exists(self) -> None:
        """
        Ensure that the cache sub-folder exists.
        """
        os.makedirs(self.CACHE_SUB_FOLDER, exist_ok=True)

    def create_directory(self, path: str) -> str:
        """
        Create a directory within the cache sub-folder.
        """
        full_path = os.path.join(self.CACHE_SUB_FOLDER, path)
        os.makedirs(full_path, exist_ok=True)
        return full_path

    def create_file(self, filename: str, content: str = None) -> str:
        """
        Create a file within the cache sub-folder.
        """
        file_path = os.path.join(self.CACHE_SUB_FOLDER, filename)
        with open(file_path, 'w') as file:
            if content:
                file.write(content)
        return file_path

    def directory_exists(self, dir_path: str) -> bool:
        """
        Check if the directory exists within the cache sub-folder.
        """
        full_path = os.path.join(self.CACHE_SUB_FOLDER, dir_path)
        return os.path.exists(full_path)

    def file_exists(self, filename: str) -> bool:
        """
        Check if the file exists within the cache sub-folder.
        """
        file_path = os.path.join(self.CACHE_SUB_FOLDER, filename)
        return os.path.exists(file_path)
