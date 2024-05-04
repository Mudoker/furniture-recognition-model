import os
import zipfile
import shutil
from PIL import Image
from skimage.metrics import structural_similarity as ssim
import numpy as np
import imagehash

import matplotlib.pyplot as plt
from scripts.styler import Styler

styler = Styler()

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

    def read_images(self, path, limit=10, show=True):
        """
        Reads image files contained within the directory.

        Parameters:
            extract_dir (str): The directory containing the image files.
            limit (int): Maximum number of images to read. Default is 10.
            show (bool): Whether to display the images. Default is True.
        Returns:
            list of PIL.Image.Image: List of Image objects containing the images.
        """
        images = []
        count = 0

        # Read the images from the directory
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith((".png", ".jpg", ".jpeg")):
                    # Open the image file
                    image_path = os.path.join(root, file)

                    # Read the image and close the file  afterwards
                    with open(image_path, "rb") as f:
                        image = Image.open(f)

                        # Display the image
                        if show:
                            plt.imshow(image)
                            plt.axis("off")
                            plt.show()
                        images.append(image)

                        count += 1
                        if limit != -1 and count >= limit:
                            return images

        # Empty directory
        if count == 0:
            print("No images found in the directory.")

        return images

    def detect_duplicates(
        self, path, hash_type="phash", limit=10, is_delete=False
    ):
        """
        Computes the perceptual hash of the images. And return a list of duplicate images.

        Parameters:
            path (str): The path to the directory containing the images.
            hash_type (str): Type of hash to use ("phash", "dhash", or "ahash").
            limit (int): Maximum number of duplicate images to display.
            is_delete (bool): Whether to delete the duplicate images.

        Returns:
            list of str: List of perceptual hash strings.
            list of PIL.Image.Image: List of duplicate images.
        """

        # Dictionary to store the hashes of the images
        hashes = {}
        duplicate_images = []
        duplicate_images_dict = {}
        count = 0

        # Hash function based on the hash_type
        if hash_type == "phash":
            hash_function = imagehash.phash
        elif hash_type == "dhash":
            hash_function = imagehash.dhash
        elif hash_type == "ahash":
            hash_function = imagehash.average_hash
        elif hash_type == "ssim":
            pass
        else:
            raise ValueError(
                "Invalid hash type. Use 'phash', 'dhash', 'ahash' or 'ssim'."
            )

        # Read the images from the directory
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith((".png", ".jpg", ".jpeg")):
                    # Open the image file
                    image_path = os.path.join(root, file)
                    image = Image.open(image_path)

                    # Compute the hash of the image
                    if hash_type == "ssim":
                        min_side = min(image.size)
                        win_size = min(7, min_side)
                        hash = lambda img: ssim(
                            np.array(img), np.array(img), win_size=win_size
                        )
                    else:
                        hash = hash_function(image)

                    # Check if the hash already exists in the dictionary
                    if hash in hashes:
                        # Add the duplicate image to the list
                        hashes[hash].append(image_path)
                        duplicate_images_dict[hash].append(image)
                    else:
                        # Add the hash to the dictionary
                        hashes[hash] = [image_path]
                        duplicate_images_dict[hash] = [image]
                    # Increment the count
                    count += 1
                    if limit != -1 and count >= limit:
                        break

        # Display the duplicate images path
        for hash, image_paths in hashes.items():
            if len(image_paths) > 1:
                styler.boxify(f"Hash: {hash}")
                counter = len(image_paths)
                for path in image_paths:
                    image_name = os.path.basename(path)
                    print(f"  - {image_name}")

                    # Delete the duplicate images
                    if is_delete:
                        if counter > 1:
                            os.remove(path)
                            counter -= 1

        print(f">>> Number of images compared: {count}")
        print()

        for hash, images in duplicate_images_dict.items():
            if len(images) > 1:
                for image in images:
                    duplicate_images.append(image)
                    break

        if len(duplicate_images) == 0:
            print(">>> No duplicate images found.")
            print()
