import os
import json
import cv2
import shutil
import re
import numpy as np

from xpinyin import Pinyin
p = Pinyin()
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QThread

class Split_Gongwei(QThread):

    _signal = QtCore.pyqtSignal(str)

    def __init__(self, input_dir=None, output_dir=None, station_list=None):
        super(Split_Gongwei, self).__init__()
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.station_list = station_list

    def log_emit(self,*args):
        self._signal.emit(str(*args))

    def split_gongwei(self, input_dir=None, output_dir=None, station_list=None):

        station_list1 = station_list.strip().split(',')

        for folder in station_list1:
            save_folder = os.path.join(output_dir, folder.strip(' '))
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)

        for root, dir, file in os.walk(input_dir):
            for name in file:
                image_path = root + "\\" + name
                if name.endswith('bmp') or name.endswith('jpg'):
                    match = [re.compile(folder.strip(' ')).findall(name)[0] for folder in station_list1 if
                             re.compile(folder.strip(' ')).findall(name) != []]
                    if match != []:
                        save_folder = os.path.join(output_dir, match[0])
                        shutil.copy(image_path, os.path.join(save_folder, name))
                        str0 = os.path.join(save_folder, name).replace("/", "\\")
                        self.log_emit(f'分类已完成，保存至 {str0}')

        self.log_emit("————————————————")
        self.log_emit(">>完成>>")
        self.log_emit(">>已在选择图片目录下完成分图>>")

    def run(self):
        self.split_gongwei(self.input_dir, self.output_dir, self.station_list)

class Average_Image_Folder(QThread):

    _signal = QtCore.pyqtSignal(str)

    def __init__(self, file_path=None, save_path=None, cut_num0=None):
        super(Average_Image_Folder, self).__init__()
        self.file_path = file_path
        self.save_path = save_path
        self.cut_num0 = cut_num0

    def log_emit(self,*args):
        self._signal.emit(str(*args))

    def average_image_folder(self, file_path, save_path, cut_num0):

        cut_num = int(cut_num0)
        n = 0

        for root, dirs, files in os.walk(file_path):
            for file in files:
                if file.endswith(".jpg") or file.endswith(".bmp"):

                    each_save_folder = str(n // cut_num)
                    if not os.path.exists(os.path.join(save_path, each_save_folder)):
                        os.mkdir(os.path.join(save_path, each_save_folder))
                    shutil.copy(os.path.join(file_path, file), os.path.join(save_path, each_save_folder, file))

                    str0 = os.path.join(save_path, each_save_folder, file)
                    str1 = str0.replace("/", "\\")
                    self.log_emit(f'{file}\n分类已完成，保存至\n{str1}')
                    n += 1

        self.log_emit("————————————————")
        self.log_emit(">>完成>>")
        self.log_emit(">>已在选择图片目录下完成分图>>")

    def run(self):
        self.average_image_folder(self.file_path, self.save_path, self.cut_num0)

class Rename_Image_Folder(QThread):

    _signal = QtCore.pyqtSignal(str)

    def __init__(self, file_path=None):
        super(Rename_Image_Folder, self).__init__()
        self.file_path = file_path

    def log_emit(self,*args):
        self._signal.emit(str(*args))

    def rename_img(self, file_path):
        for root, dirs, files in os.walk(file_path):
            for file in files:
                if file.endswith('jpg') or file.endswith('bmp'):
                    b = root.split("\\")
                    src = os.path.join(root, file)
                    dst = os.path.join(root, str(b[-1]) + "_" + file)
                    os.rename(src, dst)

                    self.log_emit(f'{file}重命名为{str(b[-1]) + "_" + file}')

        self.log_emit("————————————————")
        self.log_emit(">>完成>>")
        self.log_emit(">>已在选择图片目录下完成转换>>")

    def run(self):
        self.rename_img(self.file_path)

class Cut_Image(QThread):

    _signal = QtCore.pyqtSignal(str)

    def __init__(self, input_dir=None, output_dir=None, mode=None, h_range1=None, w_range1=None):
        super(Cut_Image, self).__init__()
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.mode = mode
        self.h_range1 = h_range1
        self.w_range1 = w_range1

    def log_emit(self,*args):
        self._signal.emit(str(*args))

    def cut_image(self, input_dir, output_dir, mode, h_range1, w_range1):

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for root, dirs, files in os.walk(input_dir):
            for f in files:
                if f.endswith(".bmp") or f.endswith(".jpg"):
                    # b = root.split("\\")
                    self.log_emit(f'正在处理{os.path.join(root, f)}')
                    img1 = Image.open(os.path.join(root, f))
                    img_format = img1.getbands()
                    W, H = img1.size

                    if len(img_format) == 1:
                        decode_mode = cv2.IMREAD_GRAYSCALE
                    if len(img_format) == 3:
                        decode_mode = cv2.IMREAD_COLOR
                    img = cv2.imdecode(np.fromfile(os.path.join(root, f), dtype=np.uint8), decode_mode)

                    if mode == '沿高方向':
                        h = h_range1.strip().split(',')
                        h_range = [int(i) for i in h]
                        for y in range(len(h_range) - 1):
                            image_split = img[h_range[y]: h_range[y + 1]]
                            save_path1 = os.path.join(output_dir, f[:-4] + "_" + str(y) + "_" + str(0) + '.jpg')
                            cv2.imencode('.jpg', image_split, [int(cv2.IMWRITE_JPEG_QUALITY), 100])[1].tofile(
                                save_path1)
                            new_name = f[:-4] + "_" + str(y) + "_" + str(0) + '.jpg'

                            self.log_emit(new_name)

                    if mode == '沿宽方向':
                        w = w_range1.strip().split(',')
                        w_range = [int(j) for j in w]
                        for x in range(len(w_range) - 1):
                            image_split = img[0:H + 1, w_range[x]: w_range[x + 1]]
                            save_path1 = os.path.join(output_dir, f[:-4] + "_" + str(0) + "_" + str(x) + '.jpg')
                            cv2.imencode('.jpg', image_split, [int(cv2.IMWRITE_JPEG_QUALITY), 100])[1].tofile(
                                save_path1)
                            new_name = f[:-4] + "_" + str(y) + "_" + str(0) + '.jpg'

                            self.log_emit(new_name)

                    if mode == '沿宽高方向':
                        h = h_range1.strip().split(',')
                        h_range = [int(i) for i in h]
                        w = w_range1.strip().split(',')
                        w_range = [int(j) for j in w]
                        for y in range(len(h_range) - 1):
                            for x in range(len(w_range) - 1):
                                image_split = img[h_range[y]:h_range[y + 1], w_range[x]:w_range[x + 1]]
                                save_path1 = os.path.join(output_dir, f[:-4] + "_" + str(y) + "_" + str(x) + '.jpg')
                                cv2.imencode('.jpg', image_split, [int(cv2.IMWRITE_JPEG_QUALITY), 100])[1].tofile(
                                    save_path1)
                                new_name = f[:-4] + "_" + str(y) + "_" + str(0) + '.jpg'

                                self.log_emit(new_name)

        self.log_emit("————————————————")
        self.log_emit(">>完成>>")
        self.log_emit(">>已在选择图片目录下完成分图>>")

    def run(self):
        self.cut_image(self.input_dir, self.output_dir, self.mode, self.h_range1, self.w_range1)

class Rename_Hanzi_Image(QThread):

    _signal = QtCore.pyqtSignal(str)

    def __init__(self, file_path=None, save_folder=None, fix_project=None):
        super(Rename_Hanzi_Image, self).__init__()
        self.file_path = file_path
        self.save_folder = save_folder
        self.fix_project = fix_project

    def log_emit(self,*args):
        self._signal.emit(str(*args))

    def rename_hanzi_img(self, file_path, save_folder, fix_project):
        for root, dirs, files in os.walk(file_path):
            for file in files:
                if file.endswith('jpg') or file.endswith('bmp'):
                    if save_folder == True:
                        b = root.split("\\")
                        new_name = str(b[-1] + '_' + file)
                        result = p.get_initials(new_name, '').replace('，', ',')
                        src = os.path.join(root, file)
                        dst = os.path.join(root, result)
                        os.rename(src, dst)
                        self.log_emit(f'{file}重命名为{result}')
                    else:
                        result = p.get_initials(file, '').replace('，', ',')
                        src = os.path.join(root, file)
                        dst = os.path.join(root, result)
                        os.rename(src, dst)
                        self.log_emit(f'{file}重命名为{result}')

                if fix_project == True:
                    if file == 'via_project.json':
                        model_via_img_metadata_new = {}
                        model_via_project = json.load(open(os.path.join(root, file), 'rb'))
                        model_via_img_metadata = model_via_project["_via_img_metadata"]
                        for key, single_img_inf in model_via_img_metadata.items():
                            if save_folder == True:

                                img_name = single_img_inf["filename"]
                                b = root.split("\\")
                                new_name = str(b[-1] + '_' + img_name)
                                result = p.get_initials(new_name, '')
                                single_img_inf["filename"] = result

                                result1 = key.replace(img_name, result)
                                model_via_img_metadata_new[result1] = single_img_inf

                            else:
                                result = p.get_initials(key, '')

                                img_name = single_img_inf["filename"]
                                result1 = p.get_initials(img_name, '')
                                single_img_inf["filename"] = result1

                                model_via_img_metadata_new[result] = single_img_inf

                        model_via_project["_via_img_metadata"] = model_via_img_metadata_new

                        with open(os.path.join(root, 'via_project_rename.json'), 'w') as f:
                            f.write(json.dumps(model_via_project))

        self.log_emit("————————————————")
        self.log_emit(">>完成>>")
        self.log_emit(">>已在选择图片目录下完成转换>>")

    def run(self):
        self.rename_hanzi_img(self.file_path, self.save_folder, self.fix_project)