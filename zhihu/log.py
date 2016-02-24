# -*- coding:utf-8 -*-
from utils import *


class Logger:
    def __init__(self, name):
        self.log_handler = open(name, 'ab+')
        # sys.stdout = self.log_handler

    def output_line_log(self, message):
        self.log_handler.write(Utils.get_current_time())
        # print type(message)
        self.log_handler.write(message.encode('utf8'))
        self.log_handler.write('\n')


class MessageLogger(Logger):
    def __init__(self):
        Logger.__init__(self, 'log.log')
        self.event(u"Message Logger Built")

    def crawl_question(self, link_id, title):
        self.output_line_log(u"Question ID:" + link_id + u"Question Title" + title + u"Crawled")

    def event(self, message):
        self.output_line_log(u"Event:" + message)


class ErrorLogger(Logger):
    def __init__(self):
        Logger.__init__(self, 'error.log')
        self.message_logger = MessageLogger()
        self.message_logger.event(u"Error Logger Built")

    def database_error(self, exception):
        error_detail = u"数据库错误，原因%d: %s" % (exception.args[0], exception.args[1])
        print(error_detail)
        self.output_line_log(error_detail)
        if "key 'PRIMARY'" in exception.args[1]:
            error_detail = u"数据已存在"
            print(error_detail)
            self.output_line_log(error_detail)

    def url_error(self, exception, url):
        if hasattr(exception, "code"):
            print exception.code
            self.output_line_log(exception.code)
        elif hasattr(exception, "reason"):
            print exception.reason
            self.output_line_log(exception.reason)
        self.output_line_log(u"request:" + url)

