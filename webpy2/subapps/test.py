import web
from web.contrib.template import render_mako
import pg

# 数据库连接
db = pg.DB(dbname='your_database_name', host='localhost', user='your_username', passwd='your_password')

# 检测并创建数据库表
def create_table():
    try:
        db.query("""
        CREATE TABLE example_users (
            id serial NOT NULL,
            user character varying(80) NOT NULL,
            pass character varying(80) NOT NULL,
            email character varying(100) NOT NULL,
            privilege integer NOT NULL DEFAULT 0,
            CONSTRAINT utilisateur_pkey PRIMARY KEY (id)
        )
        """)
        print("用户表已创建。")
    except pg.DatabaseError:
        print("用户表已存在。")

# 初始化模板渲染
render = render_mako(directories=['templates'], input_encoding='utf-8', output_encoding='utf-8')

# URL 路由
urls = (
    '/login', 'Login',
    '/reset', 'Reset',
)

# Session设置
session = web.session.Session(web.application(urls, globals()).cookie, web.session.DiskStore('sessions'), initializer={'login': 0, 'privilege': 0})

# 判断用户是否登录
def logged():
    return session.login == 1

# 权限管理
def create_render(privilege):
    if logged():
        if privilege == 0:
            return render('reader/login_double.html')
        elif privilege == 1:
            return render('user/login_double.html')
        elif privilege == 2:
            return render('admin/login_double.html')
    else:
        return render('communs/login.html')

# 登录类
class Login:
    def GET(self):
        if logged():
            return create_render(session.privilege)
        else:
            return render('communs/login.html')

    def POST(self):
        user, passwd = web.input().user, web.input().passwd
        ident = db.query("SELECT * FROM example_users WHERE user = '%s'" % user).getresult()
        try:
            if passwd == ident[0][2]:
                session.login = 1
                session.privilege = ident[0][4]
                return create_render(session.privilege)
            else:
                session.login = 0
                session.privilege = 0
                return render('communs/login_error.html')
        except IndexError:
            session.login = 0
            session.privilege = 0
            return render('communs/login_error.html')

# 注销类
class Reset:
    def GET(self):
        session.login = 0
        session.kill()
        return render('communs/logout.html')

# 创建数据库表
create_table()

# 启动web服务
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
