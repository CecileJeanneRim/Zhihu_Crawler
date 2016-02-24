# -*- coding:utf-8 -*-
from topic import *
from log import *
from database import *


class UserGetter:
    def __init__(self, links, like_limit, error_logger, message_logger, utils):
        self.links = links
        self.limit_like = like_limit
        self.message_logger = message_logger
        self.utils = utils
        self.error_logger = error_logger
        self.database = Database(self.error_logger, self.message_logger, self.utils)
        self.genderPattern = re.compile(
            '<input.*?name="gender".*?value="(.*?)".*?checked="checked".*?/>', re.S)
        self.detailPattern = re.compile(
            '<div id="zh-question-detail".*?zm-editable-content">(.*?)</div>', re.S)
        self.results = {}
        self.message_logger.event(u"User Getter Built")


class FansGetter:
    def __init__(self, error_logger, message_logger, utils):
        self.message_logger = message_logger
        self.utils = utils
        self.error_logger = error_logger
        self.database = Database(self.error_logger, self.message_logger, self.utils)
        self.fansPattern = re.compile(
            '<a.*?href="https://www.zhihu.com/people/(.*?)".*?class="zg-link".*?>', re.S)
        self.message_logger.event(u"Fans Getter Built")
        print "built"

    def get_fans(self, url):
        print "get fans"
        url = userURL + url + followers
        request = urllib2.Request(url)
        try:
            fans = self.get_response(request=request)
            self.database.users(fans)
        except urllib2.URLError, e:
            self.utils.url_error_handle(e, url)

    def get_response(self, request):
        print "get response"
        response = urllib2.urlopen(request)
        content = response.read().decode('utf-8')
        print "content"
        # print content
        fans = re.findall(self.fansPattern, content)
        print fans
        for fan in fans:
            print fan
        return fans
