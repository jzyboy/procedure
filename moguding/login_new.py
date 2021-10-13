# !/usr/bin/env python
# coding: utf-8

# 蘑菇丁项目登录模块（新）（测试）
# 作者：江致远
# 作者邮箱：1914813051@qq.com
# 语雀链接：https://www.yuque.com/ol1q37/gi94xp/kcrzm7
# 修改日期：2021年10月13日

from selenium import webdriver
import time
import random
import csv
import os
import re
from global_config import *
from PIL import Image

def login(username,password,wait_time):
    driver = webdriver.Chrome()    # 这里复制过来是需要缩进的
    driver.get("https://www.moguding.net/login")
    driver.maximize_window()
    driver.find_element_by_name("username").click()  # 点击
    driver.find_element_by_name("username").clear()  # 清空原来内容
    driver.find_element_by_name("username").send_keys(username) # 账号输入
    driver.find_element_by_name("password").click()
    driver.find_element_by_name("password").clear()
    driver.find_element_by_name("password").send_keys(password)#密码输入
    driver.find_element_by_xpath("(//input[@type='text'])[2]").click()
    time.sleep(wait_time)
    driver.find_element_by_xpath("//button[@type='button']").click()#点击确定
    time.sleep(wait_time)
    driver.find_element_by_xpath("//button[2]/span").click() #点击确定
    return driver