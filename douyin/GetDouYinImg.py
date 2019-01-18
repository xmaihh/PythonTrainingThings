# coding:utf-8
import os

from PIL import Image
from douyin.GetFaceInfo import *

# 图片压缩比例
SIZE_normal = 1.0
SIZE_small = 1.5
SIZE_more_small = 2.0


# adb手机截图
def getdouyinimg():
    # 截图
    os.system("adb shell /system/bin/screencap -p /sdcard/screenshot.png")
    os.system("adb pull /sdcard/screenshot.png douyin.jpg")
    # 压缩图片
    img = Image.open("douyin.jpg").convert('RGB')
    scale = SIZE_small
    w, h = img.size
    img.thumbnail(((int)(w / scale), (int)(h / scale)))
    img.save('douyin.jpg')


if __name__ == '__main__':
    # print('开始截屏')
    # getdouyinimg()

    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=CU0o7lOtAlxGODIxS9UUz2ZX&client_secret=8bd1pnjYbRMQO6rtA708tazfwe6QYfaU '
    token = get_token(host)
    # 调用百度人脸识别API
    face_dict = getBaiduFaceTech("douyin.jpg", token)
    # 得到的数据进行分析
    # faceinfoAnalysis(face_dict)
