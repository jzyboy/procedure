# !/usr/bin/env python
# coding: utf-8

# 作者:江致远
# 作者邮箱：1914813051@qq.com
# 修改日期:2021-2-23
# 代码的功能描述:实现蘑菇丁自动给学生打分,分别给校内、企业综合评分打分
# 注：使用此代码分辨率需改为100%


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
from login import * #添加login文件进去
from global_config import *
from get_chaojiying_tifen import *
from dingding_robbot import *


def get_excel_information(test_one_screenshot):
    """
    通过读取excel文件得到列表information
    （information列表内的数据是学生姓名和对应的评分等级）
    """
    rb = xlrd.open_workbook(test_one_screenshot)

    sheet1 = rb.sheet_by_name('Sheet1')

    _student_name = sheet1.col_values(2)
    _student_name = _student_name[5:]

    _student_scare = sheet1.col_values(5)
    _student_scare = _student_scare[5:]

    _information = dict(zip(_student_name, _student_scare))
    
    return _information


def _come_class_page(driver,wait_time):
    
    driver.get("https://www.moguding.net/practice-successEvaluateList") #实习成绩考核页面
    time.sleep(wait_time)
    driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/section/div/div[2]/form/div[1]/div/div/div/input').click()
    time.sleep(wait_time)
    driver.find_element_by_xpath('//*[contains(text(), "2020-2021(当前学年)")]').click()
    # driver.find_element_by_xpath('//*[contains(text(), "2019-2020")]').click()
    time.sleep(wait_time)
    driver.find_element_by_xpath("//div[@id='app']/div/div[3]/section/div/div[2]/form/div[2]/div/div/div/span/span/i").click()
    time.sleep(wait_time)   
    driver.find_element_by_xpath("(//input[@type='text'])[2]").send_keys("2018级商务数据分析与应用顶岗实习")
    time.sleep(wait_time)
    driver.find_element_by_xpath('//*[contains(text(), "2018级商务数据分析与应用顶岗实习")]').click()
    time.sleep(wait_time)
    driver.find_element_by_xpath('//*[contains(text(), "查询")]').click()
    time.sleep(wait_time)
    # 将展示修改为100条/页
    driver.find_element_by_xpath("(//input[@type='text'])[10]").click()
    time.sleep(wait_time)
    click_page = driver.find_element_by_xpath('//span[text()="100条/页"]')
    driver.execute_script("arguments[0].click();",click_page) 



def _extract_student_chinese_name(_student_page_html):
    """
    获取当前页面的学生名单，将其存入列表names中
    """
    _names = []
    reobj = re.compile(r'<td rowspan="1" colspan="1" class="el-table_1_column_1  "><div class="cell"><span>([\d\D]*?)</span>')
    for match in reobj.finditer(_student_page_html):
        _names.append(match.group(1))
    print(_names)
    return _names



def _get_scores(_html):
    """
    获取每一个细分项的最大分值
    如：['20', '5', '10', '10', '10', '5', '5', '5', '5', '5', '10', '10']
    """
    _scores = []
    reobj = re.compile(r'class="items-child-item"><span data-v-7a63d630="">[\d\D]*?（([\d\D]*?)%')
    for match in reobj.finditer(_html):
        a = match.group(1)
        _scores.append(a)
    return _scores



def _get_grade_stiuation(_scores,_grade_percentage):
    """
    将每个打分项的最大分值通过百分比和取整得到该学生该打分项的得分情况
    """
    print(_grade_percentage)
    _grade_stiuation = []
    for index in range(len(_scores)):
        x = round(int(_scores[index])*_grade_percentage)
        _grade_stiuation.append(str(x))
    return _grade_stiuation



def _grade_process(_grade_stiuation,driver,wait_time):
    """
    一位学生的打分过程
    """
    n = len(_grade_stiuation)
    time.sleep(wait_time)
    for i in range(n):
        a_time_grade_stiuation = _grade_stiuation[i]
        time.sleep(wait_time)
        
        # 报错处理
        try:
            driver.find_element_by_xpath("(//input[@type='text'])[" + str(i+2) + "]").click()
        except:
            print("打分报错")
            _grade_process(_grade_stiuation)

        # 每一次打分的代码    
        driver.find_element_by_xpath("(//input[@type='text'])[" + str(i+2) + "]").clear()
        driver.find_element_by_xpath("(//input[@type='text'])[" + str(i+2) + "]").send_keys(a_time_grade_stiuation)
        time.sleep(wait_time)
        driver.find_element_by_xpath("(//input[@type='text'])[" + str(i+2) + "]").clear()
        driver.find_element_by_xpath("(//input[@type='text'])[" + str(i+2) + "]").send_keys(a_time_grade_stiuation)
        print(a_time_grade_stiuation)
        


def _click_check(i,wait_time,driver):
    """
    考核打分的过程的报错处理
    """
    # 报错处理
    try:
        time.sleep(wait_time)
        driver.find_element_by_xpath("//div[@id='app']/div/div[3]/section/div/div[3]/div/div[3]/table/tbody/tr[" + str(i) + "]/td[17]/div/button/span").click()
    except:
        print("审核报错")
        print(i)
        _click_check(i,wait_time,driver)



def _a_student_grade_process(xpath,driver,wait_time,_grade_percentage,_scores_grade):    
    """
    企业综合评分和校内评分的通用格式
    （这块可能会报错，需要增加报错重启代码）
    """
    # 报错处理
    try:
        time.sleep(wait_time)
        driver.find_element_by_xpath(xpath).click()   #点击校内评分或者点击企业综合评分，由变量xpath决定
    except:
        print("修改报错")
        _a_student_grade_process(xpath,driver,wait_time,_grade_percentage,_scores_grade)
        
    time.sleep(wait_time)
    
    _scores_html = driver.page_source
    _scores = _get_scores(_scores_html)

    _grade_stiuation = _get_grade_stiuation(_scores,_grade_percentage)
    print(_grade_stiuation,"dddddddddddddddddddddD")
    _grade_process(_grade_stiuation,driver,wait_time)

    
    # 点击确定
    driver.find_element_by_xpath("//div[@id='app']/div/div[3]/section/div/div[5]/div/div[2]/div/div[2]").click()
    driver.find_element_by_xpath("//div[@id='app']/div/div[3]/section/div/div[5]/div/div[3]/span/button[2]/span").click()
    


def _a_student_all_grade_process(i,_names,driver,wait_time,_information,percents):
    # 定位到考核打分，进行模拟点击
    time.sleep(wait_time)
    #爬取名字
    _scores_grade = _information.get(_names[i-1])
    print(_names[i-1])
    print(_scores_grade)
    # 获取成绩等级的对应的百分比，如 {"优":0.93,"良":0.83,"中":0.73,"中等":0.73,"及格":0.63,"不及格":0.5}
    _grade_percentage = percents[_scores_grade]
    # 调用输入分数的函数   
    _a_student_grade_process("//div[@id='app']/div/div[3]/section/div/div[4]/div/div[2]/div[4]/div[2]/table/tbody/tr/td[4]/div/button",driver,wait_time,_grade_percentage,_scores_grade)
    time.sleep(wait_time)
    _a_student_grade_process("//div[@id='app']/div/div[3]/section/div/div[4]/div/div[2]/div[4]/div[2]/table/tbody/tr[2]/td[4]/div/button",driver,wait_time,_grade_percentage,_scores_grade)
    time.sleep(wait_time)
    # 返回实现成绩考核页面
    driver.back()
    time.sleep(wait_time)



if __name__ == '__main__':
    # 登录
    driver = f_all(username,password,implicitly_time,wait_time,get_code_image,image_screenshot,save_screenshot,chaojiying_usename,chaojiying_password,chaojiying_userid)  
    # 实现将excel中的姓名列和评级列的数据转化为列表information。
    _information = get_excel_information(test_one_screenshot)
    # 将浏览器的网页跳转到实习成绩考核页面
    _come_class_page(driver,wait_time)
    # 通过循环实现为每个学生打分的过程
    for i in range(1,len(_information) + 1):
        # 获取html，并且打印出学生列表
        _student_page_html = driver.page_source
        _names = _extract_student_chinese_name(_student_page_html)
        # 点击考核打分
        _click_check(i,wait_time,driver)
        # 实现单个学生的校内老师评分和企业综合评分
        _a_student_all_grade_process(i,_names,driver,wait_time,_information,percents)
    # 调用api获取超级鹰账号剩余的题分
    tifen_message = "剩余题分:" + str(get_chaojiying_tifen(chaojiying_usename,chaojiying_password))
    # 在钉钉群里提醒剩余的题分
    all_robbot(tifen_message,at_mobiles = [])
    
