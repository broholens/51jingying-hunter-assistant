import os
import re
import sys
import csv
import time
import json
import http
import glob
import shutil
import random
import datetime
from multiprocessing import Queue
import requests
from lxml.html import etree
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from config import get_headers, post_headers, area_code_filename, hunters_file

# requests.exceptions.ConnectionError: ('Connection aborted.', HTTPException('got more than 100 headers'))
http.client._MAXHEADERS = 1000

# 日志队列
log_q = Queue()


def generate_cookies_dir():
    # 生成cookies文件
    today = datetime.date.today()
    today_cookies_dir = 'cookies-' + str(today)
    # 匹配文件夹
    old_cookies_dirs = glob.glob('cookies-*')
    # 如果不存在今天的，就新建今天的文件夹
    if today_cookies_dir in old_cookies_dirs:
        old_cookies_dirs.remove(today_cookies_dir)
    else:
        os.mkdir(today_cookies_dir)
    # 删除过期cookies
    # 使用os.removedirs报错
    for old_cookies in old_cookies_dirs:
        shutil.rmtree(old_cookies)
        
    return today_cookies_dir

cookies_dir = generate_cookies_dir()

def generate_filename_by_username(username):
    # 生成文件路径
    return os.path.join(cookies_dir, username+'.txt')

def random_sleep(max_sleep_time):
    """随机sleep"""
    time.sleep(random.random()*max_sleep_time)

def request(url, method='GET', **kwargs):
    # 对requests的简单封装
    method = method.upper()  # get/post
    if method == 'GET':
        headers = get_headers
    else:
        method = 'POST'
        headers = post_headers
    try:
        resp = requests.request(method, url, headers=headers, **kwargs)
        return resp
    except:
        return
    
def html2tree(html):
    # 将html转为tree
    try:
        tree = etree.HTML(html)
        return tree
    except:
        return

def get_jobarea_code():
    # 获取地区及对应编码
    area_code_ptn = re.compile(r'(\d{6})\']=\'(.*?)\';')
    url = 'https://www.51jingying.com/js/dict/dd_jobarea.js?201904261337'
    resp = requests.get(url)
    area_code = {}
    for code, area in area_code_ptn.findall(resp.text):
        area_code.update({area: code})
    # 存入文件
    with open(area_code_filename, 'w')as f:
        f.write(json.dumps(area_code))
    return area_code

def load_jobarea_code():
    """加载地区与编码json文件"""
    if not os.path.exists(area_code_filename):
        area_code = get_jobarea_code()
        # 直接返回
        return area_code
    with open(area_code_filename, 'r')as f:
        # 读取后返回
        return json.loads(f.read())

def get_hunters():
    """从文件中加载hunters"""
    try:
        f = open(hunters_file, 'r', encoding='gbk')
    except:
        f = open(hunters_file, 'r', encoding='utf-8')
    hunters = list(csv.DictReader(f))
    f.close()
    hunters = replace_area_with_code(hunters)
    return hunters


def replace_area_with_code(hunters):
    """对每个猎头信息中的地址进行编码转换"""
    area_code = load_jobarea_code()
    for hunter in hunters:
        hunter['area'] = area_code.get(hunter['area'])
        if not hunter['area']:
            log_q.put('猎头信息错误,请检查配置文件！')
            return
    return hunters

hunters = get_hunters()
log_q.put('猎头信息加载完成！')

def load_cookies(filename):
    # 从文件中加载cookie
    cookies = {}
    with open(filename, 'r')as f:
        for item in json.loads(f.read()):
            cookies.update({item['name']: item['value']})
    return cookies

# 客户端检测js文件
# https://trace.51jingying.com/bigdata.js?201904291547
def make_driver(driver='chrome'):
    """只支持chrome和phantomjs"""
    if driver == 'phantomjs':
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        dcap["phantomjs.page.settings.loadImages"] = False
        # phantomjs.exe位于同级目录下
        d = webdriver.PhantomJS(desired_capabilities=dcap)
        return d
    # 创建chrome并配置
    ops = webdriver.ChromeOptions()
    ops.add_argument('--headless')
    # ops.add_argument('--no-sandbox')
    # ops.add_argument('--disable-gpu')
    ops.add_argument('--start-maximized')
    # ops.add_argument('--incognito')
    ops.add_argument('lang=zh_CN')
    # 解决window.navigator.webdriver=True的问题
    # https://wwwhttps://www.cnblogs.com/presleyren/p/10771000.html.cnblogs.com/presleyren/p/10771000.html
    ops.add_experimental_option('excludeSwitches', ['enable-automation'])
    ops.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"')
    try:
        d = webdriver.Chrome(options=ops)
    except:
        d = webdriver.Chrome(chrome_options=ops)
    # d.set_window_size(1024,768)
    return d

def get_cookies():
    # selenium模拟登陆，获取并保存cookie
    login_url = 'https://www.51jingying.com/common/login.php?loginas=spy'
    home_url = 'https://www.51jingying.com/spy/index.php?act=generalSpyIndex'
    logout_url = 'https://www.51jingying.com/common/login.php?act=logout'
    offline_url = 'https://www.51jingying.com/spy/offline.php'
    d = make_driver()
    d.get('https://www.baidu.com/')
    d.get(login_url)
    for hunter in hunters:
        # cookie file
        filename = generate_filename_by_username(hunter['username'])
        # 如果cookie存在则直接跳过
        if os.path.exists(filename):
            continue
        # 获取并保存cookie
        uname = d.find_element_by_name('_username')
        uname.clear()
        uname.send_keys(hunter['username'])
        passwd = d.find_element_by_name('_password')
        passwd.clear()
        passwd.send_keys(hunter['password'])
        passwd.send_keys(Keys.ENTER)

        time.sleep(3)
        if d.current_url == home_url:
            print(hunter['username'], '登陆成功!')
            log_q.put('{}登陆成功！'.format(hunter['username']))
        # 强制下线
        elif offline_url in d.current_url:
            d.find_element_by_link_text('强制下线').click()
            time.sleep(1)
            if d.current_url == home_url:
                print(hunter['username'], '登陆成功!')
                log_q.put('{}登陆成功！'.format(hunter['username']))
        else:
            print(hunter['username'], '未知错误发生')
            log_q.put('{}未知错误发生'.format(hunter['username']))
            continue
        # d.refresh()
        cookies = d.get_cookies()
        
        with open(filename, 'w')as f:
            f.write(json.dumps(cookies))
        print(hunter['username'], 'cookie 已保存！')
        log_q.put('{}cookie 已保存！'.format(hunter['username']))
        # 重定向到登陆页面
        d.get(logout_url)
        # d.delete_all_cookies()
        time.sleep(3)
    d.quit()