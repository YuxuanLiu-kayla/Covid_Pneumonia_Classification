# The purpose of the code is to identify and classify common pneumonia, covid pneumonia and normal controls
import os
import shutil
import zipfile
import numpy as np
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers

# import SimpleITK and glob to convert multiple png files to one single nifti file
import SimpleITK as sitk
import glob
from shutil import move
import gzip

BASEDIR = "Desktop/Projects/Covid_Pneumonia_Classification/images"  # current working directory
CATEGORIES = ["Normal", "CovidP", "CP"]  # Normal: controls  CovidP: covid pneumonia  CP: common pneumonia


# function that convert multiple png files to one nifti file
# parent_path: patient ;  child_path: inner folder (each patient has 1 or 2 such folders)
# here child_path is current path
def convert_nifti(parent_path, child_path):
    file_names = glob.glob(os.path.join(child_path, "*.png"))
    reader = sitk.ImageSeriesReader()
    reader.SetFileNames(file_names)
    vol = reader.Execute()
    sitk.WriteImage(vol, "3D_Scan.nii.gz")  # note that the output file from SimpleITK is zipped

    # move the result zipped nifti image to parent folder (patient folder)
    move(os.path.join(child_path, "3D_Scan.nii.gz"), parent_path)
    # unzip the nifti file
    with gzip.open("3D_Scan.nii.gz", "rb") as f_in:
        with open("3D_Scan.nii", "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)


# first convert all png files in all categories to nifti files for future processing
for category in CATEGORIES:  # iterate through all categories
    cur_path = os.path.join(BASEDIR, category)  # create path to Normal, CovidP and CP
    patients_list = os.listdir(".")  # get all dirs in current path (all patients)

    # iterate through all patients in current category and produce nifti files
    for patient in patients_list:
        patient_path = os.path.join(cur_path, patient)
        all_dir = os.listdir(path = patient_path)
        if (len(all_dir) == 2):
            # create nifti file based on the second directory in patient
            convert_nifti(patient_path, os.path.join(patient_path, all_dir[1]))
        else:  # only 1 folder in patient
            convert_nifti(patient_path, os.path.join(patient_path, all_dir[0]))


# now we have nifti files of all patients. Continue handling these nifti files.

