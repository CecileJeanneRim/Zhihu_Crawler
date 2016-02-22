import urllib2
import urllib
import cookielib

filename = 'cookie.txt'
cookie = cookielib.MozillaCookieJar(filename)
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
postdata = urllib.urlencode({
    'username': 'xxx',
    'pwd': 'xxx'
})
loginURL = "http://xx.xx.com"
result = opener.open(loginURL, postdata)
cookie.save(ignore_discard=True, ignore_expires=True)

useCookieURL = "http://bb.cc.com"
result = opener.open(useCookieURL)
print result.read()
