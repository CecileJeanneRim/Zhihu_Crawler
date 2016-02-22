import urllib2
import cookielib

# define a CookieJar to save cookie
cookie = cookielib.CookieJar()

# use HTTPCookieProcessor in urllib2 to create cookie processor
handler = urllib2.HTTPCookieProcessor(cookie)

# build opener
opener = urllib2.build_opener(handler)

request = "https://www.baidu.com"
response = opener.open(request)
for item in cookie:
    print 'Name =' + item.name
    print 'Value =' + item.value

# _______________________________

# save cookie in file
filename = 'cookie.txt'
# define a object
cookie = cookielib.MozillaCookieJar(filename)

handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)
response = opener.open(request)
cookie.save(ignore_discard=True, ignore_expires=True)

# ________________________________

# read cookie from file
cookie.load('cookie.txt', ignore_expires=True, ignore_discard=True)
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
response = opener.open(request)
print response.read()

















