#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename:floders.py

import os
import numpy as np
import shutil
import cv2
import threading
import re


def bp2jpg_thr(file_path,output_file_path,KEEP_ORIGIN):
    def gen_list(file_path):
        listx = []
        i = 0
        for root, dirs, files in os.walk(file_path):
            for name in files:
                if '.bmp' or '.png' in name:
                    i += 1
                    listx.append([i, root, name])
        return listx

    # 图片转存jpg
    def save_threads(listx):
        len_list = len(listx)
        n = 1

        if not os.path.exists(output_file_path):
            os.mkdir(output_file_path)

        for i, root, name in listx:
            n += 1
            print('Process: %.4f' % (n / len_list))

            save_path2 = root.replace(str(file_path), str(output_file_path))
            # print(save_path2)


            img = cv2.imdecode(np.fromfile(os.path.join(root, name), dtype=np.uint8), 1)
            save_path = os.path.join(save_path2, name[:-3] + 'jpg')
            cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])[1].tofile(save_path)

            if not KEEP_ORIGIN:
                save_path = os.path.join(save_path2, name[:-3] + 'jpg')
                os.remove(os.path.join(root, name))
                cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])[1].tofile(save_path)


    for root0, dirs0, files0 in os.walk(file_path):
        for name in files0:
            split_path = root0.split('\\')
            dir_path = split_path[len(file_path.split('\\')):]
            a = ''
            for ii in dir_path:
                a += '\\' + ii
            save_path0 = output_file_path + a
            if (os.path.exists(save_path0)):
                shutil.rmtree(save_path0)
            os.makedirs(save_path0)


    num_threads = 16

    listx = gen_list(file_path)
    list_threads = np.array_split(listx, num_threads)

    threadpool = []
    for n in range(len(list_threads)):
        list_n = np.array(list_threads[n])
        t = threading.Thread(target=save_threads, args=(list_n,))
        threadpool.append(t)

    # 启动线程池
    for i in range(num_threads):
        threadpool[i].start()
    for i in range(num_threads):
        threadpool[i].join()

    print('finished....')

if __name__ == '__main__':
    file_path = r'E:\Desktop\123'  # 3
    output_file_path = r'E:\Desktop\125'
    bp2jpg_thr(file_path, output_file_path, KEEP_ORIGIN=True)