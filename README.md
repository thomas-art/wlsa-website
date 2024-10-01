0.1 修复了文件加密功能，在上传可打开的.lyy文件，其原文件名包含空格导致无法下载。

0.1.1 修复了上传包含空格文件，生成的下载连接中包含空格的错误。

0.1.2 添加了图片视频等文件预览功能，以及缓存资源的逻辑304

0.1.3 重构了错误url到/error/... 修改了文件详情页的传输逻辑：chunk分块传输？

0.1.4 重写chunk分块传输和断点续传，实现了电脑端视频在线播放

0.1.5 重写端点续传，移除chunk分块传输，修复了手机端无法播放的问题？

0.1.6 添加了上传进度条，文件大小校验（头“x-file-size”），添加文件上传中取消，XMLHttpRequest实现上传进度条

0.1.7 重写了网站首页ui

0.1.8 优化网站首页ui（添加加载界面，更换背景等......），添加'/resource/path'无加密路径访问。修改目录界面背景图，实现目录展开和折叠。

0.1.9 优化网站首页ui（更改鼠标图案，添加动态视频背景，音频是否播放按钮等......）

0.1.10 优化加载进度条（动态图片和真进度条fetch实现）；重构网站代码（静态资源分开，js，css，html分开放）；增加搜索文件功能；添加多种字体；静态资源单独存放“/static/”；添加背景视频伪高清图层；修改目录表格大小到12%。

0.1.11 修改字体，添加字体加载进度条，加载伪延时0.2秒


0.2.0 与wlsaSH合作，添加子应用

0.2.1 如果是手机，不显示鼠标图样。加载结束后移除加载动画标签，而不是设置display:none避免干扰页面排版

0.2.2 Change hyperlink hover effect, Remove home button, Fix index href

0.2.3 破译了校宝的登录哈希，lib.py中封装了自动生成校宝的md5（下一步模拟请求校宝并检测是否通过请求）

0.2.4 2024/9/30 12:39 封装了校宝密码校验函数check_xiaobao_login(username, password)在lib.py中，账号密码正确会返回True，错误会返回False，发生异常会返回None

0.2.5 2024/9/30 14:56 新建了config.py用于存储常量；在wlsaSH中新建页面/login来实现登录逻辑

0.2.6 2024/9/30 20:04 重构项目逻辑：将大部分html转移到templates中；使用webpy.render动态加载html，而不是pages.py；将网盘与学校网站写为总网站的子应用（模块化）；

0.2.7 2024/9/30 21:12 重构了wlsash的资源html，并修改为render加载

0.2.8 2024/10/1 12:38 Rewrite start.bat, py.bat and 一键启动.vbs, so that it could cd to current folder automatically, as well as determine use a conda env python or python in system path automatically and give out info; Changed the archives page.

0.2.9 2024/10/1 22:14 Resturctured static dir; improved wlsash, archives page

0.3.0 2024/10/2 01:02 (Calvin) Fixed the bug that path displays Unicode encoding for non Latin letters, Fixed icons8-link.svg, changed hover and active effects for li tags, and set fixed width and height for li and img tags in li

下个版本的目标: 1.修改dict逻辑到render里面; 2.翻一下static的实现逻辑; 3.notify.html template; 4.config实现作用; 5.js和css的模块复用; 6.规范化变量，函数，类和文件的命名
