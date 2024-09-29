import os

import web

urls = (
    "", "Rewlsa",
    '/favicon.ico', 'Favicon',
    "/archives", "Archives",
    "/", "Index",
    "/(.*)", "PageNotFound"
)


class Favicon:
    def GET(self):
        favicon_path = os.path.join(os.getcwd(), 'wlsash/static/index/Favicon.ico')
        web.header('Content-Type', 'image/x-icon')
        return open(favicon_path, 'rb').read()


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
