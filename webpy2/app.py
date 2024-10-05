import web
import urllib.parse
import config
from lib import *
from subapps import lyyND
from subapps import wlsaSH


if not os.path.exists(config.ROOT_STORAGE_DIR):
    os.makedirs(config.ROOT_STORAGE_DIR)


urls = (
    '/wlsash', wlsaSH,
    '/disk', lyyND,
    '/(.*)', "Redirect"
)

def notfound():
    raise web.seeother(web.ctx.home + '/')

class Redirect:
    def GET(self, path):
        encoded_path = urllib.parse.quote(path)  # 对路径进行 URL 编码
        raise web.seeother('/disk/' + encoded_path)


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.notfound = notfound
    app.run()
