from config.config import data
import lib.adb_command as adb
import lib.api as api
import cv2 as cv2
import time
from PIL import Image
import matplotlib as plt
import lib.find as f
# import os
# import plugins.Turn as Turn
# import plugins.auto_battle as auto
# import decisions.decision_1 as de1
import plugins.active as active
import plugins.wilderness as wilderness
import plugins.mission as mission
import numpy as np
import plugins.path as path
#import config.config as config
#import lib.ppocr as pp
import lib.const as const

def show(img, name):
    cv2.imshow(name, img)
def mask_coloring(mask):
    expected_color = (255, 255, 255)
    color_mask = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)
    color_mask[mask == 255.0, :] = expected_color
    plt.imshow(color_mask)
def ff():
    image = cv2.imread("cache/screenshot.png")
    black = np.zeros([0, 0, 0])
    max_width = 1600
    max_height = 900
    # cv2.rectangle(image, (0, 0), (max_width, 270), black, -1)
    # cv2.rectangle(image, (0, 270 + 50), (max_width, 650), black, -1)
    # cv2.rectangle(image, (0, 650 + 50), (max_width, max_height), black, -1)
    # std = np.std(image, axis=2)
    #
    #
    # image[std > 1] = [0, 0, 0]
    point = f.find(const.IMAGE_TEAM_1)
    cv2.circle(image, (int(point[0]), int(point[1])), int(10),
               (0, 0, 255), 3)
    point = f.find(const.IMAGE_TEAM_2)
    cv2.circle(image, (int(point[0]), int(point[1])), int(10),
               (0, 0, 255), 3)
    point = f.find(const.IMAGE_TEAM_3)
    cv2.circle(image, (int(point[0]), int(point[1])), int(10),
               (0, 0, 255), 3)
    point = f.find(const.IMAGE_TEAM_4)
    cv2.circle(image, (int(point[0]), int(point[1])), int(10),
               (0, 0, 255), 3)
    # method 2, use np
    # mask = np.repeat(std[:,:,np.newaxis], image.shape[2], axis=2) > 1
    # modified = np.where(mask, np.array([0,0,0], dtype=np.uint8), image)
    show(image, "image")
    cv2.waitKey()
    cv2.destroyAllWindows()
    return
    h, w, c = image.shape
    ri = image.reshape(h, w, c)
    print(image.shape)
    print(ri.shape)
    np.where(np.std(image[:, :])<0.5)
    mask_coloring(image)
    np.where()

    # loc = np.where(image != 255)
    # np.all(image[loc], (0, 0, 0))
    # show(image, "image")
    return


    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    show(gray, "gray")

    blurred = cv2.GaussianBlur(gray, (11, 11), 0)
    show(blurred, "blurred")

    thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)[1]
    show(thresh, "thresh")
    cv2.waitKey()
    cv2.destroyAllWindows()
    return


    # converting to LAB color space
    lab = cv.cvtColor(image, cv.COLOR_BGR2LAB)
    l_channel, a, b = cv.split(lab)

    # Applying CLAHE to L-channel
    # feel free to try different values for the limit and grid size:
    clahe = cv.createCLAHE(clipLimit=20.0, tileGridSize=(8, 8))
    cl = clahe.apply(l_channel)

    # merge the CLAHE enhanced L-channel with the a and b channel
    limg = cv.merge((cl, a, b))

    # Converting image from LAB Color model to BGR color spcae
    enhanced_img = cv.cvtColor(limg, cv.COLOR_LAB2BGR)
    cv.imshow('enhanced_img', enhanced_img)

    
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    cv.imwrite("cache/" + str(time.time()) + "gray.png", gray)

    sobel = cv.Sobel(image, cv.CV_64F, 1, 0, ksize=3)
    show(sobel, "Sobel")

    scharr = cv.Scharr(gray, cv.CV_64F, 1, 0);
    show(scharr, "Scharr")

    laplacian = cv.Laplacian(gray, cv.CV_64F)
    show(laplacian, "Laplacian")

    cv.waitKey()
    cv.destroyAllWindows()

ff()

# print('开始初始化adb')
# device = adb.is_device_connected()
# if not device:
#     print("Error: 未连接设备，请回看上面的错误信息")
#     exit(1)
# #检测游戏是否运行，如果没有运行就启动游戏
# adb.is_game_on()
# #进入主菜单
# path.to_menu()
# print(pp.ocr_cn('cache/screenshot.png'))
# #active.Auto_Active(LEVEL_6,)
# adb.touch(f.find('imgs/enter_the_show'))
# print("正在进入主会场")
# time.sleep(1)

# mission.mission_start()
# wilderness.wild_start()
# img = cv.imread('cache/huoli.png')
# gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# res, img2 = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)
# cv.imwrite('cache/binary.png', img2)
# print(pp.ocr_xy('cache/binary.png','12'))









"""
def match_icon(image, icon):
    image = cv.imread(image)
    # 读取透明背景的图标，并转换成无符号8位整数类型
    template = cv.imread(icon,cv.IMREAD_UNCHANGED)
    template = np.uint8(template)

    # 分离alpha通道，作为模板匹配的掩码
    channels = cv.split(template)
    mask = np.array(channels[3])

    # 根据alpha通道的值，设置掩码的值
    mask[channels[3] == 0] = 1
    mask[channels[3] == 100] = 0

    # 使用cv2.TM_SQDIFF方法进行模板匹配，并传入掩码参数
    method = cv.TM_SQDIFF  

    # 初始化一个空列表，用于存放每个通道和灰度图像的匹配结果
    results = []

    # 对每个通道和灰度图像进行模板匹配，并把结果添加到列表中
    for i in range(4):
    # 如果是第四个通道，就把图像转换成灰度图像
        if i == 3:
            img = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
            temp = cv.cvtColor(template, cv.COLOR_BGR2GRAY)
        # 否则就取对应的通道
        else:
            img = image[:,:,i]
            temp = template[:,:,i]
        # 进行模板匹配，并获取最小值、最大值、最小位置和最大位置
        result = cv.matchTemplate(img, temp, method, mask=mask)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        # 计算目标中心点的坐标
        target_center = (max_loc[0] + temp.shape[1] / 2, max_loc[1] + temp.shape[0] / 2)
        # 把坐标和相似度作为元组添加到列表中
        results.append((target_center, max_val))
        print(max_val,max_loc)
print(match_icon('cache/test.png', 'imgs/go_back_2_alpha.png'))
img = cv.imread("cache/test.png")
img_terminal = cv.imread(f'imgs/go_back_2.png')

# print(img_terminal.shape)
height, width, dep = img_terminal.shape

result = cv.matchTemplate(img, img_terminal, cv.TM_SQDIFF_NORMED)

upper_left = cv.minMaxLoc(result)[2]
img2 = img[upper_left[1]:upper_left[1]+height,
            upper_left[0]:upper_left[0] + width]
lower_right = (upper_left[0]+width, upper_left[1]+height)

avg = (int((upper_left[0]+lower_right[0])/2),
        int((upper_left[1]+lower_right[1])/2),
        f.similar(img_terminal, img2))
print(avg)
"""