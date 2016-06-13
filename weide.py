#/usr/bin/env python
# coding:utf8
import json
import time
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from conf import conf

class Site(object):
    def __init__(self, siteName):
        self.siteName = siteName
        self.browser = webdriver.Chrome(conf['chromedriver'])
        os.environ["webdriver.chrome.driver"] = conf['chromedriver']
        self.browser.implicitly_wait(10)
        self.conf = conf['sites'][siteName]

    def login(self):
        self.browser.get(self.conf['url'])

        # 自动填充用户名密码
        inputUserName = self.browser.find_element_by_id('username')
        inputPasswd   = self.browser.find_element_by_id('password')
        # inputRmNum    = self.browser.find_element_by_id('rmNum')
        btnLogin      = self.browser.find_element_by_class_name('buttons__login-bar--login')
        inputUserName.send_keys(self.conf['username'])
        inputPasswd.send_keys(self.conf['passwd'])
        print '自动填充用户名密码'
        btnLogin.click()

    def clear(self):
        try:
            self.browser.close()
            self.browser.quit()
        except Exception, e:
            pass
        finally:
            print '关闭浏览器退出'


if __name__ == '__main__':
    try:
        s = Site('weide')
        s.login()
        time.sleep(100)
    except Exception, e:
        raise e
    finally:
        s.clear()

