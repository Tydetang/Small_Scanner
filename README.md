# Small_Scanner
大二数据结构课设

源码存在于Tool.py当中

代码使用pyinstaller.py库生成可执行文件Tool.exe，打开时会存在黑框，并不影响使用

C段端口扫描正确格式为IP地址如:127.0.0.1，当前在工具中只能扫描端口，端口使用存在于port.txt中

目录扫描正确格式为网站地址如:http://www.baidu.com/ 扫描的目录为同一文件夹下http.txt文件中

一句话爆破正确格式为网站地址如:http://www.baidu.com/yijvhua.php 当前只能爆破php一句话，爆破字典存在于pass.txt中

zip爆破正确格式为当前目录下的zip后缀文件如:pass.zip，当前为爆破4位同类型密码

此文件只在win7 64位下测试运行成功

可执行文件并没有打包第三方库，如若不能运行成功，请确保是否安装所需要的第三方库：requests，Tkinter等
