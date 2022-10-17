import cv2
import numpy as np
import json
import os

class Split():

    def __init__(self,work_dir ):
        self.work_dir = work_dir

        self.split_range_x = [0, 2016, 4096, 6144, 8192, 8192+2048, 8192+4096, 8192+6112, 8192+8192]  # 15606   16384
        # self.split_range_x = [0, 16384]


        # self.split_range_s1 = [0, 12288]  # 22032,24480,25000     21681        22528,24576,25000        ,22000
        # self.split_range_s2 = [12288, 20480]
        self.split_range_s1 = [0, 2048, 4096, 6176, 8256, 10208, 12288]  # 22032,24480,25000     21681        22528,24576,25000        ,22000
        self.split_range_s2 = [12288+0, 12288+2048, 12288+4096, 12288+6176, 12288+8192]




        # self.output_path = os.path.join(self.work_dir,"size_test")
        # if not os.path.exists(self.output_path): #判断路径下文件是否存在
        #     os.mkdir(self.output_path)  #用于以数字权限模式创建目录  os.mkdir(path[, mode])  path -- 要创建的目录，可以是相对或者绝对路径。mode -- 要为目录设置的权限数字模式。

    def split_image(self):
        images_name = os.listdir(self.work_dir)
        for each_image in images_name:
            print(each_image)
            if each_image.endswith(".jpg"):
                # output_path = os.path.join(self.work_dir, each_image[:-4]+"_rows")
                output_path = os.path.join(self.work_dir, "split")
                if not os.path.exists(output_path):
                    os.mkdir(output_path)

                image_np = cv2.imdecode(np.fromfile(os.path.join(self.work_dir, each_image), dtype=np.uint8), 1)
                for j in range(len(self.split_range_s1) - 1):
                    for i in range(len(self.split_range_x) - 1):  # len()返回字符串、列表、字典、元组等长度 range()连续增加整数生成参数列表
                        print(i)

                        image_np_split = image_np[self.split_range_s1[j]:self.split_range_s1[j + 1],
                                         self.split_range_x[i]:self.split_range_x[i + 1], :]

                        print(j)
                        cv2.imencode('.jpg', image_np_split)[1].tofile(
                            os.path.join(output_path,
                                         "{}.jpg".format(each_image[:-4] + "_" + str(j) + "_" + str(i))))

                for j1 in range(len(self.split_range_s2) - 1):
                    for i in range(len(self.split_range_x) - 1):  # len()返回字符串、列表、字典、元组等长度 range()连续增加整数生成参数列表
                        print(i)

                        image_np_split = image_np[self.split_range_s2[j1]:self.split_range_s2[j1 + 1],
                                         self.split_range_x[i]:self.split_range_x[i + 1], :]
                        print(j1)
                        cv2.imencode('.jpg', image_np_split)[1].tofile(
                            os.path.join(output_path, "{}.jpg".format(
                                each_image[:-4] + '111' + "_" + str(j1) + "_" + str(i))))

                    # print(self.split_range[i])
                    # print(self.split_range[i + 1])

"""
                for i1 in range(len(self.split_range_x1) - 1):  # len()返回字符串、列表、字典、元组等长度 range()连续增加整数生成参数列表
                    print(i1)
                    for j1 in range(len(self.split_range_1) - 1):
                        # print(len(self.split_range))
                        # print(range(len(self.split_range)-1))

                        image_np_split_1 = image_np[self.split_range_1[j1]:self.split_range_1[j1 + 1],self.split_range_x1[i1]:self.split_range_x1[i1 + 1], :]
                        # print(image_np_split)
                        print(j1)
                        # print(self.split_range_x1[i1])
                        # print(self.split_range_x1[i1 + 1])
                        # print(self.split_range[i])
                        # print(self.split_range[i + 1])
                        cv2.imencode('.jpg', image_np_split_1)[1].tofile(os.path.join(self.output_path, "{}.jpg".format(each_image[:-4] + "_"+str(10) + str(i1) + "_"+str(10)+str(j1))))
                    # print(self.split_range_1 [i1])
                    # print(self.split_range_1[i1 + 1])
"""


if __name__ == "__main__":
    worker = Split(r"F:\project\gbdz\gbdzqtcs\0815_578\3")
    worker.split_image()