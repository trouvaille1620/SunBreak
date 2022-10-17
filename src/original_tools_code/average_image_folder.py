import os
import shutil


def copy_file(file_path, save_path):
    for i, each_image in enumerate(os.listdir(file_path)):
        print(i)
        if each_image.endswith(".jpg"):
            print(each_image)
            each_save_folder = str(i // 100)
            if not os.path.exists(os.path.join(save_path, each_save_folder)):
                os.mkdir(os.path.join(save_path, each_save_folder))
            shutil.copy(os.path.join(file_path, each_image), os.path.join(save_path, each_save_folder, each_image))

def average_image_folder(file_path, save_path, cut_num0):

        cut_num = int(cut_num0)

        n = 0
        for root, dirs, files in os.walk(file_path):
            for file in files:
                if file.endswith(".jpg") or file.endswith(".bmp"):
                    n += 1
                    each_save_folder = str(n // cut_num)
                    if not os.path.exists(os.path.join(save_path, each_save_folder)):
                        os.mkdir(os.path.join(save_path, each_save_folder))
                    shutil.copy(os.path.join(file_path, file), os.path.join(save_path, each_save_folder, file))

        print(n)

        # for root, dirs, files in os.walk(file_path):
        #     for file in files:
        #         if file.endswith(".jpg") or file.endswith(".bmp"):
        #             each_save_folder = str(n // cut_num)
        #             # each_save_folder = str(i // cut_num)
        #             if not os.path.exists(os.path.join(save_path, each_save_folder)):
        #                 os.mkdir(os.path.join(save_path, each_save_folder))
        #             shutil.copy(os.path.join(file_path, file), os.path.join(save_path, each_save_folder, file))
                    # for i in range(0, each_save_folder):
                    #     if not os.path.exists(os.path.join(save_path, str(i))):
                    #         os.mkdir(os.path.join(save_path, str(i)))
                    #     shutil.copy(os.path.join(file_path, file),
                    #                 os.path.join(save_path, str(i), file))
                    #
                    #     str0 = os.path.join(save_path, str(i))
                    #     str1 = str0.replace("/", "\\")


        # for i, each_image in enumerate(os.listdir(file_path)):
        #     if each_image.endswith(".jpg"):
        #         each_save_folder = str(i // cut_num)
        #         if not os.path.exists(os.path.join(save_path, each_save_folder)):
        #             os.mkdir(os.path.join(save_path, each_save_folder))
        #         shutil.copy(os.path.join(file_path, each_image), os.path.join(save_path, each_save_folder, each_image))
        #
        #         str0 = os.path.join(save_path, each_save_folder)
        #         str1 = str0.replace("/", "\\")
        #         self.log_emit(f'{each_image}\n分类已完成，保存至\n{str1}')


if __name__ == '__main__':
    file_path = r"E:\Desktop\bokelin\test\1"
    save_path = r"E:\Desktop\bokelin\test\1_1"
    average_image_folder(file_path, save_path)
