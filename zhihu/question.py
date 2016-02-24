# -*- coding:utf-8 -*-
from .user import *
from .database import *
from .client import *


class Question:
    def __init__(self, links, like_limit, error_logger, message_logger, utils):
        self.links = links
        self.limit_like = like_limit
        self.message_logger = message_logger
        self.utils = utils
        self.error_logger = error_logger
        self.database = Database(self.error_logger, self.message_logger, self.utils)
        self.titlePattern = re.compile(
            '<h2 class="zm-item-title zm-editable-content">(.*?)</h2>', re.S)
        self.detailPattern = re.compile(
            '<div id="zh-question-detail".*?zm-editable-content">(.*?)</div>', re.S)
        self.answerPattern = re.compile(
            # 0: vote, 1: author url, 2: author name, 3: answer content
            '<span class="count">(.*?)</span>.*?<a class="author-link".*?href="/people/(.*?)">(.*?)</a>.*?'
            '<div class="zm-editable-content clearfix">(.*?)</div>', re.S)
        self.results = {}
        self.message_logger.event("Answer Getter Built")

    def question_crawler(self):
        for link in self.links:
            request = urllib2.Request(link)
            self.answer_crawler(request, link)

    def answer_crawler(self, request, link):
        try:
            content_list = self.get_response(request=request)
            self.print_response(content_list)
            link_id = link.replace(questionURL, "")
            self.message_logger.crawl_question(link_id, content_list[0].group(1))
            self.results = {
                "question_id": link_id,
                "title": content_list[0].group(1)
            }

            self.database.users(content_list[2])
            self.database.insert_data(self.results, "questions")
        except urllib2.URLError, e:
            self.utils.url_error_handle(e, link)

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
