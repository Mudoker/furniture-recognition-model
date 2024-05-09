import os
import zipfile
import shutil
from PIL import Image
from skimage.metrics import structural_similarity as ssim
import numpy as np
import pandas as pd
import imagehash
import keras
import cv2
from keras import layers
from keras.models import Sequential  # type: ignore

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

    def detect_duplicates(self, path, hash_type="phash", limit=10, is_delete=False):
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

    def augment_image(
        self,
        image_path,
        output_dir,
        df_train,
        num_images=3,
        rotation=0.5,
        contrast=0.5,
    ):
        """
        Augments an image by applying random transformations.

        Parameters:
            image_path (str): The path to the image file.
            output_dir (str): The directory to save the augmented images.
            num_images (int): The number of augmented images to generate. Default is 3.
            df_train (pd.DataFrame): The DataFrame to store the augmented image paths, classes, styles, widths, and heights.
            flip_direction (str): The direction to flip the image ("horizontal" or "vertical"). Default is "vertical".
            rotation (float): The maximum rotation angle in degrees. Default is 0.5.
            contrast (float): The maximum contrast factor. Default is 0.5.
        """
        # Initialize df_train as an empty DataFrame if not provided
        if df_train is None:
            raise ValueError("df_train is required.")

        data_augmentation = Sequential(
            [
                layers.RandomFlip(),
                layers.RandomRotation(rotation),
                layers.RandomContrast(contrast),
            ]
        )

        img = cv2.imread(image_path)

        img_array = np.expand_dims(img, axis=0)

        styler.boxify(f"Augmenting image: {image_path}")

        image_filename = os.path.basename(image_path)

        path_parts = image_path.split(os.path.sep)

        if len(path_parts) >= 5:
            category = path_parts[-2]
            style = path_parts[-3]
        else:
            category = "unknown"
            style = "unknown"

        # Apply data augmentation transformations
        for i in range(num_images):
            augmented_img = data_augmentation(img_array)
            augmented_img = (
                augmented_img.numpy()
            )  # Convert from TensorFlow tensor to numpy array
            augmented_img = augmented_img[0]

            # Convert image to correct data type and range for OpenCV
            augmented_img = np.clip(augmented_img, 0, 255).astype(np.uint8)

            # Save the augmented image
            filename = f"aug_{image_filename}_{i}.jpg"

            output_path = os.path.join(output_dir, filename)
            cv2.imwrite(output_path, augmented_img)

            # Add the augmented image to the dataframe
            new_row = pd.DataFrame(
                {
                    "Path": [output_path],
                    "Category": [category],
                    "Style": [style],
                    "Width": [augmented_img.shape[1]],
                    "Height": [augmented_img.shape[0]],
                }
            )

            df_train = pd.concat([df_train, new_row], ignore_index=True)

            # Add the augmented image to the dataframe
            print(f"  - Saved augmented image: {filename}")

        return df_train

    def load_data_frame(self, dir: str) -> pd.DataFrame:
        """
        Load the images from the directory into a pandas DataFrame.

        Parameters:

            dir (str): The directory containing the images.

        Returns:

                pd.DataFrame: A DataFrame containing the image paths, classes, styles, widths, and heights.
        """

        data_dict = {
            "Path": [],
            "Category": [],
            "Style": [],
            "Width": [],
            "Height": [],
        }

        data_dir = os.path.relpath(dir)

        categories = [
            folder
            for folder in os.listdir(data_dir)
            if os.path.isdir(os.path.join(data_dir, folder))
        ]

        for category in categories:
            category_dir = os.path.join(data_dir, category)
            styles = [
                folder
                for folder in os.listdir(category_dir)
                if os.path.isdir(os.path.join(category_dir, folder))
            ]

            for style in styles:
                style_dir = os.path.join(category_dir, style)
                for file in os.listdir(style_dir):
                    img_path = os.path.join(style_dir, file)
                    data_dict["Path"].append(img_path)
                    data_dict["Category"].append(category)
                    data_dict["Style"].append(style)

                    # Get width and height of the image
                    try:
                        with Image.open(img_path) as img:
                            width, height = img.size
                            data_dict["Width"].append(width)
                            data_dict["Height"].append(height)
                    except Exception as e:
                        print(f"Error processing image '{img_path}': {e}")

        return pd.DataFrame(data_dict)

    def resize_image(self, path, width, height):
        """
        Resizes the image to the specified width and height.

        Parameters:
            path (str): The path to the image file.
            width (int): The width of the resized image.
            height (int): The height of the resized image.
        """
        # Open the image file
        with open(path, "rb") as f:
            image = Image.open(f)

            # Resize the image
            resized_image = image.resize((width, height))

            # Save the resized image
            resized_image.save(path)

    def normalise_pixel_values(self, image_path):
        """
        Normalises the pixel values of the image to the range [0, 1].

        Parameters:
            image (PIL.Image.Image): The image to normalise.

        Returns:
            np.ndarray: The normalised image as a NumPy array.
        """
        # Convert the image to a NumPy array
        image = Image.open(image_path)
        image_array = np.array(image)

        # Normalise the pixel values to the range [0, 1]
        normalised_image = image_array / 255.0

        return normalised_image

    def remove_folder(self, path):
        """
        Removes a folder and its contents.

        Parameters:
            path (str): The path to the folder to remove.
        """
        shutil.rmtree(path)
