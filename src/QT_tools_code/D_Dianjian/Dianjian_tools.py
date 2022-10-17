import os
import ast
import json
import shutil
import xlsxwriter as xw

from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None

from PyQt5 import QtCore
from PyQt5.QtCore import QThread


class Extract_label(QThread):

    _signal = QtCore.pyqtSignal(str)

    def __init__(self, input_dir=None, output_dir=None, label_num=None):
        super(Extract_label, self).__init__()
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.label_num = label_num

    def log_emit(self,*args):
        self._signal.emit(str(*args))

    def extract_label(self, input_dir, output_dir, label_num):
        n = 0
        for category in range(0, int(label_num)):
            save_path = os.path.join(output_dir, str(category))
            os.makedirs(save_path, exist_ok=True)

        for root, dirs, files in os.walk(input_dir):
            for name in files:
                if '.txt' in name:
                    with open(root + '/' + name) as f:
                        label_list = f.readlines()
                        for single_label in label_list:
                            save_path0 = os.path.join(output_dir, str(single_label.split(' ')[0]))
                            shutil.copy(root + '/' + name, save_path0)
                            shutil.copy(root + '/' + name[:-3] + 'jpg', save_path0)
                        n += 1

                        self.log_emit(f"正在复制第{n}张图片 {root + '/' + name[:-3] + 'jpg'}")

        output_dir1 = save_path0.replace("/", "\\")
        self.log_emit(f'分类已完成，保存至\n{output_dir1}')

        self.log_emit("————————————————")
        self.log_emit(">>完成>>")
        self.log_emit(">>已在选择图片目录下完成复制>>")

    def run(self):
        self.extract_label(self.input_dir, self.output_dir, self.label_num)

class Img_name2xlsx(QThread):

    _signal = QtCore.pyqtSignal(str)

    def __init__(self, filter_path=None, save_path=None):
        super(Img_name2xlsx, self).__init__()
        self.filter_path = filter_path
        self.save_path = save_path

    def log_emit(self,*args):
        self._signal.emit(str(*args))

    def img_name2txt(self, filter_path, save_path):

        if os.path.exists(os.path.join(save_path, 'img_name.xlsx')):
            os.remove(os.path.join(save_path, 'img_name.xlsx'))

        def xw_toExcel(data, fileName):  # xlsxwriter库储存数据到excel
            workbook = xw.Workbook(fileName)  # 创建工作簿
            worksheet1 = workbook.add_worksheet("sheet1")  # 创建子表
            worksheet1.activate()  # 激活表
            # title = ['序号', '标签', '数量']  # 设置表头
            # worksheet1.write_row('A1', title)  # 从A1单元格开始写入表头
            i = 1  # 从第二行开始写入数据
            for j in range(len(data)):
                insertData = [data[j]["image"]]
                row = 'A' + str(i)
                worksheet1.write_row(row, insertData)
                i += 1
            workbook.close()  # 关闭表
        results = []
        for root, dirs, files in os.walk(filter_path):
            for file in files:
                if file.endswith('jpg') or file.endswith('bmp'):
                    img_name = {}
                    img_name['image'] = file
                    results.append(img_name)

        xlsx_save_path = os.path.join(save_path, 'img_name.xlsx')
        xw_toExcel(results, xlsx_save_path)

        output_dir = os.path.join(save_path, 'img_name.xlsx').replace("/", "\\")
        self.log_emit(f'写入已完成，保存至\n{output_dir}')

        self.log_emit("————————————————")
        self.log_emit(">>完成>>")
        self.log_emit(">>已在选择文件下完成统计>>")

    def run(self):
        self.img_name2txt(self.filter_path, self.save_path)

class Extract_label_project(QThread):

    _signal = QtCore.pyqtSignal(str)

    def __init__(self, input_dir=None, label=None):
        super(Extract_label_project, self).__init__()
        self.input_dir = input_dir
        self.label = label

    def log_emit(self,*args):
        self._signal.emit(str(*args))

    def extract_label_project(self, input_dir, label0):
        label1 = label0.strip().split(',')
        label2 = [i.strip(' ') for i in label1]

        for root, dirs, files in os.walk(input_dir):
            for file in files:
                if "via_project.json" == file:
                    for label in label2:
                        with open(os.path.join(root, file), encoding='utf-8')as f:
                            result_list = json.load(f)
                            imgs_list = result_list["_via_img_metadata"]
                            for i in imgs_list:
                                new_img_regions = []
                                for index, img_info in enumerate(imgs_list[i]["regions"]):
                                    if list(img_info["region_attributes"].items())[0][1] == label:
                                        new_img_regions.append(imgs_list[i]["regions"][index])
                                result_list["_via_img_metadata"][i]["regions"] = new_img_regions

                                self.log_emit(f'正在提取{i}中{label}标注信息')

                            project_label_list = list(result_list["_via_attributes"]["region"].values())[0]["options"]
                            new_options = {}
                            for sigle_label in project_label_list.keys():
                                if sigle_label == label:
                                    new_options[sigle_label] = ''
                                    last_name = sigle_label
                            list(result_list["_via_attributes"]["region"].values())[0]["options"] = new_options
                            list(result_list["_via_attributes"]["region"].values())[0]["default_options"] = {
                                last_name: True}

                        json_name = 'via_' + label + '_project.json'
                        with open(os.path.join(root, json_name), "w", encoding='utf-8') as f:
                            f.write(json.dumps(result_list, indent=4, ensure_ascii=False))

                        output_dir0 = os.path.join(root, json_name)
                        output_dir1 = output_dir0.replace("/", "\\")
                        self.log_emit(f'提取已完成，保存至\n{output_dir1}')

        self.log_emit("————————————————")
        self.log_emit(">>完成>>")
        self.log_emit(">>已在选择文件下完成提取标签>>")

    def run(self):
        self.extract_label_project(self.input_dir, self.label)

class Build_blank_project_model(QThread):

    _signal = QtCore.pyqtSignal(str)

    def __init__(self, input_dir=None, category_id0=None):
        super(Build_blank_project_model, self).__init__()
        self.input_dir = input_dir
        self.category_id0 = category_id0

    def log_emit(self,*args):
        self._signal.emit(str(*args))

    def build_blank_project_model(self, input_dir, category_id0):
        category_id = ast.literal_eval(category_id0)

        # 定义超类名字，只有一种就写项目名字即可
        super_cate = "fitow"

        # 建立一个VIA格式的模板，之后将via_img_metadata信息填进去就行了
        json_ = {
            "_via_settings": {
                "ui": {
                    "annotation_editor_height": 25,
                    "annotation_editor_fontsize": 0.8,
                    "leftsidebar_width": 18,
                    "image_grid": {
                        "img_height": 80,
                        "rshape_fill": "none",
                        "rshape_fill_opacity": 0.3,
                        "rshape_stroke": "yellow",
                        "rshape_stroke_width": 2,
                        "show_region_shape": True,
                        "show_image_policy": "all"
                    },
                    "image": {
                        "region_label": super_cate,  # 这里如果无超类，那这里就是类的代号
                        "region_color": "__via_default_region_color__",
                        "region_label_font": "10px Sans",
                        "on_image_annotation_editor_placement": "NEAR_REGION"
                    }
                },
                "core": {
                    "buffer_size": 18,
                    "filepath": {},
                    "default_filepath": ""
                },
                "project": {"name": "pre_prediction"}  # 这里是VIA文件的名字
            },
            "_via_img_metadata": {},
            "_via_attributes": {
                "region": {
                    super_cate: {
                        "type": "dropdown",
                        "description": "",
                        # “_via_attributes”下的"options"是每个类别的空值字典，照着填好即可
                        "options": {
                            "kp": "",
                            "sx": "",
                            "yw": "",
                            "yc": "",

                        },
                        "default_options": {}
                    }
                },
                "file": {}
            }
        }

        n = 0
        for root, dirs, files in os.walk(input_dir):
            for key_file_names in files:
                if key_file_names[-3:] == 'jpg':

                    img_metadata = {
                        "filename": "",
                        "size": None,
                        "regions": [],
                        "file_attributes": {}
                    }
                    file_name = key_file_names
                    img_path = os.path.join(root, file_name)
                    img = open(img_path, 'rb').read()

                    size = len(img)

                    img_metadata["filename"] = file_name
                    img_metadata["size"] = size
                    img_metadata_key = file_name + str(size)
                    json_["_via_img_metadata"][img_metadata_key] = img_metadata
                    self.log_emit(f'正在处理 {key_file_names}')
                    n += 1
            self.log_emit(f'共计处理{n}张图片')

        projest_labels = {}
        for label_index, single_category in category_id.items():
            projest_labels[single_category] = ""
        json_["_via_attributes"]["region"][super_cate]["options"] = projest_labels
        with open(input_dir + r'\via_model_project.json', 'w', encoding='gbk') as f:
            json.dump(json_, f)

        output_dir = input_dir + r'\via_model_project.json'
        output_dir1 = output_dir.replace("/", "\\")
        self.log_emit(f'保存在{output_dir1}')

        self.log_emit("————————————————")
        self.log_emit(">>完成>>")
        self.log_emit(">>已在选择图片目录下完成建立>>")

    def run(self):
        self.build_blank_project_model(self.input_dir, self.category_id0)

class Merge_project_by_label(QThread):

    _signal = QtCore.pyqtSignal(str)

    def __init__(self, model_path=None, label_path=None):
        super(Merge_project_by_label, self).__init__()
        self.model_path = model_path
        self.label_path = label_path

    def log_emit(self,*args):
        self._signal.emit(str(*args))

    def merge_project_by_label(self, model_path, label_path):

        model_via_project = json.load(open(model_path, 'rb'), encoding='gbk')
        model_via_img_metadata = model_via_project["_via_img_metadata"]
        label_via_project = json.load(open(label_path, 'rb'))
        label_via_img_metadata = label_via_project["_via_img_metadata"]

        for key, single_img_inf in label_via_img_metadata.items():
            label_regions = single_img_inf["regions"]
            model_via_img_metadata[key]["regions"] += label_regions

            with open(model_path, 'w', encoding='gbk') as f:
                f.write(json.dumps(model_via_project))

            self.log_emit(f'正在添加{key}标注信息至via_model_project.json')

        label = label_path.split('_')[1]
        self.log_emit(f'已将{label}标注信息添加至via_model_project.json')

        self.log_emit("————————————————")
        self.log_emit(">>完成>>")
        self.log_emit(">>已在选择文件下完成添加>>")

    def run(self):
        self.merge_project_by_label(self.model_path, self.label_path)