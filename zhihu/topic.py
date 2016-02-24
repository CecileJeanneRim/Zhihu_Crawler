# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
from common import *


class Topic:
    def __init__(self, topic, error_logger, message_logger, utils):
        self.topic = topic
        self.links = []
        self.title = []
        self.message_logger = message_logger
        self.utils = utils
        self.error_logger = error_logger
        self.pattern = re.compile(
            '<a class="question_link".*?href="/question/(.*?)">(.*?)</a>', re.S)
        self.message_logger.event(u"Link Getter Built")

    def links_crawler(self):
        topic_url = topicURL + str(self.topic)
        request = urllib2.Request(topic_url)
        try:
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
            self.utils.url_error_handle(e, topic_url)

    def get_links(self):
        return self.links