import cv2
import glob
import os
import numpy as np
import matplotlib.pyplot as plt

# Load an image from file

image_path = 'D:/cafe7984/coffee_color_leveler_source'
image_file_lst = glob.glob(image_path + '/*.jpg')
image_fpath = image_file_lst[-1]
image = cv2.imread(image_fpath)

# Back ground delete
# rembg 패키지에서 remove 클래스 불러오기
from rembg import remove

# PIL 패키지에서 Image 클래스 불러오기
from PIL import Image

# Lenna.png파일 불러오기
img = Image.open(image_fpath)

# 배경 제거하기
out = remove(img)

# 변경된 이미지 저장하기
out.save(image_fpath.replace('.jpg', '_rembg.png'))
out.save(image_fpath.replace('.JPG', '_rembg.png'))
