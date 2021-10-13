# !/usr/bin/env python
# coding:utf-8

# 教师月报的编写（半成品）
# 作者：江致远
# 作者邮箱：1914813051@qq.com
# 语雀链接：https://www.yuque.com/ol1q37/gi94xp/kcrzm7
# 修改日期：2020年7月29日


from selenium import webdriver
import time
import random
import csv
import os
import re
import schedule
from PIL import Image
import datetime
import codecs
import pyautogui
import requests
import os.path
from hashlib import md5
from login import * #添加login文件进去
from global_config import *
from selenium.webdriver.common.keys import Keys
from dingding_robbot import *


class NumberToHanzi():
    '''
      把一个四位的数字字符串变成汉字字符串
      num_str 需要被转换的四位的数字字符串
      返回四位的数字字符串被转换成汉字字符串
    '''
    def __init__(self):
        self.han_list = ["零" , "一" , "二" , "三" , "四" , "五" , "六" , "七" , "八" , "九"]
        self.unit_list = ["十" , "百" , "千"]

    def four_to_hanstr(self,num_str):
        result = ""
        num_len = len(num_str)
        for i in range(num_len):
            num = int(num_str[i])
            if i != num_len - 1 and num != 0 :
                result += self.han_list[num] + self.unit_list[num_len - 2 - i]
            else :
                if num == 0 and result and result[-1] == "零":
                    continue
                else:
                    result += self.han_list[num]
        return result

    def dig2cn(self,num_str):
        str_len = len(num_str)
        if str_len > 12 :
            print("数字太大，翻译不了")
            return
        # 如果大于8位，包含单位亿
        elif str_len > 8:
            hanstr = self.four_to_hanstr(num_str[:-8]) + "亿" + \
                self.four_to_hanstr(num_str[-8: -4]) + "万" + \
                self.four_to_hanstr(num_str[-4:])
        # 如果大于4位，包含单位万
        elif str_len > 4:
            hanstr = self.four_to_hanstr(num_str[:-4]) + "万" + \
                self.four_to_hanstr(num_str[-4:])
        else:
            hanstr = self.four_to_hanstr(num_str)

        if hanstr[-1] == "零":
            hanstr = hanstr[:-1]
        return hanstr


def _get_month(driver,wait_time):
    """
    完成选择月份的操作
    """    
    # 点击选择月份
    driver.find_element_by_xpath("//div[@id='app']/div/div[3]/section/div/div[4]/div/div[2]/div/form/div/div/div/span/i").click()
    month = datetime.datetime.now().month
    num = str(datetime.datetime.now().month)
    nth = NumberToHanzi()
    chinese_month = nth.dig2cn(num) + "月"
    time.sleep(wait_time)
    driver.find_element_by_link_text(u"" + chinese_month + "").click()
    return month,chinese_month,driver


def _get_title(driver,chinese_month,wait_time):
    """
    完成输入标题的操作
    """
    # 点击标题框
    driver.find_element_by_xpath("(//input[@type='text'])[5]").click()
    time.sleep(wait_time)
    # 清空标题框
    driver.find_element_by_xpath("(//input[@type='text'])[5]").clear()
    time.sleep(wait_time)
    # 输入标题
    driver.find_element_by_xpath("(//input[@type='text'])[5]").send_keys("" + chinese_month + "份走访月报" + "")
    return driver


def _get_particulars(driver,month,wait_time,test_four_folder):
    """
    完成输入内容的操作
    """
    f = open(test_four_folder + "\\" + str(month) + ".txt","r",encoding = "utf-8")   # 设置文件对象
    datalist = f.readlines()  #直接将文件中按行读到list里，效果与方法2一样
    f.close()             #关闭文件
    str_datalist = str(datalist)
    fin_str_datalist = str_datalist[2:-2]
    # 点击详情框
    driver.find_element_by_xpath("//div[@id='app']/div/div[3]/section/div/div[4]/div/div[2]/div/form/div[3]/div/div/textarea").click()
    time.sleep(wait_time)
    # 清空详情框
    driver.find_element_by_xpath("//div[@id='app']/div/div[3]/section/div/div[4]/div/div[2]/div/form/div[3]/div/div/textarea").clear()
    time.sleep(wait_time)
    # 输入详情
    driver.find_element_by_xpath("//div[@id='app']/div/div[3]/section/div/div[4]/div/div[2]/div/form/div[3]/div/div/textarea").send_keys(r"" + fin_str_datalist + "")
    return driver


def _get_photo(driver,wait_time,month,test_four_folder):
    """
    完成上传图片的操作
    """
    driver.find_element_by_xpath("//div[@id='app']/div/div[3]/section/div/div[4]/div/div[2]/div/form/div[4]/div/div/div/div/i").click()
    time.sleep(wait_time)
    pyautogui.hotkey("ALT", "N")
    time.sleep(wait_time)
    pyautogui.typewrite(test_four_folder + "\\" + str(month) + ".jpg") 
    time.sleep(wait_time)
    pyautogui.hotkey("enter")
    time.sleep(wait_time)
    pyautogui.hotkey("ALT", "O")
    return driver


def _get_accessory(driver,month,wait_time,test_four_folder):
    """
    完成上传附件的操作
    """
    driver.find_element_by_xpath("//div[@id='acc-upload']/div/div/div/button/span").click()
    time.sleep(wait_time)
    pyautogui.hotkey("ALT", "N")
    time.sleep(wait_time)
    pyautogui.typewrite(test_four_folder + "\\" + str(month) + ".docx") 
    time.sleep(wait_time)
    pyautogui.hotkey("enter")
    time.sleep(wait_time)
    pyautogui.hotkey("ALT", "O")
    return driver


def _all(driver,wait_time):
    """
    执行新增月报的所有过程
    """
    url = "https://www.moguding.net/practice-teaMonthly"
    driver.get(url)
    time.sleep(wait_time)
    # 点击新增月报
    driver.find_element_by_xpath("//div[@id='app']/div/div[3]/section/div/div/div/p").click()
    time.sleep(wait_time)
    month,chinese_month,driver = _get_month(driver,wait_time)
    time.sleep(wait_time)
    driver = _get_title(driver,chinese_month,wait_time)
    time.sleep(wait_time)
    driver = _get_particulars(driver,month,wait_time,test_four_folder)
    time.sleep(wait_time)
    driver = _get_photo(driver,wait_time,month,test_four_folder)
    time.sleep(wait_time)
    driver = _get_accessory(driver,month,wait_time,test_four_folder)
    time.sleep(wait_time)
    # increase_ok = driver.find_element_by_xpath('//span[text()="确定"]')
    # driver.execute_script("arguments[0].click();",increase_ok)


def _test_four_job(username,password,implicitly_time,wait_time,get_code_image,image_screenshot,save_screenshot,chaojiying_usename,chaojiying_password,chaojiying_userid):
    """
    执行登录和新增月报的所有过程
    """
    driver = f_all(username,password,implicitly_time,wait_time,get_code_image,image_screenshot,save_screenshot,chaojiying_usename,chaojiying_password,chaojiying_userid)  
    _all(driver,wait_time)


def job():
    _test_four_job(username,password,implicitly_time,wait_time,get_code_image,image_screenshot,save_screenshot,chaojiying_usename,chaojiying_password,chaojiying_userid)


if __name__ == "__main__":
    """
    设置每个月执行一次
    """
    execute_times = "17:01"
    schedule.every().day.at(execute_times).do(job)
    while True:
        day = datetime.datetime.now().day
        if day == 5 :
            schedule.run_pending()
            time.sleep(wait_time)


