import os
import shutil
import re


# def station_spilt(file_path, save_path, station_list):
#     for station in station_list:
#         print(station)
#         for file in os.listdir(file_path):
#             each_img_dir = os.path.join(file_path, file)
#             for each_img in os.listdir(each_img_dir):
#                 each_img_path = os.path.join(each_img_dir, each_img)
#                 print(each_img_path)
#                 for ecah_name in os.listdir(each_img_dir):
#                     print(ecah_name)
#                     if ecah_name.endswith(".jpg"):
#                         if station in ecah_name:
#                             save_img_path = os.path.join(save_path, station)
#                             if not os.path.exists(save_img_path):
#                                 os.mkdir(save_img_path)
#                             shutil.copy(os.path.join(each_img_dir, ecah_name), os.path.join(save_img_path, ecah_name))
#                             print(ecah_name)

def split_gongwei(input_dir, output_dir, station_list):

    station_list1 = station_list.strip().split(',')

    for folder in station_list1:
        save_folder = os.path.join(output_dir, folder)
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

    for root, dir, file in os.walk(input_dir):
        for name in file:
            image_path = root + "\\" + name
            if name.endswith('bmp') or name.endswith('jpg'):
                match = [re.compile(folder).findall(name)[0] for folder in station_list1 if
                         re.compile(folder).findall(name) != []]
                if match != []:
                    save_folder = os.path.join(save_path, match[0])
                    shutil.copy(image_path, os.path.join(save_folder, name))
                    print(os.path.join(save_folder, name))


if __name__ in "__main__":
    file_path = r"E:\Desktop\qietu_test"
    save_path = r"E:\Desktop\qietu_save"
    station_list = ["Camera1_0", "Camera3_0", "Camera41_0", "Camera42_0", "Camera43_0", "Camera51_0", "Camera52_0",
                    "Camera53_0"]
    # station_list = ["01_001","02_001"]
    split_gongwei(file_path, save_path, station_list)

    # Camera1_0, Camera3_0, Camera41_0, Camera42_0, Camera43_0, Camera51_0, Camera52_0, Camera53_0
