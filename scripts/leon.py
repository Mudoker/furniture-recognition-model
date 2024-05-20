import os
import zipfile
import shutil
from PIL import Image
from skimage.metrics import structural_similarity as ssim
import numpy as np
import pandas as pd
import imagehash
import cv2
from keras import layers
from keras.models import Sequential  # type: ignore
import matplotlib.pyplot as plt
from scripts.styler import Styler

styler = Styler()


class Leon:
    def read_zip(self, path):
        """
        Extracts a ZIP file, reads the image files contained within it, and deletes the ZIP file afterwards.

        Parameters:
            path (str): The path to the ZIP file.

        Returns:
            list of PIL.Image.Image: List of Image objects containing the images from the ZIP file.
        """
        if not os.path.exists(path):
            print(f"File not found: {path} or has been unzipped.")
            return

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
        if not os.path.exists(path):
            raise FileNotFoundError(f"Directory not found: {path}")

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
        if not os.path.exists(path):
            raise FileNotFoundError(f"Directory not found: {path}")

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
                counter = len(image_paths)
                for path in image_paths:
                    # Delete the duplicate images
                    if is_delete:
                        if counter > 1:
                            os.remove(path)
                            counter -= 1

        for hash, images in duplicate_images_dict.items():
            if len(images) > 1:
                for image in images:
                    duplicate_images.append(image)
                    break

    def augment_image(
        self,
        image_path,
        output_dir,
        df_train,
        num_images=5,
        rotation=0.5,
        contrast=0.5,
    ):
        """
        Augments an image by applying random transformations.

        Parameters:
            image_path (str): The path to the image file.
            output_dir (str): The directory to save the augmented images.
            num_images (int): The number of augmented images to generate. Default is 5.
            df_train (pd.DataFrame): The DataFrame to store the augmented image paths, classes, styles, widths, and heights.
            flip_direction (str): The direction to flip the image ("horizontal" or "vertical"). Default is "vertical".
            rotation (float): The maximum rotation angle in degrees. Default is 0.5.
            contrast (float): The maximum contrast factor. Default is 0.5.
        """
        # Error handling
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"File not found: {image_path}")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        if df_train is None:
            raise ValueError("df_train is required.")

        # Data augmentation transformations
        data_augmentation = Sequential(
            [
                layers.RandomFlip("horizontal_and_vertical"),
                layers.RandomRotation(0.4),
                layers.RandomCrop(0.8, 0.8),
                layers.RandomContrast(0.2),
                layers.RandomZoom(0.3),
                layers.RandomTranslation(0.2, 0.2),
                layers.RandomSheer(0.1),
            ]
        )

        # Read the image
        img = cv2.imread(image_path)

        # Convert the image to a numpy array and add a batch dimension
        img_array = np.expand_dims(img, axis=0)

        image_filename = os.path.basename(image_path).split(".")[0]

        path_parts = image_path.split(os.path.sep)

        # Extract the category and style from the image path
        category = path_parts[-3]
        style = path_parts[-2]

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
                    "MinValue": [np.min(augmented_img)],
                    "MaxValue": [np.max(augmented_img)],
                    "StdDev": [np.std(augmented_img)],
                }
            )

            df_train = pd.concat([df_train, new_row], ignore_index=True)

        return df_train

    def load_data_frame(self, dir: str) -> pd.DataFrame:
        """
        Load the images from the directory into a pandas DataFrame.

        Parameters:

            dir (str): The directory containing the images.

        Returns:

                pd.DataFrame: A DataFrame containing the image paths, classes, styles, widths, and heights.
        """
        if not os.path.exists(dir):
            raise FileNotFoundError(f"Directory not found: {dir}")

        # Initialize the dictionary to store the data
        data_dict = {
            "Path": [],
            "Category": [],
            "Style": [],
            "Width": [],
            "Height": [],
            "MinValue": [],
            "MaxValue": [],
            "StdDev": [],
        }

        data_dir = os.path.relpath(dir)

        # Get the categories and styles
        categories = [
            folder
            for folder in os.listdir(data_dir)
            if os.path.isdir(os.path.join(data_dir, folder))
        ]

        for category in categories:
            # Get the styles for each category
            category_dir = os.path.join(data_dir, category)
            styles = [
                folder
                for folder in os.listdir(category_dir)
                if os.path.isdir(os.path.join(category_dir, folder))
            ]

            # Iterate over the styles
            for style in styles:
                style_dir = os.path.join(category_dir, style)

                # Iterate over the images in the style directory
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

                            # Convert image to numpy array
                            img_array = np.array(img)

                            # Compute statistics
                            min_val = np.min(img_array)
                            max_val = np.max(img_array)
                            std_dev = np.std(img_array)

                            # Add statistics to the dictionary
                            data_dict["MinValue"].append(min_val)
                            data_dict["MaxValue"].append(max_val)
                            data_dict["StdDev"].append(std_dev)
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
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        # Open the image file
        with open(path, "rb") as f:
            image = Image.open(f)

            # Resize the image
            resized_image = image.resize((width, height))

            # Save the resized image
            resized_image.save(path)

    def normalize_image(self, image_path, min_value=0, max_value=1):
        """
        Normalize the pixel values of an image to the range [0, 1].

        Parameters:
            image_path (str): The path to the image file.
            min_value (float): The minimum value of the normalized range. Default is 0.
            max_value (float): The maximum value of the normalized range. Default is 1.

        Returns:
            str: The path to the normalized image.
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"File not found: {image_path}")

        if not isinstance(min_value, (int, float)) or not isinstance(
            max_value, (int, float)
        ):
            raise TypeError("min_value must be an integer or float")

        if min_value >= max_value:
            raise ValueError("min_value must be less than max_value")

        styler.boxify(f"Normalizing image: {image_path}")
        # Open the image
        image = cv2.imread(image_path)

        # Normalize the pixel values to the range [0, 1]
        normalized_image = cv2.normalize(
            image, None, min_value, max_value, cv2.NORM_MINMAX, dtype=cv2.CV_32F
        )

        print(">>> Processed successfully")

        return normalized_image

    def remove_folder(self, path):
        """
        Removes a folder and its contents.

        Parameters:
            path (str): The path to the folder to remove.
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"Folder not found: {path}")

        print(
            "This is a destructive operation as folder will be deleted permanently. Are you sure you want to continue? (y/n)"
        )

        response = input()

        if response.lower() != "y" and response.lower() != "yes":
            print("Operation cancelled.")
            return

        shutil.rmtree(path)

    # Remove output folders and files generated by the previous run

    def remove_nonraw_files(self, img_paths=[]):
        """
        Removes output folders and files generated by the previous run.

        Parameters:
            img_paths (list[str]): List of image paths in the training set.
        """
        # Check if img_paths is provided
        if not img_paths:
            raise ValueError("img_paths is required.")

        # Confirm with the user before proceeding
        print(
            "This is a destructive operation as files will be deleted permanently. Are you sure you want to continue? (y/n)"
        )

        response = input()

        if response.lower() != "y" and response.lower() != "yes":
            print("Operation cancelled.")
            return

        print("\nPlease wait and do not interrupt the process.\n")
        print("Removing non-raw files...\n")

        # Initialize set to store processed directories
        processed_directories = set()

        # Get all image path in the training set
        for img_path in img_paths:
            # Extract directory name
            directory = os.path.dirname(img_path)

            # Check if directory has already been processed
            if directory in processed_directories:
                continue

            # Add directory to the set of processed directories
            processed_directories.add(directory)

            # Remove files starting with "augmented_" if they exist
            files_in_directory = os.listdir(directory)
            for file_name in files_in_directory:
                # Check if file name starts with "aug_"
                if file_name.startswith("aug_") or file_name.endswith("_norm.jpg"):
                    # Construct file path
                    file_path = os.path.join(directory, file_name)

                    # Remove file
                    try:
                        os.remove(file_path)
                    except OSError as e:
                        print(f"Error removing file: {file_path}, {e}")

    def get_image_paths(self, directory):
        """
        Get the paths of all image files in the directory and its subdirectories.

        Parameters:
            directory (str): The directory to search for image files.

        Returns:
            list of str: List of image paths.
        """
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory not found: {directory}")

        image_paths = []
        # Walk through the directory and its subdirectories
        for root, dirs, files in os.walk(directory):
            # Iterate over the files in the current directory
            for file in files:
                # Check if the file is an image (you can modify this condition as needed)
                if file.endswith((".jpg")):
                    # Construct the full path to the image file
                    image_path = os.path.join(root, file)
                    # Add the image path to the list
                    image_paths.append(image_path)
        return image_paths
