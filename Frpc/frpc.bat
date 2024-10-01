chcp 65001
set currentDir=%~dp0
cd /d "%currentDir%"
echo 当前目录: %currentDir%
start /b frpc.exe -c frpc.ini
