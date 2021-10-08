# !/usr/bin/env python
# coding: utf-8

# 钉钉提醒周报功能封装
# 作者：江致远
# 作者邮箱：1914813051@qq.com
# 语雀链接：https://www.yuque.com/ol1q37/gi94xp/kcrzm7
# 修改日期：2021年2月24日


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
from login import * #添加login文件进去
from global_config import *
from selenium.webdriver.common.keys import Keys
from dingding_robbot import *
from datetime import timedelta
from get_chaojiying_tifen import *
# 首先，我们可以看到这块导入模块的作用，这块的作用的导入所需的模块





def get_write_list(driver,wait_time):
    """
    爬取周报页面所有的提交者的姓名和提交日期，并且存入列表write中
    """
    url = "https://www.moguding.net/practice-reportReviewweek"
    driver.get(url)
    write = []
    time.sleep(wait_time)
    html = driver.page_source
    reobj = re.compile(r'<tr class="el-table__row">[\d\D]*?<div class="cell"><span>([\d\D]*?)<[\d\D]*?class="el-table_1_column_9[\d\D]*?<span>([\d\D]*?)<')
    for match in reobj.finditer(html):
        write_man = match.group(1)
        write_data = match.group(2)
        writer_message = (write_man,write_data)
        write.append(writer_message)
    write = list(set(write))
    driver.close()
    return write
# 然后我们就看到了这个函数get_write_list，这个函数的作用是在网页中利用正则表达式来爬出页面中提交周报人的姓名和提交日期，并且将其存入列表write中，最后，将输出这个列表write。



def get_now_week_start_end(now):
    """
    获取本周的开始日和结束日的日期
    """
    this_week_start = now - timedelta(days = now.weekday() + 1)
    this_week_end = now + timedelta(days = 7 - now.weekday())
    this_week_start_fin = str(this_week_start.year) + "-" + str(this_week_start.month) + "-" + str(this_week_start.day)
    this_week_end_fin = str(this_week_end.year) + "-" + str(this_week_end.month) + "-" + str(this_week_end.day)
    this_week_start_fin = datetime.datetime.strptime(this_week_start_fin, "%Y-%m-%d")
    this_week_end_fin = datetime.datetime.strptime(this_week_end_fin, "%Y-%m-%d")
    return this_week_start_fin,this_week_end_fin
# 这个函数的作用是计算出本周的开始日和结束日，最后再输出本周的开始日和结束日，至于这个开始日和结束日有什么作用呢，下面你就知道了。




def get_not_write_list(write,this_week_start_fin,this_week_end_fin,student_list,student_message_list):
    """
    获取未写周报学生的名单
    """
    datetime.datetime.now()
    write_student = []
    not_student_phone_number = []
    not_write_student_remind = []
    for writer_message in write:
        get_write_time = writer_message[1]
        get_write_time = datetime.datetime.strptime(get_write_time, "%Y-%m-%d")
        if get_write_time >= this_week_start_fin and get_write_time <= this_week_end_fin:
            write_student.append(writer_message[0])
    not_write_student_list = list(set(student_list) - set(write_student))

    for student_message in student_message_list:
        for not_write_student in not_write_student_list:
            if student_message[0] == not_write_student:
                not_student_phone_number.append(student_message[1])

    not_write_student_remind_dingding = "有" + str(len(not_write_student_list)) + "位同学未写周报，" + "请尽快写周报"
    return not_write_student_remind_dingding,not_student_phone_number
# 这个函数的作用很简单，就是讲之前获得的write列表进行遍历，再将其列表中的日期与本周开始日和结束日进行对比
# （没错，之前的本周开始日和结束日的作用就是判断编辑周报的学生是否补交，只有在日期内的学生交的周报才会被记入编写周报的学生的名单）
# 那么，在进行对比之后，我们就可以得到未写周报的学生的名单，再进行处理，输出处理后的名单以及一个名为not_write_student_remind_dingding的变量
# 那么not_write_student_remind_dingding这个变量的作用是什么呢，这次老师就不卖关子了，这个变量就是之后被钉钉机器人调用的变量。 




def every_week_remind(username,password,implicitly_time,wait_time,get_code_image,image_screenshot,save_screenshot,chaojiying_usename,chaojiying_password,chaojiying_userid,student_list,student_message_list):
    # 登录
    driver = f_all(username,password,implicitly_time,wait_time,get_code_image,image_screenshot,save_screenshot,chaojiying_usename,chaojiying_password,chaojiying_userid)  
    # 爬取周报页面所有的提交者的姓名和提交日期，并且存入列表write中
    write = get_write_list(driver,wait_time)
    # 获取本周的开始日和结束日的日期
    this_week_start_fin,this_week_end_fin = get_now_week_start_end(now)
    # 获取未写周报学生的名单
    not_write_student_remind_dingding,not_student_phone_number = get_not_write_list(write,this_week_start_fin,this_week_end_fin,student_list,student_message_list)
    # 用钉钉机器人提醒未写的人
    all_robbot(not_write_student_remind_dingding,at_mobiles = not_student_phone_number)
    # 调用api获取超级鹰账号剩余的题分
    tifen_message = "剩余题分:" + str(get_chaojiying_tifen(chaojiying_usename,chaojiying_password))
    # 在钉钉群里提醒剩余的题分
    all_robbot(tifen_message,at_mobiles = [])

# 这个函数很厉害，将刚刚所有的函数都联系在了一起，最后再调用钉钉机器人，在钉钉群里说出本周未写周报学生的人数以及@未编辑周报的学生
    



def job():
    try:
        every_week_remind(username,password,implicitly_time,wait_time,get_code_image,image_screenshot,save_screenshot,chaojiying_usename,chaojiying_password,chaojiying_userid,student_list,student_message_list)
    except:
        job()

# 而在这个地方，我们又将刚刚的函数调用了一次，这是为什么呢，我们请看下面的代码。





# if __name__ == "__main__":
#     schedule.every().friday.at("20:00").do(job)
#     schedule.every().saturday.at("16:00").do(job)
#     # schedule.every().wednesday.at("17:08").do(job)
#     while True:
#         schedule.run_pending()
#         time.sleep(wait_time)
# 在这个地方，你就可以看到我们调用了schedule这个库，而这个库的作用就是定时调用job函数，我们可以自定义job函数来达到让其定时运行代码的效果，而在这个地方，我们需要其运行的时间设置为
# 周五晚上20点和周六下午16点，每到了这个时间，这个代码就会运行一次，然后在钉钉群里发送本周编辑周报的情况。




if __name__ == "__main__":
    # 登录
    driver = f_all(username,password,implicitly_time,wait_time,get_code_image,image_screenshot,save_screenshot,chaojiying_usename,chaojiying_password,chaojiying_userid)  
    # 通过操控enter键来跳过弹窗
    time.sleep(wait_time)
    pyautogui.hotkey("enter")
    # 爬取周报页面所有的提交者的姓名和提交日期，并且存入列表write中
    write = get_write_list(driver,wait_time)
    # 获取本周的开始日和结束日的日期
    this_week_start_fin,this_week_end_fin = get_now_week_start_end(now)
    # 获取未写周报学生的名单
    not_write_student_remind_dingding,not_student_phone_number = get_not_write_list(write,this_week_start_fin,this_week_end_fin,student_list,student_message_list)
    # 用钉钉机器人提醒未写的人
    all_robbot(not_write_student_remind_dingding,at_mobiles = not_student_phone_number)
    # 调用api获取超级鹰账号剩余的题分
    tifen_message = "剩余题分:" + str(get_chaojiying_tifen(chaojiying_usename,chaojiying_password))
    test_two_message = "批改已完成"
    # 在钉钉群里提醒剩余的题分
    all_robbot(tifen_message,at_mobiles = [])
    # 在钉钉群里告诉大家批改完成
    all_robbot(test_two_message,at_mobiles = [])

