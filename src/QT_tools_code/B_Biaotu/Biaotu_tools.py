import os
import json
import cv2
import shutil
import ast
import datetime
import threading
import numpy as np

from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QThread


class Bp2jpg_thr(QThread):

    _signal = QtCore.pyqtSignal(str)

    def __init__(self, file_path=None, output_file_path=None, KEEP_ORIGIN=None):
        super(Bp2jpg_thr, self).__init__()
        self.file_path = file_path
        self.output_file_path = output_file_path
        self.KEEP_ORIGIN = KEEP_ORIGIN

    def log_emit(self,*args):
        self._signal.emit(str(*args))

    def bp2jpg_single(self, file_path, output_file_path, KEEP_ORIGIN):

        str1 = file_path.replace("/", "\\")
        split_path = str1.split('\\')
        image_name = split_path[-1]

        self.log_emit(f'正在处理{image_name}')

        img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), 1)
        save_path = os.path.join(output_file_path, image_name[:-3] + 'jpg')
        cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])[1].tofile(save_path)

        self.log_emit("————————————————")
        self.log_emit(">>完成>>")
        self.log_emit(">>已在选择图片目录下完成转换>>")

        if not KEEP_ORIGIN:
            self.log_emit(f'正在处理{file_path}')

            save_path = os.path.join(output_file_path, file_path[:-3] + 'jpg')
            os.remove(file_path)
            cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])[1].tofile(save_path)

            self.log_emit("————————————————")
            self.log_emit(">>完成>>")
            self.log_emit(">>已在选择图片目录下完成转换>>")

    def bp2jpg_thr(self, file_path, output_file_path, KEEP_ORIGIN):

        def gen_list(file_path):
            listx = []
            i = 0
            for root, dirs, files in os.walk(file_path):
                for name in files:
                    if name.endswith('bmp') or name.endswith('png'):
                        i += 1
                        listx.append([i, root, name])
            return listx

        # 图片转存jpg
        def save_threads(listx, image_num, index):
            len_list = len(listx)
            n = 1
            for i, root, name in listx:
                # print('Process: %.4f' % (n / len_list))
                str0 = root + "/" + name
                str1 = str0.replace("/", "\\")

                save_path2 = root.replace(str(file_path), str(output_file_path))

                self.log_emit(f'正在处理{name}')

                img = cv2.imdecode(np.fromfile(os.path.join(root, name), dtype=np.uint8), 1)
                save_path = os.path.join(save_path2, name[:-3] + 'jpg')
                cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])[1].tofile(save_path)

                if not KEEP_ORIGIN:
                    self.log_emit(f'正在处理{name}')

                    save_path = os.path.join(save_path2, name[:-3] + 'jpg')
                    os.remove(os.path.join(root, name))
                    cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])[1].tofile(save_path)

        image_num = 0
        roots = []

        for root0, dirs0, files0 in os.walk(file_path):
            roots.append(root0)
            for i in files0:
                if i.endswith('bmp') or i.endswith('png'):
                    image_num += 1
        for dir in roots[1:]:
            save_path0 = dir.replace(file_path, output_file_path)
            os.makedirs(save_path0)

        num_threads = 16
        listx = gen_list(file_path)
        list_threads = np.array_split(listx, num_threads)

        threadpool = []
        index = 0
        for n in range(len(list_threads)):
            list_n = np.array(list_threads[n])
            t = threading.Thread(target=save_threads, args=(list_n, image_num, index))
            threadpool.append(t)

        # 启动线程池
        for i in range(num_threads):
            threadpool[i].start()
        for i in range(num_threads):
            threadpool[i].join()

        self.log_emit("————————————————")
        self.log_emit(">>完成>>")
        self.log_emit(">>已在选择图片目录下完成转换>>")

    def run(self):
        self.bp2jpg_thr(self.file_path, self.output_file_path, self.KEEP_ORIGIN)

class Coco2project(QThread):

    _signal = QtCore.pyqtSignal(str)

    def __init__(self, coco_path=None):
        super(Coco2project, self).__init__()
        self.coco_path = coco_path

    def log_emit(self,*args):
        self._signal.emit(str(*args))

    def coco2project(self, coco_path):
        def get_all_project_path_list(coco_path):
            via_coco_path_list = []
            for root, dirs, files in os.walk(coco_path):
                for each_file in files:
                    # if 'coco' in each_file and each_file.endswith('.json'):
                    if each_file == 'via_export_coco.json':
                        via_coco_path_list.append(os.path.join(root, each_file))
            return via_coco_path_list

        def convert_coco_to_via_project(via_coco_path_list):

            img_path = os.path.dirname(via_coco_path_list)
            save_path = os.path.join(img_path, 'via_project.json')

            imageIdName = {}
            classIdName = {}
            via_img_metadata = {}
            options = {}
            regions = []

            with open(via_coco_path_list, 'r', encoding='utf-8') as f:
                coco_data = json.load(f)

            for image_info in coco_data['images']:
                imageIdName[image_info['id']] = image_info['file_name']

            for class_info in coco_data['categories']:
                classIdName[class_info['id']] = class_info['name']

            for num, cla in classIdName.items():
                options[cla] = ''

            via_attributes = {
                "region": {
                    "fitow": {
                        "type": "dropdown",
                        "description": "",
                        "options": options,
                        "default_options": {"": "true"}
                    }
                },
                "file": {}
            }

            via_settings = {
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
                        "region_label": "fitow",
                        "region_color": "fitow",
                        "region_label_font": "10px Sans",
                        "on_image_annotation_editor_placement": "NEAR_REGION"
                    }
                },
                "core": {
                    "buffer_size": 18,
                    "filepath": {},
                    "default_filepath": ""
                },
                "project": {"name": "via_project"}
            }

            oldID = -1
            for ann in coco_data['annotations']:
                nowID = ann['image_id']
                if nowID != oldID:
                    for num_null in range(int(nowID) - int(oldID) - 1, -1, -1):
                        if num_null != 0:
                            print(num_null)
                        filename = imageIdName[int(nowID) - num_null]
                        imageSize = os.path.getsize(os.path.join(img_path, filename))
                        viaDataName = filename + str(imageSize)
                        via_img_metadata[viaDataName] = {
                            "filename": filename,
                            "size": imageSize,
                            "regions": [],
                            "file_attributes": {}
                        }
                oldID = nowID
                filename = imageIdName[int(nowID) - num_null]
                imageSize = os.path.getsize(os.path.join(img_path, filename))
                viaDataName = filename + str(imageSize)
                attribute = {
                    "shape_attributes": {
                        "name": "rect",
                        "x": ann['bbox'][0],
                        "y": ann['bbox'][1],
                        "width": ann['bbox'][2],
                        "height": ann['bbox'][3]
                    },
                    "region_attributes": {"fitow": classIdName[ann['category_id']]}
                }
                via_img_metadata[viaDataName]['regions'].append(attribute)

            via = {
                '_via_settings': via_settings,
                '_via_img_metadata': via_img_metadata,
                '_via_attributes': via_attributes
            }

            with open(save_path, 'w', encoding='utf_8') as f:
                json.dump(via, f)

            save_path1 = save_path.replace("/", "\\")
            self.log_emit(f'转换已完成，保存至\n{save_path1}')

        """
        将输入文件夹下的所有via_export_coco.json转换为via_project.json。
        使用批量处理，需要保证via_project.json和其下所有图片处于相同路径下。
        :param input_dir: 输入目录，包含所有待转换的via_project.json，允许存在多层文件夹。
        :return:
        """
        all_project_path_list = get_all_project_path_list(coco_path)
        for each_project_path in all_project_path_list:
            convert_coco_to_via_project(each_project_path)

        self.log_emit("————————————————")
        self.log_emit(">>完成>>")
        self.log_emit(">>已在选择图片目录下完成转换>>")

    def run(self):
        self.coco2project(self.coco_path)

class Cut_project(QThread):

    _signal = QtCore.pyqtSignal(str)

    def __init__(self, file_path=None, save_path=None, starting_point=None, End=None):
        super(Cut_project, self).__init__()
        self.file_path = file_path
        self.save_path = save_path
        self.starting_point = starting_point
        self.End = End

    def log_emit(self,*args):
        self._signal.emit(str(*args))

    def Cut_project(self, file_path=None, save_path=None, starting_point=None, End=None):

        def dict_cut(ori_dict, start, end):
            slice_dict = {k: ori_dict[k] for k in list(ori_dict.keys())[start - 1 :end]}
            return slice_dict

        via_dict = json.load(open(os.path.join(file_path, "via_project.json"), 'rb'))
        # via_dict = json.load(open(file_path, 'rb'))
        via_dict["_via_img_metadata"] = dict_cut(via_dict["_via_img_metadata"], starting_point, End)
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        with open(os.path.join(save_path, "via_project_cut.json"), 'w') as f:
            json.dump(via_dict, f)

        via_dict = json.load(open(os.path.join(save_path, "via_project_cut.json"), "rb"))
        count = 1

        for key in via_dict["_via_img_metadata"]:
            lif = (list([key])[0].split('jpg')[0] + 'jpg')
            for fil in os.listdir(file_path):
                if lif == fil:
                    if lif.endswith(".jpg"):
                        filter_lif_path = os.path.join(file_path, fil)
                        save_lif_path = os.path.join(save_path, fil)
                        if not os.path.exists(save_path):
                            os.mkdir(save_path)
                            shutil.copy2(filter_lif_path, save_lif_path)
                        else:
                            shutil.copy2(filter_lif_path, save_lif_path)
                            print(count)
                            count += 1

        str = os.path.join(save_path, "via_project_cut.json")
        str1 = str.replace("/", "\\")
        self.log_emit(f'转换已完成，保存至 {str1}')

        self.log_emit("————————————————")
        self.log_emit(">>完成>>")
        self.log_emit(">>已在选择图片目录下完成裁剪>>")

    def run(self):
        self.Cut_project(self.file_path, self.save_path, self.starting_point, self.End)

class Merge_via_project(QThread):

    _signal = QtCore.pyqtSignal(str)

    def __init__(self, via_file_list0=None, output_dir=None, copy_img=None):
        super(Merge_via_project, self).__init__()
        self.via_file_list0 = via_file_list0
        self.output_dir = output_dir
        self.copy_img = copy_img

    def log_emit(self,*args):
        self._signal.emit(str(*args))

    def merga_via_project(self, via_file_list0, output_dir, copy_img):

        via_file_list = [via_file_list0]

        def merge_project(project_list, save_project_dir):
            img_metadata_merged = {}
            for single_project_file in project_list:
                self.log_emit(f'正在合并 {single_project_file}')
                via_project = json.load(open(single_project_file, 'rb'))
                via_img_metadata = via_project["_via_img_metadata"]
                img_metadata_merged.update(via_img_metadata)
                via_project_merged = json.load(open(single_project_file, 'rb'))
                via_project_merged["_via_img_metadata"] = img_metadata_merged
                with open(save_project_dir, 'w') as f:
                    json.dump(via_project_merged, f)

        save_path = os.path.join(output_dir, 'merge_data')
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        via_project_file_names = []

        for via_file in via_file_list:
            for root, dirs, files in os.walk(via_file):
                for file in files:
                    if "via_project.json" == file:
                        filename = file
                        via_project_file = os.path.join(root, filename)
                        via_project_file_names.append(via_project_file)
                        if copy_img == True:
                            single_via_project_info = json.load(open(via_project_file, 'r'))
                            single_via_img_metadata = single_via_project_info["_via_img_metadata"]
                            for key, info in single_via_img_metadata.items():
                                img_name = info['filename']
                                src_path = os.path.join(root, img_name)
                                shutil.copy(src_path, os.path.join(save_path, img_name))

        output_dir = save_path + "/via_project_merge.json"
        merge_project(via_project_file_names, output_dir)
        str1 = output_dir.replace("/", "\\")
        self.log_emit(f'合并已完成，保存至 {str1}')

        self.log_emit("————————————————")
        self.log_emit(">>完成>>")
        self.log_emit(">>已在选择图片目录下完成合并>>")

    def run(self):
        self.merga_via_project(self.via_file_list0, self.output_dir, self.copy_img)

class Project2coco(QThread):

    _signal = QtCore.pyqtSignal(str)

    def __init__(self, input_dir=None):
        super(Project2coco, self).__init__()
        self.input_dir = input_dir

    def log_emit(self,*args):
        self._signal.emit(str(*args))

    def project2coco(self, input_dir):

        def get_all_project_path_list(input_dir):
            via_project_path_list = []
            for root, dirs, files in os.walk(input_dir):
                for each_file in files:
                    # if 'project' in each_file and each_file.endswith('.json'):
                    if each_file == 'via_project.json':
                        via_project_path_list.append(os.path.join(root, each_file))
            return via_project_path_list

        def convert_via_project_to_coco(via_project_input_path, image_dir='', via_coco_output_path=''):
            """
            将via_project.json转换为via_export_coco.json，同时检测via_project.json中的图片是否存在缺失。
            :param via_project_input_path: 输入的via_project.json的路径。
            :param image_dir: 输入的图片目录，如果未指定，默认为via_project.json的同级目录。
            :param via_coco_output_path: 输出的via_export_coco.json的路径，如果未指定，默认为via_project.json的同级目录+via_export_coco.json。
            :return:
            """
            # 如果image_dir为空，默认输入图片路径为via_project.json的同级目录。
            if not image_dir:
                image_dir = os.path.dirname(via_project_input_path)
            # 如果via_coco_output_path为空，默认输出via_export_coco.json的目录为via_project.json的同级目录。
            if not via_coco_output_path:
                via_coco_output_path = os.path.join(os.path.dirname(via_project_input_path), 'via_export_coco.json')

            via_project_input_path1 = via_project_input_path.replace("/", "\\")
            self.log_emit(f'开始处理: {via_project_input_path1}')

            now_datetime = datetime.datetime.now()

            images_list = []
            annotations_list = []
            categories_list = []
            with open(via_project_input_path, 'r', encoding='utf-8') as f:
                project_dict = json.load(f)
                supercategory = list(project_dict['_via_attributes']['region'].keys())[0]
                options_list = list(list(project_dict['_via_attributes']['region'].values())[0]['options'].keys())
                for i in range(len(options_list)):
                    each_category_dict = {
                        'id': i + 1,
                        'name': options_list[i],
                        'supercategory': supercategory
                    }
                    categories_list.append(each_category_dict)
                image_id = 0
                annotation_id = 0
                for each_val in project_dict['_via_img_metadata'].values():

                    self.log_emit(f"正在处理第{image_id + 1}张图片 {each_val['filename']}")

                    image_path = os.path.join(image_dir, each_val['filename'])
                    try:
                        img = Image.open(image_path)
                    except:
                        # TODO 使用日志系统，替换print
                        print(f'图片不存在或者无法读取，图片路径为{image_path}')
                        raise Exception('读取图片发生错误。')

                    w, h = img.size
                    each_image_dict = {
                        'id': image_id,
                        'width': w,
                        'height': h,
                        'file_name': each_val['filename'],
                        'license': 1,
                        'date_captured': ''
                    }
                    images_list.append(each_image_dict)

                    for each_region in each_val['regions']:
                        if 'x' in each_region['shape_attributes']:
                            x = each_region['shape_attributes']['x']
                            y = each_region['shape_attributes']['y']
                            width = each_region['shape_attributes']['width']
                            height = each_region['shape_attributes']['height']
                        else:
                            all_points_x_list = each_region['shape_attributes']['all_points_x']
                            all_points_y_list = each_region['shape_attributes']['all_points_y']
                            x = min(all_points_x_list)
                            y = min(all_points_y_list)
                            width = max(all_points_x_list) - x
                            height = max(all_points_y_list) - y
                            if width <= 0 or height <= 0:
                                # TODO 使用日志系统，替换print
                                print('异常的标注框：')
                                print(each_val['filename'])
                                print(all_points_x_list)

                        each_annotation_dict = {
                            'id': annotation_id,
                            'image_id': str(image_id),
                            'category_id': options_list.index(each_region['region_attributes'][supercategory]) + 1,
                            # TODO segmentation为bbox格式，如果使用mask需要修改segmentation
                            'segmentation': [x, y, x + width, y, x + width, y + height, x, y + height],
                            'area': width * height,
                            'bbox': [x, y, width, height],
                            'iscrowd': 0  # TODO iscrow目前固定为0
                        }

                        annotations_list.append(each_annotation_dict)
                        annotation_id += 1
                    image_id += 1

            via_export_coco_dict = {
                'info': {
                    'year': int(now_datetime.year),
                    'version': '1',
                    'description': 'Exported using VGG Image Annotator (http://www.robots.ox.ac.uk/~vgg/software/via/)',
                    'contributor': '',
                    'url': 'http://www.robots.ox.ac.uk/~vgg/software/via/',
                    'date_created': now_datetime.strftime('%a %b %d %Y %H:%M:%S GMT+0800')
                },
                'images': images_list,
                'annotations': annotations_list,
                'licenses': [{
                    'id': 1,
                    'name': 'Unknown',
                    'url': ''
                }],
                'categories': categories_list
            }

            with open(via_coco_output_path, 'w', encoding='utf-8') as f:
                f.write(json.dumps(via_export_coco_dict, ensure_ascii=False))

            via_coco_output_path1 = via_coco_output_path.replace("/", "\\")
            self.log_emit(f'转换已完成，保存至\n{via_coco_output_path1}')

        """
        将输入文件夹下的所有via_project.json转换为via_export_coco.json。
        使用批量处理，需要保证via_project.json和其下所有图片处于相同路径下。
        :param input_dir: 输入目录，包含所有待转换的via_project.json，允许存在多层文件夹。
        :return:
        """
        all_project_path_list = get_all_project_path_list(input_dir)
        for each_project_path in all_project_path_list:
            convert_via_project_to_coco(each_project_path)

        self.log_emit("————————————————")
        self.log_emit(">>完成>>")
        self.log_emit(">>已在选择图片目录下完成转换>>")

    def run(self):
        self.project2coco(self.input_dir)

class Project2txt(QThread):

    _signal = QtCore.pyqtSignal(str)

    def __init__(self, input_dir=None):
        super(Project2txt, self).__init__()
        self.input_dir = input_dir

    def log_emit(self,*args):
        self._signal.emit(str(*args))

    def project2txt(self, input_dir):

        def split_to_yolo(single_project):
            via_project = json.load(open(single_project, 'rb'))
            save_path = os.path.split(single_project)[0]
            via_img_metadata = via_project["_via_img_metadata"]
            super_category = list(via_project["_via_attributes"]["region"].keys())[0]
            labels = list(list(via_project["_via_attributes"]["region"].values())[0]["options"].keys())
            for key, single_img_inf in via_img_metadata.items():
                file_name = single_img_inf["filename"]
                regions = single_img_inf["regions"]
                im = Image.open(os.path.join(save_path, file_name), 'r')
                ann_info_dic = ""

                export_file = os.path.join(save_path, file_name[:-4] + ".txt")
                if os.path.exists(export_file):
                    os.remove(export_file)

                if regions != []:
                    # print(file_name)
                    for single_label_inf in regions:
                        label_index = labels.index(single_label_inf["region_attributes"][super_category])
                        label_w = single_label_inf["shape_attributes"]["width"]
                        label_h = single_label_inf["shape_attributes"]["height"]
                        # 将边框规范到图内
                        if label_w > im.width:
                            label_w = im.width
                        if label_h > im.height:
                            label_h = im.height

                        ann_info_dic = str(label_index) \
                                       + ' ' + str((single_label_inf["shape_attributes"]["x"] +
                                                    label_w / 2) / im.width) \
                                       + ' ' + str((single_label_inf["shape_attributes"]["y"] +
                                                    label_h / 2) / im.height) \
                                       + ' ' + str(label_w / im.width) \
                                       + ' ' + str(label_h / im.height) \
                                       + '\n'
                        with open(export_file, "a+") as out_file:
                            out_file.write(ann_info_dic)
                else:
                    with open(export_file, "a+") as out_file:
                        out_file.write(ann_info_dic)

        input_dir_list = []
        input_dir_list.append(input_dir)
        project_path_list = []
        for single_path in input_dir_list:
            for root, dirs, files in os.walk(single_path):
                for name in files:
                    if name == 'via_project.json':
                        project_path_list.append(os.path.join(root, name))

        for single_project in project_path_list:

            single_project0 = single_project.replace("/", "\\")
            self.log_emit(f'正在处理 {single_project0}')

            split_to_yolo(single_project)

        self.log_emit("————————————————")
        self.log_emit(">>完成>>")
        self.log_emit(">>已在选择图片目录下完成转换>>")

    def run(self):
        self.project2txt(self.input_dir)

class Txt2project(QThread):

    _signal = QtCore.pyqtSignal(str)

    def __init__(self, input_dir=None, category_id0=None):
        super(Txt2project, self).__init__()
        self.input_dir = input_dir
        self.category_id0 = category_id0

    def log_emit(self,*args):
        self._signal.emit(str(*args))

    def txt2project(self, input_dir, category_id0):
        category_id = ast.literal_eval(category_id0)
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

        def extract_yololabel_inf(root, key_file_names, img_w, img_h):
            with open(root + '/' + key_file_names[:-3] + 'txt', "r") as f:
                img_label_inf = {}
                key_imgname = str(key_file_names)
                img_label_inf[key_imgname] = []
                line_list = []
                lines = f.readlines()
                for line in lines:
                    line_inf = line.split()
                    line_list.append(int(line_inf[0]) + 1)
                    line_list.append(float(line_inf[1]) * img_w - float(line_inf[3]) * img_w / 2)
                    line_list.append(float(line_inf[2]) * img_h - float(line_inf[4]) * img_h / 2)
                    # line_list.append(float(line_inf[1]) * img_w + float(line_inf[3]) * img_w / 2)
                    # line_list.append(float(line_inf[2]) * img_h + float(line_inf[4]) * img_h / 2)
                    line_list.append(float(line_inf[3]) * img_w)
                    line_list.append(float(line_inf[4]) * img_h)
                    img_label_inf[key_imgname].append(line_list)
                    line_list = []
                return img_label_inf

        n = 0
        for root, dirs, files in os.walk(input_dir):
            for key_file_names in files:
                if key_file_names[-3:] == 'jpg' or key_file_names[-3:] == 'bmp':
                    img_wh = cv2.imdecode(np.fromfile(os.path.join(root, key_file_names), dtype=np.uint8), 1)
                    img_w = img_wh.shape[1]
                    img_h = img_wh.shape[0]
                    img_label_inf = extract_yololabel_inf(root, key_file_names, img_w, img_h)
                    value_DT = img_label_inf[key_file_names]
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
                    for each_DT in value_DT:  # 获取DT类别id，DTbbox
                        # 建立结构体
                        region_dict = {
                            "shape_attributes": {
                                "name": "rect",
                                "x": None,
                                "y": None,
                                "width": None,
                                "height": None
                            },
                            "region_attributes": {super_cate: None}
                        }

                        category = category_id[each_DT[0]]
                        w = each_DT[3]
                        h = each_DT[4]
                        x = each_DT[1]
                        y = each_DT[2]

                        region_dict["region_attributes"][super_cate] = category
                        region_dict["shape_attributes"]["x"] = x
                        region_dict["shape_attributes"]["y"] = y
                        region_dict["shape_attributes"]["width"] = w
                        region_dict["shape_attributes"]["height"] = h
                        img_metadata["regions"].append(region_dict)
                    img_metadata["filename"] = file_name
                    img_metadata["size"] = size
                    img_metadata_key = file_name + str(size)
                    json_["_via_img_metadata"][img_metadata_key] = img_metadata
                    n += 1

                    self.log_emit(f"正在处理第{n}张图片 {key_file_names}")

        projest_labels = {}
        for label_index, single_category in category_id.items():
            projest_labels[single_category] = ""
        json_["_via_attributes"]["region"][super_cate]["options"] = projest_labels
        with open(input_dir + '\\via_project.json', 'w') as f:
            json.dump(json_, f)

        savepath = (input_dir + '\\via_project.json').replace("/", "\\")
        self.log_emit(f'转换已完成，保存至\n{savepath}')

        self.log_emit("————————————————")
        self.log_emit(">>完成>>")
        self.log_emit(">>已在选择图片目录下完成转换>>")

    def run(self):
        self.txt2project(self.input_dir, self.category_id0)

class Via_coco2normal_coco(QThread):

    _signal = QtCore.pyqtSignal(str)

    def __init__(self, input_dir=None, output_dir=None):
        super(Via_coco2normal_coco, self).__init__()
        self.input_dir = input_dir
        self.output_dir = output_dir

    def log_emit(self,*args):
        self._signal.emit(str(*args))

    def via_coco2normal_coco(self, input_dir, output_dir):

        for root, dirs,files in os.walk(input_dir):
            for file in files:
                if file == 'via_export_coco.json':

                    coco_json = json.load(open(os.path.join(root, file), "rb"))
                    annotations = coco_json["annotations"]
                    for i, each_anno in enumerate(annotations):
                        new_seg = []
                        each_anno_image_id = int(each_anno["image_id"])
                        annotations[i]["image_id"] = each_anno_image_id
                        new_seg.append(each_anno["segmentation"])
                        annotations[i]["segmentation"] = new_seg
                    coco_json["annotations"] = annotations

                    # coco_path = os.path.join(root, file)
                    save_path = root.replace(input_dir, output_dir)
                    if not os.path.exists(save_path):
                        os.makedirs(save_path)

                    with open(os.path.join(save_path, "via_export_coco_normal.json"), 'w') as f:
                        json.dump(coco_json, f)

                    out_dir0 = os.path.join(save_path, "via_export_coco_normal.json")
                    out_dir1 = out_dir0.replace("/", "\\")
                    self.log_emit(f'标准coco格式文件保存至{out_dir1}')
        self.log_emit("————————————————")
        self.log_emit(">>完成>>")
        self.log_emit(">>已在选择图片目录下完成修正>>")

    def run(self):
        self.via_coco2normal_coco(self.input_dir, self.output_dir)