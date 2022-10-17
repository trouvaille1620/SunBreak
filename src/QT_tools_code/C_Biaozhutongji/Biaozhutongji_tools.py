import os
import json
import shutil
import xlsxwriter as xw

from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QThread


class Extract_assign_labelindex(QThread):

    _signal = QtCore.pyqtSignal(str)

    def __init__(self, input_dir=None, output_dir=None, label_index=None):
        super(Extract_assign_labelindex, self).__init__()
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.label_index = label_index

    def log_emit(self,*args):
        self._signal.emit(str(*args))

    def extract_assign_labelindex_data(self, input_dir, output_dir, label_index):
        n = 0
        for root, dirs, files in os.walk(input_dir):
            for name in files:
                if '.txt' in name:
                    with open(root + '/' + name) as f:
                        label_list = f.readlines()
                        for single_label in label_list:
                            if single_label.split(' ')[0] == label_index:

                                save_path = root.replace(input_dir, output_dir)
                                if not os.path.exists(save_path):
                                    os.makedirs(save_path)

                                shutil.copy(root + '/' + name, save_path)
                                shutil.copy(root + '/' + name[:-3] + 'jpg', save_path)
                        n += 1

                        self.log_emit(f"正在复制第{n}张图片 {root + '/' + name[:-3] + 'jpg'}")

        save_path1 = save_path.replace("/", "\\")
        self.log_emit(f'提取已完成，保存至\n{save_path1}')

        self.log_emit("————————————————")
        self.log_emit(">>完成>>")
        self.log_emit(">>已在选择目录下完成提取>>")

    def run(self):
        self.extract_assign_labelindex_data(self.input_dir, self.output_dir, self.label_index)

class No_label_check_project(QThread):

    _signal = QtCore.pyqtSignal(str)

    def __init__(self, filter_path=None, save_path0=None):
        super(No_label_check_project, self).__init__()
        self.filter_path = filter_path
        self.save_path0 = save_path0

    def log_emit(self,*args):
        self._signal.emit(str(*args))

    def no_label_check_project(self, filter_path, save_path0):

        for root, dirs, files in os.walk(filter_path):
            for file in files:
                if file == 'via_project.json':

                    file_name_list = []
                    via_project = json.load(open(os.path.join(root, file), 'rb'))
                    metadata = via_project["_via_img_metadata"]

                    for each_img in metadata.values():
                        each_filename = each_img["filename"]

                        for each_region_attributes in each_img["regions"]:
                            sa = each_region_attributes["region_attributes"]
                            if sa["fitow"] == '':
                                file_name_list.append(each_filename)
                                file_name_list = list(set(file_name_list))

                    save_path = root.replace(filter_path, save_path0)
                    if not os.path.exists(save_path):
                        os.makedirs(save_path)

                    if len(file_name_list) != 0:
                        with open(os.path.join(save_path, 'no_label_check.txt'), 'w') as file:
                            for img in file_name_list:
                                a = str('含有空签的图为： ' + img)
                                self.log_emit(a)
                                file.write(img + '\n')

                        output_dir = os.path.join(save_path, 'no_label_check.txt').replace("/", "\\")
                        self.log_emit(f'检查已完成，保存至\n{output_dir}')

        self.log_emit("————————————————")
        self.log_emit(">>完成>>")
        self.log_emit(">>已在选择文件下完成检查>>")

    def run(self):
        self.no_label_check_project(self.filter_path, self.save_path0)

class Statistics_project(QThread):

    _signal = QtCore.pyqtSignal(str)

    def __init__(self, filter_path=None, save_xlsx= None):
        super(Statistics_project, self).__init__()
        self.filter_path = filter_path
        self.save_xlsx = save_xlsx

    def log_emit(self,*args):
        self._signal.emit(str(*args))

    def statistics_project(self, filter_path, save_xlsx):

        def xw_toExcel(data, fileName):  # xlsxwriter库储存数据到excel
            workbook = xw.Workbook(fileName)  # 创建工作簿
            worksheet1 = workbook.add_worksheet("sheet1")  # 创建子表
            worksheet1.activate()  # 激活表
            title = ['序号', '标签', '数量']  # 设置表头
            worksheet1.write_row('A1', title)  # 从A1单元格开始写入表头
            i = 2  # 从第二行开始写入数据
            for j in range(len(data)):
                insertData = [data[j]["id"], data[j]["label"], data[j]["num"]]
                row = 'A' + str(i)
                worksheet1.write_row(row, insertData)
                i += 1
            workbook.close()  # 关闭表

        cat_list = []
        file_name_list = []
        cat_id_list = []
        id_list = []
        id_quantity = []
        results = []

        via_project = json.load(open(filter_path, 'rb'))
        metadata = via_project["_via_img_metadata"]
        attributes = via_project["_via_attributes"]
        for each_img in metadata.values():
            each_filename = each_img["filename"]
            file_name_list.append(each_filename)
            for each_region_attributes in each_img["regions"]:
                sa = each_region_attributes["region_attributes"]
                for each_cat in sa.values():
                    cat_list.append(each_cat)
        for each_region in attributes.values():
            for catgry in each_region.values():
                for keys, values in catgry["options"].items():
                    cat_id_list.append(keys)
        for cat_id in cat_id_list:
            elm_count = cat_list.count(cat_id)
            id_list.append(cat_id)
            id_quantity.append(elm_count)

        self.log_emit(f'图片总数： {len(file_name_list)}')
        id = 1
        for label, num in zip(id_list, id_quantity):
            info = {}
            str0 = str('label:'+ str(label) + '   ' + 'num:' + str(num))
            self.log_emit(str0)
            info['id'] = str(id)
            info['label'] = str(label)
            info['num'] = str(num)
            results.append(info)
            id += 1

        if save_xlsx == True:
            file_dir = os.path.dirname(filter_path)
            xlsx_save_path = os.path.join(file_dir, 'label_num.xlsx')
            xw_toExcel(results, xlsx_save_path)

        self.log_emit("————————————————")
        self.log_emit(">>完成>>")
        self.log_emit(">>已在选择文件下完成统计>>")

    def run(self):
        self.statistics_project(self.filter_path, self.save_xlsx)

class Check_folder_project_img(QThread):

    _signal = QtCore.pyqtSignal(str)

    def __init__(self, file_path=None):
        super(Check_folder_project_img, self).__init__()
        self.file_path = file_path

    def log_emit(self,*args):
        self._signal.emit(str(*args))

    def check_folder_project_img(self, file_path):
        project_nohave_img = []
        folder_nohave_img = []
        for root, dirs, files in os.walk(file_path):
            for file in files:
                if file == 'via_project.json':
                    via_project = json.load(open(os.path.join(root, file), 'rb'))
                    via_img_metadata = via_project["_via_img_metadata"]
                    for key, info in via_img_metadata.items():
                        img_name = info['filename']
                        project_img_path = os.path.join(root, img_name)
                        if not os.path.exists(project_img_path):
                            folder_nohave_img.append(img_name)
                    if len(folder_nohave_img) != 0:
                        with open(os.path.join(root, 'check_img_project.txt'), 'w') as f:
                            f.write('project中存在但文件夹中不存在的图为' + '\n')
                            for img in folder_nohave_img:
                                f.write(img + '\n')
                        output_dir0 = os.path.join(root, 'check_img_folder.txt').replace("/", "\\")
                        self.log_emit(f'检查已完成，保存至\n{output_dir0}')

                via_project = json.load(open(os.path.join(root, 'via_project.json'), 'rb'))
                via_img_metadata = via_project["_via_img_metadata"]
                img_list = []
                for key, info in via_img_metadata.items():
                    img_name = info['filename']
                    img_list.append(img_name)

                if file.endswith('jpg') or file.endswith('bmp'):
                    if file not in img_list:
                        project_nohave_img.append(file)
                        print(project_nohave_img)

        if len(project_nohave_img) != 0:
            with open(os.path.join(root, 'check_img_folder.txt'), 'w') as f:
                f.write('文件夹中存在但project中不存在的图为' + '\n')
                for img in project_nohave_img:
                    f.write(img + '\n')
            output_dir1 = os.path.join(root, 'check_img_folder.txt').replace("/", "\\")
            self.log_emit(f'检查已完成，保存至\n{output_dir1}')

        self.log_emit("————————————————")
        self.log_emit(">>完成>>")
        self.log_emit(">>已在选择文件下完成检查>>")

    def run(self):
        self.check_folder_project_img(self.file_path)