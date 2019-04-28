import time
import random
from utils import html2tree, request
from config1 import hunters, get_headers, post_headers, post_data


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

    def get_basic_info(self):
        # 获取专业值和已递出名片的数量
        resp = request(self.home_url, headers=self.get_headers)
        try:
            tree = html2tree(resp.text)
            delivered_count = tree.xpath('//div[contains(@class, "spyindex_resume")]/p/span/text()')
            professional_score = tree.xpath('//p[@class="ss_Message_name"]/span/a/text()')[-1]
        except:
            return -1, -1
        delivered_count = delivered_count[0] if delivered_count else -1
        return int(professional_score), int(delivered_count)

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
        professional_score, delivered_count = self.get_basic_info()
        if professional_score == -1:
            print('未获取到专业值！ 请尝试更新cookie！')
            return 
        if professional_score < 200:
            # BUG: 专业值小于200且已经投递过简历
            delivered_count = 0
        print('目前专业值为{}, 今日已递出{}个名片'.format(professional_score, delivered_count))
        # 每天投递20个
        remaining = 20 - delivered_count
        # 获取第一页经理人id
        managers = self.get_managers_ids()
        if managers == []:
            print('未获取到经理人ID！ 请尝试更新cookie！ ')
            return 
        print('获取经理人信息成功！')
        while remaining > 0 and len(managers) > 0:
            manager = managers.pop()
            if self.recommend(manager, self.case_id) is True:
                print('递送成功！经理人id:', manager)
                remaining -= 1
            else:
                print('递送失败！经理人id:', manager)
            time.sleep(random.random()*30)
        print('今日投递任务完成！')
        # professional_score, delivered_count = self.get_basic_info()
        # print('目前专业值为{}, 今日已递出{}个名片'.format(professional_score, delivered_count))


if __name__ == '__main__':
    for hunter in hunters:
        assistant = HunterAssistant(hunter)
        assistant.deliver_card()
        time.sleep(random.random()*60)
