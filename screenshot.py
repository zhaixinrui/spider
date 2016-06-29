from PIL import Image
import pytesseract
from selenium import webdriver

url='http://xxxxx.com'
driver = webdriver.Chrome()
driver.maximize_window()  #将浏览器最大化
driver.get(url)
driver.save_screenshot('f://aa.png')  #截取当前网页，该网页有我们需要的验证码
imgelement = driver.find_element_by_xpath('//img[@src="rand!loginRand.action"]')  #定位验证码
location = imgelement.location  #获取验证码x,y轴坐标
size=imgelement.size  #获取验证码的长宽
rangle=(int(location['x']),int(location['y']),int(location['x']+size['width']),int(location['y']+size['height'])) #写成我们需要截取的位置坐标
i=Image.open("f://aa.png") #打开截图
frame4=i.crop(rangle)  #使用Image的crop函数，从截图中再次截取我们需要的区域
frame4.save('f://frame4.jpg')
qq=Image.open('f://frame4.jpg')
text=pytesseract.image_to_string(qq).strip() #使用image_to_string识别验证码
print text
