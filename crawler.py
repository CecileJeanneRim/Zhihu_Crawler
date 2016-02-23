# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import thread
import time

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
            if hasattr(e, "code"):
                print e.code
            elif hasattr(e, "reason"):
                print e.reason

    def get_links(self):
        return self.links


class AnswerGetter:
    # def initKey(self, links, like_limit):
    #     self.links = links
    #     self.limit_like = like_limit

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
            response = urllib2.urlopen(request)
            content = response.read().decode('utf-8')
            title = re.search(self.titlePattern, content)
            print title.group(1)
            detail = re.search(self.detailPattern, content)
            print detail.group(1)
            answers = re.findall(self.answerPattern, content)
            # print answers
            for answer in answers:
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

        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            elif hasattr(e, "reason"):
                print e.reason


class Utils:
    # 去除img标签,7位长空格
    removeImg = re.compile('<img.*?>|</img>')
    # 删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    # 把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    # 将表格制表<td>替换为\t
    replaceTD = re.compile('<td>')
    # 把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    # 将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    # 将其余标签剔除
    removeExtraTag = re.compile('<.*?>')

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


topicLinkGetter = LinkGetter(topic=cs)
topicLinkGetter.links_crawler()
linksCollection = topicLinkGetter.get_links()
answerGetter = AnswerGetter(links=linksCollection, like_limit=100)
# answerGetter = AnswerGetter(like_limit=100)
# answerGetter.answer_crawler(request="https://www.zhihu.com/question/40490365")
answerGetter.question_crawler()
