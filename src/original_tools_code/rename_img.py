import os

file_path = r'E:\Desktop\qietu_test\wkw'
save_path = r'E:\Desktop\qietu_test\wkw1'

for root, dirs, files in os.walk(file_path):
    for file in files:
        if file.endswith('jpg') or file.endswith('bmp'):
            b = root.split("\\")
            src = os.path.join(root, file)
            dst = os.path.join(root, str(b[-1]) + "_" + file)
            os.rename(src, dst)
            print('src', src)
            print('dst', dst)

def rename_img(file_path):
    for root, dirs, files in os.walk(file_path):
        for file in files:
            if file.endswith('jpg') or file.endswith('bmp'):
                b = root.split("\\")
                src = os.path.join(root, file)
                dst = os.path.join(root, str(b[-1]) + "_" + file)
                os.rename(src, dst)
                print('src', src)
                print('dst', dst)