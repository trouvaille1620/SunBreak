import datetime
import json
import os
from PIL import Image
#project转coco


def get_all_project_path_list(input_dir):
    """
    获取输入文件夹下所有via_project.json的绝对路径，用于批量处理。
    :param input_dir: 输入目录，包含所有待转换的via_project.json，允许存在多层文件夹。
    :return: 所有via_project.json的路径列表。
    """
    via_project_path_list = []
    for root, dirs, files in os.walk(input_dir):
        for each_file in files:
            if 'project' in each_file and each_file.endswith('.json'):
                via_project_path_list.append(os.path.join(root, each_file))
    return via_project_path_list


def convert_via_project_to_coco(via_project_input_path, image_dir='', via_coco_output_path=''):
    """
    将via_project.json转换为via_export_coco.json，同时检测via_project.json中的图片是否存在缺失。
    :param via_project_input_path: 输入的via_project.json的路径。
    :param image_dir: 输入的图片目录，如果未指定，默认为via_project.json的同级目录。
    :param via_coco_output_path: 输出的via_export_coco.json的路径，如果未指定，默认为via_project.json的同级目录+via_export_coco.json。
    :return:
    """
    # 如果image_dir为空，默认输入图片路径为via_project.json的同级目录。
    if not image_dir:
        image_dir = os.path.dirname(via_project_input_path)
    # 如果via_coco_output_path为空，默认输出via_export_coco.json的目录为via_project.json的同级目录。
    if not via_coco_output_path:
        via_coco_output_path = os.path.join(os.path.dirname(via_project_input_path), 'via_export_coco.json')

    print(f'开始处理: {via_project_input_path}')
    now_datetime = datetime.datetime.now()
    images_list = []
    annotations_list = []
    categories_list = []
    with open(via_project_input_path, 'r', encoding='utf-8') as f:
        project_dict = json.load(f)
        supercategory = list(project_dict['_via_attributes']['region'].keys())[0]
        options_list = list(list(project_dict['_via_attributes']['region'].values())[0]['options'].keys())
        for i in range(len(options_list)):
            each_category_dict = {
                'id': i + 1,
                'name': options_list[i],
                'supercategory': supercategory
            }
            categories_list.append(each_category_dict)
        image_id = 0
        annotation_id = 0
        for each_val in project_dict['_via_img_metadata'].values():
            print(f"正在处理第{image_id + 1}张图片 {each_val['filename']}")
            image_path = os.path.join(image_dir, each_val['filename'])
            try:
                img = Image.open(image_path)
            except:
                # TODO 使用日志系统，替换print
                print(f'图片不存在或者无法读取，图片路径为{image_path}')
                raise Exception('读取图片发生错误。')

            w, h = img.size
            each_image_dict = {
                'id': image_id,
                'width': w,
                'height': h,
                'file_name': each_val['filename'],
                'license': 1,
                'date_captured': ''
            }
            images_list.append(each_image_dict)

            for each_region in each_val['regions']:
                if 'x' in each_region['shape_attributes']:
                    x = each_region['shape_attributes']['x']
                    y = each_region['shape_attributes']['y']
                    width = each_region['shape_attributes']['width']
                    height = each_region['shape_attributes']['height']
                else:
                    all_points_x_list = each_region['shape_attributes']['all_points_x']
                    all_points_y_list = each_region['shape_attributes']['all_points_y']
                    x = min(all_points_x_list)
                    y = min(all_points_y_list)
                    width = max(all_points_x_list) - x
                    height = max(all_points_y_list) - y
                    if width <= 0 or height <= 0:
                        # TODO 使用日志系统，替换print
                        print('异常的标注框：')
                        print(each_val['filename'])
                        print(all_points_x_list)

                # print("{} 超类 {}".format(each_region['region_attributes'], supercategory))
                each_annotation_dict = {
                    'id': annotation_id,
                    'image_id': str(image_id),
                    'category_id': options_list.index(each_region['region_attributes'][supercategory]) + 1,
                    # TODO segmentation为bbox格式，如果使用mask需要修改segmentation
                    'segmentation': [x, y, x + width, y, x + width, y + height, x, y + height],
                    'area': width * height,
                    'bbox': [x, y, width, height],
                    'iscrowd': 0  # TODO iscrow目前固定为0
                }

                annotations_list.append(each_annotation_dict)
                annotation_id += 1
            image_id += 1

    via_export_coco_dict = {
        'info': {
            'year': int(now_datetime.year),
            'version': '1',
            'description': 'Exported using VGG Image Annotator (http://www.robots.ox.ac.uk/~vgg/software/via/)',
            'contributor': '',
            'url': 'http://www.robots.ox.ac.uk/~vgg/software/via/',
            'date_created': now_datetime.strftime('%a %b %d %Y %H:%M:%S GMT+0800')
        },
        'images': images_list,
        'annotations': annotations_list,
        'licenses': [{
            'id': 1,
            'name': 'Unknown',
            'url': ''
        }],
        'categories': categories_list
    }

    with open(via_coco_output_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(via_export_coco_dict, ensure_ascii=False))
    print(f'转换已完成，保存至 {via_coco_output_path}')


def batch_convert_via_project_to_coco(input_dir):
    """
    将输入文件夹下的所有via_project.json转换为via_export_coco.json。
    使用批量处理，需要保证via_project.json和其下所有图片处于相同路径下。
    :param input_dir: 输入目录，包含所有待转换的via_project.json，允许存在多层文件夹。
    :return:
    """
    all_project_path_list = get_all_project_path_list(input_dir)
    for each_project_path in all_project_path_list:
        convert_via_project_to_coco(each_project_path)

def project2coco(input_dir):

    def get_all_project_path_list(input_dir):
        """
        获取输入文件夹下所有via_project.json的绝对路径，用于批量处理。
        :param input_dir: 输入目录，包含所有待转换的via_project.json，允许存在多层文件夹。
        :return: 所有via_project.json的路径列表。
        """
        via_project_path_list = []
        for root, dirs, files in os.walk(input_dir):
            for each_file in files:
                if 'project' in each_file and each_file.endswith('.json'):
                    via_project_path_list.append(os.path.join(root, each_file))
        return via_project_path_list

    def convert_via_project_to_coco(via_project_input_path, image_dir='', via_coco_output_path=''):
        """
        将via_project.json转换为via_export_coco.json，同时检测via_project.json中的图片是否存在缺失。
        :param via_project_input_path: 输入的via_project.json的路径。
        :param image_dir: 输入的图片目录，如果未指定，默认为via_project.json的同级目录。
        :param via_coco_output_path: 输出的via_export_coco.json的路径，如果未指定，默认为via_project.json的同级目录+via_export_coco.json。
        :return:
        """
        # 如果image_dir为空，默认输入图片路径为via_project.json的同级目录。
        if not image_dir:
            image_dir = os.path.dirname(via_project_input_path)
        # 如果via_coco_output_path为空，默认输出via_export_coco.json的目录为via_project.json的同级目录。
        if not via_coco_output_path:
            via_coco_output_path = os.path.join(os.path.dirname(via_project_input_path), 'via_export_coco.json')

        print(f'开始处理: {via_project_input_path}')
        now_datetime = datetime.datetime.now()
        images_list = []
        annotations_list = []
        categories_list = []
        with open(via_project_input_path, 'r', encoding='utf-8') as f:
            project_dict = json.load(f)
            supercategory = list(project_dict['_via_attributes']['region'].keys())[0]
            options_list = list(list(project_dict['_via_attributes']['region'].values())[0]['options'].keys())
            for i in range(len(options_list)):
                each_category_dict = {
                    'id': i + 1,
                    'name': options_list[i],
                    'supercategory': supercategory
                }
                categories_list.append(each_category_dict)
            image_id = 0
            annotation_id = 0
            for each_val in project_dict['_via_img_metadata'].values():
                print(f"正在处理第{image_id + 1}张图片 {each_val['filename']}")
                image_path = os.path.join(image_dir, each_val['filename'])
                try:
                    img = Image.open(image_path)
                except:
                    # TODO 使用日志系统，替换print
                    print(f'图片不存在或者无法读取，图片路径为{image_path}')
                    raise Exception('读取图片发生错误。')

                w, h = img.size
                each_image_dict = {
                    'id': image_id,
                    'width': w,
                    'height': h,
                    'file_name': each_val['filename'],
                    'license': 1,
                    'date_captured': ''
                }
                images_list.append(each_image_dict)

                for each_region in each_val['regions']:
                    if 'x' in each_region['shape_attributes']:
                        x = each_region['shape_attributes']['x']
                        y = each_region['shape_attributes']['y']
                        width = each_region['shape_attributes']['width']
                        height = each_region['shape_attributes']['height']
                    else:
                        all_points_x_list = each_region['shape_attributes']['all_points_x']
                        all_points_y_list = each_region['shape_attributes']['all_points_y']
                        x = min(all_points_x_list)
                        y = min(all_points_y_list)
                        width = max(all_points_x_list) - x
                        height = max(all_points_y_list) - y
                        if width <= 0 or height <= 0:
                            # TODO 使用日志系统，替换print
                            print('异常的标注框：')
                            print(each_val['filename'])
                            print(all_points_x_list)

                    # print("{} 超类 {}".format(each_region['region_attributes'], supercategory))
                    each_annotation_dict = {
                        'id': annotation_id,
                        'image_id': str(image_id),
                        'category_id': options_list.index(each_region['region_attributes'][supercategory]) + 1,
                        # TODO segmentation为bbox格式，如果使用mask需要修改segmentation
                        'segmentation': [x, y, x + width, y, x + width, y + height, x, y + height],
                        'area': width * height,
                        'bbox': [x, y, width, height],
                        'iscrowd': 0  # TODO iscrow目前固定为0
                    }

                    annotations_list.append(each_annotation_dict)
                    annotation_id += 1
                image_id += 1

        via_export_coco_dict = {
            'info': {
                'year': int(now_datetime.year),
                'version': '1',
                'description': 'Exported using VGG Image Annotator (http://www.robots.ox.ac.uk/~vgg/software/via/)',
                'contributor': '',
                'url': 'http://www.robots.ox.ac.uk/~vgg/software/via/',
                'date_created': now_datetime.strftime('%a %b %d %Y %H:%M:%S GMT+0800')
            },
            'images': images_list,
            'annotations': annotations_list,
            'licenses': [{
                'id': 1,
                'name': 'Unknown',
                'url': ''
            }],
            'categories': categories_list
        }

        with open(via_coco_output_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(via_export_coco_dict, ensure_ascii=False))
        print(f'转换已完成，保存至 {via_coco_output_path}')

    """
    将输入文件夹下的所有via_project.json转换为via_export_coco.json。
    使用批量处理，需要保证via_project.json和其下所有图片处于相同路径下。
    :param input_dir: 输入目录，包含所有待转换的via_project.json，允许存在多层文件夹。
    :return:
    """
    all_project_path_list = get_all_project_path_list(input_dir)
    for each_project_path in all_project_path_list:
        convert_via_project_to_coco(each_project_path)

if __name__ == '__main__':
    # input_path = r'\\192.168.1.5\fitow_12T_2\大众铝筏板\数据\066b\已训练标注数据\guangdufa\铝阀板_zhengmian_v5.0_20210222_郑长禹_272\via_project.json'
    # convert_via_project_to_coco(input_path)
    input_dir = r'E:\Desktop\bokelin\0811\yibiaozhu\1'
    project2coco(input_dir)
    # batch_convert_via_project_to_coco(input_dir)