# !/usr/bin/env python
# coding: utf-8

# 学生激活情况提醒
# 作者：江致远
# 作者邮箱：1914813051@qq.com
# 语雀链接：https://www.yuque.com/ol1q37/gi94xp/kcrzm7
# 修改日期：2020年7月21日


from selenium import webdriver
import time
import random
import os
import re
import os.path
from PIL import Image
import requests
from hashlib import md5
from login import * #添加login文件进去
from global_config import *
from selenium.webdriver.common.keys import Keys
from dingding_robbot import *


student_information = []
all_student_information = []
not_activation = []


def _inquire(driver,wait_time):
    """
    查询当前学年的所有学生
    """
    time.sleep(wait_time)
    url = "https://www.moguding.net/practice-myIntern"
    driver.get(url)
    time.sleep(wait_time)
    # 下拉列表框，选择2020-2021(当前学年)
    driver.find_element_by_xpath("//input[@type='text']").click()
    time.sleep(wait_time)
    driver.find_element_by_xpath('//*[contains(text(),"2020-2021(当前学年)")]').click()
    time.sleep(wait_time)
    # 下拉列表框，选择2018级商务数据分析与应用顶岗实习
    driver.find_element_by_xpath("(//input[@type='text'])[2]").click()
    time.sleep(wait_time)
    driver.find_element_by_xpath('//*[contains(text(), "2018级商务数据分析与应用顶岗实习")]').click()
    time.sleep(wait_time)
    # 点击查询
    look_up = driver.find_element_by_xpath('//span[text()="查询"]')
    driver.execute_script("arguments[0].click();",look_up) 
    time.sleep(wait_time)
    html = driver.page_source
    return html


def _get_student_information(html):
    """
    将所有学生的姓名的激活状态存入列表all_student_information中
    """
    reobj = re.compile(r'class="el-table_1_column_1  "[\d\D]*?n>([\d\D]*?)<[\d\D]*? class="el-table_1_column_6  "><div class="cell"><span>([\d\D]*?)<')
    for match in reobj.finditer(html):
        name = match.group(1)
        state = match.group(2)
        student_information.append(name)
        student_information.append(state)
        tuple_student_information = tuple(student_information)
        all_student_information.append(tuple_student_information)
        student_information.clear()
    return all_student_information


def _get_not_activation(all_student_information):
    """
    查找出所有学生中未激活学生的姓名，存入列表not_activation中
    """
    for student_information in all_student_information:
        if student_information[1] == "未激活":
            not_activation_student = "@" + student_information[0] 
            not_activation.append(not_activation_student)
    final_not_activation = "有" + str(len(not_activation)) + "位同学未激活蘑菇丁，" + " ".join(not_activation)  + ",请尽快激活"
    return final_not_activation


def all_student_information_final(username,password,implicitly_time,wait_time,get_code_image,image_screenshot,save_screenshot,chaojiying_usename,chaojiying_password,chaojiying_userid):
    # 登录
    driver = f_all(username,password,implicitly_time,wait_time,get_code_image,image_screenshot,save_screenshot,chaojiying_usename,chaojiying_password,chaojiying_userid)  
    # 查询当前学年的所有学生
    html = _inquire(driver,wait_time)
    # 将所有学生的姓名的激活状态存入列表all_student_information中
    all_student_information = _get_student_information(html)
    # 查找出所有学生中未激活学生的姓名，存入列表not_activation中
    final_not_activation = _get_not_activation(all_student_information)
    # 用钉钉机器人提醒未激活的人
    all_robbot(final_not_activation)


if __name__ == "__main__":
    all_student_information_final(username,password,implicitly_time,wait_time,get_code_image,image_screenshot,save_screenshot,chaojiying_usename,chaojiying_password,chaojiying_userid)