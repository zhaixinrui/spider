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
from selenium.webdriver.common.action_chains import ActionChains
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

        try:
            # 登录成功后自动关掉提示框
            WebDriverWait(self.browser, 10).until(EC.alert_is_present())
            self.browser.switch_to.alert.accept()
            WebDriverWait(self.browser, 10).until(EC.alert_is_present())
            self.browser.switch_to.alert.accept()
            print '登录成功后自动关掉提示框'
        except Exception, e:
            pass

        # 同意用户协议
        btns = self.browser.find_elements_by_class_name('za_button')
        btns[1].click()
        print '同意用户协议'
        time.sleep(5)

    def touzhu(self):
        try:
            # print self.browser.page_source
            # element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "LS-first")))
            a1 = s.browser.find_element_by_link_text('体育赛事')
            action = ActionChains(self.browser);
            action.move_to_element(a1).perform();
            a2 = s.browser.find_element_by_link_text('体育投注')
            a2.click()
        except Exception, e:
            print '跳投注页异常'

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
        s.touzhu()
        time.sleep(10000)
    except Exception, e:
        raise e
    finally:
        s.clear()

