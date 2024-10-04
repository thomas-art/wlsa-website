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

def logged():
    cookie_value = web.cookies().get("auth")
    if cookie_value:
        return check_auth(cookie_value)
    return False

def check_auth(cookie_value):
    # This function should validate the cookie value against stored credentials
    # Here you would implement your logic to validate the user's login status
    # This is a placeholder implementation
    return True  # Replace with actual logic

class Login:
    def GET(self):
        if logged():
            return f"logged, welcome: {web.cookies().get('user')}"
        else:
            return render.login()

    def POST(self):
        user = web.input().user
        passwd = web.input().passwd

        if check_xiaobao_login(user, passwd):
            cookie_value = hashlib.sha256(f"{user}:{passwd}".encode()).hexdigest()
            web.setcookie("auth", cookie_value, 3600)
            web.setcookie("user", user, 3600)  # Store username in a cookie

            return f"login success, welcome: {user}"
        else:
            return 'login error'

class Reset:
    def GET(self):
        web.setcookie("auth", "", expires=-1)
        web.setcookie("user", "", expires=-1)
        return 'logged out'
test = web.application(urls, globals())

# 启动web服务
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
