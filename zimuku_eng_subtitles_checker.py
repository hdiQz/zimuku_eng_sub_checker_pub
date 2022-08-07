from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd
import requests
import time
import os

os.chdir('~')

print('开始运行')
n = 0
keywords = '英'
tconst = pd.read_csv('~.csv', delimiter=',', encoding='utf-8').values #年份
for line in tconst:
    #print(line)
    tt = line[0]
    initial_url = 'https://zimuku.org'
    url_search = 'https://zimuku.org/search?q=' + str(tt)
    html_search = requests.get(url_search).text
    soup = BeautifulSoup(html_search, 'html.parser')
    subtitle_num = soup.find('div', {'class': 'pagination r clearfix'}).get_text().strip().replace('共 ', '').replace(' 条记录', '')
    subtitle_num = int(subtitle_num)
    if subtitle_num == 0:
        print(tt, "无字幕")
        with open ('~.txt', 'a') as nosubwriter: #年份
            nosubwriter.write(tt)
            nosubwriter.write('\n')
        n = n + 1
        continue
    if subtitle_num > 0:
        search_a = soup.find('a', {'target': '_blank'})
        subs_href = search_a['href']
        url_subs = initial_url + subs_href
        html_subs = requests.get(url_subs).text
        soup = BeautifulSoup(html_subs, 'html.parser')
        tr = soup.find_all('tr', {'class': ['odd', 'even']})
        for line in tr:
            a = line.find_all('a')
            for line in a:
                a_text = line.get_text().strip()
                if keywords in a_text:
                    detail_hrefs = a[0]['href']
                    #返回最后一个符合条件的链接
                    #if detail_hrefs == None:
                        #print(tt, "无英文字幕")
                        #n = n + 1
                        #continue
                        #有的有英文字幕但是标题里没写
        try:
            download_href = detail_hrefs.replace('detail', 'dld')
        except:
            print(tt, "不确定字幕")
            with open('~.txt', 'a') as noengwriter: #年份
                noengwriter.write(tt)
                noengwriter.write('\n')
            n = n + 1
            continue
        #url_download_page = initial_url + download_href
        #time.sleep(3)
        #html_download = requests.get(url_download_page, headers = headers).text
        #soup = BeautifulSoup(html_download, 'html.parser')
        #first_a = soup.find('a')
        #first_a_href = first_a['href']
        #url_download = initial_url + first_a_href
        #print(tt, '下载链接：', url_download)
        print(tt, "有英文字幕")
        with open('~.txt', 'a') as engttwriter: #年份
            engttwriter.write(tt)
            engttwriter.write('\n')
        n = n + 1
print('运行结束')
