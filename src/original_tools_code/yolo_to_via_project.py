# -*- encoding: utf-8 -*-
"""
@File    : create_fitow_tfrecord.py
@Time    : 2019/9/6 14:24
@Author  : XXX
@Email   : XXXX@fitow-alpha.com
@Software: PyCharm
# Copyright 2019 The Fitow Authors. All Rights Reserved.

Please note that this tool creates sharded output files.
"""
import json
import os
import numpy as np
import cv2
import io
from PIL import Image
import base64

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 读入DT_dict，DT_dict就是inference_on_image.py生成的DT_dict
# input_dir=os.path.join(r'E:\TrainingDataBackup\panzhuangshebeiJHC\预标注_ng\1\202009', 'DT_dict.json')
# yolo_data_dir = r'E:\Desktop\exp'
# # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#
# # 建立类别ID的字典
# category_id = {1: "hd",  #博科林瓶身
#                2: "ls",
#                3: "ptbx",
#                4: "jl",
#                5: "hmxmb",
#                6: "logo",
#                7: "zjbq",
#                }
# category_id = {1: "cm_hp",  #博科林瓶身
#                2: "cd_hp",
#                3: "kp",
#                }

# 定义超类名字，只有一种就写项目名字即可
# super_cate = "fitow"
#
# # 建立一个VIA格式的模板，之后将via_img_metadata信息填进去就行了
# json_ = {
#     "_via_settings": {
#         "ui": {
#             "annotation_editor_height": 25,
#             "annotation_editor_fontsize": 0.8,
#             "leftsidebar_width": 18,
#             "image_grid": {
#                 "img_height": 80,
#                 "rshape_fill": "none",
#                 "rshape_fill_opacity": 0.3,
#                 "rshape_stroke": "yellow",
#                 "rshape_stroke_width": 2,
#                 "show_region_shape": True,
#                 "show_image_policy": "all"
#             },
#             "image": {
#                 "region_label": super_cate,  # 这里如果无超类，那这里就是类的代号
#                 "region_color": "__via_default_region_color__",
#                 "region_label_font": "10px Sans",
#                 "on_image_annotation_editor_placement": "NEAR_REGION"
#             }
#         },
#         "core": {
#             "buffer_size": 18,
#             "filepath": {},
#             "default_filepath": ""
#         },
#         "project": {"name": "pre_prediction"}  # 这里是VIA文件的名字
#     },
#     "_via_img_metadata": {},
#     "_via_attributes": {
#         "region": {
#             super_cate: {
#                 "type": "dropdown",
#                 "description": "",
#                 # “_via_attributes”下的"options"是每个类别的空值字典，照着填好即可
#                 "options": {
#                     "kp": "",
#                     "sx": "",
#                     "yw": "",
#                     "yc": "",
#
#                 },
#                 "default_options": {}
#             }
#         },
#         "file": {}
#     }
# }
#
#
# def extract_yololabel_inf(root, key_file_names, img_w, img_h):
#     with open(root + '/' + key_file_names[:-3] + 'txt', "r") as f:
#         img_label_inf = {}
#         key_imgname = str(key_file_names)
#         img_label_inf[key_imgname] = []
#         line_list = []
#         lines = f.readlines()
#         for line in lines:
#             line_inf = line.split()
#             line_list.append(int(line_inf[0]) + 1)
#             line_list.append(float(line_inf[1]) * img_w - float(line_inf[3]) * img_w / 2)
#             line_list.append(float(line_inf[2]) * img_h - float(line_inf[4]) * img_h / 2)
#             # line_list.append(float(line_inf[1]) * img_w + float(line_inf[3]) * img_w / 2)
#             # line_list.append(float(line_inf[2]) * img_h + float(line_inf[4]) * img_h / 2)
#             line_list.append(float(line_inf[3]) * img_w)
#             line_list.append(float(line_inf[4]) * img_h)
#             img_label_inf[key_imgname].append(line_list)
#             line_list = []
#         return img_label_inf
#
# n = 0
# for root, dirs, files in os.walk(yolo_data_dir):
#     for key_file_names in files:
#         if key_file_names[-3:] == 'jpg':
#             img_wh = cv2.imdecode(np.fromfile(os.path.join(root, key_file_names), dtype=np.uint8), 1)
#             img_w = img_wh.shape[1]
#             img_h = img_wh.shape[0]
#             img_label_inf = extract_yololabel_inf(root, key_file_names, img_w, img_h)
#             value_DT = img_label_inf[key_file_names]
#             img_metadata = {
#                 "filename": "",
#                 "size": None,
#                 "regions": [],
#                 "file_attributes": {}
#             }
#             file_name = key_file_names
#             img_path = os.path.join(root, file_name)
#             img = open(img_path, 'rb').read()
#
#             size = len(img)
#             for each_DT in value_DT:  # 获取DT类别id，DTbbox
#                 # 建立结构体
#                 region_dict = {
#                     "shape_attributes": {
#                         "name": "rect",
#                         "x": None,
#                         "y": None,
#                         "width": None,
#                         "height": None
#                     },
#                     "region_attributes": {super_cate: None}
#                 }
#
#                 category = category_id[each_DT[0]]
#                 w = each_DT[3]
#                 h = each_DT[4]
#                 x = each_DT[1]
#                 y = each_DT[2]
#
#                 region_dict["region_attributes"][super_cate] = category
#                 region_dict["shape_attributes"]["x"] = x
#                 region_dict["shape_attributes"]["y"] = y
#                 region_dict["shape_attributes"]["width"] = w
#                 region_dict["shape_attributes"]["height"] = h
#                 img_metadata["regions"].append(region_dict)
#             img_metadata["filename"] = file_name
#             img_metadata["size"] = size
#             img_metadata_key = file_name + str(size)
#             json_["_via_img_metadata"][img_metadata_key] = img_metadata
#             print(key_file_names)
#             n += 1
#             print(n)
#
# projest_labels = {}
# for label_index, single_category in category_id.items():
#     projest_labels[single_category] = ""
# json_["_via_attributes"]["region"][super_cate]["options"] = projest_labels
# with open(yolo_data_dir + '\yolo_to_via_project.json', 'w') as f:
#     json.dump(json_, f)
# print("DONE")

def txt2project(input_dir, category_id):

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
            if key_file_names[-3:] == 'jpg':
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
                print(key_file_names)
                n += 1
                print(n)

    projest_labels = {}
    for label_index, single_category in category_id.items():
        projest_labels[single_category] = ""
    json_["_via_attributes"]["region"][super_cate]["options"] = projest_labels
    with open(input_dir + '\yolo_to_via_project.json', 'w') as f:
        json.dump(json_, f)
    print("DONE")

if __name__ in "__main__":
    input_dir = r'E:\Desktop\exp'
    # 博科林瓶身
    category_id = {1: "hd",
                   2: "ls",
                   3: "ptbx",
                   4: "jl",
                   5: "hmxmb",
                   6: "logo",
                   7: "zjbq",
                   }
    txt2project(input_dir, category_id)