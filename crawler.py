# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import thread
import time
import sys
import types
import BeautifulSoup
import MySQLdb

mainURL = "https://www.zhihu.com/"
topicURL = "https://www.zhihu.com/topic/"
questionURL = "https://www.zhihu.com/question/"
like = u"赞同:"
author = u"作者:"
colon = u":"
split = u"————————————————————"
# 计算机科学 话题
cs = 19580349


class LinkGetter:
    def __init__(self, topic):
        self.topic = topic
        self.links = []
        self.title = []
        self.utils = Utils()
        self.pattern = re.compile(
            '<a class="question_link".*?href="/question/(.*?)">(.*?)</a>'
            , re.S
        )

    def links_crawler(self):
        topic_url = topicURL + str(self.topic)
        try:
            request = urllib2.Request(topic_url)
            response = urllib2.urlopen(request)
            content = response.read().decode('utf-8')
            results = re.findall(self.pattern, content)

            counter = 0
            for result in results:
                print result[1] + colon + questionURL + result[0]
                self.links.append(questionURL + result[0])
                self.title.append(result[1])
                counter += 1
        except urllib2.URLError, e:
            self.utils.url_error_handle(exception=e)

    def get_links(self):
        return self.links


class AnswerGetter:
    def __init__(self, links, like_limit):
        self.links = links
        self.limit_like = like_limit
        self.utils = Utils()
        self.titlePattern = re.compile(
            '<h2 class="zm-item-title zm-editable-content">(.*?)</h2>'
            , re.S
        )
        self.detailPattern = re.compile(
            '<div id="zh-question-detail".*?zm-editable-content">(.*?)</div>'
            , re.S
        )
        self.answerPattern = re.compile(
            # 0: vote, 1: author url, 2: author name, 3: answer content
            '<span class="count">(.*?)</span>.*?<a class="author-link".*?href="/people/(.*?)">(.*?)</a>.*?'
            '<div class="zm-editable-content clearfix">(.*?)</div>'
            , re.S
        )
        self.results = []

    def question_crawler(self):
        for link in self.links:
            request = urllib2.Request(link)
            self.answer_crawler(request)

    def answer_crawler(self, request):
        try:
            content_list = self.get_response(request=request)
            self.print_response(content_list)
        except urllib2.URLError, e:
            self.utils.url_error_handle(e)

    def get_response(self, request):
        response = urllib2.urlopen(request)
        content = response.read().decode('utf-8')
        title = re.search(self.titlePattern, content)
        detail = re.search(self.detailPattern, content)
        answers = re.findall(self.answerPattern, content)
        content_list = [title, detail, answers]
        return content_list

    def print_response(self, responses):
        print responses[0].group(1)
        print responses[1].group(1)
        for answer in responses[2]:
            like_count = answer[0]
            if answer[0].find("K"):
                like_count = answer[0].replace("K", "000")
            try:
                if int(like_count) >= int(self.limit_like):
                    print split
                    print like + answer[0]
                    print author + answer[2]
                    print self.utils.replace(answer[3])
            except ValueError, e:
                print e


class Utils:
    def __init__(self):
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
        # 将换行符或双换行符替换为\n
        self.replaceBR = re.compile('<br><br>|<br>')
        # 将其余标签剔除
        self.removeExtraTag = re.compile('<.*?>')

        self.logger = Logger()

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

    def url_error_handle(self, exception):
        if hasattr(exception, "code"):
            print exception.code
        elif hasattr(exception, "reason"):
            print exception.reason

    def mysqldb_error_handle(self, exception):
        print "数据库错误，原因%d: %s" % (exception.args[0], exception.args[1])
        if "key 'PRIMARY'" in exception.args[1]:
            print self.logger.get_current_time(), "数据已存在"


class Logger:
    @staticmethod
    def get_current_time(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))

    @staticmethod
    def get_current_data(self):
        return time.strftime('%Y-%m-%d', time.localtime(time.time()))

    @staticmethod
    def output_log(self):
        handler = open('log.log', 'w')
        sys.stdout = handler


class Test:
    def test(self):
        topic_link_getter = LinkGetter(topic=cs)
        topic_link_getter.links_crawler()
        links_collection = topic_link_getter.get_links()
        answer_getter = AnswerGetter(links=links_collection, like_limit=100)
        answer_getter.question_crawler()


class Database:
    def __init__(self):
        self.utils = Utils()
        try:
            self.db = MySQLdb.connect('ip', 'username', 'password', 'db_name')
            self.cur = self.db.cursor()
            self.db.set_character_set('utf8')
        except MySQLdb.Error, e:
            self.utils.mysqldb_error_handle(exception=e)

    def insert_data(self, data_dict, table):
        try:
            sql = self.insert_sql_construct(data_dict, table)
        except MySQLdb.Error, e:
            self.utils.mysqldb_error_handle(e)

    def insert_sql_construct(self, data_dict, table):
        cols = ', '.join(data_dict.keys())
        values = '"," '.join(data_dict.values())
        return "INSERT INTO %s (%s) VALUES (%s)" % (table, cols, '"' + values + '"')

    def execute_insert(self, sql):
        try:
            result = self.cur.execute(sql)
            insert_id = self.db.insert_id()
            self.db.commit()
            if result:
                return insert_id
            else:
                return -1
        except MySQLdb.Error, e:
            self.db.rollback()



tester = Test()
tester.test()
