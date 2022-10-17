from peewee import *
import os
import logging
import json
import tqdm
import time
import subprocess
"""
功能定级
无 单文件夹操作
v2 多文件夹操作

"""

logger = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
DB_PATH = './works.db'

#数据库相关的工具类，各种奇怪工具的集合，使用时实例化后调取
class DataBaseTool():

    def __init__(self):
        pass

    #===========================================以下是单文件夹操作==============================================#
    #基本工具，获得单文件夹下文件数目和名字列表 返回：文件个数 和 文件名字列表[]
    def get_folder_info(self , path):
        file_list = os.listdir(path)
        file_numbers = len(file_list)
        logger.info("数据工具——获取文件夹信息——文件数：{}".format(file_numbers))
        return file_numbers , file_list

    #基本工具，先判断文件夹下是否有via出来的文件，返回via是否存在bool,分别是project和coco
    def if_via_exists(self, path ):
        file_list = os.listdir(path)
        if_project_exists = "via_project.json" in file_list
        if_coco_exists = "via_export_coco.json" in file_list
        logger.info("数据工具——判断文件夹标注文件是否存在——project:{}, coco:{}".format(if_project_exists, if_coco_exists))
        return if_project_exists , if_coco_exists

    #基本工具，返回路径下via_project的路径
    def get_via_project_path(self , path):
        via , coco = self.if_via_exists(path)
        if via:
            logger.info("数据工具——获取via_project路径——{}".format(os.path.join(path,"via_project")))
            return os.path.join(path,"via_project")
        else:
            logger.info("数据工具——获取via_project路径——路径下无可获取文件")

    #基本工具，返回路径下via_export_coco的路径
    def get_via_export_coco_path(self , path):
        via, coco = self.if_via_exists(path)
        if coco:
            logger.info("数据工具——获取via_export_coco路径——{}".format(os.path.join(path,"via_project")))
            return os.path.join(path,"via_export_coco.json")
        else:
            logger.info("数据工具——获取via_export_coco路径——路径下无可获取文件")

    #===========================================V2: 以下是多子文件夹操作==============================================#
    # 基本工具，用于获得数据集的结构，快速注册数据集
    def get_folder_info_v2(self, path): #使用os.walk进行遍历，root每次进入一个文件夹内部，dirs总是文件夹下文件夹的名字列表，files总是文件夹下文件的名字
        t1 = time.time()
        root = []
        t2 = time.time()
        print(t2 -t1 )

    #遍历复合大文件专用，多进程遍历
    def IterateFiles_CMD(self, directory):
        t1 = time.time()
        assert os.path.isdir(directory), 'make sure directory argument should be a directory'
        cmd = 'dir /s /B /A-D ' + directory
        ret = []
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for line in p.stdout.readlines():
            ret.append(line)
        t2 = time.time()
        print(t2-t1)
        if p.wait() == 0:
            return ret

    # 基本工具，先判断文件夹下是否有via出来的文件，返回via是否存在bool,分别是project和coco
    def if_via_exists_v2(self, path):
        file_list = os.listdir(path)
        if_project_exists = "via_project.json" in file_list
        if_coco_exists = "via_export_coco.json" in file_list
        logger.info("数据工具——判断文件夹标注文件是否存在——project:{}, coco:{}".format(if_project_exists, if_coco_exists)) #
        return if_project_exists, if_coco_exists

    # 基本工具，返回路径下via_project的路径
    def get_via_project_path_v2(self, path):
        via, coco = self.if_via_exists(path)
        if via:
            logger.info("数据工具——获取via_project路径——{}".format(os.path.join(path, "via_project")))
            return os.path.join(path, "via_project")
        else:
            logger.info("数据工具——获取via_project路径——路径下无可获取文件")

    # 基本工具，返回路径下via_export_coco的路径
    def get_via_export_coco_path_v2(self, path):
        via, coco = self.if_via_exists(path)
        if coco:
            logger.info("数据工具——获取via_export_coco路径——{}".format(os.path.join(path, "via_project")))
            return os.path.join(path, "via_export_coco.json")
        else:
            logger.info("数据工具——获取via_export_coco路径——路径下无可获取文件")

if __name__ == "__main__":
    worker = DataBaseTool()
    worker.get_folder_info_v2(r"G:\项目文件\FT210020_医乐世\进场后数据\训练数据")