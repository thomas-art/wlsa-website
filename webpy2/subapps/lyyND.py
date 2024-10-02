import shutil
import urllib
import web
from lib import *
import config

urls = (
    '/search/', 'Search',
    '/test', 'Test',
    '/dict', 'Dict',
    '/favicon.ico', 'Favicon',
    '/error/filealreadyexist', 'Filealreadyexist',
    '/error/emptyfile', 'Emptyfile',
    '/error/deleterror', 'Deleterror',
    '/getfile/(.*)', 'GetFile',
    '/detail/(.*)', 'Detail',
    '/del/(.*)', 'Del',
    '/(.*)/', 'Redirect',
    '/(.*)', 'Upload',
)

if not os.path.exists(config.UPLODADS):
    os.makedirs(config.UPLODADS)
if not os.path.exists(r"static/lyynd/dict/dict.html"):
    list_directory(config.UPLODADS, config.BASE_URL)
render = web.template.render('templates/lyynd/')

def get_ip(request):
    x_forwarded_for = request.ctx.env.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 多次反向代理后会有多个ip值，第一个ip才是真实ip
    else:
        ip = request.ctx.env.get('REMOTE_ADDR')  # 这里获得代理ip
    return ip


class Test:
    def GET(self):
        return render.test()


class Search:
    def GET(self):
        input_data = web.input(q='')
        return list_directory_keyword(config.UPLODADS, config.BASE_URL, input_data.q)


class Redirect:
    def GET(self, path):
        web.seeother('/' + path)


class Detail:
    def GET(self, file_path):
        # 定义一个生成器用于分块发送文件
        def file_chunk_generator(file_path, start, end, chunk_size=4194304):
            with open(file_path, 'rb') as f:
                f.seek(start)
                remaining = end - start + 1
                while remaining > 0:
                    chunk_size_to_read = min(chunk_size, remaining)
                    chunk = f.read(chunk_size_to_read)
                    if not chunk:
                        break
                    yield chunk
                    remaining -= len(chunk)

        if file_path is None:
            raise web.seeother(web.ctx.home + '/dict')
        file_path = file_path.replace("/", "\\")
        file_path = encoded_file_path_regardless_end(file_path)
        # 检查文件是否存在
        print(file_path)
        if not os.path.isfile(file_path):
            raise web.seeother(web.ctx.home + '/dict')
        fn = os.path.basename(file_path)
        fn = decode_filename(fn)
        safe_filename = urllib.parse.quote(fn)  # 对文件名进行 URL 编码
        web.header('Content-Type', get_content_type(fn))
        web.header('Connection', 'keep-alive')
        web.header('Content-Disposition', f'inline; filename*=UTF-8\'\'{safe_filename}')
        web.header('accept-ranges', 'bytes')

        last_modified_time = os.path.getmtime(file_path)
        last_modified_datetime = datetime.datetime.utcfromtimestamp(last_modified_time)
        last_modified_str = web.httpdate(last_modified_datetime)

        # 获取文件 ETag（基于文件大小和最后修改时间生成）
        file_size = os.path.getsize(file_path)
        etag = hashlib.md5(f"{file_size}{last_modified_time}".encode()).hexdigest()

        # 检查浏览器是否发来条件请求
        if web.ctx.env.get('HTTP_IF_MODIFIED_SINCE') == last_modified_str:
            return web.notmodified()  # 返回 304 Not Modified

        if web.ctx.env.get('HTTP_IF_NONE_MATCH') == etag:
            return web.notmodified()  # 返回 304 Not Modified
        # 设置 Last-Modified 和 ETag 头部
        web.header('Last-Modified', last_modified_str)
        web.header('ETag', etag)
        # 读取文件内容并返回

        # 获取 Range 请求头
        range_header = web.ctx.env.get('HTTP_RANGE')
        start = 0
        end = file_size - 1  # 默认发送整个文件

        if range_header:
            # 解析 Range 请求头
            range_value = range_header.strip().split('=')[1]
            start, end = range_value.split('-')
            start = int(start) if start else 0
            end = int(end) if end else file_size - 1

            # 返回部分内容的 Content-Range 响应头
            web.header('Content-Range', f'bytes {start}-{end}/{file_size}')
            web.ctx.status = '206 Partial Content'  # 标记为部分内容响应

        content_length = end - start + 1
        web.header('Content-Length', str(content_length))
        # 使用生成器流式传输文件内容
        return file_chunk_generator(file_path, start, end)


class Del:
    def GET(self, file_path_password):
        list = file_path_password.split(' ')
        if len(list) == 0:
            raise web.seeother(web.ctx.home + '/dict')
        elif len(list) == 1:
            return render.passwordinput()

        file_path = list[0]
        password = list[1]

        file_path = encoded_file_path_regardless_end(file_path)

        if not os.path.exists(file_path):
            raise web.seeother(web.ctx.home + '/dict')

        # 检查文件位置
        root_dir = config.UPLODADS
        # 获取文件的绝对路径和根目录的绝对路径
        abs_file_path = os.path.abspath(file_path)
        abs_root_dir = os.path.abspath(root_dir)
        # 判断文件是否在根目录下或其子目录中
        web.header('connection', 'keep-alive')
        if os.path.commonpath([abs_file_path, abs_root_dir]) == abs_root_dir:
            md5 = MD5_salt(get_file_time(abs_file_path))
            if password == md5:
                try:
                    os.remove(abs_file_path)
                    list_directory(config.UPLODADS, config.BASE_URL)
                    return render.successdelfile(decode_file_path(abs_file_path))
                except:
                    pass
        return web.seeother(web.ctx.home + '/error/deleterror')


class Favicon:
    def GET(self):
        # 获取 favicon 文件路径
        favicon_path = os.path.join(os.getcwd(), 'static/lyynd/images/favicon.ico')
        web.header('Content-Type', 'image/x-icon')  # 设置响应头为图标类型
        return open(favicon_path, 'rb').read()  # 以二进制模式读取文件并返回


class Dict:
    def GET(self):
        web.header('connection', 'keep-alive')
        with open(r"static/lyynd/dict/dict.html", 'rb') as f:
            return f.read()


class GetFile:
    def GET(self, file_path):
        if file_path is None:
            raise web.seeother(web.ctx.home + '/dict')
        file_path = file_path.replace("/", "\\")
        file_path = encoded_file_path_regardless_end(file_path)
        # 检查文件是否存在
        if not os.path.isfile(file_path):
            raise web.seeother(web.ctx.home + '/dict')
        fn = os.path.basename(file_path)
        fn = decode_filename(fn)
        safe_filename = urllib.parse.quote(fn)  # 对文件名进行 URL 编码
        file_size = os.path.getsize(file_path)
        web.header('connection', 'keep-alive')
        web.header('Content-Type', 'application/octet-stream')
        web.header('Content-Disposition', f'attachment; filename*=UTF-8\'\'{safe_filename}')
        web.header('Content-Length', str(file_size))
        # 读取文件内容并返回
        with open(file_path, "rb") as file:
            return file.read()


class Upload:
    def GET(self, n):
        return render.index()

    def POST(self, n):
        x = web.input(myfile={})
        size = web.ctx.env.get('HTTP_X_FILE_SIZE', None)
        if size is None:
            web.seeother(web.ctx.home + '/dict')
        if 'myfile' not in x or not hasattr(x['myfile'], 'filename') or not hasattr(x['myfile'], 'value'):
            return render.uploademptyfile()

        disk_usage = shutil.disk_usage(config.LYYND_FILE_PATH)
        file_size = len(x['myfile'].value)

        if file_size > disk_usage.free - 10 * 1024 * 1024 * 1024:
            return "服务器磁盘不足"  # 返回内存不足的消息

        ip = get_ip(web)
        print(ip)
        t1 = time.strftime('%Y%m%d', time.localtime())

        filename = x['myfile'].filename
        filename1 = replace_list(filename,
                                 [' ', '\x00', '%', '\\', '/', '*', ':', '"', "'", '?', '>', '<', '[', ']', '|'])
        web.header('connection', 'keep-alive')
        if x['myfile'].value != b'':
            if not os.path.isdir(f'{config.UPLODADS}\\{t1}'):
                os.makedirs(f'{config.UPLODADS}\\{t1}')

            filename = encode_filename_regardless_end(filename1)
            if len(filename) > 250:
                return "文件名太长了"
            file_path = f"{config.UPLODADS}\\{t1}\\{filename}"
            if os.path.exists(file_path):  # 重复的文件？
                raise web.seeother(web.ctx.home + '/error/filealreadyexist')
            with open(file_path, 'wb') as f:
                f.write(x['myfile'].value)

            expected_file_size = int(size)
            if expected_file_size != os.path.getsize(file_path):
                os.remove(file_path)  # 删除不匹配的文件
                return render.md5error()
            md5 = MD5_salt(get_file_time(file_path))
            list_directory(f"{config.UPLODADS}", config.BASE_URL)
            return render.successuploadfile(config.BASE_URL, t1, filename1, md5)
        else:
            raise web.seeother(web.ctx.home + '/error/emptyfile')


class Filealreadyexist:
    def GET(self):
        return render.filealreadyexist()


class Emptyfile:
    def GET(self):
        return render.uploademptyfile()


class Deleterror:
    def GET(self):
        return render.delerror()
    

lyyND = web.application(urls, locals())

