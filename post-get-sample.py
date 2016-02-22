# _*_ coding: utf-8 -*-

import urllib2
import urllib

# post
values = {"username": "aaaa", "password": "aaa"}
valuesOr = {}
valuesOr["username"] = "aaaa"

data = urllib.urlencode(values)
url = "https://passport.xxxx"
request = urllib2.Request(url, data)
response = urllib2.urlopen(request)
print response.read()

# get
geturl = url + "?" + data
request = urllib2.Request(geturl, data)
response = urllib2.urlopen(request, timeout=10)
print response.read()
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}
headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
           'Referer': 'http://www.zhihu.com/articles'}
request = urllib2.Request(url, data, headers)
