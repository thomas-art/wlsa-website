import os
from lib import *
import web
import config
import json
from subapps.wlsaSHsubapps.community import forum
from subapps.wlsaSHsubapps.community import model # 论坛的数据库操作
from subapps.wlsaSHsubapps.xiaobao import *
test_lib()
urls = (
    '/favicon.ico', 'Favicon',
    '/community', forum.community,
    '/login', 'Login',
    '/logout', 'Logout',
    "/archives", "Archives",
    "/archives/preview", "FilePreview",
    "/dashboard", "Dashboard",
    "/pt-booking", "PT",
    "/ptold", "PTOld",
    "/api/files","FileAPI",
    "/api/xb", "XiaobaoAPI",
    "/api/pt/(.*)", "PTAPI",
    "/", "Index",
    "", "Rewlsa",
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
class Rewlsa:
    def GET(self): raise web.seeother('/')

class Login:
    def GET(self):
        auth = web.cookies().get("auth")
        key = web.cookies().get("key")
        cname = web.cookies().get("cname")
        ename = web.cookies().get("ename")

        if logged():
            md5auth = MD5_salt(auth)
            # passwd = xor_encrypt_decrypt(key, md5auth)
            # return f"logged, welcome: {web.cookies().get('user')};\ncurrent password: {passwd};\nchinese name: {cname};\nenglish name: {ename}"
            # return render.login(f"你好，{cname} {ename}")
            # return render.alreadylogged(ename)
            return web.seeother("/dashboard")
        else:
            captcha, log_sessionid = check_if_need_captcha()

            # 这里要加一下captcha==None的处理方法
            if captcha != 'noneed' and log_sessionid != 'noneed':
                # 此时的captcha和log_sessionid是有值的，需要返回给用户
                return render.login(captcha_display = 'block', captcha_src = captcha, captcha_required="required", sessionid=log_sessionid)
            
            return render.login(sessionid=log_sessionid)

    def POST(self):
        if logged():
            return """<script>window.history.go(-1);</script>"""
        try:
            data = web.input()

            #先检查表单的元素是否齐了
            required_fields = ['user', 'timestamp', 'auth', 'hash']
            for field in required_fields:
                if field not in data:
                    return {"message": f"Missing field: {field}", "successful": False}
                
            user = web.input().user
            timestamp = web.input().timestamp
            pwd = web.input().auth
            hash = web.input().hash


            pwd = base64.b64decode(pwd)
            pwd = pwd.decode('utf-8')
            passwd = xor_encrypt_decrypt(pwd, hash)

            sessionid = web.input().sessionid
            captcha_input = web.input().captcha
            if sessionid == 'noneed':
                sessionid=''
                captcha_input=''
                # 走到这里，就说明，校宝说不需要验证码，此时可以直接登录

            # 到这里，要么sessionid是"",要么就是上次传递的数值，不可能是None
            studentinfo, flag, xbid = check_xiaobao_login(user, passwd, captcha_input, sessionid)

            if flag is None:
                # 内部连接api失败
                return json.dumps({
                    "successful": False,
                    "message": "内部错误，请稍后再试"
                })

            if flag and ('data' in studentinfo and studentinfo['data']):
                c_name = studentinfo['data'].get('cName')  # 中文名
                e_name = studentinfo['data'].get('eName')  # 英文名
                user_id = studentinfo['data'].get('studentInfoId')

                if not (c_name and e_name and user_id):
                    # return 'login error'
                    return json.dumps({
                        "successful": False,
                        "message": "请求参数不全"
                    })
                
                t = current_timestamp()
                md5user = MD5_salt(user)
                auth = MD5_salt(md5user + t + c_name + e_name + str(user_id))
                md5auth = MD5_salt(auth)
                key = xor_encrypt_decrypt(passwd, md5auth)

                web.setcookie("auth", auth, 3600) # 86400s = 24h
                web.setcookie("key", key, 3600)
                web.setcookie("user", user, 3600)  # Store username in a cookie
                web.setcookie("timestamp", t, 3600)
                web.setcookie("cname", c_name, 3600)
                web.setcookie("ename", e_name, 3600)
                web.setcookie("user_id", user_id, 3600)
                web.setcookie("SessionId", xbid, 3600)

                # 能走到这里就说明账号和密码的验证已经通过了
                # 登陆成功后，试图将账号添加到数据库
                try:
                    model.User().new("samplemail@mail.com", user, e_name, passwd, user_id)
                    model.User().update(user_id, description=f"{c_name}, {e_name}")
                    return json.dumps({
                            "successful": True,
                            "message": "登录成功！"
                    })
                    # 如果数据库中新建用户成功，就说明是第一次登录
                except Exception as e:
                    # 新建用户失败，说明不是第一次登录，只需更新用户的密码即可
                    # 以后可能还会尝试更新用户的username，因为username是可以更改的
                    try:
                        model.User().update(user_id, password=passwd)
                        return json.dumps({
                            "successful": True,
                            "message": "登录成功！"
                        })
                    except:
                        # 数据库访问失败，就会跳转到这里
                        web.setcookie("auth", "", expires=-1)
                        web.setcookie("user", "", expires=-1)
                        web.setcookie("key", "", expires=-1)
                        web.setcookie("timestamp", "", expires=-1)
                        web.setcookie("cname", "", expires=-1)
                        web.setcookie("ename", "", expires=-1)
                        web.setcookie("user_id", "", expires=-1)
                        return json.dumps({
                            "successful": False,
                            "message": "服务器内部错误"
                        })
            else:
                return json.dumps({
                    "successful": False,
                    "message": "账号或密码错误"
                })
        except Exception as e:
            return json.dumps({
                "successful": False,
                "message": "登录失败，错误信息：" + e
            })
class Logout:
    def GET(self):
        web.setcookie("auth", "", expires=-1)
        web.setcookie("user", "", expires=-1)
        web.setcookie("key", "", expires=-1)
        web.setcookie("timestamp", "", expires=-1)
        web.setcookie("cname", "", expires=-1)
        web.setcookie("ename", "", expires=-1)
        web.setcookie("user_id", "", expires=-1)
        return render.logout()
class Index:
    def GET(self):
        if logged():
            return web.seeother("/dashboard")
        else:
            cname = web.cookies().get("cname")
            ename = web.cookies().get("ename")
            if cname and ename:
                return render.index(f"welcome: {cname}", "out")
            return render.index()
class PageNotFound:
    def GET(self, n):
        raise web.NotFound()
class Dashboard:
    def GET(self):
        auth = web.cookies().get("auth")
        key = web.cookies().get("key")
        cname = web.cookies().get("cname")
        ename = web.cookies().get("ename")

        if logged():
            md5auth = MD5_salt(auth)
            # passwd = xor_encrypt_decrypt(key, md5auth)
            # return f"logged, welcome: {web.cookies().get('user')};\ncurrent password: {passwd};\nchinese name: {cname};\nenglish name: {ename}"
            # return render.login(f"你好，{cname} {ename}")
            return render.dashboard((', ' + ename))
        else:
            return web.seeother("login?redir=/wlsash/dashboard")
class Archives:
    def GET(self):
        if logged():
            return render.archives('out')
        else: 
            return render.archives('in')
class PT:
    def GET(self):
        if logged():
            return render.pt()
        else:
            return web.seeother("login?redir=/wlsash/pt-booking")
class PTOld:
    def GET(self):
        return render.ptold()

# APIs
class FileAPI:
    def GET(self):
        params = web.input()
        path = os.path.join(wlsa_path, params.get("path"))
        # isfile = int(params.get("file"))
        isfile = not os.path.isdir(path)
        web.header("Is-File", isfile)
        if not isfile:
            try:
                return list_directory_json(os.path.join(wlsa_path, path))
            except:
                return "[]"
        else:
            f = open(os.path.join(wlsa_path, path), "rb")
            data = f.read()
            f.close()
            return data
class FilePreview:
    def GET(self):
        # I don't want to create a separate file for only a few lines of code
        return """
            <script>
            window.addEventListener("message", e => {
                alert(e.data);
                document.write = e.data;
            })
            </script>
        """
class XiaobaoAPI:
    def GET(self):
        link = web.input().get("link")
        try:
            return requestXiaobao(link, web.cookies().get("SessionId"))
        except Exception as e:
            print("Error in XiaobaoAPI:", e)
            return {}
class PTAPI:
    def GET(action):
        try:
            match action:
                case "get":
                    begin = int(web.input().get("begin"))
                    end = int(web.input().get("end"))
                    userId = requestXiaobao("https://wlsastu.schoolis.cn/api/MemberShip/GetCurrentStudentInfo", web.cookies().get("SessionId"))["studentInfoId"]
                    reqListSQL = model.PTRequest.fromUserId(userId)
                    reqList = []
                    for thing in reqListSQL:
                        jsonThing = {
                            "tutor_id": thing.tutor, 
                            "tutee_id": thing.tutee, 
                            "begin": thing.begin, 
                            "end": thing.end, 
                            "verify": thing.verify, 
                            "subj": thing.subj
                        }
                        reqList.append(jsonThing)
                    return json.dumps(reqList)
                case _:
                    return "No such action"
        except:
            return json.dumps([])
    def POST(action):
        return 0    # for security reasons
        try:
            match action:
                case "add":
                    begin = int(web.input().get("begin"))
                    end = int(web.input().get("end"))
                    tutorName = int(web.input().get("tname"))   # The user shouldn't know anyone else's ID
                    subj = int(web.input().get("id"))
                    userId = requestXiaobao("https://wlsastu.schoolis.cn/api/MemberShip/GetCurrentStudentInfo", web.cookies().get("SessionId"))["studentInfoId"]
                    
                    tutee = model.User.matched_id(ename = tutorName)
                    res = model.PTRequest(tutee.user_id, userId, subj, begin, end)
                    
                    return res.id
                case _:
                    return "No such action"
        except:
            return -1

wlsaSH = web.application(urls, locals())
