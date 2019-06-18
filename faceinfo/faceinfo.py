# -*- coding: utf-8 -*-
#
# BaiduFaceDetect
#
# 获取百度人脸检测接口信息返回
#
# 百度人脸检测接口文档：
# https://ai.baidu.com/docs#/Face-Detect-V3/top
#
# ==============================================================================

import base64
import json
import urllib
import urllib.request
from urllib import request


def get_token(host):
    header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
                   "Content-Type": "application/json"}
    req = request.Request(url=host, headers=header_dict)
    res = request.urlopen(req)
    res = res.read()
    res_json = json.loads(res.decode('utf-8'))
    print(res_json)
    return res_json["access_token"]


'''
进行post请求
url:请求地址
values:请求体
'''


def get_info_post_json_data(url, value):
    header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
                   "Content-Type": "application/json"}
    req = request.Request(url=url, data=value, headers=header_dict)
    res = request.urlopen(req)
    res = res.read()
    return (res.decode('utf-8'))


'''
调用百度API,进行人脸探测
imgPath: 图片地址
access_token: 开发者token
'''


def getBaiduFaceTech(imgPath, access_token):
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
    # 二进制方式打开图片文件
    f = open(imgPath, 'rb')
    # 图片转换成base64
    img = base64.b64encode(f.read())
    params = {"image": img, "image_type": "BASE64",
              "face_field": "age,beauty,expression,face_shape,gender,glasses,landmark,race,quality,face_type"}
    params = urllib.parse.urlencode(params).encode(encoding='utf-8')
    request_url = request_url + "?access_token=" + access_token
    # 调用post其请求方法
    face_info = get_info_post_json_data(request_url, params)
    # json字符串转为对象
    face_json = json.loads(face_info)
    if face_json["error_code"] != 0:
        print("没有发现人像")
    # 如果没有发现人像,会返回为空
    elif face_json["result"]['face_num'] != 0:
        # 把想要的部分提取存入字典中
        result = face_json['result']['face_list'][0]
        print("分值:" + str(result['beauty']))
        print("年龄:" + str(result['age']))
        print("性别:" + result['gender']['type'] + "\n可能性:" + str(result['gender']['probability']))
        gender = result['gender']['type']
        age = str(result['age'])
        beauty = str(result['beauty'])
        probability = str(result['gender']['probability'])
        face_dict = {"gender": gender, "age": age, "probability": probability, "beauty": beauty}
        return face_dict


if __name__ == '__main__':
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=【百度云应用的AK】&client_secret=【百度云应用的SK】'
    token = get_token(host)
    # 调用百度人脸识别API
    face_dict = getBaiduFaceTech("face.jpg", token)
