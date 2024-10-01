Set ws = CreateObject("Wscript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' 获取当前目录
currentDirectory = fso.GetParentFolderName(WScript.ScriptFullName)
WScript.Echo currentDirectory

' 构建 start.bat 的完整路径
startbat = fso.BuildPath(currentDirectory, "\start.bat")

ws.run "cmd /c """ & startbat & """", vbhide
