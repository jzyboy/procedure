# !/usr/bin/env python
# coding: utf-8

# 爬取学生的姓名和电话号码，作为钉钉机器人的@用处
# 作者：江致远
# 作者邮箱：1914813051@qq.com
# 修改日期：2021年2月25日


from selenium import webdriver
import time
import random
import csv
import os
import re
from PIL import Image
import requests
from hashlib import md5
import pyautogui
import xlrd
from lxml import etree
from global_config import *
from login import * #添加login文件进去
from dingding_robbot import *
from get_chaojiying_tifen import *


student_data = []


def get_student_data(html):
    reobj = re.compile(r'<span data-v-74ef62c3="">姓名[\d\D]*?</span>([\d\D]*?)<[\d\D]*?电话[\d\D]*?>([\d\D]*?)<')
    for match in reobj.finditer(html):
        student_name = match.group(1)
        student_phone = match.group(2)
        a_student_data = [student_name,student_phone]
        return a_student_data


if __name__ == "__main__":
     # 登录
    driver = f_all(username,password,implicitly_time,wait_time,get_code_image,image_screenshot,save_screenshot,chaojiying_usename,chaojiying_password,chaojiying_userid)
    student_url = "https://www.moguding.net/practice-myIntern"
    driver.get(student_url)
    time.sleep(wait_time)
    student_list_html = driver.page_source
    reobj = re.compile(r'column_1  "><div class="cell"><span>([\d\D]*?)</span></div>')
    student_list = reobj.findall(student_list_html)
    time.sleep(wait_time)
    for i in range(1,len(student_list) + 1):
        driver.find_element_by_xpath("//div[@id='app']/div/div[3]/section/div/div[3]/div/div[4]/div[2]/table/tbody/tr[" + str(i) + "]/td[8]/div/button/span").click()
        time.sleep(wait_time)
        html = driver.page_source
        a_student_data = get_student_data(html)
        print(a_student_data)
        student_data.append(a_student_data)
        time.sleep(wait_time)
        driver.back()
        time.sleep(wait_time)
    
    print(student_data)
    
    # 调用api获取超级鹰账号剩余的题分
    tifen_message = "剩余题分:" + str(get_chaojiying_tifen(chaojiying_usename,chaojiying_password))
    # 在钉钉群里提醒剩余的题分
    all_robbot(tifen_message,at_mobiles = [])
        