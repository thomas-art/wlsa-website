import base64
import datetime
import hashlib
import mimetypes
import os
import time
import requests
import config
import json


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


def list_directory_json(dir):
    '''
    Creates a JSON string of the files in a directory. 
    Interface:
    [
        {type: folder | file, name: string},
        ...
    ]
    '''

    if not os.path.exists(dir):
        raise Exception(dir + " don't exist")
    
    entries = []
    for entry in os.listdir(dir):
        if entry == "links.json":
            continue
        
        entryType = "file"
        if os.path.isdir(os.path.join(dir, entry)):
            entryType = "folder"
        entries.append({
            "type": entryType,
            "name": entry
        })

    try:
        flinks = open(os.path.join(dir, "links.json"), "r")
        links = json.loads(flinks.read())
        for link in links:
            link["type"] = "link"
            entries.append(link)
        flinks.close()
    except Exception as e:
        print(e)
        pass # links are optional

    return json.dumps(entries)


def load_directory_structure():
    with open(config.DICT_SAVE_JSON_PATH, 'r', encoding='utf-8') as f:
        dir_structure = json.load(f)
    return dir_structure


def list_directory_list(root_dir):
    # 遍历目录的函数
    def traverse_dir(dir_path):
        entries = []
        for entry in sorted(os.listdir(dir_path), key=lambda x: os.path.getmtime(os.path.join(dir_path, x)), reverse=True):
            full_path = os.path.join(dir_path, entry)
            if os.path.isdir(full_path):
                entries.append({
                    'name': entry,
                    'type': 'directory',
                    'children': traverse_dir(full_path)
                })
            else:
                de = decode_file_path(full_path)
                entries.append({
                    'name': os.path.basename(de),
                    'type': 'file',
                    'size': get_file_size(full_path),
                    'time': get_modified_time(full_path),
                    'path': de
                })
        return entries
    
    dir = traverse_dir(root_dir)
    with open(config.DICT_SAVE_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(dir, f, ensure_ascii=False, indent=4)
    return dir


def list_directory_list_keyword(root_dir, keyword):
    start_time = time.time()
    # 遍历目录的函数
    def traverse_dir(dir_path):
        i = 0
        entries = []
        for entry in sorted(os.listdir(dir_path), key=lambda x: os.path.getmtime(os.path.join(dir_path, x)), reverse=True):
            full_path = os.path.join(dir_path, entry)
            if os.path.isdir(full_path):
                sub_entries, subcount = traverse_dir(full_path)
                entries.extend(sub_entries)
                i += subcount
            else:
                de = decode_file_path(full_path)
                if keyword in os.path.basename(de):
                    i += 1
                    entries.append({
                        'name': os.path.basename(de),
                        'type': 'file',
                        'size': get_file_size(full_path),
                        'time': get_modified_time(full_path),
                        'path': de
                    })
        return entries, i
    
    dir, i = traverse_dir(root_dir)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return dir, i, elapsed_time


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


def MD5_salt(string='20240917140059'):
    hasher = hashlib.md5()
    hasher.update(config.SALT_1.encode('utf-8'))
    hasher.update(string.encode('utf-8'))
    hasher.update(config.SALT_2.encode('utf-8'))

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


def current_timestamp():
    timestamp = int(time.time()) #生成一个10位秒时间戳
    timestamp_str = str(timestamp)[:10]
    return timestamp_str


def xor_encrypt_decrypt(input_string, key):
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(input_string))


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
    
