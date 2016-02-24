# -*- coding:utf-8 -*-
# import cookielib
import urllib
import time
import json
import importlib
from .topic import *
from .common import *


class Client:
    def __init__(self, cookie=None):
        self.session = requests.Session()
        self.session.headers.update(defaultHeader)
        if cookie is not None:
            assert isinstance(cookie, str)
            self.login_with_cookie(cookie)

    @staticmethod
    def get_captcha_url():
        return captchaURL + str(int(time.time() * 1000))

    def get_captcha(self):
        # fuck the zhihu login logic
        self.session.get(mainURL)
        data = {'email': '', 'password': '', 'remember_me': 'true'}
        self.session.post(loginURL, data=data)
        response = self.session.get(self.get_captcha_url())
        return response.content

    def login(self, email, password, captcha):
        data = {'email': email, 'password': password, 'remember_me': 'true', 'captcha': captcha}
        response = self.session.post(loginURL, data=data)
        response_json = response.json()
        print(response_json)
        code = int(response_json['r'])
        message = response_json['msg']
        cookie_str = json.dumps(self.session.cookies.get_dict()) if code == 0 else ''
        return code, message, cookie_str

    def login_with_cookie(self, cookie):
        """
        set session cookie
        :param cookie: file path or cookies
        :return:
        """
        if os.path.isfile(cookie):
            with open(cookie) as f:
                cookie = f.read()
        cookie_dict = json.loads(cookie)
        self.session.cookies.update(cookie_dict)

    def login_in_terminal(self):
        """
        login without cookies
        :return: cookies
        """
        print(zhihuLoginStart)
        email = input(inputEmail)
        password = input(inputPassword)
        captcha_data = self.get_captcha()
        with open(captchaFile, 'wb') as f:
            f.write(captcha_data)
        print(checkCaptcha)
        captcha = input(inputCaptcha)
        os.remove(captchaFile)
        print(zhihuLogging)
        code, msg, cookie = self.login(email, password, captcha)

        if code == 0:
            print(loginSuccess)
        else:
            print(loginFailed.format(msg))
        return cookie

    def set_proxy(self, proxy: str):
        """
        set proxy, or the ip will be banned
        Client instance and other zhihu instance use a public session,
        so this function will set proxy for all classes
        :param proxy: "http://example.com:port"
        :return:
        """
        self.session.proxies.update({'http': proxy})
