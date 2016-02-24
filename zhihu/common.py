# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as BS
from bs4 import Tag,NavigableString
import requests
import functools
import re
import os
import lxml


# ___________________________URL/Header/zhihu ID_______________________________________________
mainURL = "https://www.zhihu.com"
loginURL = mainURL + '/login/email'
topicURL = mainURL + "/topic/"
questionURL = mainURL + "/question/"
userURL = mainURL + "/people/"
followers = "/followers"
captchaURL = mainURL + '/captcha.gif?r='
like = "赞同:"
author = "作者:"
colon = ":"
split = "————————————————————"
# 计算机科学 话题
cs = 19580349

defaultHeader = {'X-Requested-With': 'XMLHttpRequest',
                  'Referer': 'http://www.zhihu.com',
                  'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; '
                                'rv:39.0) Gecko/20100101 Firefox/39.0',
                  'Host': 'www.zhihu.com'}

# __________________________Strings________________________________________
zhihuLoginStart = "===== Login Zhihu ====="
inputEmail = "E-mail:"
inputPassword = "Password:"
checkCaptcha = "Please check captcha.gif"
inputCaptcha = "Captcha:"
zhihuLogging = "===== Logging ====="
loginSuccess = "===== Login Successfully ====="
loginFailed = "===== Login Failed =====\n===== Reason: {0} ====="


# __________________________Files____________________________________________
captchaFile = "captcha.gif"
