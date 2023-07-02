import os
import json
import time

import cv2 as cv
from config.config import user_config,ADB_HEAD
from imutils import contours
from skimage import measure
import numpy as np
import argparse
import imutils

def get_screen_shot():
    os.system(f'{ADB_HEAD} exec-out screencap -p > cache/screenshot.png')
    return 'cache/screenshot.png'

def get_scrren_shot_bytes():
    os.system(f'{ADB_HEAD} exec-out screencap -p > cache/screenshot.png')
    img=cv.imread('cache/screenshot.png')
    return img

def write_config():
    with open('config.json', 'w') as f:
        json.dump(user_config, f, indent=4)

def improve_contrast(image):
    # converting to LAB color space
    lab = cv.cvtColor(image, cv.COLOR_BGR2LAB)
    l_channel, a, b = cv.split(lab)

    # Applying CLAHE to L-channel
    # feel free to try different values for the limit and grid size:
    clahe = cv.createCLAHE(clipLimit=0.0, tileGridSize=(8, 8))
    cl = clahe.apply(l_channel)

    # merge the CLAHE enhanced L-channel with the a and b channel
    limg = cv.merge((cl, a, b))

    # Converting image from LAB Color model to BGR color spcae
    enhanced_img = cv.cvtColor(limg, cv.COLOR_LAB2BGR)
    return enhanced_img

def do_find_brightest_area(image, radius):
    # load the image and convert it to grayscale
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # apply a Gaussian blur to the image then find the brightest
    # region
    gray = cv.GaussianBlur(gray, (radius, radius), 0)

    (minVal, maxVal, minLoc, maxLoc) = cv.minMaxLoc(gray)
    return maxLoc

def find_brightest_area():

    # load the image, convert it to grayscale, and blur it
    image = cv.imread("cache/screenshot.png")

    loc = do_find_brightest_area(image, 41)
    # image = improve_contrast(image)
    return loc