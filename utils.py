import os
import re
import time
import json
import http
import glob
import datetime
import requests
from lxml.html import etree
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from config import hunters, get_headers, post_headers

# requests.exceptions.ConnectionError: ('Connection aborted.', HTTPException('got more than 100 headers'))
http.client._MAXHEADERS = 1000

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
    for old_cookies in old_cookies_dirs:
        os.removedirs(old_cookies)
        
    return today_cookies_dir

cookies_dir = generate_cookies_dir()

def generate_filename_by_username(username):
    # 生成文件路径
    return os.path.join(cookies_dir, username+'.txt')

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

def get_jobarea_dict():
    # 获取地区及对应编码
    area_code_ptn = re.compile('(r\d{6})\']=\'(.*?)\';')
    url = 'https://www.51jingying.com/js/dict/dd_jobarea.js?201904261337'
    resp = requests.get(url)
    for code, area in area_code_ptn.findall(resp.text):
        yield code, area

def load_cookies(filename):
    # 从文件中加载cookie
    cookies = {}
    with open(filename, 'r')as f:
        for item in json.loads(f.read()):
            cookies.update({item['name']: item['value']})
    return cookies

# 客户端检测js文件
# https://trace.51jingying.com/bigdata.js?201904291547
def make_driver():
    # 创建chrome并配置
    ops = webdriver.ChromeOptions()
    ops.add_argument('--headless')
    ops.add_argument('--no-sandbox')
    ops.add_argument('--disable-gpu')
    ops.add_argument('--start-maximized')
    ops.add_argument('--incognito')
    ops.add_argument('lang=zh_CN')
    # 解决window.navigator.webdriver=True的问题
    # https://wwwhttps://www.cnblogs.com/presleyren/p/10771000.html.cnblogs.com/presleyren/p/10771000.html
    ops.add_experimental_option('excludeSwitches', ['enable-automation'])
    ops.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"')
    d = webdriver.Chrome(options=ops)
    return d

def get_cookies():
    # selenium模拟登陆，获取并保存cookie
    login_url = 'https://www.51jingying.com/common/login.php?loginas=spy'
    home_url = 'https://www.51jingying.com/spy/index.php?act=generalSpyIndex'
    logout_url = 'https://www.51jingying.com/common/login.php?act=logout'
    offline_url = 'https://www.51jingying.com/spy/offline.php'
    d = make_driver()
    d.get('https://www.baidu.com/')
    for hunter in hunters:
        # 获取并保存cookie
        d.get(login_url)
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
        # 强制下线
        elif offline_url in d.current_url:
            d.find_element_by_link_text('强制下线').click()
            time.sleep(1)
            if d.current_url == home_url:
                print(hunter['username'], '登陆成功!')
        else:
            print(hunter['username'], '未知错误发生')
            continue
        d.refresh()
        cookies = d.get_cookies()
        # TODO: 保存在数据库中
        filename = generate_filename_by_username(hunter['username'])
        with open(filename, 'w')as f:
            f.write(json.dumps(cookies))
        print(hunter['username'], 'cookie 已保存！')
        # 重定向到登陆页面
        # d.get(logout_url)
        d.delete_all_cookies()
        time.sleep(3)
    d.quit()