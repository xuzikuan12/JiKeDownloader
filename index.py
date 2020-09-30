# coding=utf-8
import requests, json
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from ffmpy import FFmpeg
import sys
import os
import time
import re

work_path = r'D:\Codes\Python\JiKeDownloader'
storage_path = r"C:\Users\xuzik\OneDrive - mail.ustc.edu.cn\Backup\bilibili\jike\\"

class JiKeDownloader(object):
    def __init__(self):
        self.headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,\
            image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) \
                AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 \
                Safari/604.1'
        }

    def run(self):
        self.share_url = input('请输入分享链接（输入q推出）：')
        # self.share_url = 'https://m.okjike.com/originalPosts/5c4d6e0b4e12980010692d31?\
            # username=53095E59-8ADB-4EE7-BED1-37B6F2F458FF&\
            # share_distinct_id=168ae1ca463197-0b8d10da4c4d01-481f3700-1764000-168ae1ca464bc2&\
            # share_depth=1' 
       
        if self.share_url == 'q':
            return 'q'
       
        if len(self.share_url) < 59:
            print("请重新输入分享链接（输入q推出）") 
            return

        url_parse = urlparse(self.share_url)
        try:
            url_id = url_parse.path.split('/')[2];
        except IndexError as e:
            print("未识别url_id，请重新输入分享链接") 
            return
        else:
            print("url_id: %s" % url_id)
        if not re.match('[a-z0-9]{24}', url_id):
            print("re未通过，请重新输入分享链接") 
            return

        m3u8_url = "https://api.ruguoapp.com/1.0/mediaMeta/play?type=ORIGINAL_POST&id="\
            + url_id  #2020-09-08
        ret = requests.get(m3u8_url, headers=self.headers)
        bf = BeautifulSoup(ret.text, 'lxml')
        json_url = json.loads(bf.p.string)
        
        if not json_url['url']:
            print("解析视频链接错误，请重试")
            return

        localtime =  "%s-%s-%s " % time.localtime()[:3]
        
        ff = FFmpeg(
            inputs={json_url['url'] : None},
            outputs={localtime + url_id + '.mp4': None}
        ) 

        ff.run()
        
def flv_handle():
    os.chdir(work_path)
    for file in os.listdir():
        if file[-4:] == ".mp4":
            os.system('cp "%s" "%s" && del "%s"' % (file, storage_path, file))
   
if __name__ == '__main__':
    jk = JiKeDownloader()
    while True:
        res = jk.run()
        flv_handle()
        if res == 'q':
            break

