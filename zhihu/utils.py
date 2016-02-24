# -*- coding:utf-8 -*-
import re
import time


class Utils:
    def __init__(self, error_logger, message_logger):
        # 去除img标签,7位长空格
        self.removeImg = re.compile('<img.*?>|</img>')
        # 删除超链接标签
        self.removeAddr = re.compile('<a.*?>|</a>')
        # 把换行的标签换为\n
        self.replaceLine = re.compile('<tr>|<div>|</div>|</p>')
        # 将表格制表<td>替换为\t
        self.replaceTD = re.compile('<td>')
        # 把段落开头换为\n加空两格
        self.replacePara = re.compile('<p.*?>')
        self.replaceBR = re.compile('<br>|<br />')
        # 将其余标签剔除
        self.removeExtraTag = re.compile('<.*?>')

        self.message_logger = message_logger
        self.error_logger = error_logger
        self.message_logger.event(u"Utils Built")

    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n    ", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        # strip()将前后多余内容删除
        return x.strip()

    def url_error_handle(self, exception, url):
        self.error_logger.url_error(exception, url)

    def mysqldb_error_handle(self, exception):
        self.error_logger.database_error(exception)

    @staticmethod
    def get_current_time():
        return time.strftime(u'[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))

    @staticmethod
    def get_current_data():
        return time.strftime(u'%Y-%m-%d', time.localtime(time.time()))

