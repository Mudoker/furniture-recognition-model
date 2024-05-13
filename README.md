# COSC 2753 - Machine Learning

## _Furniture Detection and Classification_

This project endeavors to construct a machine learning model capable of identifying furniture items and categorizing them into respective types based on image analysis. By scrutinizing diverse features and attributes of furniture pieces, the model can discern patterns distinguishing between various categories like chairs, tables, sofas, etc., and further subdivide them into specific types within each category.

### Project Setup Guide

This guide delineates the essential steps to establish the project structure for efficient management of datasets and notebooks. Additionally, it's crucial to note that alterations in file locations may lead to improper library imports.

Since the dataset exceeds the upload limit of GitHub, it is housed in a OneDrive folder. Please procure the dataset from the provided link:

Note 1: Only use the `Dataset for EDA` if your task is related to the EDA steps as it contains raw images taken from the lecturer. For subsequent steps, please use the latter dataset to avoid re-running the entire cleaning process.

Note 2 (Only applicable to EDA Dataset): Once the dataset is obtained, create a new `data` folder at the root of the project and then put the zip file into the `data/raw` subfolder (create one if not exist). Ensure not to alter the name of the zip file.

[Dataset for EDA](https://rmiteduau-my.sharepoint.com/personal/bao_nguyenthien_rmit_edu_vn/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fbao_nguyenthien_rmit_edu_vn%2FDocuments%2FFurniture_Data%2Ezip&parent=%2Fpersonal%2Fbao_nguyenthien_rmit_edu_vn%2FDocuments&ga=1)

[Processed Dataset](https://rmiteduau-my.sharepoint.com/:u:/g/personal/s3927776_student_rmit_edu_au/Ec3FSIyZfBdDi8SvBxrMuh4BaKMLwDFfFZu9QLpKcx8WgA?e=snVpuQ)

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

  - Python 3.12.2: [Downloads]([https://www.python.org/downloads/](https://www.python.org/downloads/release/python-3122/)).

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
