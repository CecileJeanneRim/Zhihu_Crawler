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
        