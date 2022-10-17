import json
import os
import shutil
from pathlib import Path


#字典剪切（project）

class Cut_dict():
    def __init__(self, starting_point=None, End=None, filter_path=None, save_path=None):
        self.starting_point = starting_point
        self.End = End
        self.filter_path = filter_path
        self.save_path = save_path
        self.over = "over"

    def dict_cut_via(self):
        # save_path = os.path.join(filter_path, "cut")

        def dict_cut(ori_dict, start, end):
            slice_dict = {k: ori_dict[k] for k in list(ori_dict.keys())[start:end]}
            return slice_dict

        via_dict = json.load(open(os.path.join(self.filter_path, "via_project.json"), 'rb'))
        via_dict["_via_img_metadata"] = dict_cut(via_dict["_via_img_metadata"], self.starting_point, self.End)
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        with open(os.path.join(save_path, "via_project_new.json"), 'w') as f:
            json.dump(via_dict, f)

    def dict_img(self):
        via_dict = json.load(open(os.path.join(save_path, "via_project_new.json"), "rb"))
        count = 1
        for key in via_dict["_via_img_metadata"]:
            lif = (list([key])[0].split('jpg')[0] + 'jpg')
            for fil in os.listdir(filter_path):
                if lif == fil:
                    if lif.endswith(".jpg"):
                        filter_lif_path = os.path.join(filter_path, fil)
                        save_lif_path = os.path.join(save_path, fil)
                        if not os.path.exists(save_path):
                            os.mkdir(save_path)
                            shutil.copy2(filter_lif_path, save_lif_path)
                        else:
                            shutil.copy2(filter_lif_path, save_lif_path)
                            print(count)
                            count += 1


if __name__ == "__main__":
    filter_path = r'F:\医乐世\3\相机2'  # 原始数据路径
    save_path = r'F:\医乐世\3\相机2\tian'  # 保存文件路径
    # print("请输入原始数据路径")
    # filter_path = input()
    # print("请输入保存文件路径")
    # save_path = input()
    starting_point = 84  # 起点减1
    End = 150  # 终点
    worker = Cut_dict(filter_path=filter_path, save_path=save_path, starting_point=starting_point, End=End)
    worker.dict_cut_via()#切via，根据需求选择运行。
    worker.dict_img()  # 根据via查找并复制图片，根据需求选择运行。
    print(worker.over)  # 打印结束
