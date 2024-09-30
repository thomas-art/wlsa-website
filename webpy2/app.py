import web
import urllib.parse
from lib import *
from subapps import lyyND
from subapps import wlsaSH

urls = (
    '/wlsash', wlsaSH,
    '/disk', lyyND,
    '/(.*)', "Redirect"
)

class Redirect:
    def GET(self, path):
        encoded_path = urllib.parse.quote(path)  # 对路径进行 URL 编码
        web.seeother('/disk/' + encoded_path)


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
