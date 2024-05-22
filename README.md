# COSC 2753 - Machine Learning

## _Furniture Detection and Classification_

This project endeavors to construct a machine learning model capable of identifying furniture items and categorizing them into respective types based on image analysis. By scrutinizing diverse features and attributes of furniture pieces, the model can discern patterns distinguishing between various categories like chairs, tables, sofas, etc., and further subdivide them into specific types within each category.

### Project Structure Guide

This guide outlines the essential steps to establish the project structure for efficient management of datasets and notebooks. Additionally, it's crucial to note that altering file locations may lead to improper library imports.

Since the dataset exceeds the upload limit of GitHub, it is housed in a OneDrive folder. Please procure the dataset from the provided links:

**Note 1:** Only use the `Dataset for EDA` if your task is related to the EDA steps, as it contains raw images taken from the lecturer. For subsequent steps, please use the processed dataset to avoid re-running the entire cleaning process.

**Instructions:**

1. Unzip the data and split it into two identical folders: `data_1` and `data_2`. Move the deepest child out of `Furniture_Data/Furniture_Data` to the appropriate location.
2. Ensure the folder structure looks like `data_1/raw/beds/1.jpg` or `data_2/raw/chairs/2.jpg`.

These steps are only necessary for the EDA part or if you want to test the pipeline. For running the project, just use `dataset_1` and `dataset_2` provided, and place them in the root of the project (do not zip them together).

```
project_root/
├── data_1/
│   └── raw/
│       ├── beds/
│       │   ├── 1.jpg
│       │   ├── 2.jpg
│       │   └── ...
│       ├── chairs/
│       │   ├── 1.jpg
│       │   ├── 2.jpg
│       │   └── ...
│       └── ...
├── data_2/
│   └── raw/
│       ├── beds/
│       │   ├── 1.jpg
│       │   ├── 2.jpg
│       │   └── ...
│       ├── chairs/
│       │   ├── 1.jpg
│       │   ├── 2.jpg
│       │   └── ...
│       └── ...
├── notebooks/
│   └── ... (Jupyter notebooks)
├── scripts/
│   └── ... (Python script files)
└── README.md
```

[Raw Dataset](https://rmiteduau-my.sharepoint.com/personal/bao_nguyenthien_rmit_edu_vn/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fbao_nguyenthien_rmit_edu_vn%2FDocuments%2FFurniture_Data%2Ezip&parent=%2Fpersonal%2Fbao_nguyenthien_rmit_edu_vn%2FDocuments&ga=1)

[Dataset_1](https://rmiteduau-my.sharepoint.com/:u:/g/personal/s3927776_student_rmit_edu_au/Ec3FSIyZfBdDi8SvBxrMuh4BaKMLwDFfFZu9QLpKcx8WgA?e=snVpuQ)

[Dataset_2](https://drive.google.com/file/d/1sVsG79K0DZ-DwxgDokLXVOEObqnOL4KZ/view?usp=sharing)

### Branch Naming Convention

When creating branches for development or issue tracking, adhere to the following naming convention:

1. Branch format should be `indicator_title` or `indicator/title` (either should be fine).
2. Indicator includes:
   - `feat` for new features
   - `fix` to fix a bug
   - `ref` for restructuring folders or clean codes
   - `style` for changing UI
   - `perf` for optimizing code for better performance
3. Example: `feature/univariate_analysis`
4. Do not include your name in the branch name, as it serves no purposes.

### Installation

Prior to executing this notebook, ensure the requisite libraries are installed.

- #### **Obtain the recommended version of Python**

  - Python 3.11.9: [Downloads]([https://www.python.org/downloads/](https://www.python.org/downloads/release/python-3119/)).

- #### **Acquire the packages**

```bash
pip install -r requirements.txt # Install the latest version of libraries
```

### Author

- [Huu Quoc Doan - s3927776@rmit.edu.vn](https://github.com/Mudoker)
- [Seokyung Kim - s3939114@rmit.edu.vn](https://github.com/lluciiiia)
- [Nguyen Dinh Viet - s3927291@rmit.edu.vn](https://github.com/Mudoker)
- [Tran Vu Quang Anh - s3916566@rmit.edu.vn](https://github.com/Mudoker)

_I declare that in submitting all work for this assessment I have read, understood and agree to the content and expectations of the Assessment declaration._
