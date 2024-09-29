def passwordinput():
    with open('static/pages/passwordinput.html', 'r', encoding='utf-8') as f:
        return f.read()


def successdelfile(file_path, base_url):
    with open('static/pages/successdelfile.html', 'r', encoding='utf-8') as f:
        return f.read() % (file_path, base_url)


def delerror(base_url):
    with open('static/pages/delerror.html', 'r', encoding='utf-8') as f:
        return f.read() % base_url


def index():
    with open('static/pages/index.html', 'r', encoding='utf-8') as f:
        return f.read()


def test():
    with open('static/pages/test.html', 'r', encoding='utf-8') as f:
        return f.read()


def uploademptyfile(base_url):
    with open('static/pages/uploademptyfile.html', 'r', encoding='utf-8') as f:
        return f.read() % base_url


def filealreadyexist(base_url):
    with open('static/pages/filealreadyexist.html', 'r', encoding='utf-8') as f:
        return f.read() % base_url


def md5error(base_url):
    with open('static/pages/md5error.html', 'r', encoding='utf-8') as f:
        return f.read() % base_url


def successuploadfile(base_url, t1, filename, md5):
    with open('static/pages/successuploadfile.html', 'r', encoding='utf-8') as f:
        return f.read() % (base_url, t1, filename, base_url, t1, filename, md5, base_url)
