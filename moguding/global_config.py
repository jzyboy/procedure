# !/usr/bin/env python
# coding: utf-8

# 蘑菇丁项目所用到的各种变量
# 作者：江致远
# 作者邮箱：1914813051@qq.com
# 语雀链接：https://www.yuque.com/ol1q37/gi94xp/kcrzm7
# 修改日期：2021年10月13日


import os.path
from selenium import webdriver
from datetime import timedelta
import datetime
now = datetime.datetime.now()
base_folder = r"f:\moguding"
test_four_folder = r"f:\test_four"
test_one_folder = r"C:\Users\19148\Desktop"
test_one_screenshot = os.path.join(test_one_folder,"顶岗实习商数181成绩.xlsx")
save_screenshot = os.path.join(base_folder,"pic.png")
image_screenshot = os.path.join(base_folder,"pic.png")
get_code_image = os.path.join(base_folder,"yanzhen.png")
chaojiying_usename = "1830822911"
chaojiying_password = "gk1830822911"
chaojiying_userid = "923304"
wait_time = 3
implicitly_time = 8
test_two_message = "批改完成"
username = "15268112200"
password = "zhoubt"
username_new = "33090219741119092X"
password_new = "760596"
student_list = ["陈贤导","杨雯晴","汪毅菲","陈于昕","杨沈佳","楼宇鑫","康晓妍","李清瑶","王慧星","邵静萍","贺巧童","毕浩天","滕星瑜","潘纪鸿","胡骞"]
student_message_list = [['陈贤导','19857153165'],['杨雯晴','17816730064'],['汪毅菲','15858967589'],['陈于昕','15158437826'],
                        ['杨沈佳','15557383526'],['楼宇鑫','15325792679'],['康晓妍','18958977065'],['李清瑶','18258007361'],
                        ['王慧星','15285349842'],['邵静萍','18757138155'],['贺巧童','13073852706'],['毕浩天','13087179888'],
                        ['滕星瑜','19817853744'],['潘纪鸿','13454136635'],['胡骞','18368160385']]
percents = {"优":0.93,"良":0.83,"中":0.73,"及格":0.63,"不及格":0.5} # _ 作为内部函数，不作为外部使用
# mingzidengji = {'金岩': '良', '肖婷元': '良', '周佳宇': '及格', '陈娇妮': '中', '徐鹏': '良', '严金蕊': '中', '任炳瑜': '中', '徐恩美': '中', '郑旭佳': '良', '应丽雯': '优', '何玉峰': '优', '张芦滔': '中'}
list_pingyu = ['你在实习期间，态度极其认真，工作用心细心踏实，能虚心理解指导。',
        '对本职工作兢兢业业，注重个人成长;工作成绩进步大，业绩发展迅速，老师为你感到骄傲。',
        '你在实习期间工作认真，勤奋好学，踏实肯干，在工作中遇到不懂的地方，能够虚心向富有教训的前辈请教，善于思考，能够举一反三。',
        '不要气馁，端正态度，加油！相信你可以的！',
        '实习中遇到的困难都将是你的成长，要勇于克服困难，才能更好的成长。']

