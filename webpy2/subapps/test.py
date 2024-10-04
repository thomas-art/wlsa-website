import web
from web.contrib.template import render_mako
from lib import *
import hashlib
import os

render = web.template.render('templates/test/')
urls = (
    '/login', 'Login',
    '/reset', 'Reset',
)

def logged(auth, key, user, t):
    if auth and key and user and t:
        md5user = MD5_salt(user)
        auth1 = MD5_salt(md5user + t)
        return auth == auth1
    return False
    

class Login:
    def GET(self):
        auth = web.cookies().get("auth")
        key = web.cookies().get("key")
        user = web.cookies().get("user")
        t = web.cookies().get("timestamp")

        if logged(auth, key, user, t):
            md5auth = MD5_salt(auth)
            passwd = xor_encrypt_decrypt(key, md5auth)
            return f"logged, welcome: {web.cookies().get('user')};\ncurrent password: {passwd}"
        else:
            return render.login()

    def POST(self):
        user = web.input().user
        passwd = web.input().passwd

        if check_xiaobao_login(user, passwd):
            t = current_timestamp()
            md5user = MD5_salt(user)
            auth = MD5_salt(md5user + t)
            md5auth = MD5_salt(auth)
            key = xor_encrypt_decrypt(passwd, md5auth)

            web.setcookie("auth", auth, 3600) # 86400s = 24h
            web.setcookie("key", key, 3600)
            web.setcookie("user", user, 3600)  # Store username in a cookie
            web.setcookie("timestamp", t, 3600)

            return f"login success, welcome: {user}"
        else:
            return 'login error'

class Reset:
    def GET(self):
        web.setcookie("auth", "", expires=-1)
        web.setcookie("user", "", expires=-1)
        web.setcookie("key", "", expires=-1)
        web.setcookie("timestamp", "", expires=-1)
        return 'logged out'
test = web.application(urls, globals())

# 启动web服务
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
