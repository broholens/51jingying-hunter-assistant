# 猎头
hunters = [
    {
        'username': '',  # 用户名
        'password': '',  # 密码
        'case_id': '',   # 职位id
        'keyword': '',   # 搜索关键字
        'area': ''       # 期望工作地
    }
]

# get方法请求头
get_headers = {
    'Host': 'www.51jingying.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Cookie': ''
} 

# post方法请求头
post_headers = {
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'www.51jingying.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Cookie': ''
}

# 搜索简历要提交的表单
post_data = {
    'url': 'https://www.51jingying.com/spy/searchmanager.php?act=getResumeSrch',
    'fulltext': '',
    'exparea': '',
    'onlyfunc': 1,
    'srchpage': 1,  # 查找第一页
    'type': 'searchall',
    'downandup': 0,
    'mgrsort': 0,
    'resumetime': 6
}