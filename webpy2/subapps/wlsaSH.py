import os
from lib import *
import web
import config

urls = (
    "", "Rewlsa",
    '/favicon.ico', 'Favicon',
    '/login', 'Login',
    "/archives", "Archives",
    "/api/files","FileAPI",
    "/", "Index",
    "/(.*)", "PageNotFound"
)

render = web.template.render('templates/wlsash/')
wlsa_path = config.WLSA_PATH

if not os.path.exists(wlsa_path):
    os.makedirs(wlsa_path)

class Favicon:
    def GET(self):
        favicon_path = os.path.join(os.getcwd(), 'static/wlsash/index/Favicon.ico')
        web.header('Content-Type', 'image/x-icon')
        return open(favicon_path, 'rb').read()


class Login:
    def GET(self):
        params = web.input()
        username = params.get('username')  # 从URL中获取用户名
        password = params.get('password')  # 从URL中获取密码

        if username and password:
            flag = check_xiaobao_login(username, password)
            if flag:
                return("xiaobao check success")
        else:
            return render.login()

        return("login failed")
    
    def POST(self):
        params = web.input()
        username = params.get('name')  # 从表单中获取用户名
        password = params.get('password')  # 从表单中获取密码

        if username and password:
            flag = check_xiaobao_login(username, password)
            if flag:
                return "xiaobao check success"
        return "login failed"


class Rewlsa:
    def GET(self): raise web.seeother('/')


class Index:
    def GET(self):
        return render.index()
        
class PageNotFound:
    def GET(self, n):
        raise web.NotFound()
    
class Archives:
    def GET(self):
        return render.archives()
    
class FileAPI:
    def GET(self):
        params = web.input()
        path = params.get("path")
        try:
            # print(os.path.join(wlsa_path, path))
            return list_directory_json(os.path.join(wlsa_path, path))
        except:
            return "[]"
        
# print(wlsa_path)

wlsaSH = web.application(urls, locals())
