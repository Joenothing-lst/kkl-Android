# -*- coding:utf-8 -*-
import requests
import re
#import time
import random
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
def update():
    for i in range(1,11):
        img = requests.get('https://api.lolicon.app/setu/view.php',headers=header)
        p = '<img src=\\"(.*?)\\">'
        link = re.findall(p,img.text)
        print('正在下载色图' + str(i)+ '...')
        pic = requests.get(link[0],headers = header)
        image_name = 'C:\\Users\\Administrator\\Downloads\\CQP-xiaoi\\酷Q Pro\\data\\image\\色图库\\' + '色图' + str(i) + '.png'
        f = open(image_name, 'wb')
        f.write(pic.content)
        f.close()
        print('色图' + str(i) + '下载完成！')
#        time.sleep(random.randint(3,10))

'''
n = 1
for i in image:
    pic = requests.get(i,headers = header)
    image_name = 'C:/Users/Administrator/Desktop/色图库/' + '色图' + str(n) + '.jpg'
    print('正在下载色图' + str(n)+ '...')
    with open() as f:
        fp.write(pic.content)
    fp.close()
    print('色图' + str(n) + '下载完成！')
    n += 1
'''

