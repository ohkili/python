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

from coffee_color_leveler.Extract_image_attr import Extract_simple_average_rgb_color


def Remove_background_image(image_fpath= 'D:/cafe7984/coffee_color_roasting_source/BRZ_181_231216 (1).jpg'):

    # Load the input image
    # input_image = Image.open(image_fpath)
    input_image = cv2.imread(image_fpath)
    input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)
    image_rgb_origin = input_image.copy()
    # Convert the input image to a numpy array
    input_array = np.array(input_image)
    # image_rgb_origin = input_array.copy()

    # Apply background removal using rembg
    output_array = rembg.remove(input_array)

    image_rgb_remove_bg = cv2.cvtColor(output_array,cv2.COLOR_RGBA2RGB)
    # image_rgb_remove_bg = np.array(image_rgb_remove_bg)

    # Create a PIL Image from the output array
    # output_image = Image.fromarray(output_array)
    #
    # image_rgb_remove_bg = np.array(output_image.convert("RGB"))
    # from PIL import Image
    # im_in = Image.fromarray(image_rgb_origin)
    # im_in.save('D:/cafe7984/coffee_color_roasting_output/test11.jpg')
    # im_out = Image.fromarray(image_rgb_remove_bg)
    # im_out.save('D:/cafe7984/coffee_color_roasting_output/test11_remove_1.jpg')
    return image_rgb_origin, image_rgb_remove_bg
def Change_pixel_black_to_white(cropped_image_rgb):
    cropped_image_rgb_r = cropped_image_rgb[:, :, 0]
    cropped_image_rgb_g = cropped_image_rgb[:, :, 1]
    cropped_image_rgb_b = cropped_image_rgb[:, :, 2]
    cropped_image_rgb_mask = (cropped_image_rgb_r == 0) & (cropped_image_rgb_g == 0) & (cropped_image_rgb_b == 0)
    cropped_image_rgb[:, :, :][cropped_image_rgb_mask] = np.uint8([255, 255, 255])

    return cropped_image_rgb
#
# fpath_input_image  = 'D:/cafe7984/coffee_color_roasting_source\\BRZ_181_231218.jpg'
# image_rgb_origin, image_rgb_remove_bg = Remove_background_image(fpath_input_image)
# image = image_rgb_origin.copy()
# image = image_rgb_remove_bg.copy()
#
#
# minRadius = int(np.min([image.shape[0] / 2, image.shape[1] / 2]) * 0.7)  # 0.7 is hyperparameter
# maxRadius = int(np.min([image.shape[0] / 2, image.shape[1] / 2]) * 1.0)  # 1.0 is hyperparameter
# minDist = int(minRadius * 0.7)  # 0.7 is hyperparameter
# crop_ratio = 0.6  # # 0.6 is hyperparameter
def Crop_circle_area(image, minDist=500, minRadius=800,maxRadius=1600, crop_ratio = 0.8):

    # # Load the image

    # _,image = Remove_background_image()
    image_origin = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # Apply GaussianBlur to reduce noise and help the circle detection
    gray_blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    # Use Hough Circle Transform to detect circles
    circles = cv2.HoughCircles(gray_blurred,cv2.HOUGH_GRADIENT, dp=1.2,minDist=minDist,param1=100,param2=30, minRadius=minRadius, maxRadius=maxRadius) # param1=50,# param2=30)
    # If circles are detected, create a 2D array with circle area set to 1
    if circles is not None:
        circles = np.uint16(np.around(circles))

        # Create a binary mask with the same shape as the original image
        mask = np.zeros_like(gray)

        for i in circles[0, :]:
            # Get the circle coordinates and radius
            x, y, radius = i[0], i[1], i[2]

            # Set the circle area to 1 in the mask
            cv2.circle(mask, (x, y), int(radius * crop_ratio), 1, thickness=cv2.FILLED)
            cv2.circle(image, (x, y), int(radius), (255, 0, 255), 3)

        # Display the binary mask
        # print(mask)
    else:
        print("No circles detected.")
    # cv2.imshow("detected circles", mask)




    image_r = image_origin[:, :, 0]
    image_g = image_origin[:, :, 1]
    image_b = image_origin[:, :, 2]
    image_r_masked = image_r * mask
    image_g_masked = image_g * mask
    image_b_masked = image_b * mask
    image_masked = np.ones((image_origin.shape[0], image_origin.shape[1], image_origin.shape[2]), dtype=np.uint8)
    image_masked[:, :, 0] = image_r_masked
    image_masked[:, :, 1] = image_g_masked
    image_masked[:, :, 2] = image_b_masked

    # ... get array s.t. arr.shape = (3,256, 256)
    cropped_image_rgb = image_masked.copy()
    # cropped_image = Image.fromarray(cropped_image_rgb, 'RGB')
    # cropped_image.save("D:/cafe7984/crop_"+str(crop_ratio)+".jpg")
    image_circle_detected = image.copy()
    "test image save"
    # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    # if os.path.exists('D:/cafe7984/coffee_color_roasting_source/test_image.jpg'):
    #     os.remove('D:/cafe7984/coffee_color_roasting_source/test_image.jpg')
    # else:
    #     pass
    # cv2.imwrite('D:/cafe7984/coffee_color_roasting_source/test_image.jpg', image)
    #
    # cropped_image_rgb = cv2.cvtColor(cropped_image_rgb,cv2.COLOR_RGB2BGR)
    # if os.path.exists('D:/cafe7984/coffee_color_roasting_source/test_image_cropped.jpg'):
    #     os.remove('D:/cafe7984/coffee_color_roasting_source/test_image_cropped.jpg')
    # else:
    #     pass
    # cv2.imwrite('D:/cafe7984/coffee_color_roasting_source/test_image_cropped.jpg', cropped_image_rgb)
    #

    return cropped_image_rgb ,image_circle_detected
def Show_and_save_image_patch_plus(image_rgb_origin,present_color_patch, kmeans_patch_del_bg, kmeans_patch,simple_avg_patch , cropped_image_rgb, roasting_level = 83,fpath = 'D:/one_color_rev1.jpg'):
    fig, ax = plt.subplots(2, 5, figsize=(20, 10))

    # image_dict= {'original image':image_rgb,'Present color': present_color_patch,'Dominant colors del back':kmeans_patch_del_bg,
    #              'Dominant colors':kmeans_patch,'Simple average color':simple_avg_patch }
    #
    #
    # ax_lst = [ax0, ax1, ax2, ax3, ax4]
    # for key in image_dict:


    ax[0,0].imshow(image_rgb_origin)
    ax[0,0].set_title('original image')
    ax[0,0].axis('on')
    ax[0,0].axes.get_xaxis().set_visible(False)
    ax[0,0].axes.get_yaxis().set_visible(False)

    ax[0,1].imshow(present_color_patch)
    ax[0,1].set_title('Present color')
    ax[0,1].axis('on')
    ax[0,1].axes.get_xaxis().set_visible(False)
    ax[0,1].axes.get_yaxis().set_visible(False)


    ax[0,2].imshow(kmeans_patch_del_bg)
    ax[0,2].set_title('Dominant colors del back')
    ax[0,2].axis('on')
    ax[0,2].axes.get_xaxis().set_visible(False)
    ax[0,2].axes.get_yaxis().set_visible(False)

    ax[0,3].imshow(kmeans_patch)
    ax[0,3].set_title('Dominant colors')
    ax[0,3].axis('on')
    ax[0,3].axes.get_xaxis().set_visible(False)
    ax[0,3].axes.get_yaxis().set_visible(False)


    ax[0,4].imshow(simple_avg_patch)
    ax[0,4].set_title('Simple average color')
    ax[0,4].axis('on')
    ax[0,4].axes.get_xaxis().set_visible(False)
    ax[0,4].axes.get_yaxis().set_visible(False)

    ax[1, 0].imshow(cropped_image_rgb)
    ax[1, 0].set_title('Cropped image')
    ax[1, 0].axis('on')
    ax[1, 0].axes.get_xaxis().set_visible(False)
    ax[1, 0].axes.get_yaxis().set_visible(False)


    ax[1,1].barh(['roasting_level'],[roasting_level],color='lightblue')
    ax[1,1].bar_label(ax[1, 1].containers[0],label_type = 'center',fontsize=60)


    if os.path.exists(fpath):
        os.remove(fpath)
    else:
        pass
    plt.savefig(fpath)
    plt.close()
def Save_image_gallerry(image_gallery_dict,fpath = 'D:/one_color_rev1.jpg'):


    ncols = 5
    nrows = len(image_gallery_dict)  % ncols

    fig, ax = plt.subplots(nrows, ncols, figsize=(20, 10))

    # for key in image_dict:
    i = 0
    for key in image_gallery_dict:

        coorx, coory = divmod(i,ncols)[0],divmod(i,ncols)[1]
        ax[coorx,coory].imshow(image_gallery_dict[key])
        ax[coorx,coory].set_title(key)
        ax[coorx,coory].axis('on')
        ax[coorx,coory].axes.get_xaxis().set_visible(False)
        ax[coorx,coory].axes.get_yaxis().set_visible(False)
        i += 1

    if os.path.exists(fpath):
        os.remove(fpath)
    else:
        pass
    plt.savefig(fpath)
    plt.close()




def Make_text_to_image_patch(input_text):
    input_text = str(input_text)
    font = cv2.FONT_HERSHEY_SIMPLEX
    xsize, ysize = 1000, 1000
    virtual_img = np.ones((xsize, ysize, 3), np.uint8)
    virtual_img *= 255
    y, x = int(xsize * 0.6), int(ysize * 0.25)
    font_scale = 10
    thickness = int(font_scale * 2)
    cv2.putText(virtual_img, input_text, (x, y), font, font_scale, (0, 0, 0), thickness, cv2.LINE_AA)
    return virtual_img


def Extract_palette_and_counts_by_kmeans(image_rgb, n_colors):
    'k-means'
    pixels = np.float32(image_rgb.reshape(-1, 3))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS
    _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)
    "dominant color"
    dominant = palette[np.argmax(counts)]
    return  palette ,counts

# [38.66482911, 32.69018743, 28.06174201]
# [44.69790518, 34.67916207, 26.99558986]
def Extact_distance_from_brown_color_map(target_rgb =[38.66482911, 32.69018743, 28.06174201]):
    brown_color_map_hexa_code = ['#f7f5f2','#f4f1ec','#f1ede7','#eee9e2','#ebe5dd',
                                 '#e8e1d8','#e5ddd3','#e2d9cd','#dfd5c8','#dcd1c3',
                                 '#d9cdbe','#d6c9b9','#d3c5b4','#d0c1ae','#cdbda9',
                                 '#cab9a4','#c7b59f','#c4b19a','#c1ad95','#bea990',
                                 '#bba58a','#b8a185','#b59d80','#b2997b','#af9576',
                                 '#ac9171','#a98d6b','#a68966','#a38561','#a0815c',
                                 '#9a7c59','#957856','#907453','#8b7050','#866c4d',
                                 '#81684a','#7b6347','#765f44','#715b41','#6c573e',
                                 '#67533b','#624f38','#5c4a35','#574632','#52422f',
                                 '#4d3e2c','#483a29','#433626','#3d3123','#382d20',
                                 '#33291d','#2e251a','#292117','#241d14','#1e1811',
                                 '#19140e','#14100b','#0f0c08','#0a0805','#050402']

    brown_color_map_hexa_code = [val.upper()[1:] if val.upper().find('#') == 0 else val.upper()
                                 for val in brown_color_map_hexa_code ]
    brown_color_map_rgb_code = [[int(val[:2],base=16),int(val[2:4],base=16),int(val[4:6],base=16)] for val in brown_color_map_hexa_code]

    val=brown_color_map_rgb_code[-1]
    distance_list = [np.sqrt((val[0]-target_rgb[0])**2+(val[1]-target_rgb[1])**2+(val[2]-target_rgb[2])**2) for val in brown_color_map_rgb_code]
    index_min = np.argmin(distance_list)
    matched_brown_color_rgb = brown_color_map_rgb_code[index_min]
    color_distance_level = round((index_min +1)/60 *100,1)  # first value is 0, convert 100%

    return color_distance_level

def Color_leveler(fpath_input_image, n_colors, background_remove,circle_crop, resize_ratio=0.3):

    image_rgb_origin, image_rgb_remove_bg = Remove_background_image(fpath_input_image)

    if background_remove:
        image_rgb = image_rgb_remove_bg.copy()
    else:
        image_rgb = image_rgb_origin.copy()


    #
    # image_rgb_origin = Load_image_with_cv2(fpath_input_image)
    # image_rgb = image_rgb_origin.copy()
    # image_rgb = cv2.imread(fpath_input_image)
    # image_rgb = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2RGB)
    "Capture circle and crop it"
    if circle_crop:


        minRadius = int(np.min([image_rgb.shape[0] / 2, image_rgb.shape[1] / 2]) * 0.7)  # 0.7 is hyperparameter
        maxRadius = int(np.min([image_rgb.shape[0] / 2, image_rgb.shape[1] / 2]) * 1.0)  # 1.0 is hyperparameter
        minDist = int(minRadius * 0.7)  # 0.7 is hyperparameter
        crop_ratio = 0.6  # # 0.6 is hyperparameter
        cropped_image_rgb, image_circle_detected = Crop_circle_area(image_rgb, minDist=minDist, minRadius=minRadius,
                                                                    maxRadius=maxRadius, crop_ratio=crop_ratio)
        cropped_image_rgb = Change_pixel_black_to_white(cropped_image_rgb)
        image_rgb = cropped_image_rgb.copy()
    else:
        cropped_image_rgb = np.ones((image_rgb.shape[0],image_rgb.shape[1],3), dtype=np.uint8)
        cropped_image_rgb *= 255
        pass

    "simple average patch"
    simple_average_palette = image_rgb.mean(axis=0).mean(axis=0)
    simple_avg_patch = np.ones(shape=image_rgb.shape, dtype=np.uint8) * np.uint8(simple_average_palette)

    "k-means color"
    resize_x, resize_y = int(image_rgb.shape[0] * resize_ratio), int(image_rgb.shape[1] * resize_ratio)
    image_rgb = cv2.resize(image_rgb, dsize=(resize_x, resize_y), interpolation=cv2.INTER_CUBIC)

    print(f'resize ratio is {resize_ratio}, resized image size shape is {image_rgb.shape}')

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
        kmeans_patch_del_bg[rows_del_bg[i]:rows_del_bg[i + 1], :, :] += np.uint8(palette_del_bg[indices_del_bg[i]])
    'present color'
    present_color_palette = kmeans_patch_del_bg.mean(axis=0).mean(axis=0)
    # present_color_palette = palette_del_bg[indices_del_bg[0]]
    present_color_patch = np.ones(shape=image_rgb.shape, dtype=np.uint8) * np.uint8(present_color_palette)

    if background_remove and circle_crop:
        selected_color_palette = present_color_patch.copy()
        selected_color_patch =  present_color_patch.copy()
    elif not background_remove and circle_crop:
        selected_color_palette = present_color_patch.copy()
        selected_color_patch = present_color_patch.copy()
    else:
        selected_color_palette = simple_average_palette.copy()
        selected_color_patch = simple_avg_patch.copy()
    # roasting_level_float = Extact_distance_from_brown_color_map(list(selected_color_palette))

    "weighted average"
    weighted_average_level = 0
    tot = sum(counts_del_bg)
    for indice in indices_del_bg:
        roasting_level_float = Extact_distance_from_brown_color_map(list(palette_del_bg[indice]))
        weighted_average_level += roasting_level_float * counts_del_bg[indice]/tot
        weighted_average_level = round(weighted_average_level,1)

    roasting_level_float = weighted_average_level.copy()


    roasting_level_patch = Make_text_to_image_patch(roasting_level_float)

    image_gallery_dict = {'Original image': image_rgb_origin,
                          'Present color': selected_color_patch,
                          'Dominant colors after BG del': kmeans_patch_del_bg,
                          'K-means colors': kmeans_patch,
                          'Simple average color': simple_avg_patch,
                          'Cropped image': cropped_image_rgb,
                          'Roasting level': roasting_level_patch
                          }

    return image_gallery_dict, roasting_level_float



def main_president_color_kmeans_oneshot():
    'present color by k-means '


    path_image_folder = 'D:/cafe7984/coffee_color_roasting_source'
    path_output_folder = 'D:/cafe7984/coffee_color_roasting_output'

    n_colors = 5
    background_remove = True
    circle_crop = True

    os.makedirs(path_image_folder, exist_ok=True)
    os.makedirs(path_output_folder,exist_ok=True)

    input_image_file_list = glob.glob(os.path.join(path_image_folder, '*.jpg'))

    for fpath_input_image in input_image_file_list:
        # fpath_input_image = input_image_file_list[7]
        try:
            ratio = 30
            resize_ratio = round(ratio * 0.01, 1)
            image_gallery_dict, roasting_level_flot = Color_leveler(fpath_input_image, n_colors, background_remove, circle_crop,resize_ratio)
            output_suffix = '_roast_level[bg_remove][circle_crop]' + '~' + str(ratio) + '~' + '(' + str(
                roasting_level_flot) + ').jpg'
            if background_remove:
                pass

            else:
                output_suffix = output_suffix.replace('[bg_remove]', '')

            if circle_crop:
                pass
            else:
                output_suffix = output_suffix.replace('[circle_crop]', '')

            fpath_output_image = os.path.join(path_output_folder,
                                              fpath_input_image.replace('.jpg', output_suffix).replace('\\', '/').
                                              split('/')[-1]).replace('\\', '/')
            Save_image_gallerry(image_gallery_dict, fpath=fpath_output_image)
        except:
            pass


        # fpath_input_image = input_image_file_list[2]
        # for ratio in range(10,110,10):
        #
        #     try:
        #
        #         resize_ratio = round(ratio * 0.01,1)
        #         image_gallery_dict, roasting_level_int = Color_leveler(fpath_input_image, n_colors,background_remove, resize_ratio)
        #         output_suffix = '_roast_level[bg_remove]' + '~' + str(ratio) + '~' + '(' + str(
        #             int(roasting_level_int)) + ').jpg'
        #         if background_remove:
        #             pass
        #
        #         else:
        #             output_suffix = output_suffix.replace('[bg_remove]','')
        #
        #         fpath_output_image = os.path.join(path_output_folder,
        #                                           fpath_input_image.replace('.jpg', output_suffix).replace('\\', '/').
        #                                           split('/')[-1]).replace('\\', '/')
        #         Save_image_gallerry(image_gallery_dict, fpath=fpath_output_image)
        #     except:
        #         pass



if __name__ == "__main__":
    main_president_color_kmeans_oneshot()

    #
    # image_rgb_origin, image_rgb_remove_bg = Remove_background_image(fpath_input_image)
    # size_ratio = 0.5
    # resize_x , resize_y = int(image_rgb_origin.shape[0]*size_ratio),int(image_rgb_origin.shape[1]*size_ratio)
    # res = cv2.resize(image_rgb_origin, dsize=(resize_x,resize_y), interpolation=cv2.INTER_CUBIC)
    #
    #
    # # main_president_color_kmeans_oneshot(n_colors=5,background_remove = True)
    #
    #
    # # image = input_image.copy()
    # # image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
    # # image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    # # image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    # radius_con_lst = [round(f * 0.1,1) for f in range(1,11,1)]
    # dist_con_lst =[round(f * 0.1,1) for f in range(1,11,1)]
    # crop_ratio_lst = [round(f * 0.1,1) for f in range(1,11,1)]
    #
    # for radius in radius_con_lst:
    #     for dist in dist_con_lst:
    #         for crop in crop_ratio_lst:
    #             fpath_input_image = 'D:/cafe7984/coffee_color_roasting_source\\BRZ_181_231216 (1).jpg'
    #             image_rgb_origin, image_rgb_remove_bg = Remove_background_image(fpath_input_image)
    #             image = image_rgb_origin.copy()
    #
    #             minRadius = np.min([int(image.shape[0] / 2 * radius), int(image.shape[1] / 2 * radius)])
    #             minDist = int(minRadius * dist)
    #             crop_ratio = crop
    #
    #             cropped_image, image_origin = Crop_circle_area(image,minDist,minRadius ,crop_ratio)
    #
    #             image_origin = cv2.cvtColor(image_origin, cv2.COLOR_RGB2BGR)
    #             fpath_image = os.path.join('D:/cafe7984/coffee_color_roasting_source','_'.join(['image',str(radius),str(dist),str(crop)])+'.jpg')
    #             if os.path.exists(fpath_image):
    #                 os.remove(fpath_image)
    #             else:
    #                 pass
    #             cv2.imwrite(fpath_image, image_origin)
    #
    #             cropped_image = cv2.cvtColor(cropped_image,cv2.COLOR_RGB2BGR)
    #             fpath_cropped_image = os.path.join('D:/cafe7984/coffee_color_roasting_source', '_'.join(['image', str(radius), str(dist), str(crop)])+'_cropped.jpg')
    #             if os.path.exists(fpath_cropped_image):
    #                 os.remove(fpath_cropped_image)
    #             else:
    #                 pass
    #             cv2.imwrite(fpath_cropped_image, cropped_image)


    fpath_input_image = 'D:/cafe7984/coffee_color_roasting_source\\BRZ_181_231216 (1).jpg'
    # input_image = cv2.imread(fpath_input_image)
    # Convert the image to HSV color space
    input_image_origin, input_image = Remove_background_image(fpath_input_image)
    input_image_origin = cv2.cvtColor(input_image_origin, cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(input_image_origin, cv2.COLOR_BGR2HSV)

    # Adjust the value (brightness) channel
    brightness_factor = 1.5  # You can adjust this factor as needed
    hsv[:, :, 2] = np.clip(hsv[:, :, 2] * brightness_factor, 0, 255)

    # Convert the image back to BGR color space
    brightened_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # add_light = 10
    for add_light in range(0,60):
        # add_light = 50
        input_image_origin, input_image = Remove_background_image(fpath_input_image)

        # hsv = cv2.cvtColor(input_image, cv2.COLOR_RGB2BGR)
        hsv = cv2.cvtColor(input_image_origin, cv2.COLOR_RGB2HSV)

        # Adjust the value (brightness) channel
        brightness_factor = 1 + add_light*0.01  # You can adjust this factor as needed
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * brightness_factor, 0, 255)

        # Convert the image back to BGR color space
        brightened_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        fpath_out_image = fpath_input_image.replace('\\','/').split('.jpg')[0]+'~'+ 'addlight('+ str(add_light) + ')' + '.jpg'
        cv2.imwrite(fpath_out_image,brightened_image)


