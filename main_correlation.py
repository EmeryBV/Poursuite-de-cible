# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import cv2
import numpy as np
import glob
import os
import math

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    DIR = './Ghost4'
    path = './Ghost4/GITS00'
    filename = './Ghost4/GITS001.bmp'
    weight, height = 640, 352
    numberOfFile = len([name for name in os.listdir(DIR)])
    pointX_start, pointY_start = 220, 260
    pointX_end, pointY_end = 240, 280

    # pointX_start, pointY_start = 410, 140
    # pointX_end, pointY_end = 430, 160

    # pointX_start, pointY_start = 400, 120
    # pointX_end, pointY_end = 420, 140

    lenghtX = pointX_end - pointX_start
    lenghtY = pointY_end - pointY_start
    # 1er image
    img = cv2.imread(filename)
    start_point = (pointX_start - 1, pointY_start - 1)
    end_point = (pointX_end + 1, pointY_end + 1)
    colorRed = (0, 0, 255)
    colorBlue = (255, 0, 0)
    colorGreen = (0, 255, 0)
    thickness = 1

    pixelImage1 = []
    for y in range(pointY_start, pointY_end + 1):
        for x in range(pointX_start, pointX_end + 1):
            # print(x)
            pixelImage1.append(img[y, x])
    pixelImage2 = []

    img = cv2.rectangle(img, start_point, end_point, colorRed, thickness)
    # cv2.imshow('Rectangle', img)

    img_array = [img]
    for i in range(2, numberOfFile - 1):
        print("\nTraitement image " + str(i))
        if (i > 9):
            path = './Ghost4/GITS0'
        if i != 2:
            img = img2
        filename = path + str(i) + '.bmp'
        img2 = cv2.imread(filename)

        height, width, layers = img.shape
        size = (width, height)

        for y in range(pointY_start, pointY_end + 1):
            for x in range(pointX_start, pointX_end + 1):
                pixelImage2.append(img2[y, x])

        ok = False
        u_amplitude = 10
        v_amplitude = 10

        searchX_start, searchY_start = 0, 0
        searchX_end, searchY_end = 0, 0

        while not ok:
            if pointX_start - u_amplitude > 0 and pointX_end + u_amplitude < weight \
                    and pointY_start - v_amplitude > 0 and pointY_end + v_amplitude < height:
                searchX_start = pointX_start - u_amplitude
                searchY_start = pointY_start - v_amplitude
                searchX_end = pointX_end + u_amplitude
                searchY_end = pointY_end + v_amplitude
                ok = True
            else:
                u_amplitude -= 1
                v_amplitude -= 1

        SSD = 0

        offsetX = 0
        offsetY = 0
        saveOffsetX = 0
        saveOffsetY = 0
        start_point = (pointX_start - 1, pointY_start - 1)
        end_point = (pointX_end + 1, pointY_end + 1)

        for offsetY in range(-v_amplitude, v_amplitude + 1):
            for offsetX in range(-u_amplitude, u_amplitude + 1):
                val = 0.0

                moyenneImg1 = 0
                moyenneImg2 = 0
                for y in range(0, lenghtY + 1):
                    for x in range(0, lenghtX + 1):
                        moyenneImg1 += img[y, x][0]
                        moyenneImg2 += img2[searchY_start + y + offsetY + v_amplitude, searchX_start
                                            + x + offsetX + u_amplitude][0]

                moyenneImg1 = moyenneImg1 / (lenghtX * lenghtY)
                moyenneImg2 = moyenneImg2 / (lenghtX * lenghtY)

                sigmaImg1 = 0
                sigmaImg2 = 0
                for y in range(0, lenghtY + 1):
                    for x in range(0, lenghtX + 1):
                        sigmaImg1 += ((img[y, x] - moyenneImg1)[0] ** 2)
                        sigmaImg2 += ((img2[searchY_start + y + offsetY + v_amplitude, searchX_start
                                            + x + offsetX + u_amplitude] - moyenneImg2)[0] ** 2)
                        sigmaImg1 = sigmaImg1 / (lenghtX * lenghtY)
                        sigmaImg2 = sigmaImg2 / (lenghtX * lenghtY)

                for v in range(0, lenghtY + 1):
                    for u in range(0, lenghtX + 1):
                        # print(img2[pointY_start + v, pointX_start + u][0])
                        # print(img[ searchY_start + v + offsetY + v_amplitude, searchX_start + u + offsetX + u_amplitude][0])
                        # print( searchY_start + v + offsetY + v_amplitude)
                        # print(searchX_start + u + offsetX + u_amplitude)

                        val = val + (sigmaImg1 * sigmaImg2)/math.sqrt(sigmaImg1*sigmaImg2)
                        # val = val + ((img[v, u] - moyenneImg1)[0] * (img2[searchY_start + v + offsetY + v_amplitude, searchX_start
                        #                     + u + offsetX + u_amplitude] - moyenneImg2)[0])/math.sqrt(sigmaImg1*sigmaImg2)
                        # print(val)
                # input("Press Enter to continue...")
                val = val / (lenghtX * lenghtY)
                # print('offsetY = '+str(offsetY) +' offsetX = ' + str(offsetX) + ' val= '+ str(val) + 'SSD actual ' + str(SAD))
                if val > SSD:
                    SSD = val
                    saveOffsetX = -offsetX
                    saveOffsetY = -offsetY

        # print('MIN : offsetY = ' + str(saveOffsetX) + ' offsetX = ' + str(saveOffsetY) + ' val= ' + str(SAD))
        pointX_start = pointX_start + saveOffsetX
        pointY_start = pointY_start + saveOffsetY

        pointX_end = pointX_end + saveOffsetX
        pointY_end = pointY_end + saveOffsetY

        start_point_bis = (pointX_start - 1, pointY_start - 1)
        end_point_bis = (pointX_end + 1, pointY_end + 1)

        start_point_Area = (
            searchX_start - 1, searchY_start - 1)
        end_point_Area = (searchX_end + 1, searchY_end + 1)

        img2 = cv2.rectangle(img2, start_point, end_point, colorRed, 1)
        # img2 = cv2.rectangle(img2, start_point_Area, end_point_Area, colorGreen, 1)

        # img2 = cv2.rectangle(img2, start_point_bis, end_point_bis, colorBlue, 1)

        img_array.append(img2)
        # cv2.imshow('image', img)
        # cv2.imshow('image2', img2)
        # cv2.waitKey(0)

    out = cv2.VideoWriter('Poursuite de cible.avi', cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
    for i in range(len(img_array) - 1):
        out.write(img_array[i])
    out.release()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
