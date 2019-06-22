#!/usr/bin/python
# coding=UTF-8
# 需要先安装argparse和paramiko模块

import os
import sys
import argparse
import paramiko
import xml.dom.minidom
import datetime

#----------ssh远程执行命令 & 上传下载文件----------#

# 定义远程执行命令的函数，作用是在一台远程主机上执行一条命令并返回标准输出和错误输出。执行命令须是字符串，远程IP须是字符串
def remote_execute(exe_cmd,remote_ip):

	# 远程连接主机
	ssh = paramiko.SSHClient()

	# 自动添加主机名和主机密钥保存到本地的HostKeys
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	
	# 输入关键SSH参数：主机名(可以是IP)，端口号，用户名，密码
	ssh.connect(hostname=remote_ip,port=lgsshp,username=lgusn,password=lgpsw)

	# 顺序执行命令，无报错则认为成功
	stdin,stdout,stderr = ssh.exec_command(exe_cmd)
	result_err = stderr.readline()
	result_out = stdout.readline()
	
	# 关闭ssh连接
	ssh.close()
	
	return result_out,result_err

# 定义远程传送文件的函数，作用是往一台远程主机传输一个文件。本地路径和远端路径必须是字符串，远程IP必须是字符串
def remote_put(Localpath,Remotepath,remote_IP):

	# 指定远程登录主机和登录端口
	trans = paramiko.Transport((remote_IP,int(lgsshp)))
	
	# 连接远端主机
	trans.connect(username=lgusn,password=lgpsw)
	
	# 指定对象sftp
	sftp = paramiko.SFTPClient.from_transport(trans)
	
	# 上传文件到远端主机
	sftp.put(Localpath,Remotepath)
	
	# 结束连接
	trans.close()

# 定义远程下载文件的函数，作用是从一台远程主机下载文件。本地路径和远端路径必须是列表类型，远程IP必须是字符串
def remote_get(Localpath,Remotepath,remote_IP):
			
	# 指定远程登录主机和登录端口
	trans = paramiko.Transport((remote_IP,int(lgsshp)))
	
	# 连接远端主机
	trans.connect(username=lgusn,password=lgpsw)
	
	# 指定对象sftp
	sftp = paramiko.SFTPClient.from_transport(trans)
			
	msg = "Downloading files from remote host: %s\n"%(Remotepath)
	log_record_print(log_name,msg)
	
	# 上传文件到远端主机
	sftp.get(Remotepath,Localpath)
	
	# 结束连接
	trans.close()

#----------创建日志文件----------#
def log_creation():
	print('\n--------------------Creating Log File--------------------\n')
	current_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
	
	c_w_d = sys.path[0]
	
	log_root_dir = os.path.join(c_w_d,'log')
	if os.path.exists(log_root_dir) == True:
		print('%s exists, skipped\n'%(log_root_dir))
	else:
		os.mkdir(log_root_dir)
		print('log directory created: %s\n'%(log_root_dir))
		
	log_file_name = os.path.join(log_root_dir,'log-%s.txt'%(current_time))
	# 打开文件，'w'参数代表作为写入模式，如果该文件不存在则创建该文件，如果该文件存在则追加覆盖文本内容；
	logfile = open(log_file_name,'w')
	logfile.write('--------------------start--------------------\n')
	logfile.close()
	print('log file created: %s\n'%(log_file_name))
	
	return log_file_name

#----------记录日志----------#
def log_record_print(log_file_name,log_msg):
		
	# 打开日志文件并追加内容在最后一行
	logfile = open(log_file_name,'a')
	
	# 写入文件时如果是以对象的方式传递字符串，系统并不能识别该字符串前后的换行符，所以需要额外换行
	logfile.write('\n')
		
	# 记录信息
	current_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
	logfile.write("%s: %s"%(current_time,log_msg))
	print("%s: %s"%(current_time,log_msg))
	
	logfile.close()
			
#----------配置前检查----------#

def Pre_Check():
	
	msg = "--------------------Pre_Check start--------------------\n"
	log_record_print(log_name,msg)
	
	# 错误计数器
	Error_Counter = 0
	
	# 脚本所在目录
	cwd_path = sys.path[0]
	
	# 检查目录正确性
	
	Dir_List = [OSimagedir,Yumdir,Pydir]
	
	msg = "--------------------Directory Checking--------------------\n"
	log_record_print(log_name,msg)
	
	for c in range(len(Dir_List)):
		if os.path.exists(os.path.join(cwd_path,Dir_List[c])):
			msg = "Directory %s exists\n"%(Dir_List[c])
			log_record_print(log_name,msg)
		else:
			msg = "Error: Directory %s not exists\n"%(Dir_List[c])
			log_record_print(log_name,msg)
			Error_Counter += 1
			
	# 检查文件名正确性
	
	File_List = [OSimagename,Yumname,Pyname]
	
	msg = "--------------------File Checking--------------------\n"
	log_record_print(log_name,msg)
	
	for c in range(len(File_List)):
		if os.path.exists(os.path.join(cwd_path,Dir_List[c],File_List[c])):
			msg = "File %s exists\n"%(File_List[c])
			log_record_print(log_name,msg)
		else:
			msg = "Error: File %s not exists\n"%(File_List[c])
			log_record_print(log_name,msg)
			Error_Counter += 1
			
	# 检查网络是否可达
	
	msg = "--------------------Network Checking--------------------\n"
	log_record_print(log_name,msg)
	
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	
	for c in range(len(rmipls)):
		try:
			ssh.connect(hostname=rmipls[c],port=lgsshp,username=lgusn,password=lgpsw)
			msg = "Connection succeeded: %s\n"%(rmipls[c])
			log_record_print(log_name,msg)
		except OSError as err_msg:
			msg = "%s\n Can't reach IP Address: %s\n"%(err_msg,rmipls[c])
			log_record_print(log_name,msg)
			Error_Counter += 1
		except paramiko.ssh_exception.AuthenticationException as err_msg:
			msg = "%s\n username or password is wrong: %s\n"%(err_msg,rmipls[c])
			log_record_print(log_name,msg)
			Error_Counter += 1
	
	# 检查结束
	msg = "--------------------Pre_Check finished--------------------\n"
	log_record_print(log_name,msg)
	
	if Error_Counter == 0:
		msg = "--------------------Setup start--------------------\n"
		log_record_print(log_name,msg)
		
	return Error_Counter

#----------上传文件----------#

def Trans_File():	
	
	# 错误计数器初始化
	Error_Counter = 0

	# 获取当前脚本所在路径，注意不要改动文件目录结构
	rootpath = sys.path[0]

	# 定义本端的文件位置，用于put，和远端的文件位置一一对应
	lcp_put = [
			   os.path.join(rootpath,OSimagedir,OSimagename),
			   os.path.join(rootpath,Yumdir,Yumname),
			   os.path.join(rootpath,Pydir,Pyname)
			  ]
	# 定义远端的文件位置，用于put，和本端的文件位置一一对应
	rmp_put = [
			   os.path.join(rmflc,OSimagename),
			   os.path.join(rmflc,Yumname),
			   os.path.join(rmflc,Pyname)
			  ]
			  
	# 如果目录不存在则创建
	Dir_CMD = 'test ! -d %s && mkdir %s || echo "Warning: Directory exists"'%(rmflc,rmflc)	
	
	# 循环迭代：先主机后文件
	for c in range(len(rmipls)):
		
		MachineNo = c + 1
		
		msg = "--------------------Machine%s Transporting--------------------\n"%(MachineNo)
		log_record_print(log_name,msg)
		
		RMIP = rmipls[c]
		
		# 创建远端文件夹
		msg = "Creating directory: %s\n"%(rmflc)
		log_record_print(log_name,msg)
		result = remote_execute(Dir_CMD,RMIP)
		
		for n in range(len(result)):
			if result[n]:
				msg = "%s"%(result[n])
				log_record_print(log_name,msg)
		
		# 先检查文件是否已存在，如果存在则不传输
		
		for n in range(len(rmp_put)):
			dir_name,file_name = os.path.split(rmp_put[n])
			msg = "Transporting file: %s\n"%(file_name)
			log_record_print(log_name,msg)
			
			# 检查文件是否已存在，不存在则返回1，存在则返回0
			result = remote_execute('test ! -f %s && echo 1 || echo 0'%(rmp_put[n]),RMIP)				
				
			#分析检查结果，1则传输文件，0则跳过传输	
			if result[0] == '1\n':
				remote_put(lcp_put[n],rmp_put[n],RMIP)
			elif result[0] == '0\n':
				msg = "File %s exists, skipped\n"%(rmp_put[n])
				log_record_print(log_name,msg)
		
		# 检查文件是否传输成功
		Fail_Record = []
		for	n in range(len(rmp_put)):
		
			# 检查文件是否已传输成功，成功则返回1，失败则返回0
			result = remote_execute('test -f %s && echo 1 || echo 0'%(rmp_put[n]),RMIP)
			
			# 记录失败文件名
			if result[0] == '0\n':
				Error_Counter += 1
				Fail_Record.append("%s: file %s transport failed"%(RMIP,rmp_put[n]))
	
	# 打印失败结果
	if Error_Counter > 0:
		
		msg = "--------------------Failed to transport these files:--------------------\n"
		log_record_print(log_name,msg)	
		
		for m in range(len(Fail_Record)):
			msg = "%s\n"%(Fail_Record[m])
			log_record_print(log_name,msg)	
	
	return Error_Counter
	
#----------基本配置----------#

def Initial_Config():

	# 错误计数器初始化
	Error_Counter = 0
	
	for c in range(len(rmipls)):
		
		MachineNo = c + 1
		
		msg = "--------------------Machine%s configuration-------------------\n"%(MachineNo)
		log_record_print(log_name,msg)
		
		# 定义远程执行的命令(基本配置)
		Initial_CMD = [
					   'hostnamectl set-hostname --static %s'%(nhnls[c]),
					   'groupadd %s'%(nusg),
					   'useradd -g %s %s'%(nusg,nusn),
					   'echo %s | passwd %s --stdin'%(nupsw,nusn),
					  ]
		RMIP = rmipls[c]	
		remote_execute(Initial_CMD,RMIP)
	
	return Error_Counter
	
#----------配置Yum本地源----------#

def Yum_Repo_Src():

	# 错误计数器初始化
	Error_Counter = 0
	
	# 定义yum配置命令
	Yum_CMD = [
				 'mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.bak',
				 'cp %s /etc/yum.repos.d/CentOS-Base.repo'%(os.path.join(rmflc,Yumname)),
				 'mkdir %s'%(yumlc),
				 'mkdir /tmp/CentOS7;mount %s /tmp/CentOS7'%(os.path.join(rmflc,OSimagename)), #创建临时目录挂载镜像
				 'cp -r /tmp/CentOS7/* %s'%(yumlc),
				 'umount /tmp/CentOS7;rm -rf /tmp/CentOS7' #取消挂载并删除临时目录
			  ]

	for c in range(len(rmipls)):
		
		MachineNo = c + 1
		
		msg = "--------------------Machine%s Yum config--------------------\n"%(MachineNo)
		log_record_print(log_name,msg)
		
		RMIP = rmipls[c]
		
		remote_execute(Yum_CMD,RMIP)
	
	return Error_Counter
	
#----------安装python----------#

def Python_Install():

	# 错误计数器初始化
	Error_Counter = 0
	
	# 定义python安装命令
	PySetup_CMD = [
				   'mkdir %s/Python3'%(rmflc),
				   'tar -zxvf %s -C %s/Python3'%(os.path.join(rmflc,Pyname),rmflc),
				   'yum install -y zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel libffi-devel gcc make',
				   'cd %s/Python3/Python-3.7.3 && ./configure --prefix=/usr/local/python3 && make && make install'%(rmflc), 
				   'mv /usr/bin/python /usr/bin/python.bak',
				   'ln /usr/local/python3/bin/python3.7 /usr/bin/python',
				   'ln -s /usr/local/python3/bin/pip3 /usr/bin/pip',
				   "cp /usr/bin/yum /usr/bin/yum.bak;sed -i '1c\#! /usr/bin/python2' /usr/bin/yum",
				   "cp /usr/libexec/urlgrabber-ext-down /usr/libexec/urlgrabber-ext-down.bak;sed -i '1c\#! /usr/bin/python2' /usr/libexec/urlgrabber-ext-down"
				  ]
				  
	for c in range(len(rmipls)):
		
		MachineNo = c + 1
		
		msg = "--------------------Machine%s Python installation--------------------\n"%(MachineNo)
		log_record_print(log_name,msg)
		
		RMIP = rmipls[c]
		
		remote_execute(PySetup_CMD,RMIP)
	
	return Error_Counter
	
#----------程序主体----------#

log_name = log_creation()

try: 
	#----------外传参数----------#
	# 外传参数方法调用
	parser = argparse.ArgumentParser()
	# 定义外传参数：xml文件名称
	parser.add_argument('-xmlfile',required=True,dest='XMLfile',help='xml file name')
	# 装载外传参数到args
	args = parser.parse_args()

	# 打开xml文件
	dom = xml.dom.minidom.parse('%s'%(args.XMLfile))

	# 获取远程IP列表
	RMIPLS = dom.getElementsByTagName('remoteIP')
	# 获取新主机名列表
	NHNLS = dom.getElementsByTagName('newhostname')
	# 获取ssh登录用户名
	LGUSN = dom.getElementsByTagName('loginuser')
	# 获取ssh登录密码
	LGPSW = dom.getElementsByTagName('loginpassword')
	# 获取ssh登录端口号
	LGSSHP = dom.getElementsByTagName('sshport')
	# 获取新建用户组
	NUSG = dom.getElementsByTagName('newusergroup')
	# 获取新建用户名
	NUSN = dom.getElementsByTagName('newuser')
	# 获取新建用户密码
	NUPSW = dom.getElementsByTagName('newpassword')
	# 获取远端主机保存位置
	RMFLC = dom.getElementsByTagName('file_path')
	# 获取远端主机yum源目录
	YUMLC = dom.getElementsByTagName('yum_location')
	# 获取镜像名称
	OSIMN = dom.getElementsByTagName('osimagename')
	# 获取repo文件名称
	YRPN = dom.getElementsByTagName('yumreponame')
	# 获取python安装文件名称
	PYISLN = dom.getElementsByTagName('pythoninstaller')

	# 提取所有参数
	rmipls = []
	for c in range(len(RMIPLS)):
		rmipls.append(RMIPLS[c].firstChild.data)
		
	nhnls = []
	for c in range(len(NHNLS)):
		nhnls.append(NHNLS[c].firstChild.data)
		
	lgusn = LGUSN[0].firstChild.data
	lgpsw = LGPSW[0].firstChild.data
	lgsshp = LGSSHP[0].firstChild.data
	nusg = NUSG[0].firstChild.data
	nusn = NUSN[0].firstChild.data
	nupsw = NUPSW[0].firstChild.data
	rmflc = RMFLC[0].firstChild.data
	yumlc = YUMLC[0].firstChild.data
	OSimagename = OSIMN[0].firstChild.data
	Yumname = YRPN[0].firstChild.data
	Pyname = PYISLN[0].firstChild.data

	Para_Dict = {
				 "remote host IP list":rmipls,
				 "new host name list":nhnls,
				 "login user":lgusn,
				 "login password":lgpsw,
				 "ssh port":lgsshp,
				 "new user group":nusg,
				 "new user":nusn,
				 "new password":nupsw,
				 "remote files location":rmflc,
				 "yum source location":yumlc,
				 "OS image name":OSimagename,
				 "yum repo name":Yumname,
				 "python installer name":Pyname
				 }
	
	# 以下为配置文件存放文件夹，请不要修改，除非修改安装包
	OSimagedir = 'OS_Image'
	Yumdir = 'Yum_Repo'
	Pydir = 'Python'

	# 打印提取结果
	msg = '\n--------------------Parameter Analysis Result--------------------\n'
	log_record_print(log_name,msg)
	
	para_check_errors = 0
	Not_Defined_Para = []
	
	for key in Para_Dict.keys():
		if Para_Dict[key]:
			if (key == "login password") | (key == "new password"):
				msg = "%s:\n***\n"%(key)
				log_record_print(log_name,msg)
			else:	
				msg = "%s:\n%s\n"%(key,Para_Dict[key])
				log_record_print(log_name,msg)
		else:
			msg = "%s NOT defined\n"%(key)
			log_record_print(log_name,msg)
			para_check_errors += 1
			Not_Defined_Para.append(key)
	
except FileNotFoundError:
	msg = "Error: Can't find xml file in specified location, please enter correct path\n"
	log_record_print(log_name,msg)

else:
	if para_check_errors > 0:
		msg = "Script stopped because some parameter not defined. Please check log file: %s\n"%(log_name)
		log_record_print(log_name,msg)
	elif Pre_Check() > 0: 
		msg = "Script stopped because pre-check failed. Please check log file: %s\n"%(log_name)
		log_record_print(log_name,msg)
	# 开始设置远程主机
	elif Trans_File() > 0:
		msg = "Script stopped because transportation failed. Please check log file: %s\n"%(log_name)
		log_record_print(log_name,msg)
	'''
	elif Initial_Config() > 0:	
		msg = "Script stopped because initial Configuration failed. Please check log file: %s\n"%(log_name)
		log_record_print(log_name,msg)
	elif Yum_Repo_Src() > 0:
		msg = "Script stopped because yum setup failed. Please check log file: %s\n"%(log_name)
		log_record_print(log_name,msg)
	elif Python_Install() > 0:
		msg = "Script stopped because python installation failed. Please check log file: %s\n"%(log_name)
		log_record_print(log_name,msg)
	'''
	
	# 结束设置远程主机
	msg = "--------------------Finished--------------------\n"
	log_record_print(log_name,msg)
	print("Log record in file: %s\n"%(log_name))
