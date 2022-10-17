import json
import os

model_path = r'E:\Desktop\bokelin\0811\yibiaozhu\1\1\50\via_model_project.json'
label_path = r'E:\Desktop\bokelin\0811\yibiaozhu\1\1\50\via_logo_project.json'

def merge_project_by_label(model_path, label_path):
    model_via_project = json.load(open(model_path, 'rb'))
    model_via_img_metadata = model_via_project["_via_img_metadata"]
    label_via_project = json.load(open(label_path, 'rb'))
    label_via_img_metadata = label_via_project["_via_img_metadata"]

    for key, single_img_inf in label_via_img_metadata.items():
        label_file_name = key
        label_regions = single_img_inf["regions"]
        model_via_img_metadata[key]["regions"] += label_regions

        with open(model_path, 'w') as f:
            f.write(json.dumps(model_via_project))




