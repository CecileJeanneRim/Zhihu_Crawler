# -*- coding:utf-8 -*-
from zhihu.user import *
from zhihu.client import *


class Test:
    def __init__(self):
        self.message_logger = MessageLogger()
        self.error_logger = ErrorLogger()
        self.utils = Utils(self.error_logger, self.message_logger)

    def test_all(self):
        topic_link_getter = Topic(cs, self.error_logger, self.message_logger, self.utils)
        topic_link_getter.links_crawler()
        links_collection = topic_link_getter.get_links()
        answer_getter = AnswerGetter(links_collection, 100, self.error_logger, self.message_logger, self.utils)
        answer_getter.question_crawler()

    def test_fans(self):
        loginer = Client()
        loginer.login(loginURL)
        fans_getter = FansGetter(self.error_logger, self.message_logger, self.utils)
        fans_getter.get_fans(u"yolfilm")
