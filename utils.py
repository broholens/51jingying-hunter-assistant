import requests
from lxml.html import etree

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