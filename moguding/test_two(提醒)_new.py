# !/usr/bin/env python
# coding: utf-8

# 蘑菇丁查找没写周报的学生（新）
# 作者：江致远
# 作者邮箱：1914813051@qq.com
# 语雀链接：https://www.yuque.com/ol1q37/gi94xp/kcrzm7
# 修改日期：2021年10月13日

from selenium import webdriver
import time
import random
import os
import re
import os.path
import datetime
import schedule
from PIL import Image
import requests
from hashlib import md5
from login_new import * #添加login文件进去
from global_config import *
from selenium.webdriver.common.keys import Keys
from dingding_robbot import *


def get_write_list(driver,wait_time):
    """
    爬取周报页面所有的提交者的姓名和提交日期，并且存入列表write中
    """
    url = "https://www.moguding.net/practice-reportReviewweek"
    driver.get(url)
    time.sleep(wait_time)
    driver.find_element_by_xpath("//div[@id='app']/div/div[3]/section/div/div/div[2]/button/span").click()  #作用是点击周报未提交名单
    time.sleep(wait_time)
    html = driver.page_source
    reobj = re.compile(r'<td rowspan="1" colspan="1" class="el-table_2_column_16 is-center "><div class="cell"><span>([\d\D]*?)</span></div></td>')
    not_write_student_list = reobj.findall(html)
    return not_write_student_list

def get_number_list(not_write_student_list):
    not_student_phone_number = []
    for student_message in student_message_list:
        for not_write_student in not_write_student_list:
            if student_message[0] == not_write_student:
                not_student_phone_number.append(student_message[1])
    not_write_student_remind_dingding = "有" + str(len(not_write_student_list)) + "位同学未写周报，" + "请尽快写周报"

    return not_student_phone_number,not_write_student_remind_dingding

if __name__ == "__main__":
    driver = login(username,password,wait_time)
    time.sleep(wait_time)
    not_write_student_list = get_write_list(driver,wait_time)
    not_student_phone_number,not_write_student_remind_dingding = get_number_list(not_write_student_list)
    all_robbot(not_write_student_remind_dingding,at_mobiles = not_student_phone_number)
