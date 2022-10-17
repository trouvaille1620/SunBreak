# -*- encoding: utf-8 -*-
"""
取出单独标签
"""

import shutil
import os

input_dir = r'E:\Desktop\bokelin\0811\yibiaozhu\50'
output_dir = r'E:\Desktop\bokelin\0811\yibiaozhu\50_2'
label_num = 5  # yololabel索引

# os.makedirs(output_dir,exist_ok=True)

for category in range(0, label_num):
    save_path = os.path.join(output_dir, str(category))
    os.makedirs(save_path, exist_ok=True)

for root, dirs, files in os.walk(input_dir):
    for name in files:
        if '.txt' in name:
            with open(root + '/' + name) as f:
                label_list = f.readlines()
                for single_label in label_list:
                    save_path = os.path.join(output_dir, str(single_label.split(' ')[0]))
                    shutil.copy(root + '/' + name, save_path)
                    shutil.copy(root + '/' + name[:-3] + 'jpg', save_path)


                        # print(single_label.split(' ')[0])
                        # if single_label.split(' ')[0] == category:
                        #     shutil.copy(root + '/' + name, save_path)
                        #     shutil.copy(root + '/' + name[:-3] + 'jpg', save_path)
