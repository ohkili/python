import cv2
import glob
import os
import numpy as np
import matplotlib.pyplot as plt

# rembg 패키지에서 remove 클래스 불러오기
import rembg

# PIL 패키지에서 Image 클래스 불러오기
from PIL import Image
import matplotlib.pyplot as plt
def Load_image_with_cv2(image_path = 'D:/cafe7984/coffee_color_leveler_source_remove_background/coffee_laosting (2)_remove_bg.png',background_white =True):

    # Path to your image file

    # Read the image using OpenCV
    image = cv2.imread(image_path)
    # OpenCV reads images in BGR format, convert it to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # remove [0,0,0], [255,255,255]
    image_rgb_dup = image_rgb.copy()
    # np.where((image_rgb[:,:,0]==0)& (image_rgb[:,:,1]==0) & (image_rgb[:,:,2]==0))
    # index_vals = np.where(np.all(image_rgb==np.array([0,0,0]),axis=-1))
    # image_rgb[image_rgb == [0,0,0]]= [255,255,255]
    # image_rgb[index_vals[0][0]][index_vals[1][0]] = [255,255,255]



    if background_white:

        r = image_rgb[:, :, 0]
        g = image_rgb[:, :, 1]
        b = image_rgb[:, :, 2]
        mask = (r == 0) & (g == 0) & (b == 0)
        image_rgb[:, :, :][mask] = np.uint8([255, 255, 255])


        # image_rgb.shape
        # for i in range(image_rgb.shape[0]):
        #     for j in range(image_rgb.shape[1]):
        #         if all(image_rgb[i][j] == [0,0,0]):
        #             image_rgb[i][j] = [255,255,255]
        #         else:
        #             pass
    else:
        pass
    return image_rgb


def Extract_kmeans_patch_deleted_background(image_path='D:/cafe7984/coffee_color_leveler_source_remove_background/coffee_laosting (17)_remove_bg.png', n_colors=5):
    image_rgb = Load_image_with_cv2(image_path)
    palette, counts = Extract_palette_and_counts_by_kmeans(image_rgb, n_colors)
    "kmeans color deleted background"
    palette_new = palette.copy()


    min_palette = [255,255,255]
    max_palette = [0,0,0]
    i = 0
    min_palette_order = 0
    max_palette_order = 0

    while (i < len(palette)):
        if np.mean(min_palette) > np.mean(palette[i]):
            min_palette = palette[i].copy()
            min_palette_order = i
        if np.mean(max_palette) < np.mean(palette[i]):
            max_palette = palette[i].copy()
            max_palette_order = i
        i += 1


    max_val = np.min(palette[max_palette_order])
    min_val = np.max(palette[min_palette_order])

    'cut off'
    cutoff_ratio = 0.99
    if max_val >= 255 * cutoff_ratio:
        pass
    else :
        max_val = 255
    if min_val <= 255 * (1- cutoff_ratio):
        pass
    else:
        max_val = 0

    del_index_lst = []
    for i in range(len(palette_new)):
        if all(palette_new[i] >= max_val):
            del_index_lst.append(i)
        elif all(palette_new[i] <= min_val):
            del_index_lst.append(i)
    palette_del_bg = np.delete(palette_new, del_index_lst, 0)
    counts_del_bg = np.delete(counts, del_index_lst, 0)
    indices_del_bg = np.argsort(counts_del_bg)[::-1]
    freqs_del_bg = np.cumsum(np.hstack([[0], counts_del_bg[indices_del_bg] / float(counts_del_bg.sum())]))
    rows_del_bg = np.int_(image_rgb.shape[0] * freqs_del_bg)
    kmeans_patch_del_bg = np.zeros(shape=image_rgb.shape, dtype=np.uint8)
    for i in range(len(rows_del_bg) - 1):
        # i = 0
        kmeans_patch_del_bg[rows_del_bg[i]:rows_del_bg[i + 1], :, :] += np.uint8(palette_del_bg[indices_del_bg[i]])
    return palette_del_bg , kmeans_patch_del_bg
def Extract_kmeans_patch(image_path='D:/cafe7984/coffee_color_leveler_source_remove_background/coffee_laosting (18)_remove_bg.png', n_colors=5  ):
    "kmeans color"
    image_rgb = Load_image_with_cv2(image_path)
    palette, counts = Extract_palette_and_counts_by_kmeans(image_rgb, n_colors)
    indices = np.argsort(counts)[::-1]
    freqs = np.cumsum(np.hstack([[0], counts[indices] / float(counts.sum())]))
    rows = np.int_(image_rgb.shape[0] * freqs)
    kmeans_patch = np.zeros(shape=image_rgb.shape, dtype=np.uint8)
    for i in range(len(rows) - 1):
        kmeans_patch[rows[i]:rows[i + 1], :, :] += np.uint8(palette[indices[i]])
    return kmeans_patch
def Extract_simple_average_rgb_color(image_path='D:/cafe7984/coffee_color_leveler_source_remove_background/coffee_laosting (18)_remove_bg.png'):
    "full image's average color"
    image_rgb = Load_image_with_cv2(image_path)
    simple_average_palette = image_rgb.mean(axis=0).mean(axis=0)
    simple_avg_patch = np.ones(shape=image_rgb.shape, dtype=np.uint8) * np.uint8(simple_average_palette)
    return simple_average_palette, simple_avg_patch
def Extract_present_color_patch(image_path='D:/cafe7984/coffee_color_leveler_source_remove_background/coffee_laosting (18)_remove_bg.png', n_colors=5):
    image_rgb = Load_image_with_cv2(image_path)
    palette_del_bg , kmeans_patch_del_bg = Extract_kmeans_patch_deleted_background(image_path, n_colors=5)
    'present color : goal'
    present_color_palette = kmeans_patch_del_bg.mean(axis=0).mean(axis=0)
    #
    # row_one_color = np.int_(image_rgb.shape[0] * np.array([0,1]))
    # present_color_patch = np.zeros(shape=image_rgb.shape, dtype=np.uint8)
    #
    # for i in range(len(row_one_color) - 1):
    #     # i = 0
    #     present_color_patch[row_one_color[i]:row_one_color[i + 1], :, :] += np.uint8(present_color_palette)
    present_color_patch = np.ones(shape=image_rgb.shape, dtype=np.uint8) * np.uint8(present_color_palette)
    return present_color_palette, present_color_patch
def dominant_colors_kmeans_oneshot( n_colors = 9):
    # image_path='D:/cafe7984/coffee_color_leveler_source_remove_background/coffee_laosting ('+str(no)+')_remove_bg.png'
    image_path='D:/cafe7984/keep/agtrron.jpg'
    image_rgb = Load_image_with_cv2(image_path)
    simple_average_palette, simple_avg_patch = Extract_simple_average_rgb_color(image_path)

    palette, counts = Extract_palette_and_counts_by_kmeans(image_rgb, n_colors)
    indices = np.argsort(counts)[::-1]
    freqs = np.cumsum(np.hstack([[0], counts[indices] / float(counts.sum())]))
    rows = np.int_(image_rgb.shape[0] * freqs)
    kmeans_patch = np.zeros(shape=image_rgb.shape, dtype=np.uint8)
    for i in range(len(rows) - 1):
        kmeans_patch[rows[i]:rows[i + 1], :, :] += np.uint8(palette[indices[i]])

    "kmeans color deleted background"
    palette_new = palette.copy()

    min_palette = [255, 255, 255]
    max_palette = [0, 0, 0]
    i = 0
    min_palette_order = 0
    max_palette_order = 0

    while (i < len(palette)):
        if np.mean(min_palette) > np.mean(palette[i]):
            min_palette = palette[i].copy()
            min_palette_order = i
        if np.mean(max_palette) < np.mean(palette[i]):
            max_palette = palette[i].copy()
            max_palette_order = i
        i += 1

    max_val = np.min(palette[max_palette_order])
    min_val = np.max(palette[min_palette_order])

    'cut off'
    cutoff_ratio = 0.99
    if max_val >= 255 * cutoff_ratio:
        pass
    else:
        max_val = 255
    if min_val <= 255 * (1 - cutoff_ratio):
        pass
    else:
        min_val = 0

    del_index_lst = []
    for i in range(len(palette_new)):
        if all(palette_new[i] >= max_val):
            del_index_lst.append(i)
        elif all(palette_new[i] <= min_val):
            del_index_lst.append(i)
    palette_del_bg = np.delete(palette_new, del_index_lst, 0)
    counts_del_bg = np.delete(counts, del_index_lst, 0)
    indices_del_bg = np.argsort(counts_del_bg)[::-1]
    freqs_del_bg = np.cumsum(np.hstack([[0], counts_del_bg[indices_del_bg] / float(counts_del_bg.sum())]))
    rows_del_bg = np.int_(image_rgb.shape[0] * freqs_del_bg)
    kmeans_patch_del_bg = np.zeros(shape=image_rgb.shape, dtype=np.uint8)
    for i in range(len(rows_del_bg) - 1):
        # i = 0
        kmeans_patch_del_bg[rows_del_bg[i]:rows_del_bg[i + 1], :, :] += np.uint8(palette_del_bg[indices_del_bg[i]])

    'present color'
    present_color_palette = kmeans_patch_del_bg.mean(axis=0).mean(axis=0)

    present_color_patch = np.ones(shape=image_rgb.shape, dtype=np.uint8) * np.uint8(present_color_palette)

    Show_and_save_image_patch(image_rgb, present_color_patch, kmeans_patch_del_bg, kmeans_patch, simple_avg_patch, fpath='D:/one_color_rev3.jpg')


def main_remove_background_image():
    # Load an image from file

    # input path
    image_path_origin = 'D:/cafe7984/coffee_color_leveler_source'

    # output path
    image_path_remove_background = 'D:/cafe7984/coffee_color_leveler_source_remove_background'
    os.makedirs(image_path_remove_background, exist_ok=True)

    image_file_lst = glob.glob(image_path_origin + '/*.jpg')

    for image_fpath in image_file_lst:
        image_file_name = image_fpath.replace('\\','/').split('/')[-1].split('.')[0]
        out_fpath = os.path.join(image_path_remove_background,image_file_name + '_remove_bg.png')
        image_rgb_origin, image_rgb_remvoe_bg = Remove_background_image(image_fpath)


def Show_and_save_image_patch(image_rgb,present_color_patch, kmeans_patch_del_bg, kmeans_patch,simple_avg_patch ,fpath = 'D:/one_color_rev1.jpg'):
    fig, (ax0, ax1, ax2, ax3, ax4) = plt.subplots(1, 5, figsize=(20, 10))

    # image_dict= {'original image':image_rgb,'Present color': present_color_patch,'Dominant colors del back':kmeans_patch_del_bg,
    #              'Dominant colors':kmeans_patch,'Simple average color':simple_avg_patch }
    #
    #
    # ax_lst = [ax0, ax1, ax2, ax3, ax4]
    # for key in image_dict:


    ax0.imshow(image_rgb)
    ax0.set_title('original image')
    ax0.axis('on')
    ax0.axes.get_xaxis().set_visible(False)
    ax0.axes.get_yaxis().set_visible(False)

    ax1.imshow(present_color_patch)
    ax1.set_title('Present color')
    ax1.axis('on')
    ax1.axes.get_xaxis().set_visible(False)
    ax1.axes.get_yaxis().set_visible(False)


    ax2.imshow(kmeans_patch_del_bg)
    ax2.set_title('Dominant colors del back')
    ax2.axis('on')
    ax2.axes.get_xaxis().set_visible(False)
    ax2.axes.get_yaxis().set_visible(False)

    ax3.imshow(kmeans_patch)
    ax3.set_title('Dominant colors')
    ax3.axis('on')
    ax3.axes.get_xaxis().set_visible(False)
    ax3.axes.get_yaxis().set_visible(False)


    ax4.imshow(simple_avg_patch)
    ax4.set_title('Simple average color')
    ax4.axis('on')
    ax4.axes.get_xaxis().set_visible(False)
    ax4.axes.get_yaxis().set_visible(False)

    plt.savefig(fpath)
    plt.close()