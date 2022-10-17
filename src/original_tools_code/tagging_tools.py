import os
import cv2
import numpy as np
import threading
import json
import shutil


def bp2jpg_thr0(file_path,output_file_path,KEEP_ORIGIN):

    def gen_list(file_path):
        listx = []
        i = 0
        for root, dirs, files in os.walk(file_path):
            for name in files:
                print(name)
                if '.bmp' or '.png' in name:
                    i += 1
                    listx.append([i, root, name])
        return listx

    # 图片转存jpg
    def save_threads(listx, save_path0):
        len_list = len(listx)
        n = 1

        if not os.path.exists(output_file_path):
            os.mkdir(output_file_path)

        for root0, dirs0, files0 in os.walk(file_path):
            for j in files0:
                split_path = root0.split('\\')
                dir_path = split_path[len(file_path.split('\\')):]
                a = ''
                for ii in dir_path:
                    a += '\\' + ii
                # print(a)
                save_path0 = output_file_path + a
                if (os.path.exists(save_path0)):
                    shutil.rmtree(save_path0)
                os.makedirs(save_path0)

        for i, root, name in listx:
            n += 1
            print('Process: %.4f' % (n / len_list))
            img = cv2.imdecode(np.fromfile(os.path.join(root, name), dtype=np.uint8), 1)

            # save_path0 = os.path.join(root, name[:-3] + 'jpg')
            # if not os.path.exists(save_path0):
            #     os.mkdir(save_path0)

            save_path = os.path.join(save_path0, name[:-3] + 'jpg')
            cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])[1].tofile(save_path)


            if not KEEP_ORIGIN:
                save_path = os.path.join(save_path0, name[:-3] + 'jpg')
                os.remove(os.path.join(root, name))
                cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])[1].tofile(save_path)


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
            # if (os.path.exists(save_path0)):
            #     shutil.rmtree(save_path0)
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

#coco转project
def coco2project(root_path):
    coco_path = root_path + r'\via_export_coco.json'
    img_path = root_path
    save_path = root_path + r'\via_project.json'

    imageIdName = {}
    classIdName = {}
    via_img_metadata = {}
    options = {}
    regions = []

    with open(coco_path, 'r', encoding='utf-8') as f :
        coco_data = json.load(f)

    for image_info in coco_data['images'] :
        imageIdName[image_info['id']] = image_info['file_name']

    for class_info in coco_data['categories'] :
        classIdName[class_info['id']] = class_info['name']

    for num, cla in classIdName.items() :
        options[cla] = ''

    via_attributes = {
        "region": {
          "fitow": {
            "type": "dropdown",
            "description": "",
            "options": options,
            "default_options": { "": "true" }
          }
        },
        "file": {}
      }

    via_settings = {
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
            "region_label": "fitow",
            "region_color": "fitow",
            "region_label_font": "10px Sans",
            "on_image_annotation_editor_placement": "NEAR_REGION"
          }
        },
        "core": {
          "buffer_size": 18,
          "filepath": {},
          "default_filepath": ""
        },
        "project": { "name": "via_project" }
      }

    oldID = -1
    for ann in coco_data['annotations'] :
        nowID = ann['image_id']
        if nowID != oldID :
            for num_null in range(int(nowID) - int(oldID) - 1, -1 , -1) :
                if num_null != 0 :
                    print(num_null)
                filename = imageIdName[int(nowID) - num_null]
                imageSize = os.path.getsize(os.path.join(img_path, filename))
                viaDataName = filename + str(imageSize)
                via_img_metadata[viaDataName] = {
                        "filename": filename,
                        "size": imageSize,
                        "regions": [],
                        "file_attributes": {}
                        }
        oldID = nowID
        filename = imageIdName[int(nowID) - num_null]
        imageSize = os.path.getsize(os.path.join(img_path, filename))
        viaDataName = filename + str(imageSize)
        attribute = {
              "shape_attributes": {
                "name": "rect",
                "x": ann['bbox'][0],
                "y": ann['bbox'][1],
                "width": ann['bbox'][2],
                "height": ann['bbox'][3]
              },
              "region_attributes": { "fitow": classIdName[ann['category_id']] }
            }
        via_img_metadata[viaDataName]['regions'].append(attribute)

    via = {
        '_via_settings' : via_settings,
        '_via_img_metadata' : via_img_metadata,
        '_via_attributes' : via_attributes
    }

    with open(save_path, 'w', encoding='utf_8') as f :
        json.dump(via, f)



if __name__ == '__main__':
    bp2jpg_thr(r'E:\Desktop\123',r'E:\Desktop\jpg', KEEP_ORIGIN=True)
    # coco2project(r'E:\Desktop\123')
