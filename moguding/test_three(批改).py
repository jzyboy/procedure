# !/usr/bin/env python
# coding: utf-8

# 蘑菇丁周报批改
# 作者：江致远，李文，王俊杰
# 作者邮箱：1914813051@qq.com
# 语雀链接：https://www.yuque.com/ol1q37/gi94xp/kcrzm7
# 修改日期：2021年9月26日


from selenium import webdriver
import time
import random
import os
import re
import os.path
import schedule
from PIL import Image
import requests
import pyautogui
from hashlib import md5
from login import * #添加login文件进去
from global_config import *
from selenium.webdriver.common.keys import Keys
from get_chaojiying_tifen import *
from dingding_robbot import *


#进入详情页封装：
def navigator_to_week_report_page(wait_time,driver):
    """
    进入周报批阅-未批阅-2021到2022的详情页
    """
    # 直接转到实习中的周报批阅
    url2 = "https://www.moguding.net/practice-reportReviewweek"
    driver.get(url2)
    time.sleep(wait_time)
    # 点击未批阅
    driver.find_element_by_xpath("//div[@id='app']/div/div[3]/section/div/div/div/div/label[3]/span").click()
    # 下拉年份列表框
    driver.find_element_by_xpath('//*[@id = "app"]/div/div[3]/section/div/div[2]/form/div[1]/div/div/div/input').click()
    time.sleep(wait_time)
    driver.find_element_by_xpath('//*[contains(text(), "2021-2022(当前学年)")]').click() 
    # 选择2021-2022(当前学年)这一时间段
    time.sleep(wait_time)
    look_up = driver.find_element_by_xpath('//span[text()="查询"]')
    driver.execute_script("arguments[0].click();",look_up) 
    # 点击查询
    time.sleep(wait_time)

    html = driver.page_source

    return html


def get_cyclic_num(html):
    """
    获得循环的次数
    """
    match = re.search(r'<span class="el-pagination__total">共 ([\d\D]*?)条</span>', html)
    if match:
        student_number = match.group(1)
        print(student_number)
    return int(student_number)


def _get_submit_state(html):
    """
    获取交报告时的状态，是按时还是补交
    """
    match = re.search(r'>报告状态</label>[\d\D]*?style="margin-top: 5px;">([\d\D]*?)<', html)
    if match:
        submit_state = match.group(1)
        print(submit_state)
    return submit_state


def _get_pics_num(html): 
    """
    抽取图片数的函数定义
    """
    reobj = re.compile(r'<img data-v-654df94c="" src="([\d\D]*?)"')#这里不要选择猫头鹰中的倒数第三个，用findall的
    pics = reobj.findall(html)
    pics_num = len(pics)
    return pics_num


def _get_text_long(html):
    """
    获取周报的字数
    """
    text_long = ""
    match = re.search(r'>姓名</label><div class="el-form-item__content" style="margin-left: 80px;">([\d\D]*?)<[\d\D]*?>报告内容</label><div class="el-form-item__content" style="margin-left: 80px;"><div data-v-654df94c="">([\d\D]*?)<d', html)
    if match:
        stu_name = match.group(1).strip()
        text = match.group(2)
        text_long = len(match.group(2).strip())
        print(text_long)
        print(stu_name)
    return text_long


def _get_text_num(text_long,wait_time):
    """
    根据周报的字数判断对应的字数等级  字数大于400即可获得5    大于等于200小于等于400即可获得4
    """
    if text_long < 300:
        text_num = 3
    elif text_long >= 300 and text_long <= 400: 
        time.sleep(wait_time)
        text_num = 4
    else:
        time.sleep(wait_time)
        text_num = 5
    return text_num


def _get_star_num(text_num,pic_num,wait_long,driver,submit_state):
    """
    通过图片数和字数等级以及提交状态来进行评星
    评星规则：先根据字数将级别分为3到5星，然后再根据提交的状态（是按时还是补交）来进行处理
    （如果是按时就不扣星，如果是补交就扣一颗星）
    """
    if pic_num + text_num < 5:
        if submit_state == "按时":
            time.sleep(wait_time)
            # 评3星
            driver.find_element_by_xpath("//div[@id='app']/div/div[3]/section/div/div[3]/form/div[10]/div/div/div/span[3]/i").click()
            
        elif submit_state == "补交":
            time.sleep(wait_time)
            # 评2星
            driver.find_element_by_xpath("//div[@id='app']/div/div[3]/section/div/div[3]/form/div[10]/div/div/div/span[2]/i").click()
            
    elif pic_num + text_num >= 5 and pic_num + text_num < 7:
        if submit_state == "按时":
            time.sleep(wait_time)
            # 评4星
            driver.find_element_by_xpath("//div[@id='app']/div/div[3]/section/div/div[3]/form/div[10]/div/div/div/span[4]/i").click()
            
        elif submit_state == "补交":
            time.sleep(wait_time)
            # 评3星
            driver.find_element_by_xpath("//div[@id='app']/div/div[3]/section/div/div[3]/form/div[10]/div/div/div/span[3]/i").click()
            
    elif pic_num + text_num >= 7:
        if submit_state == "按时": 
            time.sleep(wait_time)
            # 评5星
            driver.find_element_by_xpath("//div[@id='app']/div/div[3]/section/div/div[3]/form/div[10]/div/div/div/span[5]/i").click()
            
        elif submit_state == "补交":
            time.sleep(wait_time)
            # 评4星
            driver.find_element_by_xpath("//div[@id='app']/div/div[3]/section/div/div[3]/form/div[10]/div/div/div/span[4]/i").click()
            


def _get_star(wait_time,driver):
    """
    评星的过程
    """
    time.sleep(wait_time)
    # 获取文本学生详情页的代码
    html = driver.page_source
    # 获取交报告时的状态，是按时还是补交
    submit_state = _get_submit_state(html)
    # 输出同学的名字,通过正则输出长度用于判断星级
    text_long = _get_text_long(html)
    # 衔接定义的图片函数代码块，就能输出出来
    pic_num = _get_pics_num(html)
    # 通过文本字数判断文本等级
    text_num = _get_text_num(text_long,wait_time)
    # 通过文本等级和图片数之和判断应该评的星数
    _get_star_num(text_num,pic_num,wait_time,driver,submit_state)
    
    # 点击评星之后的通过
    read_over = driver.find_element_by_xpath('//span[text()="通过"]')
    driver.execute_script("arguments[0].click();",read_over)
    # 点击批阅之后的确定
    pyautogui.hotkey("enter")
    # driver.find_element_by_xpath("//div[3]/button[2]/span").click()
    


def _put_up_comment(driver,wait_time,list_pingyu):
    """
    评语的过程
    """
    time.sleep(wait_time)
    # 把鼠标焦点放在评语栏上
    driver.find_element_by_xpath("//div[@id='app']/div/div[3]/section/div/div[3]/form/div[15]/div/div/textarea").click()
    time.sleep(wait_time)

    a = ""
    # 产生随机数，随机数random模块已经在开始出导入
    a = int(random.randint(0,4))
    
    # 清除文本框内的内容
    driver.find_element_by_xpath("//div[@id='app']/div/div[3]/section/div/div[3]/form/div[15]/div/div/textarea").clear()
    # 随机选择一条评语放入文本框
    driver.find_element_by_xpath("//div[@id='app']/div/div[3]/section/div/div[3]/form/div[15]/div/div/textarea").send_keys(list_pingyu[a])
    
    time.sleep(wait_time)
    # 点击确定
    put_up = driver.find_element_by_xpath('//span[text()="提交评语"]')
    driver.execute_script("arguments[0].click();",put_up)        
    


def get_star_and_comment(student_number,wait_time,driver,list_pingyu):
    """
    对所有的学生进行评星，评语
    """
    for i in range(1,int(student_number)): 
        
        # 点击进入学生详情界面
        time.sleep(wait_time)
        # join_in = driver.find_element_by_xpath('(//span[text()="批阅" or text()="详情"])['+str(i)+']')
        # driver.execute_script("arguments[0].click();", join_in)
        driver.find_element_by_xpath("//div[@id='app']/div/div[3]/section/div/div[3]/div/div[4]/div[2]/table/tbody/tr["+str(i)+"]/td[15]/div/button/span").click()

        # 评星的过程
        _get_star(wait_time,driver)
        
        # 点击进入学生详情界面
        time.sleep(wait_time)
        # join_in = driver.find_element_by_xpath('(//span[text()="批阅" or text()="详情"])['+str(i)+']')
        # driver.execute_script("arguments[0].click();", join_in)
        driver.find_element_by_xpath("//div[@id='app']/div/div[3]/section/div/div[3]/div/div[4]/div[2]/table/tbody/tr["+str(i)+"]/td[15]/div/button/span").click()

        # 评语的过程
        _put_up_comment(driver,wait_time,list_pingyu)

        # 返回
        back = driver.find_element_by_xpath('//span[text()="周报批阅"]')
        driver.execute_script("arguments[0].click();",back)
        time.sleep(wait_time)
    
    driver.close()
        


if __name__ == "__main__":
    # 登录
    driver = f_all(username,password,implicitly_time,wait_time,get_code_image,image_screenshot,save_screenshot,chaojiying_usename,chaojiying_password,chaojiying_userid)    
    # 下拉列表以及确认
    time.sleep(wait_time)
    pyautogui.hotkey("enter")
    html = navigator_to_week_report_page(wait_time,driver)
    # 获得那一页的循环的次数
    student_number = get_cyclic_num(html)
    # 对所有的学生进行评星，评语
    get_star_and_comment(student_number,wait_time,driver,list_pingyu)
    # 调用api获取超级鹰账号剩余的题分
    tifen_message = "剩余题分:" + str(get_chaojiying_tifen(chaojiying_usename,chaojiying_password))
    test_two_message = "批改已完成"
    # 在钉钉群里提醒剩余的题分
    all_robbot(tifen_message,at_mobiles = [])
    # 在钉钉群里告诉大家批改完成
    all_robbot(test_two_message,at_mobiles = [])


















# def _every_week(username,password,implicitly_time,wait_time,get_code_image,image_screenshot,save_screenshot,chaojiying_usename,chaojiying_password,chaojiying_userid,list_pingyu):
#     """
#     test2的总过程
#     """
#     # 登录
#     driver = f_all(username,password,implicitly_time,wait_time,get_code_image,image_screenshot,save_screenshot,chaojiying_usename,chaojiying_password,chaojiying_userid)    
#     # 下拉列表以及确认
#     html = navigator_to_week_report_page(wait_time,driver)
#     # 获得那一页的循环的次数
#     student_number = get_cyclic_num(html)
#     # 对所有的学生进行评星，评语
#     get_star_and_comment(student_number,wait_time,driver,list_pingyu)
#     # 调用api获取超级鹰账号剩余的题分
#     tifen_message = "剩余题分:" + str(get_chaojiying_tifen(chaojiying_usename,chaojiying_password))
#     test_two_message = "批改已完成"
#     # 在钉钉群里提醒剩余的题分
#     all_robbot(tifen_message,at_mobiles = [])
#     # 在钉钉群里告诉大家批改完成
#     all_robbot(test_two_message,at_mobiles = [])




# def job():
#     try:
#         _every_week(username,password,implicitly_time,wait_time,get_code_image,image_screenshot,save_screenshot,chaojiying_usename,chaojiying_password,chaojiying_userid,list_pingyu)
#     except:
#         job()



# if __name__ == "__main__":
#     schedule.every().sunday.at("22:00").do(job)
#     # schedule.every().wednesday.at("17:25").do(job)
#     while True:
#         schedule.run_pending()
#         time.sleep(wait_time)







