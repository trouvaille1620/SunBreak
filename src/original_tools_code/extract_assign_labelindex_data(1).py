# -*- encoding: utf-8 -*-
"""
取出单独标签
"""

import shutil
import os

input_dir = r'D:\data\Pmg\新建文件夹'
output_dir = r'D:\data\Pmg\新建文件夹\3'
label_index = '2'  # yololabel索引

os.makedirs(output_dir,exist_ok=True)

for root, dirs, files in os.walk(input_dir):
    for name in files:
        if '.txt' in name:
            try:
                with open(root +'/'+ name) as f:
                    label_list = f.readlines()
                    for single_label in label_list:
                        if single_label.split()[0] == label_index:
                            shutil.copy(root +'/'+ name, output_dir)
                            shutil.copy(root +'/'+ name[:-3] + 'jpg', output_dir)
                            # print((root +'/'+ name))
                            break
            except:
                Exception()
