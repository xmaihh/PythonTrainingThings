# encoding:utf-8

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
    request_url = "https://aip.baidubce.com/rest/2.0/douyin/v3/detect"
    # 二进制方式打开图片文件
    f = open(imgPath, 'rb')
    # 图片转换成base64
    img = base64.b64encode(f.read())
    # params = {"face_fields": "age,beauty,expression,faceshape,gender,glasses,landmark,race,qualities", "image": img,
    #          "max_face_num": 5}
    # params = {"image": img,"image_type":"BASE64","face_field": "age,beauty,expression,face_shape,gender,glasses,landmark,race,quality,face_type"}
    params = {"image": img, "image_type": "BASE64", "face_field": "age,beauty,expression,face_shape,gender,glasses,landmark,race,quality,face_type"}
    print("base64编码    \t" + str(img))



    params = urllib.parse.urlencode(params).encode(encoding='utf-8')
    request_url = request_url + "?access_token=" + access_token
    # 调用post其请求方法
    face_info = get_info_post_json_data(request_url, params)
    # json字符串转为对象
    face_json = json.loads(face_info)

    File = open("hello.json", "w")
    File.write(str(face_info) + "\n")
    File.close()


    if face_json["error_code"] != 0:
        print(face_json["error_msg"] + face_info)
        print("\n")
        print(face_json['result']['face_num'])
        print("\n")

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
    '''
    将获得的数据进行分析
    face_dict:人脸识别后的数据
    '''

    def faceinfoAnalysis(face_dict):
        # 如果发现人物继续判断
        if len(face_dict) != 0:
            print("性别:" + face_dict["gender"])
            print("年龄:" + face_dict["age"])
            print("性别：" + face_dict["gender"])
            print("可能性：" + face_dict["probability"])
        else:
            print("图片中没有发现人物")

if __name__ == '__main__':
    # print('开始截屏')
    # getdouyinimg()

    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=CU0o7lOtAlxGODIxS9UUz2ZX&client_secret=8bd1pnjYbRMQO6rtA708tazfwe6QYfaU '
    token = get_token(host)
    # 调用百度人脸识别API
    face_dict = getBaiduFaceTech("douyin.jpg", token)