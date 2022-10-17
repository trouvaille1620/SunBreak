import json
import os

#coco转project

# coco_path = r'E:\Desktop\gangban\yibiaozhu\本来想早点给你的\via_export_coco.json'
# img_path = r'E:\Desktop\gangban\yibiaozhu\本来想早点给你的'
# save_path = r'E:\Desktop\gangban\yibiaozhu\本来想早点给你的\via_project.json'


# imageIdName = {}
# classIdName = {}
# via_img_metadata = {}
# options = {}
# regions = []
#
# with open(coco_path, 'r', encoding='utf-8') as f :
#     coco_data = json.load(f)
#
# for image_info in coco_data['images'] :
#     imageIdName[image_info['id']] = image_info['file_name']
#
# for class_info in coco_data['categories'] :
#     classIdName[class_info['id']] = class_info['name']
#
# for num, cla in classIdName.items() :
#     options[cla] = ''
#
# via_attributes = {
#     "region": {
#       "fitow": {
#         "type": "dropdown",
#         "description": "",
#         "options": options,
#         "default_options": { "": "true" }
#       }
#     },
#     "file": {}
#   }
#
# via_settings = {
#     "ui": {
#       "annotation_editor_height": 25,
#       "annotation_editor_fontsize": 0.8,
#       "leftsidebar_width": 18,
#       "image_grid": {
#         "img_height": 80,
#         "rshape_fill": "none",
#         "rshape_fill_opacity": 0.3,
#         "rshape_stroke": "yellow",
#         "rshape_stroke_width": 2,
#         "show_region_shape": True,
#         "show_image_policy": "all"
#       },
#       "image": {
#         "region_label": "fitow",
#         "region_color": "fitow",
#         "region_label_font": "10px Sans",
#         "on_image_annotation_editor_placement": "NEAR_REGION"
#       }
#     },
#     "core": {
#       "buffer_size": 18,
#       "filepath": {},
#       "default_filepath": ""
#     },
#     "project": { "name": "via_project" }
#   }
#
# oldID = -1
# for ann in coco_data['annotations'] :
#     nowID = ann['image_id']
#     if nowID != oldID :
#         for num_null in range(int(nowID) - int(oldID) - 1, -1 , -1) :
#             if num_null != 0 :
#                 print(num_null)
#             filename = imageIdName[int(nowID) - num_null]
#             imageSize = os.path.getsize(os.path.join(img_path, filename))
#             viaDataName = filename + str(imageSize)
#             via_img_metadata[viaDataName] = {
#                     "filename": filename,
#                     "size": imageSize,
#                     "regions": [],
#                     "file_attributes": {}
#                     }
#     oldID = nowID
#     filename = imageIdName[int(nowID) - num_null]
#     imageSize = os.path.getsize(os.path.join(img_path, filename))
#     viaDataName = filename + str(imageSize)
#     attribute = {
#           "shape_attributes": {
#             "name": "rect",
#             "x": ann['bbox'][0],
#             "y": ann['bbox'][1],
#             "width": ann['bbox'][2],
#             "height": ann['bbox'][3]
#           },
#           "region_attributes": { "fitow": classIdName[ann['category_id']] }
#         }
#     via_img_metadata[viaDataName]['regions'].append(attribute)
#
# via = {
#     '_via_settings' : via_settings,
#     '_via_img_metadata' : via_img_metadata,
#     '_via_attributes' : via_attributes
# }
#
# with open(save_path, 'w', encoding='utf_8') as f :
#     json.dump(via, f)

def coco2project(coco_path):

    img_path = os.path.dirname(coco_path)
    save_path = os.path.join(img_path, 'via_project888.json')

    imageIdName = {}
    classIdName = {}
    via_img_metadata = {}
    options = {}
    regions = []

    with open(coco_path, 'r', encoding='utf-8') as f:
        coco_data = json.load(f)

    for image_info in coco_data['images']:
        imageIdName[image_info['id']] = image_info['file_name']

    for class_info in coco_data['categories']:
        classIdName[class_info['id']] = class_info['name']

    for num, cla in classIdName.items():
        options[cla] = ''

    via_attributes = {
        "region": {
            "fitow": {
                "type": "dropdown",
                "description": "",
                "options": options,
                "default_options": {"": "true"}
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
        "project": {"name": "via_project"}
    }

    oldID = -1
    for ann in coco_data['annotations']:
        nowID = ann['image_id']
        if nowID != oldID:
            for num_null in range(int(nowID) - int(oldID) - 1, -1, -1):
                if num_null != 0:
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
            "region_attributes": {"fitow": classIdName[ann['category_id']]}
        }
        via_img_metadata[viaDataName]['regions'].append(attribute)

    via = {
        '_via_settings': via_settings,
        '_via_img_metadata': via_img_metadata,
        '_via_attributes': via_attributes
    }

    with open(save_path, 'w', encoding='utf_8') as f:
        json.dump(via, f)

    # save_path1 = save_path.replace("/", "\\")
    # QApplication.processEvents()  # 刷新界面
    # self.log.append(f'转换已完成，保存至\n{save_path1}')

if __name__ in "__main__":
    coco_path = r'E:\Desktop\gangban\2_标注图像\本来想早点给你的\via_export_coco.json'
    coco2project(coco_path)



