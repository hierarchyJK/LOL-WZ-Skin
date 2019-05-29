# -*-coding:utf-8 -*-
"""
@project:CookieTestLogin
@author:Kun_J
@file:LOLSkin.py
@ide:Pycharm
@time:2019-05-29 13:38:36
@month:五月
"""
import requests
from urllib import request
import re
import time
import os


class LOL(object):
    def __init__(self):
        self.get_figure_url = "https://lol.qq.com/biz/hero/champion.js"
        self.get_skin_url = "https://lol.qq.com/biz/hero/"
        self.get_image_url = "https://ossweb-img.qq.com/images/lol/web201310/skin/big"
        with open("E:\\untitled3\\Python\\LOL_skin\\LOL英雄.csv", "w") as f:
            f.write("英文名字" + "," + "ID" + "," + "中文名字" + "," + "称号" + "\n")

    # 获取英雄详情
    def figure_url(self):
        response = requests.get(self.get_figure_url).text

        # 英雄的ID
        re_id = re.findall(r'"id":"(.+?)"', response, re.S)

        # 英雄key
        re_key = re.findall(r'"key":"(.+?)"', response, re.S)

        # 英雄的name
        re_name = re.findall(r'"name":"(.+?)"', response, re.S)

        # 英雄的title
        re_title = re.findall(r'"title":"(.+?)"', response, re.S)

        for id, key, name, title in zip(re_id, re_key, re_name, re_title):
            # 拼接英雄皮肤的url
            url = self.get_skin_url + id + ".js"
            print("当前是:{}, url:{}".format(id, url))
            self.skin_url(url)
            time.sleep(2)
            self.save_content(
                id,
                key,
                name.encode("latin-1").decode('unicode_escape'),
                title.encode("latin-1").decode('unicode_escape'))
            print("正在保存中")
            print(id, key, name.encode("latin-1").decode('unicode_escape'),
                  title.encode("latin-1").decode('unicode_escape'))

    # 获取皮肤链接

    def skin_url(self, url="https://lol.qq.com/biz/hero/Ahri.js"):
        response = requests.get(url).text

        # 英雄皮肤的id
        re_id = re.findall(r',.*?{"id":"(.+?)","num"', response, re.S)

        # 英雄皮肤的name
        re_name = re.findall(r'"num".*?"name":"(.+?)"', response, re.S)
        # 删除默认皮肤
        del re_id[0]
        del re_name[0]
        # 英雄文件名称（如：皮城女警）
        re_name_dirName = re.findall(
            r'"data":.*?"name":"(.*?)"', response, re.S)

        print(re_name_dirName[0].encode("latin-1").decode('unicode_escape'))
        for id, name in zip(re_id, re_name):
            # 将一些不能作为文件名称的符号给替换掉
            name = name.encode("latin-1").decode('unicode_escape')
            # 拼接皮肤图片的下载地址
            image_url = self.get_image_url + id + ".jpg"
            print(id, name)

            # 下载皮肤
            self.download_img(image_url, re_name_dirName[0].encode(
                "latin-1").decode('unicode_escape'), name)

    def download_img(self, url, dir_name, fi_name):
        # 每个英雄一个目录
        directory_name = "E:/untitled3/Python/LOL_skin/LOL皮肤/" + dir_name
        # 判断目录是否存在
        if not os.path.exists(directory_name):
            print("{0}目录不存在，新建{0}目录！".format(directory_name))
            os.mkdir(directory_name)
        # 将每张图片用英雄每款皮肤的名字
        if 'K\/DA' in fi_name:
            file_name = directory_name + "/" + 'KDA'+fi_name[5:] + ".jpg"
        else:
            file_name = directory_name + "/" + fi_name + ".jpg"
        # 下载图片
        try:
            request.urlretrieve(url, file_name)
            print("下载成功！")
        except BaseException:
            print(fi_name, '不存在')
    # 将每个英雄的信息，用csv格式保存

    def save_content(self, id, key, name, title):
        with open("E:\\untitled3\\Python\\LOL_skin\\LOL英雄.csv", "a") as f:
            f.write(id + "," + key + "," + name + "," + title + "\n")


if __name__ == '__main__':
    L = LOL()
    L.figure_url()
# LOL().skin_url()
