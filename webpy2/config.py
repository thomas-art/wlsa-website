
import os
CURRENT_DICTORY = os.path.dirname(os.path.abspath(__file__))

BASE_URL = r"127.0.0.1:8080"
# BASE_URL = r"115.238.185.111:43279"
# BASE_URL = r"192.168.0.102:8080"
ROOT_STORAGE_DIR = r"C:\netfiles"

# subappfiles
LYYND_FILE_PATH = ROOT_STORAGE_DIR + r"\lyynd"
WLSASH_FILE_PATH = ROOT_STORAGE_DIR + r"\wlsash"

# lib.py
SALT_1 = r"salt1"
SALT_2 = r"盐2"

# lyynd
UPLODADS = LYYND_FILE_PATH + r"\uploads"
DICT_SAVE_JSON_PATH = r"static\lyynd\dict\dict.json"

# wlsaSH
WLSA_PATH = WLSASH_FILE_PATH + r"\wlsafiles"
# wlsaCommunity
SITE_NAME = '论坛'
AUTHOR = 'RussellLuo'
GLOBAL_PARAMS = {'site_name': SITE_NAME, 'title': SITE_NAME, 'author': AUTHOR}
##### 公共配置 #####
COOKIE_EXPIRES = 3600 # 单位s
DB_LOC = CURRENT_DICTORY + r"\subapps\wlsaSHsubapps\community\forum.db"
IMG_DIR = '/static/wlsash/community/img'
POSTS_PER_PAGE = 10 # 每页显示10篇文章


##### email服务器配置 #####
import web
web.config.smtp_server = 'smtp.gmail.com'
web.config.smtp_port = 587
web.config.smtp_username = 'your_gmail_address'
web.config.smtp_password = 'your_gmail_password'
web.config.smtp_starttls = True

##### 调试模式 #####
web.config.debug = False
