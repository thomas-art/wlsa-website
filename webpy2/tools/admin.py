import requests
import os
import sys
from bs4 import BeautifulSoup
# 这样便能导入父目录的包
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from lib import *

# 发送 GET 请求获取 HTML 内容
url = "http://115.238.185.111:43279/dict"  # 替换为实际 URL
response = requests.get(url)

# 确保请求成功
if response.status_code == 200:
    # 解析 HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    htmln = response.text
    # 查找表格内容
    table = soup.find('table')

    # 获取所有文件信息
    for tr in table.find_all('tr')[1:]:  # 跳过表头
        td_elements = tr.find_all('td')
        if len(td_elements) == 6:  # 确保是文件行
            filename = td_elements[0].text.strip()
            size = td_elements[1].text.strip()
            modified_time = td_elements[2].text.strip()
            detail_link = td_elements[3].find('a')['href']
            download_link = td_elements[4].find('a')['href']
            delete_link = td_elements[5].find('a')['href']

            ftime = replace_list(modified_time, ['/', ':'])

            print(f"文件名: {filename}")
            print(f"大小: {size}")
            print(f"修改时间: {ftime}")
            print(f"查看详情: {detail_link}")
            print(f"下载链接: {download_link}")
            print(f"删除链接: {delete_link}")
            print("-" * 50)

            htmln = htmln.replace(delete_link, (delete_link + ' ' + MD5_salt(time=ftime)))

    with open('admin.html', 'w', encoding='utf-8') as f:
        htmln = htmln.replace('/static/', 'http://115.238.185.111:43279/static/')
        htmln = htmln.replace('id="loadingAnimation"', 'id="loadingAnimation" style="display: none;"')
        htmln = htmln.replace('id="loadingAnimation"', 'id="loadingAnimation" style="display: none;"')
        htmln = htmln.replace('id="content" style="display: none;"', 'id="content" style="display: block;"')
        f.write(htmln)

else:
    print(f"请求失败，状态码: {response.status_code}")
