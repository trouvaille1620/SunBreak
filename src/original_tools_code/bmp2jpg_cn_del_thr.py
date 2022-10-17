import os
import cv2
import numpy as np
import threading

#bmp转jpg
##bmp,png,

DIR = r'D:\data\310\02_001'
KEEP_BMP = False

def gen_list(dir):
    listx = []
    i = 0
    for root, dirs, files in os.walk(dir):
        for name in files:
            if '.bmp' in name:
                i += 1
                listx.append([i,root,name])
    return listx

# 图片转存jpg
def save_threads(listx):
    len_list = len(listx)
    n = 1

    for i, root, name in listx:
        n += 1
        print('Process: %.4f' % (n/len_list))
        img = cv2.imdecode(np.fromfile(os.path.join(root, name), dtype=np.uint8), 1)

        # save_path = os.path.join(root, name[:-3] + 'jpg')
        save_path = os.path.join(root,  name[:-3] + 'jpg')
        cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])[1].tofile(save_path)

        if not KEEP_BMP:
            os.remove(os.path.join(root, name))


if __name__ == '__main__':

    num_threads = 64

    listx = gen_list(DIR)
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