import requests
import hashlib
import time

userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"

# login functions


def check_if_need_captcha():
    try:
        captcha_url = "https://wlsastu.schoolis.cn/api/MemberShip/GetStudentCaptchaForLogin"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
        }
        r1 = requests.get(captcha_url, headers=headers)
        if r1.status_code == 200:
            # 解析 JSON 数据
            json_data = r1.json()
            captcha = json_data.get("data")
            # 检查 data 键
            if captcha == "":
                return 'noneed', 'noneed'
            else:
                # 此时说明需要验证码，返回验证码图片和sessionid
                # 提取 set-cookie 中的 sessionID
                session_id = r1.cookies.get("SessionId")  # 根据实际 Cookie 名称
                if session_id:
                    return captcha, session_id
                else:
                    return None, None
        else:
            return None, None
    except:
        return None, None


def xiaobao_MD5_password(password, timestamp):
    # password = "Password123"
    # timestamp = 1727659448
    hashed_password = hashlib.md5(password.encode()).hexdigest().upper()
    hashed_twice_password = hashlib.md5(
        (hashed_password + str(timestamp)).encode()).hexdigest().upper()
    return hashed_twice_password


def check_xiaobao_login(username, password, captcha='', sessionid=''):
    try:
        login_url = f'https://wlsastu.schoolis.cn/api/MemberShip/Login?captcha={captcha}'
        studentinfo_url = 'https://wlsastu.schoolis.cn/api/MemberShip/GetCurrentStudentInfo'

        timestamp = int(time.time())  # 生成一个10位秒时间戳
        timestamp_str = str(timestamp)[:10]

        md5_pass = xiaobao_MD5_password(password, timestamp_str)

        if sessionid != '':
            # 传入了sessionid
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
                "Cookie": f"SessionId={sessionid}"
            }
        else:
            # 没有传入sessionid，使用默认headers
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
            }

        data = {
            "LanguageType": 1,
            "isWeekPassword": 0,
            "name": username,
            "password": md5_pass,
            "timestamp": timestamp
        }

        r1 = requests.post(login_url, json=data, headers=headers)
        # 访问校宝api
        if r1.status_code == 200:
            rjson = r1.json()
            # 密码正确会返回:
            # {"data":true,"msgCN":null,"msgEN":null,"state":0,"msg":null}

            # 密码错误会返回:
            # {"data":null,"msgCN":null,"msgEN":null,"state":1010076,"msg":"引发类型为“Myth.ErrorException”的异常。"}
            if rjson.get('data') is True:
                sessionid1 = r1.cookies.get('SessionId')
                if sessionid1:
                    headers1 = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
                    }
                    student_info_cookies = {'SessionId': sessionid1}
                    r2 = requests.get(
                        studentinfo_url, headers=headers1, cookies=student_info_cookies)

                    if r2.status_code == 200:
                        return r2.json(), True

            return False, False
        else:
            return None, None
    except:
        return None, None



# Xiaobao API functions
def getStudentInfo(cookie):
    try:
        req = requests.get("https://wlsastu.schoolis.cn/api/MemberShip/GetCurrentStudentInfo", headers={
            "User-Agent": userAgent,
            "Cookies": "SessionId=" + cookie
        })
        data = req.json()
        if "data" not in data:
            raise Exception("unauthorized")
        return req.json()
    except Exception as e:
        print("getInfo error:", e)
        return
def getStudentInfo(cookie):
    try:
        req = requests.get("https://wlsastu.schoolis.cn/api/MemberShip/GetCurrentStudentInfo", headers={
            "User-Agent": userAgent,
            "Cookies": "SessionId=" + cookie
        })
        data = req.json()
        if "data" not in data:
            raise Exception("unauthorized")
        return req.json()
    except Exception as e:
        print("getInfo error:", e)
        return
def getStudentInfo(cookie):
    try:
        req = requests.get("https://wlsastu.schoolis.cn/api/MemberShip/GetCurrentStudentInfo", headers={
            "User-Agent": userAgent,
            "Cookies": "SessionId=" + cookie
        })
        data = req.json()
        if "data" not in data:
            raise Exception("unauthorized")
        return req.json()
    except Exception as e:
        print("getInfo error:", e)
        return
def getStudentInfo(cookie):
    try:
        req = requests.get("https://wlsastu.schoolis.cn/api/MemberShip/GetCurrentStudentInfo", headers={
            "User-Agent": userAgent,
            "Cookies": "SessionId=" + cookie
        })
        data = req.json()
        if "data" not in data:
            raise Exception("unauthorized")
        return req.json()
    except Exception as e:
        print("getInfo error:", e)
        return