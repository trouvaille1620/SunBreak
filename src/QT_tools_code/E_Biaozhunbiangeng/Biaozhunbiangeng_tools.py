import os
import json
import shutil

from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QThread


class Delete_via_label_project(QThread):

    _signal = QtCore.pyqtSignal(str)

    def __init__(self, input_dir=None, label=None):
        super(Delete_via_label_project, self).__init__()
        self.input_dir = input_dir
        self.label = label

    def log_emit(self,*args):
        self._signal.emit(str(*args))

    def delete_via_label_project(self, input_dir, label0):
        label1 = label0.strip().split(',')
        label2 = [i.strip(' ') for i in label1]

        for root, dirs, files in os.walk(input_dir):
            for file in files:
                if "via_project.json" == file:
                    with open(os.path.join(root, file), encoding='gbk')as f:
                        result_list = json.load(f)
                        imgs_list = result_list["_via_img_metadata"]
                        for label in label2:
                            for i in imgs_list:
                                new_img_regions = []
                                for index, img_info in enumerate(imgs_list[i]["regions"]):
                                    if list(img_info["region_attributes"].items())[0][1] != label:
                                        new_img_regions.append(imgs_list[i]["regions"][index])
                                result_list["_via_img_metadata"][i]["regions"] = new_img_regions

                                self.log_emit(f'正在删除{i}中{label}标注信息')

                            project_label_list = list(result_list["_via_attributes"]["region"].values())[0]["options"]
                            new_options = {}
                            for sigle_label in project_label_list.keys():
                                if sigle_label != label:
                                    new_options[sigle_label] = ''
                                    last_name = sigle_label

                            list(result_list["_via_attributes"]["region"].values())[0]["options"] = new_options
                            list(result_list["_via_attributes"]["region"].values())[0]["default_options"] = {
                                last_name: True}

                    with open(os.path.join(root, "via_new_project.json"), "w", encoding='gbk') as f:
                        # f.write(json.dumps(result_list, indent=4, ensure_ascii=False))
                        f.write(json.dumps(result_list, indent=4))

                    output_dir0 = os.path.join(root, "via_new_project.json")
                    output_dir1 = output_dir0.replace("/", "\\")
                    self.log_emit(f'删除已完成，保存至\n{output_dir1}')

        self.log_emit("————————————————")
        self.log_emit(">>完成>>")
        self.log_emit(">>已在选择文件下完成删除标签>>")

    def run(self):
        self.delete_via_label_project(self.input_dir, self.label)