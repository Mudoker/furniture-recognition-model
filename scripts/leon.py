import os
import zipfile
import shutil
from PIL import Image
import matplotlib.pyplot as plt

version = "1.0.3"
icon = f"""
        @|\\@@
       -  @@@@                                                            LEON 1.0.0
      /7   @@@@                                         This is Leon, the friendly lion. He is here to help you
     /    @@@@@@                                     Leon is tailored to manipulate images, data and visualizations
     \\-' @@@@@@@@`-_______________                                      Made by: Team X
      -@@@@@@@@@             /    \\                                     Version: {version}
 _______/    /_       ______/      |__________-
/,__________/  `-.___/,_____________----------_)
"""


class Leon:
    def __init__(self):
        print(icon)

    def read_zip(self, path):
        """
        Extracts a ZIP file, reads the image files contained within it, and deletes the ZIP file afterwards.

        Parameters:
            path (str): The path to the ZIP file.

        Returns:
            list of PIL.Image.Image: List of Image objects containing the images from the ZIP file.
        """
        # Get the directory where the ZIP file will be extracted
        extract_dir = os.path.splitext(path)[0]

        # Check if the file extension is not .zip
        if os.path.splitext(path)[1] != ".zip":
            # Check if the extract directory already exists and is not the same as the ZIP file directory
            if os.path.exists(extract_dir) and extract_dir != os.path.dirname(path):
                # If it does, delete it and its contents
                shutil.rmtree(extract_dir)

        # Extract the contents of the ZIP file
        with zipfile.ZipFile(path, "r") as zip_ref:
            # Extract the contents of the ZIP file
            zip_ref.extractall(extract_dir)

            # Delete the "MACOSX" folder if present
            macosx_folder = os.path.join(extract_dir, "__MACOSX")
            if os.path.exists(macosx_folder) and os.path.isdir(macosx_folder):
                shutil.rmtree(macosx_folder)

        # Delete the ZIP file
        os.remove(path)

    def read_images(self, path, limit=10):
        """
        Reads image files contained within the directory.

        Parameters:
            extract_dir (str): The directory containing the image files.

        Returns:
            list of PIL.Image.Image: List of Image objects containing the images.
        """
        images = []
        count = 0
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith((".png", ".jpg", ".jpeg", ".gif")):
                    image_path = os.path.join(root, file)
                    with open(image_path, "rb") as f:
                        image = Image.open(f)
                        plt.imshow(image)
                        plt.axis("off")
                        plt.show()
                        images.append(image)
                        count += 1
                        if limit is not None and count >= limit:
                            return
        if count == 0:
            print("No images found in the directory.")
