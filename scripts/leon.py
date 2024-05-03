import os
import zipfile
import shutil
from PIL import Image
from skimage.metrics import structural_similarity as ssim
import numpy as np
import imagehash

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
        self, path, hash_type="phash", limit=10, show=True, col_num=5
    ):
        """
        Computes the perceptual hash of the images. And return a list of duplicate images.

        Parameters:
            path (str): The path to the directory containing the images.
            hash_type (str): Type of hash to use ("phash", "dhash", or "ahash").
            limit (int): Maximum number of duplicate images to display.
            show (bool): Whether to display the duplicate images.

        Returns:
            list of str: List of perceptual hash strings.
            list of PIL.Image.Image: List of duplicate images.
        """

        # Dictionary to store the hashes of the images
        hashes = {}
        duplicate_images = []
        duplicate_images_names = []
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
                        win_size = min(
                            7, min_side
                        )  # Adjust 7 as necessary based on the smallest expected image dimension
                        hash = lambda img: ssim(
                            np.array(img), np.array(img), win_size=win_size
                        )
                    else:
                        hash = hash_function(image)

                    # Check if the hash already exists in the dictionary
                    if hash in hashes:
                        duplicate_images.append(image)

                        # Save image names
                        duplicate_images_names.append(file)
                    else:
                        hashes[hash] = image

                    # Increment the count
                    count += 1
                    if limit != -1 and count >= limit:
                        break

        print(f"Number of images processed: {count}")

        # Display duplicate images side by side
        if show:
            # Get the number of duplicate images
            num_duplicates = len(duplicate_images)
            print(f"Number of duplicate images found: {num_duplicates}")

            # Display the duplicate images
            if num_duplicates > 1:
                # Show the paths of duplicate images
                print("Paths of duplicate images:")
                for path in duplicate_images_names:
                    print(path)

                # Display the duplicate images in a grid
                num_rows = (num_duplicates + col_num - 1) // col_num
                fig, axs = plt.subplots(
                    num_rows, min(num_duplicates, col_num), figsize=(20, 12)
                )
                axs = axs.flatten()

                for i, img in enumerate(duplicate_images[:num_duplicates]):
                    axs[i].imshow(img)
                    axs[i].axis("off")

                # Hide empty subplots
                for j in range(num_duplicates, len(axs)):
                    axs[j].axis("off")
                plt.show()
            else:
                print("No duplicate images found.")
