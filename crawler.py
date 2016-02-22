# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import thread
import time

mainURL = "https://www.zhihu.com/"
topicURL = "https://www.zhihu.com/topic/"
questionURL = "https://www.zhihu.com/question/"
like = "赞同:"
author = "作者:"
colon = ":"
split = "————————————————————"
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

    def __init__(self, like_limit):
        self.limit_like = like_limit
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
        # self.answerPattern = re.compile(
        #     '<div class="zm-editable-content clearfix">(.*?)</div>'
        #     , re.S
        # )
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
                if answer[0] >= self.limit_like:
                    print split
                    print like
                    print answer[0]
                    print author
                    print answer[2]
                    print answer[3]

        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            elif hasattr(e, "reason"):
                print e.reason


# topicLinkGetter = LinkGetter(topic=cs)
# topicLinkGetter.links_crawler()
# linksCollection = topicLinkGetter.get_links()
# answerGetter = AnswerGetter(links=linksCollection, like_limit=100)
answerGetter = AnswerGetter(like_limit=100)
answerGetter.answer_crawler(request="https://www.zhihu.com/question/40490365")
