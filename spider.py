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


try:
    chromedriver = "/usr/local/bin/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver

    browser = webdriver.Chrome(chromedriver)
    browser.implicitly_wait(10)
    browser.get("http://www.beequick.cn")
    browser.execute_script('$("iframe").attr("id", "iframe");')
    print browser.get_log('driver')
    # time.sleep(4)
    browser.switch_to.frame("iframe")
    # browser.set_page_load_timeout(4)
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "title-addrname"))
        )
    except Exception, e:
        raise e
    # print browser.page_source
    titleaddrname = browser.find_element_by_class_name('title-addrname')
    titleaddrname.click()
    phone = browser.find_element_by_id('autocomplete-phone')
    phone.send_keys('18612295528')
    buttonGetCode = browser.find_element_by_class_name('login-send')
    buttonGetCode.click()
    inputCode = browser.find_element_by_class_name('login-input-code')
    buttonSubmit = browser.find_element_by_class_name('login-submit')
    while True:
        v = inputCode.get_attribute("value")
        if(len(v) == 4):
            buttonSubmit.click()
            break
        time.sleep(0.1)

    inputs = browser.find_element_by_tag_name('input')
    # print inputs
    span = browser.find_elements_by_css_selector('.title-addrname', )
    # print span
    # print span.text()
    # span.click()
    ul = browser.find_element_by_id('mod-navs')
    # print ul.text()
    # print ul.get_attribute('class')
    li = browser.find_element_by_tag_name('li')
    # print li

    # browser.close()
    # browser.quit()
except Exception, e:
    raise

finally:
    time.sleep(10)
    browser.close()
    browser.quit()
