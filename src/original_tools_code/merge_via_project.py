# 合并不同路径下的project文件
import json
import os


def make_anno_info_per_img(via_file_list, output_dir):
    '''
    :param via_file_list: 存放路径的列表
    :param output_dir: 输出project的目录例如：./via_merge_project.json
    :return:
    '''
    via_project_file_names = []
    for via_file in via_file_list:
        for root, dirs, files in os.walk(via_file):
            for file in files:
                if "via_project.json" == file:
                    filename = file
                    via_project_file = os.path.join(root, filename)
                    via_project_file_names.append(via_project_file)
    merge_project(via_project_file_names, output_dir)


def merge_project(project_list, save_project_dir):
    '''
    :param project_list: 存放project的绝对路径的列表
    :param save_project_dir: 输出project的目录例如：./via_merge_project.json
    :return:
    '''
    img_metadata_merged = {}
    for single_project_file in project_list:
        via_project = json.load(open(single_project_file, 'rb'))
        via_img_metadata = via_project["_via_img_metadata"]
        img_metadata_merged.update(via_img_metadata)
        via_project_merged = json.load(open(single_project_file, 'rb'))
        via_project_merged["_via_img_metadata"] = img_metadata_merged
        with open(save_project_dir, 'w') as f:
            json.dump(via_project_merged, f)

def merga_via_project(via_file_list, output_dir):
    def merge_project(project_list, save_project_dir):
        '''
        :param project_list: 存放project的绝对路径的列表
        :param save_project_dir: 输出project的目录例如：./via_merge_project.json
        :return:
        '''
        img_metadata_merged = {}
        for single_project_file in project_list:
            via_project = json.load(open(single_project_file, 'rb'))
            via_img_metadata = via_project["_via_img_metadata"]
            img_metadata_merged.update(via_img_metadata)
            via_project_merged = json.load(open(single_project_file, 'rb'))
            via_project_merged["_via_img_metadata"] = img_metadata_merged
            with open(save_project_dir, 'w') as f:
                json.dump(via_project_merged, f)

    via_project_file_names = []
    for via_file in via_file_list:
        for root, dirs, files in os.walk(via_file):
            for file in files:
                if "via_project.json" == file:
                    filename = file
                    via_project_file = os.path.join(root, filename)
                    via_project_file_names.append(via_project_file)
    output_dir = output_dir + "/via_merge_project.json"
    merge_project(via_project_file_names, output_dir)




if __name__ == "__main__":
    via_file_list = [r'E:\Desktop\bokelin\0811\yibiaozhu']
    output_dir = r'E:\Desktop\bokelin\0811\yibiaozhu'
    # make_anno_info_per_img(via_file_list, output_dir)
    merga_via_project(via_file_list, output_dir)