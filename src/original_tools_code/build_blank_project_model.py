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


def build_blank_project_model(input_dir, category_id):

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
                img_wh = cv2.imdecode(np.fromfile(os.path.join(root, key_file_names), dtype=np.uint8), 1)
                img_w = img_wh.shape[1]
                img_h = img_wh.shape[0]

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
                print(key_file_names)
                n += 1
                print(n)

    projest_labels = {}
    for label_index, single_category in category_id.items():
        projest_labels[single_category] = ""
    json_["_via_attributes"]["region"][super_cate]["options"] = projest_labels
    with open(input_dir + r'\via_model_project.json', 'w') as f:
        json.dump(json_, f)
print("DONE")

if __name__ in '__main__':
    yolo_data_dir = r'E:\Desktop\bokelin\0811\yibiaozhu\1\1\50'
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    # 建立类别ID的字典
    category_id = {1: "ld",
                   2: "hd",
                   3: "hdq",
                   4: "logo",
                   5: "zjbq",
                   }

    build_blank_project_model(yolo_data_dir, category_id)