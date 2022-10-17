import os
import json
import shutil
import numpy as np
import pandas as pd
from collections import Counter

"""
统计project中各标签数量
"""


def statistics_project(filter_path):
    cat_list = []
    file_name_list = []
    cat_id_list = []
    id_list = []
    id_quantity = []
    via_project = json.load(open(os.path.join(filter_path, "via_project.json"), 'rb'))
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
        # print(each_region)
        for catgry in each_region.values():
            # print(catgry)
            for keys, values in catgry["options"].items():
                # print(keys)
                cat_id_list.append(keys)
    # print(cat_id_list)
    for cat_id in cat_id_list:
        elm_count = cat_list.count(cat_id)
        id_list.append(cat_id)
        id_quantity.append(elm_count)
    # print(id_list)
    # print(id_quantity)
    print(f'图片总数： {len(file_name_list)}')
    for label, num in zip(id_list, id_quantity):
        print('label:', label, '\t','num:', num)


if __name__ == "__main__":
    filter_path = r"\\10.10.1.21\fitow_12T\TFT2020039_yaopin\yibiaozhu\pingdi\20220402"
    statistics_project(filter_path)
