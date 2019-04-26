import time
import random
from utils import html2tree, request
from config import hunters, get_headers, post_headers, post_data


class HunterAssistant:
    """帮助猎头递出名片
    """

    # 首页
    home_url = 'https://www.51jingying.com/spy/index.php?act=generalSpyIndex'
    # 找精英
    resume_url = 'https://www.51jingying.com/spy/searchmanager.php?act=getResumeSrch'
    # 递出名片
    post_url = 'https://www.51jingying.com/spy/webchat.php?act=postCard'

    def __init__(self, hunter):
        post_data.update({'fulltext': hunter['keyword'], 'exparea': hunter['area']})
        self.post_data = post_data
        get_headers.update({'Cookie': hunter['cookie']})
        self.get_headers = get_headers
        post_headers.update({'Cookie': hunter['cookie']})
        self.post_headers = post_headers
        self.case_id = hunter['case_id']

    def get_delivered_count(self):
        # 获取已递出名片的数量
        resp = request(self.home_url, headers=self.get_headers)
        try:
            tree = html2tree(resp.text)
            delivered_count = tree.xpath('//div[contains(@class, "spyindex_resume")]/p/span/text()')
        except:
            return -1
        return int(delivered_count[0])

    def get_managers_ids(self):
        # 获取经理人id
        resp = request(self.resume_url, False, self.post_headers, self.post_data)
        if not resp:
            return []
        return resp.json()['mgrid']
    
    def recommend(self, manager_id, case_id):
        # 递名片
        resp = request(self.post_url, False, self.post_headers, {'userid': manager_id+'_1', 'caseid': case_id})
        if not resp:
            return False
        return True if resp.json().get('msg') == '递送成功' else False

    def deliver_card(self):
        # 获取已经投递的数量
        delivered_count = self.get_delivered_count()
        if delivered_count == -1:
            print('未获取到今日递出数量！ 请尝试更新cookie！')
            return
        print('今日已递出{}个名片'.format(delivered_count))
        # 每天投递20个
        remaining = 20 - delivered_count
        # 获取第一页经理人id
        managers = self.get_managers_ids()
        if managers == []:
            print('未获取到经理人ID！ 请尝试更新cookie！ ')
            return 
        print('获取经理人信息成功！')
        while remaining >= 0 and len(managers) > 0:
            manager = managers.pop()
            if self.recommend(manager, self.case_id) is True:
                print('递送成功！经理人id:', manager)
                remaining -= 1
            else:
                print('递送失败！经理人id：', manager)
            time.sleep(random.random()*10)
        print('今日投递简历数：', self.get_delivered_count())


if __name__ == '__main__':
    for hunter in hunters:
        assistant = HunterAssistant(hunter)
        assistant.deliver_card()