import json
import os

def statistics_project(filter_path, save_path):

    file_name_list = []

    via_project = json.load(open(filter_path, 'rb'))
    metadata = via_project["_via_img_metadata"]

    for each_img in metadata.values():
        each_filename = each_img["filename"]

        for each_region_attributes in each_img["regions"]:
            sa = each_region_attributes["region_attributes"]
            if sa["fitow"] == '':
                file_name_list.append(each_filename)
                file_name_list = list(set(file_name_list))
    print(file_name_list)
    with open(os.path.join(save_path, 'check.txt'), 'w') as file:
        for img in file_name_list:
            file.write(img + '\n')
                # with open(os.path.join(save_path, 'check.txt'), 'w') as file:
                #     file.write()

    #         for each_cat in sa.values():
    #             cat_list.append(each_cat)
    # for each_region in attributes.values():
    #     # print(each_region)
    #     for catgry in each_region.values():
    #         # print(catgry)
    #         for keys, values in catgry["options"].items():
    #             # print(keys)
    #             cat_id_list.append(keys)
    # # print(cat_id_list)
    # for cat_id in cat_id_list:
    #     elm_count = cat_list.count(cat_id)
    #     id_list.append(cat_id)
    #     id_quantity.append(elm_count)
    # print(id_list)
    # print(id_quantity)
    # print(f'图片总数： {len(file_name_list)}')
    # for label, num in zip(id_list, id_quantity):
    #     print('label:', label, '\t','num:', num)


if __name__ == "__main__":
    filter_path = r"E:\Desktop\bokelin\0811\yibiaozhu\50\via_project_test.json"
    save_path = r'E:\Desktop\bokelin\0811\yibiaozhu\50'
    statistics_project(filter_path, save_path)