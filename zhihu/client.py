# -*- coding:utf-8 -*-
import cookielib
from topic import *


class Client:
    def __init__(self):
        filename = 'cookie.txt'
        # if os.path.isfile(filename):
        #     从文件中读取cookie内容到变量
        # self.cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
        # else:
        # 声明一个CookieJar对象实例来保存cookie
        self.cookie = cookielib.MozillaCookieJar(filename)
        # 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
        self.handler = urllib2.HTTPCookieProcessor(self.cookie)
        # 通过handler来构建opener
        self.opener = urllib2.build_opener(self.handler)
        # 此处的open方法同urllib2的urlopen方法，也可以传入request

    def login(self, request):
        email = raw_input("Your email(Doesn't support telephone login): ")
        password = raw_input("Your password: ")
        postdata = urllib.urlencode({'email': email,
                                     'password': password,
                                     'remember_me': 'true',
                                     'captcha': ""
                                     })
        headers = {'X-Requested-With': 'XMLHttpRequest',
                   'Referer': 'http://www.zhihu.com',
                   'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; '
                                 'rv:39.0) Gecko/20100101 Firefox/39.0',
                   'Host': 'www.zhihu.com'}

        request_with_data = urllib2.Request(request, postdata, headers)
        response = self.opener.open(request_with_data)
        print response.read().decode()
        # 保存cookie到文件
        self.cookie.save(ignore_discard=True, ignore_expires=True)
