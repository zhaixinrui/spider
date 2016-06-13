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
        # 切到iframe
        self.browser.execute_script('document.getElementsByTagName("iframe")[0].id="iframe"')
        self.browser.switch_to.frame("iframe")
        print '切到iframe'

        # 自动填充用户名密码
        inputUserName = self.browser.find_element_by_id('username')
        inputPasswd   = self.browser.find_element_by_id('passwd')
        inputRmNum    = self.browser.find_element_by_id('rmNum')
        btnLogin      = self.browser.find_element_by_class_name('loginBTN')
        inputUserName.send_keys(self.conf['username'])
        inputPasswd.send_keys(self.conf['passwd'])
        print '自动填充用户名密码'

        # 等待验证码填写完成后登录
        while True:
            v = inputRmNum.get_attribute("value")
            if(len(v) == 4):
                btnLogin.click()
                break
            time.sleep(0.1)

        # 登录成功后自动关掉提示框
        WebDriverWait(self.browser, 10).until(EC.alert_is_present())
        self.browser.switch_to.alert.accept()
        WebDriverWait(self.browser, 10).until(EC.alert_is_present())
        self.browser.switch_to.alert.accept()
        print '登录成功后自动关掉提示框'

        # 同意用户协议
        btns = self.browser.find_elements_by_class_name('za_button')
        btns[1].click()
        print '同意用户协议'

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
        s = Site('jinniu')
        s.login()
    except Exception, e:
        raise e
    finally:
        s.clear()

