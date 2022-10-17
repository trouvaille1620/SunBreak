# -*- encoding: utf-8 -*-
"""
删除project中某类标签
"""
import json
import os


def det_label(input_dir,label):
    for via_file in input_dir:
        for root, dirs, files in os.walk(via_file):
            for file in files:
                if "via_project.json" == file:
                    with open(os.path.join(root,file), encoding='UTF-8')as f:
                        result_list = json.load(f)
                        imgs_list=result_list["_via_img_metadata"]
                        for i in imgs_list:
                            new_img_regions=[]
                            for index,img_info in enumerate(imgs_list[i]["regions"]):
                                if list(img_info["region_attributes"].items())[0][1] not in label:
                                    new_img_regions.append(imgs_list[i]["regions"][index])
                            result_list["_via_img_metadata"][i]["regions"] = new_img_regions

                        # project_label_list = result_list["_via_attributes"]["region"].values()[0]["options"]

                        project_label_list = list(result_list["_via_attributes"]["region"].values())[0]["options"]
                        new_options = {}
                        for sigle_label in project_label_list.keys():
                            if sigle_label not in label:
                                new_options[sigle_label] = ''
                                last_name = sigle_label
                        list(result_list["_via_attributes"]["region"].values())[0]["options"] = new_options
                        list(result_list["_via_attributes"]["region"].values())[0]["default_options"] = {last_name:True}

                    # with open(output_dir,"w") as f:
                    with open(os.path.join(root,"via_new_project.json"),"w") as f:
                        f.write(json.dumps(result_list,indent=4,ensure_ascii=False))


if __name__=="__main__":
    label = ['hd']
    input_dir = [r'E:\Desktop\bokelin\0811\yibiaozhu\50']
    det_label(input_dir,label)
