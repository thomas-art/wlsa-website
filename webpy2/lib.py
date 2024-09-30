import base64
import datetime
import hashlib
import mimetypes
import os
import time
import requests
import config


def decode_file_path(encoded_file_path):
    """
    获取编码文件路径的解码版本。
    """
    # 检查 '.lyy' 扩展名
    if encoded_file_path.endswith('.lyy'):
        encoded_filename = os.path.basename(encoded_file_path)
    else:
        return encoded_file_path

    # 获取根目录
    root_dir = os.path.dirname(encoded_file_path)

    # 解码文件名
    filename = decode_filename(encoded_filename)

    # 拼接新的文件路径
    decoded_file_path = os.path.join(root_dir, filename)

    return decoded_file_path


def list_directory(root_dir, baseurl):
    # 如果目录不存在，则创建它
    if not os.path.exists(root_dir):
        os.mkdir(root_dir)

    # 遍历目录的函数
    def traverse_dir(dir_path, level=0):
        html_output = ""

        entries = [(entry, os.path.getmtime(os.path.join(dir_path, entry))) for entry in os.listdir(dir_path)]

        for entry, _ in sorted(entries, key=lambda x: x[1], reverse=True):
            full_path = os.path.join(dir_path, entry)
            # 添加缩进
            indent = "&nbsp;" * 8 * level  # 缩进
            if os.path.isdir(full_path):
                # 如果是目录，使用 <details> 和 <summary> 实现可展开/关闭，目录之外
                html_output += f"""
                <tr>
                    <td colspan="6">{indent}<details>
                        <summary><b class="directory-name">{entry}/</b></summary>
                        <div style="margin-left: 20px;">
                            <table>
                                <thead>
                                    <tr>
                                        <th class="filename">文件名</th>
                                        <th class="size">大小</th>
                                        <th class="time">修改时间</th>
                                        <th class="time">文件详情</th>
                                        <th class="download">下载</th>
                                        <th class="del">删除</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {traverse_dir(full_path, level + 1)}
                                </tbody>
                            </table>
                        </div>
                    </details></td>
                </tr>
                """

            else:
                de_filepath = decode_file_path(full_path)
                file_name = os.path.basename(de_filepath)
                html_output += f"""
                <tr>
                    <td class='fl'>{file_name}</td>
                    <td class='fl'>{get_file_size(full_path)}</td>
                    <td class='fl'>{get_modified_time(full_path)}</td>
                    <td><a href="http://{baseurl}/detail/{de_filepath}" target="_blank">查看详情</a></td>
                    <td><a href="http://{baseurl}/getfile/{de_filepath}">点击下载</a></td>
                    <td><a href="http://{baseurl}/del/{de_filepath}">点击删除</a></td>
                </tr>
                """

        return html_output

    # 生成HTML页面，显示目录结构
    html_page = f"""
    <html>
    <head>
        <meta charset='UTF-8'>
        <title>查看文件</title>
        <script src="/static/dict/loadfont.js" type="text/javascript"></script>
        <link rel="stylesheet" href="/static/mouse/mouse.css">
        <link rel="stylesheet" href="/static/dict/dict.css">
    <div id="loadingAnimation">
        <div id="loadingImage" style="position: absolute; top: 20%; left: 41%;">
            <img id="loadingImage1" class="loading-frame" src="https://webcnstatic.yostar.net/ba_cn_web/prod/web/assets/avatar1.c18ce793.png" alt="connecting..." style="position: absolute; top: 0; left: 0; display: block;">
            <img id="loadingImage2" class="loading-frame" src="https://webcnstatic.yostar.net/ba_cn_web/prod/web/assets/avatar2.916294c1.png" alt="connecting..." style="position: absolute; top: 0; left: 0; display: none;">
            <img id="loadingImage3" class="loading-frame" src="https://webcnstatic.yostar.net/ba_cn_web/prod/web/assets/avatar3.5e643647.png" alt="connecting..." style="position: absolute; top: 0; left: 0; display: none;">
            <img id="loadingImage4" class="loading-frame" src="https://webcnstatic.yostar.net/ba_cn_web/prod/web/assets/avatar4.be61bf91.png" alt="connecting..." style="position: absolute; top: 0; left: 0; display: none;">
        </div>
        <div id="progressText" style="position: absolute; top: 85%; left: 41%;">connecting... 0%</div>
    </div>
    </head>
    <body>
        <div id="content" style="display: none;">
        <p><a href="/upload">点击返回</a></p>
        <div class="search-container">
        <form action="/search/" method="GET">
            <input type="text" name="q" placeholder="输入搜索关键词" required>
            <input type="submit" value="搜索">
        </form>
        </div>
        <h1>点击目录可以展开:</h1>
        <table>
            <thead>
                <tr>
                    <th class="filename">文件名</th>
                    <th class="size">大小</th>
                    <th class="time">修改时间</th>
                    <th class="time">文件详情</th>
                    <th class="download">下载</th>
                    <th class="del">删除</th>
                </tr>
            </thead>
            <tbody>
    """

    # 将递归生成的目录结构添加到页面中
    html_page += traverse_dir(root_dir)

    # 关闭HTML标签
    html_page += f"""
            </tbody>
        </table>
        <div id="customCursor">
        <img id="mouseIcon" src="data:image/png;base64,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" alt="Mouse Icon">
        </div>
        <div id="catchIcon">
        <img id="catchIco" src="data:image/png;base64,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" alt="Catch Icon" style="display:none;"> <!-- 默认隐藏 -->
    </div>
    <script src="/static/mouse/mouse.js" type="text/javascript"></script>
    </div>
    </body>
    </html>
    """

    # 将生成的 HTML 写入文件
    with open(f"static\dict\dict.html", 'w', encoding='utf-8') as f:
        f.write(html_page)

    return html_page


def list_directory_keyword(root_dir, baseurl, keyword):
    start_time = time.time()

    def traverse_dir(dir_path, level=0):
        html_output = ""
        i = 0

        entries = [(entry, os.path.getmtime(os.path.join(dir_path, entry))) for entry in os.listdir(dir_path)]

        for entry, _ in sorted(entries, key=lambda x: x[1], reverse=True):
            full_path = os.path.join(dir_path, entry)
            if os.path.isdir(full_path):
                htm, c = traverse_dir(full_path, level + 1)
                html_output += htm
                i += c
            else:
                de_filepath = decode_file_path(full_path)
                if keyword in os.path.basename(de_filepath):
                    i += 1
                    file_name = os.path.basename(de_filepath)
                    html_output += f"""
                    <tr>
                        <td class='fl'>{file_name}</td>
                        <td class='fl'>{get_file_size(full_path)}</td>
                        <td class='fl'>{get_modified_time(full_path)}</td>
                        <td><a href="http://{baseurl}/detail/{de_filepath}" target="_blank">查看详情</a></td>
                        <td><a href="http://{baseurl}/getfile/{de_filepath}">点击下载</a></td>
                        <td><a href="http://{baseurl}/del/{de_filepath}">点击删除</a></td>
                    </tr>
                    """
        return html_output, i

    # 生成HTML页面，显示目录结构

    # 将递归生成的目录结构添加到页面中
    html_page, i = traverse_dir(root_dir)
    end_time = time.time()
    elapsed_time = end_time - start_time
    html_page = f"""
    <html>
    <head>
    </div>
        <meta charset='UTF-8'>
        <title>查看文件</title>
        <script src="/static/dict/loadfont.js" type="text/javascript"></script>
        <link rel="stylesheet" href="/static/mouse/mouse.css">
        <link rel="stylesheet" href="/static/dict/dict.css">
    <div id="loadingAnimation">
        <div id="loadingImage" style="position: absolute; top: 20%; left: 41%;">
            <img id="loadingImage1" class="loading-frame" src="https://webcnstatic.yostar.net/ba_cn_web/prod/web/assets/avatar1.c18ce793.png" alt="connecting..." style="position: absolute; top: 0; left: 0; display: block;">
            <img id="loadingImage2" class="loading-frame" src="https://webcnstatic.yostar.net/ba_cn_web/prod/web/assets/avatar2.916294c1.png" alt="connecting..." style="position: absolute; top: 0; left: 0; display: none;">
            <img id="loadingImage3" class="loading-frame" src="https://webcnstatic.yostar.net/ba_cn_web/prod/web/assets/avatar3.5e643647.png" alt="connecting..." style="position: absolute; top: 0; left: 0; display: none;">
            <img id="loadingImage4" class="loading-frame" src="https://webcnstatic.yostar.net/ba_cn_web/prod/web/assets/avatar4.be61bf91.png" alt="connecting..." style="position: absolute; top: 0; left: 0; display: none;">
        </div>
        <div id="progressText" style="position: absolute; top: 85%; left: 41%;">connecting... 0%</div>
    </div>
    </head>
    <body>
    <div id="content" style="display: none;">
        <p><a href="/dict">点击返回</a></p>
        <div class="search-container">
        <form action="/search/" method="GET">
            <input type="text" name="q" placeholder="输入搜索关键词" required>
            <input type="submit" value="搜索">
        </form>
        </div>
        <h1>找到了{i}个结果, 耗时: {elapsed_time}s:</h1>
        <table>
            <thead>
                <tr>
                    <th class="filename">文件名</th>
                    <th class="size">大小</th>
                    <th class="time">修改时间</th>
                    <th class="time">文件详情</th>
                    <th class="download">下载</th>
                    <th class="del">删除</th>
                </tr>
            </thead>
            <tbody>
    """ + html_page

    # 关闭HTML标签
    html_page += f"""
            </tbody>
        </table>
        <div id="customCursor">
        <img id="mouseIcon" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACsAAAA0CAYAAAAT3cGOAAAACXBIWXMAAAsTAAALEwEAmpwYAAAFs0lEQVRogcWZ3WscVRiHn8lu+uGy2FDJnSCtFRSqBEEviqi0uehVyI164T+gV1IoQbShNqKCxtoLQVdKkMpaKbSlgqR9bULABKsxpFBIQcjHNoQ2Nmma3e1mZ3d2vJg5u2dmZ7Ob/Uh/cJjZ2TNnnvmd97znzIxx5MgRqklE3gCOAa8AYWAS+Kq7u/v3qic3UUY1WBH5GDgFGL6/bOAMcLy7uzvfGjyv2iocNwDj6tWrR4EBykFVnQ+AYRHZ2xo8r/ywhnusDae7j9fQxmFgUkReajJbmXRYwy0hoB3YaRjGqzW28wwwLiJvNxfPKwXrB90FPOHu16oI8LOIfCEioaZSutJhddDdQMSyrKUttmcAfcCvIrKnWZBKbXhd3UHJ1d2ZTGahznaPAn+LyAtNoXTVpm3DOLA73bIjmUzeaaDtZ4E/RaSnMcSSlLNtlMKgHQc8vLq62ggsQBS4JCKfiEhQ+tuS/GGgFyORSNQbBroMoB8HOtpIQ/oAU9uiAzdv3kw00rhPPcANEXmu3gYqzWAAjIyM3C8UCul6Gw/Q8zjAR+s5uQ1njleloO0DsLGx0Ux3AfbgpLYPtxrHylk/cFENpK/NFAI+A86LSKTWk3RnC3idtQHW19eb7ayut4AJEdlXS2W/s35glpeXWwkL8CLwl4gcrlZRh9VBi6EwOzvbijDway/OUvPYZpWCBpjH2dHR0TtoA66FCgODInJORHZVglUKjNu5ublMLpdbbjlqSe8Cf4jI0/4/KmUDBQy0JH1V08s4C/rX9INVnQVIp9PbEbd+dQLXReQddaAmZ9fW1rbbWaV24CcR6YIanV1aWnpcsOBMIB9BdWdtgFu3bj2OMND1JpQ7GxQG9rVr1+7atm1uL59HEShfdemTQhE4m80WTNNsdCHeiGagurPFQZZOpx9b3FqWdQ4wgmADgVOp1GOBtSzrxsWLF7+H8jComBFWVla2e5AVUqnUuVgs1huLxfKAEfZVqJhrE4lEoqura1so0+n01NjY2KenT5+eBDZwH7V0WAVW8BUbYGJiYqGnp2lP1YHK5XJ3p6env+3v7/8tn89n8D4TVnTW/4hjT01NrVuW9SAUCnU0G9K27WwikYifPHlyaHFxcYPgrGTXEgaeBU0kEmkq7Orq6ujQ0NA3w8PDd91rWUBeKxVhFbA/DGzASKfTiUgk0pRXm5lM5t+xsbGvBwcHp/CalAdygOluFTDVwsAzyB4+fJjo7OxsCNKyrLXbt2//cOLEiUvJZNLSrqUcNYEszsAy3eMFanDWk76Wl5fnDxw4UBekbdvWvXv3Lg0ODn43PT2d9F3HwnExp4FmKTlrwxadnZmZSRw6dGjLoKlU6p8LFy58GY/H53ztKzdVt2fdokKg6CoEv5Gp+NLj8uXLiXw+/6BWSNM0F8fHx/t6e3vfj8fjs5R39wbwCEi75RGl7s+7dYtmBYWBAi4LhWw2W1hYWDi/f//+9zaDLBQKmfn5+R8HBgbii4uLWV97yknV5SbewaS76XlQDfq01EbppXIUZ3m2C2fVbkSj0dDZs2c/7+joeD3oJldWViQWi50ZGRm5D2WjXDnqLzqkJ/R0hfbtC3wZEsJ9R+uCh92bMEzTtK9cuXL94MGD/0Wj0afC4fCTlmWtJ5PJyeHh4VN9fX2/zM3NpX2QKiY33JKhFJ8qNhVsRQU5a+B+rcFxNYrzjaHdvYnNpE/Z+uCp1uX6uRVVKWb1ScEzIquA6nFZS5eXxeVWYf1xprqoOJNtUl/PlyoVmdqxqnG5VVgFoC5uUvrOoL4/GAH1dDf9Xa7HZN2vojaDVS6ZlAaYrUHbvnqqbs2pqJmwurNq8rA0cPVbH+06pGfF1AhkNVgFnNf2Cy6I7rI/yeuQDXV5PbAKRu2buJ+d3DrKfb3UnIqaCasuqK/a9e9m+v9lK7RWqBqsAtIHU1Dq0rct0//nNloXLjtuNgAAAABJRU5ErkJggg==" alt="Mouse Icon">
        </div>
        <div id="catchIcon">
        <img id="catchIco" src="data:image/png;base64,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" alt="Catch Icon" style="display:none;"> <!-- 默认隐藏 -->
    </div>
    <script src="/static/mouse/mouse.js" type="text/javascript"></script>
    </div>
    </body>
    </html>
    """
    return html_page


def get_file_size(file_path):
    # 获取文件大小（字节）
    file_size = os.path.getsize(file_path)

    # 格式化为字符串
    if file_size < 1024:
        return f"{file_size} B"
    elif file_size < 1024 ** 2:
        return f"{file_size / 1024:.2f} KB"
    elif file_size < 1024 ** 3:
        return f"{file_size / 1024 ** 2:.2f} MB"
    else:
        return f"{file_size / 1024 ** 3:.2f} GB"


def get_modified_time(path):
    modification_time = os.path.getctime(path)

    # 将时间戳转换为 datetime 对象
    mod_time = datetime.datetime.fromtimestamp(modification_time)

    # 格式化为 %H:%M
    formatted_time = mod_time.strftime('%Y/%m/%d/%H:%M:%S')

    return formatted_time


def encode_filename(file_name):
    if not file_name.endswith('.lyy'):
        encoded_bytes = base64.urlsafe_b64encode(file_name.encode('utf-8'))
        encoded_str = encoded_bytes.decode('utf-8')
        return encoded_str + '.lyy'
    return file_name


def encode_filename_regardless_end(file_name):
    encoded_bytes = base64.urlsafe_b64encode(file_name.encode('utf-8'))
    encoded_str = encoded_bytes.decode('utf-8')
    return encoded_str + '.lyy'


def encoded_file_path_regardless_end(file_path):
    # 获取根目录
    root_dir = os.path.dirname(file_path)
    # 获取文件名
    filename = os.path.basename(file_path)
    # 编码文件名
    encoded_filename = encode_filename_regardless_end(filename)
    # 拼接新的文件路径
    encoded_file_path = os.path.join(root_dir, encoded_filename)
    return encoded_file_path


def decode_filename(encoded_filename):
    try:
        if encoded_filename.endswith('.lyy'):
            encode_filename = encoded_filename[:-4]
            encoded_bytes = encode_filename.encode('utf-8')
            decoded_bytes = base64.urlsafe_b64decode(encoded_bytes)
            original_filename = decoded_bytes.decode('utf-8')
            return original_filename
        else:
            return encoded_filename
    except:
        return encoded_filename

    # Base64 URL-safe 解码


def get_content_type(filename):
    # 通过文件扩展名获取对应的 MIME 类型
    content_type, encoding = mimetypes.guess_type(filename)

    # 如果无法识别类型，默认为二进制流
    if content_type is None:
        content_type = 'application/octet-stream'

    return content_type


def get_file_time(path):
    modification_time = os.path.getctime(path)

    # 将时间戳转换为 datetime 对象
    mod_time = datetime.datetime.fromtimestamp(modification_time)

    # 格式化为 %H:%M
    formatted_time = mod_time.strftime('%Y%m%d%H%M%S')

    return formatted_time


def MD5_salt(time='20240917140059'):
    hasher = hashlib.md5()
    hasher.update(config.salt1().encode('utf-8'))
    hasher.update(time.encode('utf-8'))
    hasher.update(config.salt2().encode('utf-8'))

    return hasher.hexdigest()


def md5_hash(value):
    return hashlib.md5(value.encode()).hexdigest()


def xiaobao_MD5_password(password, timestamp):
    # password = "Password123"
    # timestamp = 1727659448
    hashed_password = md5_hash(password).upper()
    hashed_twice_password = hashlib.md5((hashed_password + str(timestamp)).encode()).hexdigest().upper()
    return hashed_twice_password


def check_xiaobao_login(username, password):
    try:
        login_url = 'https://wlsastu.schoolis.cn/api/MemberShip/Login?captcha='

        timestamp = int(time.time()) #生成一个10位秒时间戳
        timestamp_str = str(timestamp)[:10]

        md5_pass=xiaobao_MD5_password(password, timestamp_str)
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
        }
        data = {
            "LanguageType": 1,
            "isWeekPassword": True,
            "name": username,
            "password": md5_pass,
            "timestamp": timestamp
        }
        r1 = requests.post(login_url, json=data, headers=headers)
        # 访问校宝api
        if r1.status_code == 200:
            rjson=r1.json()
            # 密码正确会返回:
            # {"data":true,"msgCN":null,"msgEN":null,"state":0,"msg":null}

            # 密码错误会返回:
            # {"data":null,"msgCN":null,"msgEN":null,"state":1010076,"msg":"引发类型为“Myth.ErrorException”的异常。"}
            if rjson.get('data') is True:
                return True
            return False
        else:
            return None
    except:
        return None


def replace_list(string, char_list):
    for char in char_list:
        string = string.replace(char, '')
    return string


if __name__ == "__main__":
    mode = input("调试模式 1.生成文件md5, 2.测试校宝密码是否可以登录\n\n请输入调试模式:")
    if mode=='1':
        while True:
            path = input("date: ")
            print(MD5_salt(path))
    if mode=='2':
        while True:
            name = input('username:')
            password = input('password:')
            content = check_xiaobao_login(name, password)
            print(content)
    
