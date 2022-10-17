# -*- encoding: utf-8 -*-
"""
将各路径下的project文件转成coco,会找到给定路径下的所有project,且project需与图片在同一路径下
"""

import os
import json
from PIL import Image


# def split_to_yolo(single_project):
#     via_project = json.load(open(single_project, 'rb'))
#     save_path = os.path.split(single_project)[0]
#     via_img_metadata = via_project["_via_img_metadata"]
#     super_category = list(via_project["_via_attributes"]["region"].keys())[0]
#     labels = list(list(via_project["_via_attributes"]["region"].values())[0]["options"].keys())
#     for key, single_img_inf in via_img_metadata.items():
#         file_name = single_img_inf["filename"]
#         regions = single_img_inf["regions"]
#         im = Image.open(os.path.join(save_path, file_name), 'r')
#         ann_info_dic = ""
#         export_file = os.path.join(save_path, file_name[:-4] + ".txt")
#         if regions != []:
#             # print(file_name)
#             for single_label_inf in regions:
#                 label_index = labels.index(single_label_inf["region_attributes"][super_category])
#                 label_w = single_label_inf["shape_attributes"]["width"]
#                 label_h = single_label_inf["shape_attributes"]["height"]
#                 #将边框规范到图内
#                 if label_w > im.width:
#                     label_w = im.widt
#                 if label_h > im.height:
#                     label_h = im.height
#
#                 ann_info_dic = str(label_index) \
#                                + ' ' + str((single_label_inf["shape_attributes"]["x"] +
#                                             label_w / 2) / im.width) \
#                                + ' ' + str((single_label_inf["shape_attributes"]["y"] +
#                                             label_h / 2) / im.height) \
#                                + ' ' + str(label_w / im.width) \
#                                + ' ' + str(label_h / im.height) \
#                                + '\n'
#                 with open(export_file, "a+") as out_file:
#                     out_file.write(ann_info_dic)
#         else:
#             with open(export_file, "a+") as out_file:
#                 out_file.write(ann_info_dic)
#
# def project_to_yolo(input_dir):
#     input_dir_list = []
#     input_dir_list.append(input_dir)
#     project_path_list = []
#     for single_path in input_dir_list:
#         for root, dirs, files in os.walk(single_path):
#             for name in files:
#                 if 'project' in name:
#                     project_path_list.append(os.path.join(root, name))
#     for single_project in project_path_list:
#         print(single_project)
#         split_to_yolo(single_project)
#     print("over")

def project2txt(input_dir):

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
            if regions != []:
                # print(file_name)
                for single_label_inf in regions:
                    label_index = labels.index(single_label_inf["region_attributes"][super_category])
                    label_w = single_label_inf["shape_attributes"]["width"]
                    label_h = single_label_inf["shape_attributes"]["height"]
                    # 将边框规范到图内
                    if label_w > im.width:
                        label_w = im.widt
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
                if 'project' in name:
                    project_path_list.append(os.path.join(root, name))
    for single_project in project_path_list:
        print(single_project)
        split_to_yolo(single_project)


if __name__ == "__main__":
    input_dir = r'E:\Desktop\bokelin\0811\yibiaozhu\1\1\164'
    project2txt(input_dir)
