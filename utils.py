import re
import time
import json
import requests
from lxml.html import etree
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from config import hunters

# requests.exceptions.ConnectionError: ('Connection aborted.', HTTPException('got more than 100 headers'))
import http
http.client._MAXHEADERS = 1000

area_code_ptn = re.compile('(r\d{6})\']=\'(.*?)\';')

def request(url, is_get=True, headers=None, data=None):
    # 对requests的简单封装
    try:
        if is_get is True:
            resp = requests.get(url, headers=headers)
        else:
            resp = requests.post(url, headers=headers, data=data)
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
    url = 'https://www.51jingying.com/js/dict/dd_jobarea.js?201904261337'
    resp = requests.get(url)
    for code, area in area_code_ptn.findall(resp.text):
        yield code, area


def get_captcha(cookie):
    resp = requests.get('https://www.51jingying.com/common/verifycode.php?type=2&verifytype=1', cookies=cookie)
    with open('code.png', 'wb')as f:
        f.write(resp.content)

def fuck_login():
    ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    resp = requests.get('https://www.51jingying.com/common/login.php?loginas=spy', headers={'User-Agent': ua})
    # # print(resp.content.decode('gb2312'))
    # # 手动输入验证码测试
    # while 1:
    #     get_captcha(resp.cookies)
    #     code = input('code:')
    #     is_sure = input('Are u sure?(Y/N)')
    #     if is_sure == 'Y':
    #         break
    data = {
        # 'vcode': code,
        # 'returnUrl': '',
        'role': 'xpaZpaGgxg==',
        'randomcode': '543257',
        'username': '17719674030',
        'userpwd': '****',
        'checked': '1'
    }

    # data = (('role', 'xpaZpaGgxg=='), ('randomcode', 543257), ('username', 17719674030), ('userpwd', 'muge2018'), ('checked', 1), ('randomcode', {'tody': '2019-04-28'}))
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded', 
        'User-Agent': ua,
        'Host': 'passport.51jingying.com',
        'Origin': 'https://www.51jingying.com',
        # 'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://www.51jingying.com/common/login.php?loginas=spy',
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        # 'Connection': 'keep-alive'
    }
    resp = requests.post('https://passport.51jingying.com/login.php?act=formLogin', json=data, headers=headers)
    # newcommonlogin.js
    # 204 账户被锁定
    # 203 用户名密码错误
    # 202 用户信息泄露
    # 201 验证码错误
    # 200 登录异常
    # 101 该账号已在其他地方或浏览器登录
    # 100 success
    print(re.findall('status\":\"(\d+)\"', resp.text)[0])
    print('17719674030' in resp.headers['set-cookie'])


def load_cookies(filename):
    # 从文件中加载cookie
    cookies = {}
    with open(filename, 'r')as f:
        for item in json.loads(f.read()):
            cookies.update({item['name']: item['value']})
    return cookies

# def test_login():
#     ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
#     url = 'https://www.51jingying.com/spy/searchmanager.php'
#     cookies = load_cookies()
#     # 当url = https://www.51jingying.com/spy/index.php?act=generalSpyIndex时，会报如下错误
#     # requests.exceptions.TooManyRedirects: Exceeded 30 redirects
#     resp = requests.get(url, cookies=cookies, headers={'User-Agent': ua})
#     print(resp.content.decode('gb2312'))

def get_cookies():
    # selenium模拟登陆，获取并保存cookie
    login_url = 'https://www.51jingying.com/common/login.php?loginas=spy'
    home_url = 'https://www.51jingying.com/spy/index.php?act=generalSpyIndex'
    # chrome配置
    ops = webdriver.ChromeOptions()
    ops.add_argument('--headless')
    ops.add_argument('--no-sandbox')
    ops.add_argument('--disable-gpu')
    ops.add_argument('--start-maximized')
    ops.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"')
    d = webdriver.Chrome(options=ops)

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

        time.sleep(2)
        if d.current_url == home_url:
            print(hunter['username'], '登陆成功!')
        cookies = d.get_cookies()
        # TODO: 保存在数据库中
        with open('cookies/'+str(hunter['username'])+'.txt', 'w')as f:
            f.write(json.dumps(cookies))
        print(hunter['username'], 'cookie 已保存！')
        d.close()
        time.sleep(10)
    d.quit()

fuck_login()