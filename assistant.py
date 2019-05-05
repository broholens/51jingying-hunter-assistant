import os
import time
import random
from config import hunters, post_data
from utils import html2tree, request, load_cookies, generate_filename_by_username, get_cookies

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
        self.case_id = hunter['case_id']
        self.username = hunter['username']
        filename = generate_filename_by_username(self.username)
        if not os.path.exists(filename):
            get_cookies()
        self.cookie = load_cookies(filename)

    def get_basic_info(self):
        # 获取专业值和已递出名片的数量
        resp = request(self.home_url, cookies=self.cookie)
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
        resp = request(self.resume_url, method='post', json=self.post_data, cookies=self.cookie)
        if not resp:
            return []
        return resp.json()['mgrid']
    
    def recommend(self, manager_id, case_id):
        # 递名片
        data = {'userid': manager_id+'_1', 'caseid': case_id}
        resp = request(self.post_url, method='post', data=data, cookies=self.cookie)
        if not resp:
            return False
        return True if resp.json().get('msg') == '递送成功' else False

    def deliver_card(self):
        print('*'*40)
        print('当前猎头为', self.username)
        print('*'*40)
        # 获取经理人id
        managers = self.get_managers_ids()
        if managers == []:
            print('未获取到经理人ID！ 请尝试更新cookie！ ')
            return 
        print('获取经理人信息成功！')
        # 打乱序列，解决下面pop的问题
        random.shuffle(managers)
        # while循环解决投递失败导致投递数达不到20的问题
        while 1:
            professional_score, delivered_count = self.get_basic_info()
            if professional_score == -1:
                print('未获取到专业值！ 请尝试更新cookie！')
                return 
            if professional_score < 200:
                # BUG: 重新启动程序，专业值小于200且已经投递过简历
                delivered_count = 0
            print('目前专业值为{}, 今日已递出{}个名片'.format(professional_score, delivered_count))
            if delivered_count >= 20:
                break
            self._deliever_card(managers, delivered_count)
            # 专业值小于200 跳出循环
            if professional_score < 200:
                break
        # 打印投递完成信息
        print(self.username, '今日投递任务完成！')

    def _deliever_card(self, managers, delivered_count):
        # 每天投递20个
        remaining = 20 - delivered_count
        # 投递
        while remaining > 0 and len(managers) > 0:
            manager = managers.pop()
            if self.recommend(manager, self.case_id) is True:
                print('递送成功！经理人id:', manager)
                remaining -= 1
            else:
                print('递送失败！经理人id:', manager)
            time.sleep(random.random()*30)

if __name__ == '__main__':
    for hunter in hunters:
        assistant = HunterAssistant(hunter)
        assistant.deliver_card()
        time.sleep(random.random()*60)
