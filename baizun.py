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

url = 'http://www.zun1777.com/'
username = 'bbccaa243'
passwd = 'asd1122'
chromedriver = "/usr/local/bin/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver

try:
    browser = webdriver.Chrome(chromedriver)
    browser.implicitly_wait(10)
    browser.get(url)
    # print browser.page_source

    # 切到iframe
    browser.execute_script('document.getElementsByTagName("iframe")[0].id="iframe"')
    browser.switch_to.frame("iframe")
    print '切到iframe'

    # 等待浮框加载后关掉
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ui-dialog-titlebar-close"))
        )
        btnCloseDialog = browser.find_element_by_class_name('ui-dialog-titlebar-close')
        btnCloseDialog.click()
    except Exception, e:
        raise e
    print '关掉广告浮层'

    # 自动填充用户名密码
    inputUserName = browser.find_element_by_id('username')
    inputPasswd   = browser.find_element_by_id('passwd')
    inputRmNum    = browser.find_element_by_id('rmNum')
    btnLogin      = browser.find_element_by_class_name('btnLogin')
    inputUserName.send_keys(username)
    inputPasswd.send_keys(passwd)
    print '自动填充用户名密码'

    # 等待验证码填写完成后登录
    while True:
        v = inputRmNum.get_attribute("value")
        if(len(v) == 4):
            btnLogin.click()
            break
        time.sleep(0.1)

    # 登录成功后自动关掉提示框
    WebDriverWait(browser,10).until(EC.alert_is_present())
    browser.switch_to.alert.accept()
    WebDriverWait(browser,10).until(EC.alert_is_present())
    browser.switch_to.alert.accept()
    print '登录成功后自动关掉提示框'

    # 同意用户协议
    btns = browser.find_elements_by_class_name('za_button')
    btns[1].click()
    print '同意用户协议'

    # time.sleep(5)
    # print '页面源码'

    # 等待浮框加载后关掉
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ui-dialog-titlebar-close"))
        )
        btnCloseDialog = browser.find_element_by_class_name('ui-dialog-titlebar-close')
        time.sleep(2)
        btnCloseDialog.click()
        print '关掉支付提示浮层'
    except Exception, e:
        raise e

    time.sleep(1000)

except Exception, e:
    raise

finally:
    time.sleep(300)
    browser.close()
    browser.quit()
