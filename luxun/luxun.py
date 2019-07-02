# -*- coding: utf-8 -*-
import re
import time

import pymysql
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

"""
爬取句子迷网站鲁迅的经典语录，存储数据到MySQL。使用了代理ip进行反反爬虫,
get_random_proxies方法的隧道验证信息已经过期，需要到阿布云注册申请才能运行程序

# 数据表字段
# id        唯一id
# sentence  句子
# origin    出处
# author    作者

# create TABLE `motto`(
#     `id` INT(64) NOT NULL AUTO_INCREMENT,
#     `origin` VARCHAR(64) NULL DEFAULT NULL,
#     `author` VARCHAR(64) NULL DEFAULT NULL,
#     `sentence` LONGTEXT NULL DEFAULT NULL,
#     PRIMARY KEY (`id`)
# );
"""


# 用来操作数据库的类
class MySQLCommand(object):
    # 类的初始化
    def __init__(self):
        self.host = 'localhost'
        self.port = 3306  # 端口号
        self.user = 'xmai'  # 用户名
        self.password = "Uf4bGZ53Ds*#"  # 密码
        self.db = "motto"  # 数据库
        self.table = "motto"  # 表

    # 链接数据库
    def connect_mysql(self):
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user,
                                        passwd=self.password, db=self.db, charset='utf8')
            self.cursor = self.conn.cursor()
        except:
            print('connect mysql error.')

    # 插入数据，插入之前先查询是否存在(直接查询句子sentence匹配)，如果存在就不再插入
    def insert_data(self, my_dict):
        table = self.table  # 要操作的表格
        # 注意，这里查询的sql语句sentence=' %s '中%s的前后要有空格
        print(my_dict['sentence'])

        sql_exit = "SELECT sentence FROM " + table + "  WHERE sentence = ' %s '" % (my_dict['sentence'])
        res = self.cursor.execute(sql_exit)
        print(res)
        if res:  # res为查询到的数据条数如果大于0就代表数据已经存在
            print("数据已存在", res)
            return 0
        # 数据不存在才执行下面的插入操作
        try:
            cols = ', '.join(my_dict.keys())  # 用，分割
            values = '"," '.join(map(str, my_dict.values()))
            sql = "INSERT INTO " + table + " (%s) VALUES (%s)" % (cols, '"' + values + '"')
            print(sql)
            # 拼装后的sql如下
            # INSERT INTO motto (origin, sentence, id, author) VALUES ("华盖集·杂感"," 勇者愤怒，抽刃向更强者；怯者愤怒，却抽刃向更弱者。"," 6"," 鲁迅")
            try:
                result = self.cursor.execute(sql)
                insert_id = self.conn.insert_id()  # 插入成功后返回的id
                self.conn.commit()
                # 判断是否执行成功
                if result:
                    print("插入成功", insert_id)
                    return insert_id + 1
            except pymysql.Error as e:
                # 发生错误时回滚
                self.conn.rollback()
                # 主键唯一，无法插入
                if "key 'PRIMARY'" in e.args[1]:
                    print("数据已存在，未插入数据")
                else:
                    print("插入数据失败，原因 %d: %s" % (e.args[0], e.args[1]))
        except pymysql.Error as e:
            print("数据库错误，原因%d: %s" % (e.args[0], e.args[1]))

    # 查询最后一条数据的id值
    def get_last_id(self):
        sql = "SELECT max(id) FROM " + self.table
        try:
            self.cursor.execute(sql)
            row = self.cursor.fetchone()  # 获取查询到的第一条数据
            if row[0]:
                return row[0]  # 返回最后一条数据的id
            else:
                return 0  # 如果表格为空就返回0
        except:
            print(sql + ' execute failed.')

    def close_mysql(self):
        self.cursor.close()
        self.conn.close()  # 创建数据库操作类的实例


class GetSentence:
    def __init__(self, link_list):
        self.linkList = link_list
        self.sentenceBox = []
        self.user_agent = UserAgent()
        self.skipNum = 0

    # 使用阿布云代理，代码来自使用文档
    @staticmethod
    def get_random_proxies():
        # 要访问的目标页面
        # targetUrl = "http://test.abuyun.com"
        # targetUrl = "http://proxy.abuyun.com/switch-ip"
        # targetUrl = "http://proxy.abuyun.com/current-ip"

        # 代理服务器
        proxy_host = "http-pro.abuyun.com"
        proxy_port = "9010"

        # 代理隧道验证信息
        proxy_user = "HJ0F3CB9P46M9T2P"
        proxy_pass = "2366CEB93ADA6AD8"

        proxy_meta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": proxy_host,
            "port": proxy_port,
            "user": proxy_user,
            "pass": proxy_pass,
        }

        proxies = {
            "http": proxy_meta,
            "https": proxy_meta,
        }
        return proxies

    def get_one_page(self, link, part):
        # 请求延时
        self.sentenceBox = []
        header = {"User-Agent": self.user_agent.random}
        time.sleep(5)
        proxies = self.get_random_proxies()
        try:
            res = requests.get(link, headers=header, proxies=proxies)  # 使用阿布云代理
            # res = requests.get(link, headers=header)
        except Exception as e:
            self.skipNum += 1
            return
        print(res.status_code)
        # 使用解析器为html.parser
        soup = BeautifulSoup(res.text, "html.parser")

        # 连接数据库
        mysql_command = MySQLCommand()
        mysql_command.connect_mysql()
        # 这里每次查询数据库中最后一条数据的id，新加的数据每成功插入一条id+1
        print(mysql_command.get_last_id())
        data_count = int(mysql_command.get_last_id()) + 1
        all_content = soup.find_all('div', class_="views-field-phpcode")

        for content in all_content:
            try:
                sentence = content.find('a', class_="xlistju").get_text()  # 句子
                # sentence = re.escape(sentence)  # 转义处理 对字符串中所有的非字母（ASCII letters）、数字（numbers）及下划线（'_'）的字符前都加反斜线\
                sentence = sentence.replace("\\", "\\\\")
                sentence = sentence.replace("'", "\\'")
                sentence = sentence.replace('"', '\\"')
            except Exception:
                sentence = " "

            try:
                origin = content.find('a', class_="active").get_text()  # 出处(可能为空)
                origin = "《" + origin + "》"
                # origin = re.escape(origin)  # 转义处理
                origin = origin.replace("\\", "\\\\")
                origin = origin.replace("'", "\\'")
                origin = origin.replace('"', '\\"')
            except Exception:
                origin = "  "
            author = "鲁迅"
            # 把爬取到的每条数据组合成一个字典用于数据库数据的插入
            news_dict = {
                "origin": origin,
                "sentence": sentence,
                "id": data_count,
                "author": author
            }
            try:
                # 插入数据，如果已经存在就不在重复插入
                res = mysql_command.insert_data(news_dict)
                if res:
                    data_count = res
            except Exception as e:
                print("插入数据失败", str(e))  # 输出插入失败的报错语句
        mysql_command.close_mysql()  # 最后一定要要把数据关闭
        data_count = 0

    def start(self):
        header = {'User-Agent': self.user_agent.random}
        part = 1
        for link in self.linkList:

            proxies = self.get_random_proxies()
            print(proxies)
            # 设置代理
            response = requests.get(link, headers=header, proxies=proxies)  # 使用阿布云代理
            # response = requests.get(link, headers=header)
            soup = BeautifulSoup(response.text, "html.parser")
            last_page = soup.select('.pager-last a')
            last_page = re.search(r'>(\d+)<', str(last_page[0])).group(1)
            page_sum = int(last_page)
            print("鲁迅" + str(part) + "有" + str(page_sum) + "页。")
            self.get_one_page(link, part)

            for i in range(1, page_sum):
                # 使用的是阿布云代理ip，限制每秒请求次数，无法多线程，并且每次延缓请求1s，慢慢爬
                # th=threading.Thread(target=self.CrawlOnePage,args=(link+"?page="+str(i),part))
                self.get_one_page(link + "?page=" + str(i), part)
            # th.start()
            print("鲁迅" + str(part) + "  done")
            part += 1


if __name__ == '__main__':
    # 需要爬取的链接主页
    motto = "https://www.juzimi.com/writer/鲁迅"
    linkList = [motto]
    sc = GetSentence(linkList)
    sc.start()
    print("总共跳过了" + str(sc.skipNum))
