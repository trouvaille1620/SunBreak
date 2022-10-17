import os
import cv2
import numpy as np
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None
# import threading

def cut_image(input_dir, output_dir, mode, h_range, w_range):

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for root, dirs, files in os.walk(input_dir):
        for f in files:
            if f.endswith(".bmp") or f.endswith(".jpg"):
                # b = root.split("\\")
                print(os.path.join(root, f))
                img1 = Image.open(os.path.join(root, f))
                img_format = img1.getbands()

                if len(img_format) == 1:
                    decode_mode = cv2.IMREAD_GRAYSCALE
                if len(img_format) == 3:
                    decode_mode = cv2.IMREAD_COLOR
                img = cv2.imdecode(np.fromfile(os.path.join(root, f), dtype=np.uint8), decode_mode)

                if mode == '只切高':
                    for y in range(len(h_range) - 1):
                        image_split = img[h_range[y]: h_range[y + 1]]
                        save_path1 = os.path.join(output_dir, f[:-4] + "_" + str(y) + "_" + str(0) + '.jpg')
                        cv2.imencode('.jpg', image_split, [int(cv2.IMWRITE_JPEG_QUALITY), 100])[1].tofile(save_path1)

                if mode == '只切宽':
                    for x in range(len(w_range) - 1):
                        image_split = img[0:h_range[-1], w_range[x]: w_range[x + 1]]
                        save_path1 = os.path.join(output_dir, f[:-4] + "_" + str(0) + "_" + str(x) + '.jpg')
                        cv2.imencode('.jpg', image_split, [int(cv2.IMWRITE_JPEG_QUALITY), 100])[1].tofile(save_path1)

                if mode == '宽高都切':
                    for y in range(len(h_range) - 1):
                        for x in range(len(w_range) - 1):
                            image_split = img[h_range[y]:h_range[y + 1], w_range[x]:w_range[x + 1]]
                            save_path1 = os.path.join(output_dir, f[:-4] + "_" + str(y) + "_" + str(x) + '.jpg')
                            cv2.imencode('.jpg', image_split, [int(cv2.IMWRITE_JPEG_QUALITY), 100])[1].tofile(
                                save_path1)


if __name__ in "__main__":
    path = r'E:\Desktop\qietu_test\wkw'
    save_path = r'E:\Desktop\pic_test\105'
    # mode = ['只切高', '只切宽', '宽高都切']
    mode = '宽高都切'
    cut_image(path, save_path, mode, [0, 300, 600, 900], [0, 268, 536, 804, 1072, 1340])


# 输入第一次要切图片的宽w和高h，图片的详细信息里是 w*h
# img_h = 25000
# img_w = 16384

# 按标图尺寸确定切几刀，y为高切几刀，x为宽切几刀（一般第一次只按高切，因此x用不到）
# y_range = list(range(0, img_h, img_h // 2))
# y_range.append(img_h)
# x_range = list(range(0, img_w, img_w // 8))
# x_range.append(img_w)
#
# def save_threads(path,save_path1):
#     for root, dirs, files in os.walk(path):
#
#             for f in files:
#                 if f.endswith(".bmp"):
#                     b = root.split("\\")
#                     print(os.path.join(root, f))
#                     img = cv2.imdecode(np.fromfile(os.path.join(root, f), dtype=np.uint8), 0)
#                     # save_folder = os.path.join(save_path, "split")
#                     if not os.path.exists(save_path1):
#                         os.mkdir(save_path1)
#
#                     # print(y_range)
#                     for y in range(len(y_range)-1):
#                         # for x in range(len(x_range)-1):
#                             image_split = img[y_range[y]:y_range[y+1]]
#                             save_path = os.path.join(save_path1, str(b[-1]) + "_" + f[:-4] + "_" + str(y)+ "_"+ str(0) + '.jpg')
#                             print(save_path)
#                             cv2.imencode('.jpg', image_split, [int(cv2.IMWRITE_JPEG_QUALITY), 100])[1].tofile(save_path)

# 图片转存jpg

# 输入第二次要切图片的宽w和高h
# img_h = 12500
# img_w = 16384
#
# # 按标图尺寸确定切几刀，y为高切几刀，x为宽切几刀
# y_range = list(range(0, img_h, img_h // 4))
# y_range.append(img_h)
# x_range = list(range(0, img_w, img_w // 8))
# x_range.append(img_w)
#
# def save_threads1(path):
#     for root, dirs, files in os.walk(path):
#
#         for f in files:
#             if f.endswith(".jpg"):
#                 b = root.split("\\")
#                 print(os.path.join(root, f))
#                 img = cv2.imdecode(np.fromfile(os.path.join(root, f), dtype=np.uint8), 0)
#                 save_folder = os.path.join(path, "split")
#                 if not os.path.exists(save_folder):
#                     os.mkdir(save_folder)
#
#                 # print(y_range)
#                 for y in range(len(y_range)-1):
#                     for x in range(len(x_range)-1):
#                         image_split = img[y_range[y]:y_range[y+1],x_range[x]:x_range[x+1]]
#                         save_path = os.path.join(save_folder, f[:-4] + "_" + str(y)+ "_"+ str(x) + '.jpg')
#                         print(save_path)
#                         cv2.imencode('.jpg', image_split, [int(cv2.IMWRITE_JPEG_QUALITY), 100])[1].tofile(save_path)

# if __name__ == '__main__':
#
#     # save_threads为第一次切图函数，需要输入图片路径和保存路径
#     # save_threads1为第二次切图函数，只需输入图片路径
#     # 运行其中某一函数时需要注释掉另一个函数，包括另一个函数定义宽高的那几行
#
#     # save_threads(r"\\10.10.1.10\研发中心-人工智能部\项目文件\FT210014 威卡威铝板\威卡威取图\B9LS 好板\600    20220402"
#     #              ,r'\\10.10.1.10\研发中心-人工智能部\项目文件\FT210014 威卡威铝板\威卡威取图\B9LS 好板\600    20220402\split')
#
#     save_threads1(r'\\10.10.1.10\研发中心-人工智能部\项目文件\FT210014 威卡威铝板\威卡威取图\C85MU 好板\530   20220317\split')


