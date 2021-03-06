#/usr/bin/env python
# coding:utf8
import json
import time
import os
import urllib
import random
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytesseract
from PIL import Image

from conf import conf

class Site(object):
    def __init__(self):
        self.siteName = 'baizun'
        # self.browser = webdriver.Chrome(conf['chromedriver'])
        # os.environ["webdriver.chrome.driver"] = conf['chromedriver']
        self.browser = webdriver.PhantomJS()
        self.browser.implicitly_wait(10)
        self.conf = conf['sites'][self.siteName]

    def getVerifyCode(self, imgUrl=''):
        # api = 'http://api.shikexin.com/ws/api/verifyCodeRead?appKey=dda9e208e6255dd2da3e36fd6fab7a31&codetype=1004&filetype=2&imgurl=%s' % imgUrl
        api = 'http://www.zun1777.com/app/member/verify/mkCode.php?_=%s%s' % (random.random(), ('%.3f' % time.time()).replace('.', ''))
        f = urllib.urlopen(api)
        spl = f.readline().split(';')
        # self.browser.find_element_by_name('SS').send_keys(spl[0])
        # self.browser.find_element_by_name('SR').send_keys(spl[1])
        # self.browser.find_element_by_name('TS').send_keys(spl[2])
        self.browser.execute_script('document.getElementsByName("SS").value = "%s";' % spl[0])
        self.browser.execute_script('document.getElementsByName("SR").value = "%s";' % spl[1])
        self.browser.execute_script('document.getElementsByName("TS").value = "%s";' % spl[2])
        print spl

        imgUrl = 'http://www.zun1777.com/tpl/commonFile/images/gdpic/macpic.php?SR=%s' % spl[1]
        api = 'http://api.shikexin.com/ws/api/verifyCodeRead?appKey=dda9e208e6255dd2da3e36fd6fab7a31&codetype=1004&filetype=2&imgurl=%s' % imgUrl
        f = urllib.urlopen(api)
        ret = f.readline()
        ret = json.loads(ret)
        print ret
        return ret['data']['verifyCode']

    def login(self):
        self.browser.get(self.conf['url'])
        # print self.browser.page_source

        # 切到iframe
        self.browser.execute_script('document.getElementsByTagName("iframe")[0].id="iframe"')
        self.browser.switch_to.frame("iframe")
        print '切到iframe'

        # 等待浮框加载后关掉
        try:
            element = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ui-dialog-titlebar-close"))
            )
            btnCloseDialog = self.browser.find_element_by_class_name('ui-dialog-titlebar-close')
            btnCloseDialog.click()
            print '关掉广告浮层'
        except Exception, e:
            print '关掉广告浮层失败，未找到'

        # 自动填充用户名密码
        inputUserName = self.browser.find_element_by_id('username')
        inputPasswd   = self.browser.find_element_by_id('passwd')
        inputRmNum    = self.browser.find_element_by_id('rmNum')
        btnLogin      = self.browser.find_element_by_class_name('btnLogin')
        inputUserName.send_keys(self.conf['username'])
        inputPasswd.send_keys(self.conf['passwd'])
        print '点击获取验证码'
        inputRmNum.click()
        while True:
            time.sleep(1)
            img      = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.ID, "vPic")))
            # self.browser.maximize_window()
            # print self.browser.get_window_size()
            self.browser.save_screenshot('/Users/zhaixinrui/tmp.png')  #截取当前网页，该网页有我们需要的验证码
            location = img.location  #获取验证码x,y轴坐标
            size     = img.size  #获取验证码的长宽
            rangle   = (int(location['x']),int(location['y']),int(location['x']+size['width']),int(location['y']+size['height'])) #写成我们需要截取的位置坐标
            # rangle   = [i*2 for i in rangle]
            print location, size, rangle
            tmpImg   = Image.open("/Users/zhaixinrui/tmp.png") #打开截图
            frame4   = tmpImg.crop(rangle)  #使用Image的crop函数，从截图中再次截取我们需要的区域
            frame4.save('/Users/zhaixinrui/frame4.jpg')
            vc       = pytesseract.image_to_string(Image.open('/Users/zhaixinrui/frame4.jpg')) #使用image_to_string识别验证码
            vc = filter(lambda x:x.isdigit(),vc)
            if len(vc) == 4:
                print '自动填充验证码：' + vc
                inputRmNum.send_keys(vc)
                btnLogin.click()
                break
            else:
                print '获取验证码失败：' + vc
                img.click()
                continue

        # # 登录成功后自动关掉提示框
        # WebDriverWait(self.browser,10).until(EC.alert_is_present())
        # self.browser.switch_to.alert.accept()
        # WebDriverWait(self.browser,10).until(EC.alert_is_present())
        # self.browser.switch_to.alert.accept()
        # print '登录成功后自动关掉提示框'

        # 同意用户协议
        btns = self.browser.find_elements_by_class_name('za_button')
        btns[1].click()
        print '同意用户协议'

        # 等待浮框加载后关掉
        try:
            btnCloseDialog = WebDriverWait(self.browser, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ui-dialog-titlebar-close"))
            )
            btnCloseDialog = self.browser.find_element_by_class_name('ui-dialog-titlebar-close')
            time.sleep(1)
            btnCloseDialog.click()
            print '关掉支付提示浮层'
        except Exception, e:
            print '关闭支付提示浮层失败，未找到'

    def touzhu(self):
        while True:
            try:
                # print self.browser.page_source
                a1 = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.LINK_TEXT, "体育赛事")))
                ActionChains(self.browser).move_to_element(a1).perform()
                a2 = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.LINK_TEXT, "体育投注")))
                a2.click()
                print '跳转投注页'
                break
            except Exception, e:
                time.sleep(1)


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
        s = Site()
        s.login()
        s.touzhu()
        time.sleep(10)
        print s.browser.page_source
        time.sleep(100000)
    # except Exception, e:
    #     raise e
    finally:
        s.clear()
