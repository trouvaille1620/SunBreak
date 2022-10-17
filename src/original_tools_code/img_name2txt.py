import os

a = r'D:\data\泡罩\52356ok'
with open(r'D:\data\泡罩\52356ok\UJ220309b-2.txt', 'a+') as f:
    for i in os.listdir(a):
        f.write(i)
        f.write('\n')

print('down')