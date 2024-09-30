import os
from lib import *
import web

urls = (
    "", "Rewlsa",
    '/favicon.ico', 'Favicon',
    '/login', 'Login',
    "/archives", "Archives",
    "/", "Index",
    "/(.*)", "PageNotFound"
)


class Favicon:
    def GET(self):
        favicon_path = os.path.join(os.getcwd(), 'wlsash/static/index/Favicon.ico')
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
            return """<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>登录页面</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .login-container {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        input[type="submit"] {
            background-color: #5cb85c;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            width: 100%;
        }
        input[type="submit"]:hover {
            background-color: #4cae4c;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h2>请输入校宝账号以登录</h2>
        <form action="/wlsash/login" method="post">
            <input type="text" name="name" placeholder="用户名" required>
            <input type="password" name="password" placeholder="密码" required>
            <input type="hidden" name="timestamp" value="1700000000">
            <input type="submit" value="登录">
        </form>
    </div>
</body>
</html>"""

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
        with open('static/wlsash/index/index.html', 'r', encoding='utf-8') as f:
            return f.read()
        
class PageNotFound:
    def GET(self, n):
        raise web.NotFound()
    
class Archives:
    def GET(self):
        with open('static/wlsash/archives/index.html', 'r', encoding='utf-8') as f:
            return f.read()


wlsaSH = web.application(urls, locals())
