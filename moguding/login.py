# !/usr/bin/env python
# coding: utf-8

# 超级鹰实现登录
# 作者：江致远，楼宇鑫
# 作者邮箱：1914813051@qq.com
# 语雀链接：https://www.yuque.com/ol1q37/gi94xp/kcrzm7
# 修改日期：2020年12月15日
# 注：超级鹰的使用需要将电脑分辨率改为100%


import time
from hashlib import md5
import requests
from selenium import webdriver
from PIL import Image
from global_config import *
# 首先，我们可以看到login这个文件的代码，这个文件是作为库被调用的，其作用为实现蘑菇丁这个网站的自动登录功能，最开始是调用了本次代码所需实现的库，那么接下来我们往下看。




class Chaojiying_Client(object):
    """
    超级鹰自带的代码
    """
    def __init__(self, username, password, soft_id):
        self.username = username
        password =  password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data = params, files = files, headers = self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data = params, headers = self.headers)
        return r.json()
# 上面的一大段代码为超级鹰自带的代码，作用是实现超级鹰的实现验证码功能。




def _f1(username,password,wait_time):
    """
    自动输入账号密码
    """
    driver = webdriver.Chrome()
    driver.get("https://www.moguding.net/login")
    driver.maximize_window()
    # (1)登录页面截图
    driver.save_screenshot(save_screenshot)# 可以修改保存地址
    # (2)基操
    driver.find_element_by_name("username").click()  # 点击
    driver.find_element_by_name("username").clear()  # 清空原来内容
    driver.find_element_by_name("username").send_keys(username) # 账号输入
    driver.find_element_by_name("password").click()
    driver.find_element_by_name("password").clear()
    driver.find_element_by_name("password").send_keys(password)
    time.sleep(wait_time)
    return driver
# 接下来，我们可以看到这个函数，这个函数的代码量不多，其效果也是很简单，就是巨大化网页，然后截图，并且对蘑菇丁的登录页面实现输入账号密码的操作



def _f2(driver,implicitly_time,wait_time,get_code_image,image_screenshot,save_screenshot,chaojiying_usename,chaojiying_password,chaojiying_userid):
    """
    获取验证码以及输入验证码的全过程
    """
    #(3)获取图片验证码坐标
    code_ele = driver.find_element_by_xpath("//*[@class='codeimg']")
    #driver.find_element_by_xpath('//div[@class="codeimg"]/a[1]').click()

    print("验证码的坐标为：{'x': 1500, 'y': 600}", code_ele.location) # 控制台查看{'x': 1086, 'y': 368}

    print("验证码的大小为：{'height': 40, 'width': 110}", code_ele.size)# 图片大小{'height': 40, 'width': 110}
    # (4)图片4个点的坐标位置
    left = code_ele.location['x'] #x点的坐标
    top = code_ele.location['y']  #y点的坐标
    right = code_ele.size['width'] + left #上面右边点的坐标
    height = code_ele.size['height'] + top #下面右边点的坐标
    image = Image.open(image_screenshot)
    # (5)将图片验证码截取
    code_image = image.crop((left, top, right, height))
    code_image.save(get_code_image)#截取的验证码图片保存为新的文件
    # time.sleep(wait_time)
    chaojiying = Chaojiying_Client(chaojiying_usename, chaojiying_password, chaojiying_userid)  #用户中心>>软件ID 生成一个替换 96001
    im = open(get_code_image, 'rb').read()  #本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
    # print(chaojiying.PostPic(im, 1902))  #1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()
    yzm = chaojiying.PostPic(im, 1902)['pic_str']
    print(yzm)
    # time.sleep(wait_time)
    driver.find_element_by_xpath("(//input[@type='text'])[2]").click()#定位验证码
    driver.find_element_by_xpath("(//input[@type='text'])[2]").send_keys(yzm)
    return driver
# 这个函数的代码量就比刚刚的那个函数大多了，我们可以逐步减小分析，最前面的两个步骤（通过注释来看就是（3）和（4）），这个步骤的作用为获取图片验证码的坐标以及
# 获取图片四个点的坐标，那么，获取这四个点的坐标的作用是什么呢，我们为什么要获取这个坐标呢
# 我们从接下来的代码就可以看到，获取四个坐标之后，我们对验证码的图片进行截图，然后通过制定好验证码的类型之后调用了超级鹰的代码，成功识别了验证码





def _f3(driver):
    """
    判定验证码是否正确，如果验证码错误，则返回false
    """
    driver.find_element_by_xpath("//button[@type='button']").click() # 点击登录
    time.sleep(wait_time)
    html = driver.page_source
    a = html.find('验证码错误')
    if a == -1:
        # 没找到验证码错误
        print("没找到‘验证码错误’")
        return False
    else:
        # 找到了验证码错误
        # 清空验证码
        driver.find_element_by_xpath("(//input[@type='text'])[2]").clear()
        print("找到了‘验证码错误’")
        return True
# 但是验证码可能会识别成功，也有识别失败的情况，所以，这个函数的作用为判断验证码是否识别成功
# 如果验证码识别成功，那么就会直接运行下去，如果验证码没有识别成功，那么就会清空验证码，然后重新识别验证码，直到成功为止




def f_all(username,password,implicitly_time,wait_time,get_code_image,image_screenshot,save_screenshot,chaojiying_usename,chaojiying_password,chaojiying_userid):
    """
    前面定义的函数的总流程
    """
    driver = _f1(username,password,wait_time)
    ret = True
    while ret:
        driver = _f2(driver,implicitly_time,wait_time,get_code_image,image_screenshot,save_screenshot,chaojiying_usename,chaojiying_password,chaojiying_userid)
        time.sleep(wait_time)
        ret = _f3(driver)
    return driver
# 这个函数，将前面的所有函数都连在了一起，在调用这个库的时候，只需要调用这个函数就可以实现上面的所有功能。