import json
import os


coco_json = json.load(open(r"F:\数据\新建文件夹\数据\目标检测\威卡威\ng\via_export_coco.json","rb"))
annotations = coco_json["annotations"]
for i,each_anno in enumerate(annotations):
    new_seg = []
    each_anno_image_id = int(each_anno["image_id"])
    annotations[i]["image_id"] = each_anno_image_id
    new_seg.append(each_anno["segmentation"])
    annotations[i]["segmentation"] = new_seg
coco_json["annotations"] = annotations

with open(r"F:\数据\新建文件夹\数据\目标检测\威卡威\ng\via_export_coco_normal.json", 'w') as f:
    json.dump(coco_json, f)

def via_coco2normal_coco(input_dir, output_dir):

    coco_json = json.load(open(input_dir, "rb"))
    annotations = coco_json["annotations"]
    for i, each_anno in enumerate(annotations):
        new_seg = []
        each_anno_image_id = int(each_anno["image_id"])
        annotations[i]["image_id"] = each_anno_image_id
        new_seg.append(each_anno["segmentation"])
        annotations[i]["segmentation"] = new_seg
    coco_json["annotations"] = annotations

    with open(os.path.join(output_dir, "via_export_coco_normal.json"), 'w') as f:
        json.dump(coco_json, f)