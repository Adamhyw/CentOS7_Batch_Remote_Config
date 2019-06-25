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
	result_out = stdout.readlines()
	result_err = stderr.readlines()
	
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

# 远程执行命令并记录日志（命令自带判断功能）

def execute_wt_deter(msg,CMD,rip):
	
	log_record_print(log_name,msg)
				
	result_stdout,result_errout = remote_execute(CMD,rip)
				
	if result_stdout:
		for n in range(len(result_stdout)):
			msg = "%s\n"%(result_stdout[n])
			log_record_print(log_name,msg)

# 远程执行命令并记录日志（命令不带判断功能）

def execute_wto_deter(msg,CMD,rip):

	log_record_print(log_name,msg)
			
	result_stdout,result_errout = remote_execute(CMD,rip)
			
	if result_errout:
		for n in range(len(result_errout)):
			msg = "%s\n"%(result_errout[n])
			log_record_print(log_name,msg)

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
	Dir_CMD = 'test ! -d %s && mkdir -p %s || echo "Warning: Directory exists"'%(rmflc,rmflc)	
	
	# 循环迭代：先主机后文件
	for c in range(len(rmipls)):
		
		MachineNo = c + 1
		
		msg = "--------------------Machine%s Transporting--------------------\n"%(MachineNo)
		log_record_print(log_name,msg)
		
		RMIP = rmipls[c]
		
		# 创建远端文件夹
		msg = "Creating directory: %s\n"%(rmflc)
		execute_wt_deter(msg,Dir_CMD,RMIP)
		
		# 先检查文件是否已存在，如果存在则不传输
		
		for n in range(len(rmp_put)):
			dir_name,file_name = os.path.split(rmp_put[n])
			msg = "Transporting file: %s\n"%(file_name)
			log_record_print(log_name,msg)
			
			# 检查文件是否已存在，不存在则返回1，存在则返回0
			result_stdout,result_errout = remote_execute('test ! -f %s && echo 1 || echo 0'%(rmp_put[n]),RMIP)				
				
			#分析检查结果，1则传输文件，0则跳过传输	
			if (result_stdout[0].replace('\n','')) == '1':
				remote_put(lcp_put[n],rmp_put[n],RMIP)
			elif (result_stdout[0].replace('\n','')) == '0':
				msg = "File %s exists, skipped\n"%(rmp_put[n])
				log_record_print(log_name,msg)
		
		# 检查文件是否传输成功
		Fail_Record = []
		for	n in range(len(rmp_put)):
		
			# 检查文件是否已传输成功，成功则返回1，失败则返回0
			result_stdout,result_errout = remote_execute('test -f %s && echo 1 || echo 0'%(rmp_put[n]),RMIP)
			
			# 记录失败文件名
			if (result_stdout[0].replace('\n','')) == '0':
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
		
		RMIP = rmipls[c]
		
		msg = "--------------------Machine%s initial config-------------------\n"%(MachineNo)
		log_record_print(log_name,msg)
		
		# 设置主机名，永久生效
		Hostname_CMD = 'hostnamectl set-hostname --static %s'%(nhnls[c])
		
		msg = "Setting hostname: %s\n"%(nhnls[c])
		log_record_print(log_name,msg)
		
		remote_execute(Hostname_CMD,RMIP)
		
		# 检查主机名设置是否成功
		Hostname_Check_CMD = 'hostname -f'
		result_stdout,result_errout = remote_execute(Hostname_Check_CMD,RMIP)
		if (result_stdout[0].replace('\n','')) != nhnls[c]:
			msg = "Failed to set hostname\n"
			log_record_print(log_name,msg)
			Error_Counter += 1
			
		# 创建用户组
		msg = "Creating group: %s\n"%(nusg)
		log_record_print(log_name,msg)
		
		Group_Check_CMD = 'cat /etc/group | grep %s'%(nusg)
		Group_Add_CMD = 'groupadd %s'%(nusg)
				
		# 检查该组名是否已存在，如果是，则不创建
		result_stdout,result_errout = remote_execute(Group_Check_CMD,RMIP)
		checkpoint = 0
		if result_stdout:
			for n in range(len(result_stdout)):
				groupname = result_stdout[n].split(':')
				if groupname[0] == nusg:
					msg = "Group exists: %s, skipped\n"%(nusg)
					log_record_print(log_name,msg)
					checkpoint = 1
					break
				elif (n == len(result_stdout) - 1):
					remote_execute(Group_Add_CMD,RMIP)
				else:
					continue
		else:
			remote_execute(Group_Add_CMD,RMIP)
		
		# 检查用户组是否创建成功
		if checkpoint == 0:
			result_stdout,result_errout = remote_execute(Group_Check_CMD,RMIP)
			if result_stdout:
				for n in range(len(result_stdout)):
					groupname = result_stdout[n].split(':')
					if groupname[0] == nusg:
						msg = "Group creation succeeded: %s\n"%(nusg)
						log_record_print(log_name,msg)
						break
					elif (n == len(result_stdout) - 1):
						msg = "Group creation failed: %s\n"%(nusg)
						log_record_print(log_name,msg)
						Error_Counter += 1
					else:
						continue
			else:
				msg = "Group creation failed: %s\n"%(nusg)
				log_record_print(log_name,msg)
				Error_Counter += 1
		
		# 创建用户
		msg = "Creating user: %s\n"%(nusn)
		log_record_print(log_name,msg)
		
		User_Check_CMD = 'cat /etc/passwd | grep %s'%(nusn)
		User_Add_CMD = 'useradd -g %s %s && echo %s | passwd %s --stdin'%(nusg,nusn,nupsw,nusn)
					   
		# 检查该用户是否已存在，如果是，则不创建
		checkpoint = 0
		result_stdout,result_errout = remote_execute(User_Check_CMD,RMIP)
		if result_stdout:
			for n in range(len(result_stdout)):
				username = result_stdout[n].split(':')
				if username[0] == nusn:
					msg = "User exists: %s, skipped\n"%(nusn)
					log_record_print(log_name,msg)
					checkpoint = 1
					break
				elif (n == len(result_stdout) - 1):
					remote_execute(User_Add_CMD,RMIP)
				else:
					continue
		else:
			remote_execute(User_Add_CMD,RMIP)
		
		# 检查用户是否创建成功
		if checkpoint == 0:
			result_stdout,result_errout = remote_execute(User_Check_CMD,RMIP)
			if result_stdout:
				for n in range(len(result_stdout)):
					username = result_stdout[n].split(':')
					if username[0] == nusn:
						msg = "User creation succeeded: %s\n"%(nusn)
						log_record_print(log_name,msg)
						break
					elif (n == len(result_stdout) - 1):
						msg = "User creation failed: %s\n"%(nusn)
						log_record_print(log_name,msg)
					else:
						continue
			else:
				msg = "User creation failed: %s\n"%(nusn)
				log_record_print(log_name,msg)
				Error_Counter += 1
	
	return Error_Counter
	
#----------配置Yum本地源----------#

def Yum_Repo_Src():

	# 错误计数器初始化
	Error_Counter = 0
	
	# 创建备份文件夹并保存repo文件
	Bak_Dir_CMD = 'test ! -d %s && mkdir -p %s || echo "Warning: Directory exists"'%(Backup_Dir,Backup_Dir)
	Bak_File_CMD = 'test ! -f %s/CentOS-Base.repo.bak && mv /etc/yum.repos.d/CentOS-Base.repo %s/CentOS-Base.repo.bak || echo "Warning: CentOS-Base.repo is already backup, skipped\n "'%(Backup_Dir,Backup_Dir)
	
	# 拷贝新repo文件
	New_Repo_CMD = 'test ! -f /etc/yum.repos.d/CentOS-Base.repo && cp %s /etc/yum.repos.d/CentOS-Base.repo || "Warning: There is already a CentOS-Base.repo,skipper\n"'%(os.path.join(rmflc,Yumname))
	
	# 创建镜像文件存放目录
	Yum_Dir_CMD = 'test ! -d %s && mkdir -p %s || (rm -rf %s/*;echo "Warning: Directory exists. Removing all files under it!")'%(yumlc,yumlc,yumlc)
	
	# 创建临时挂载目录
	TMP_Dir_CMD = 'test ! -d /tmp/CentOS7 && mkdir -p /tmp/CentOS7 || (rm -rf /tmp/CentOS7/*;echo "Warning: Directory exists. Removing all files under it!")'
	
	# 挂载镜像，拷贝文件，删除临时目录
	Image_Copy_CMD = 'mount %s /tmp/CentOS7 && cp -r /tmp/CentOS7/* %s && umount /tmp/CentOS7 && rm -rf /tmp/CentOS7'%(os.path.join(rmflc,OSimagename),yumlc)
	
	# 检查yum源是否设置成功
	Yum_Check_CMD = 'yum list'

	for c in range(len(rmipls)):
		
		MachineNo = c + 1
		
		msg = "--------------------Machine%s Yum config--------------------\n"%(MachineNo)
		log_record_print(log_name,msg)
		
		RMIP = rmipls[c]
		
		# 创建备份文件夹
		msg = "Creating backup directory: %s\n"%(Backup_Dir)
		execute_wt_deter(msg,Bak_Dir_CMD,RMIP)
		
		# 备份repo文件		
		msg = "Creating backup file: CentOS-Base.repo.bak\n"
		execute_wt_deter(msg,Bak_File_CMD,RMIP)
		
		# 拷贝新repo文件
		msg = "Copying new repo file: CentOS-Base.repo\n"
		execute_wt_deter(msg,New_Repo_CMD,RMIP)
			
		# 创建镜像文件存放目录
		msg = "Creating yum directory: %s\n"%(yumlc)
		execute_wt_deter(msg,Yum_Dir_CMD,RMIP)
		
		# 挂载镜像，拷贝文件，删除临时目录
		msg = "Creating tmp directory\n"
		execute_wto_deter(msg,TMP_Dir_CMD,RMIP)
		
		msg = "Copying image files\n"
		execute_wt_deter(msg,Image_Copy_CMD,RMIP)
		
		# 检查yum源是否设置成功
		msg = "Checking yum repository\n"
		log_record_print(log_name,msg)
		
		result_stdout,result_errout = remote_execute(Yum_Check_CMD,RMIP)
		
		if result_errout:
			msg = "Yum repository is not set correctly\n"
			log_record_print(log_name,msg)
			Error_Counter += 1
		else:
			msg = "Yum repository is set correctly\n"
			log_record_print(log_name,msg)
		
	return Error_Counter
	
#----------安装python----------#

def Python_Install():

	# 错误计数器初始化
	Error_Counter = 0
	
	Py3_Ins_Path = '/usr/local/python3'
	
	# 创建Python解压文件夹
	Py_Ext_Dir_CMD = 'test ! -d %s/Python3 && mkdir -p %s/Python3 || (rm -rf %s/Python3/*;echo "Warning: Directory exists")'%(rmflc,rmflc,rmflc)
	
	# 解压Python文件
	Py_Ext_CMD = 'tar -zxvf %s -C %s/Python3'%(os.path.join(rmflc,Pyname),rmflc)

	# 安装python依赖包
	Py_dep_CMD = 'yum install -y zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel libffi-devel gcc make'			   
	
	# 检查python3是否已安装
	Py3_Ver_CMD = 'test ! -d %s && echo 1 || echo 0'%(Py3_Ins_Path)
	
	# 安装python
	Py_Inst_CMD = 'cd %s/Python3/Python-3.7.3 && ./configure --prefix=%s && make && make install'%(rmflc,Py3_Ins_Path)
	
	# 创建新版本python链接
	Ln_Py_CMD = 'ln %s/bin/python3.7 /usr/bin/python3;ln -s %s/bin/pip3 /usr/bin/pip3'%(Py3_Ins_Path,Py3_Ins_Path)
	
	# 删除临时解压目录
	Py_Ext_Del_CMD = 'rm -rf %s/Python3'%(rmflc)
				  
	for c in range(len(rmipls)):
		
		MachineNo = c + 1
		
		msg = "--------------------Machine%s Python installation--------------------\n"%(MachineNo)
		log_record_print(log_name,msg)
		
		RMIP = rmipls[c]
		
		# 判断Python3是否已安装
		result_stdout,result_errout = remote_execute(Py3_Ver_CMD,RMIP)
		
		if result_stdout[0].replace('\n','') == '0':
			msg = "Warning: Python3 already installed, skipped\n"
			log_record_print(log_name,msg)
		elif result_stdout[0].replace('\n','') == '1':
			
			# 创建Python解压文件夹
			msg = "Creating Python3 extract directory: %s/Python3\n"%(rmflc)
			execute_wt_deter(msg,Py_Ext_Dir_CMD,RMIP)
			
			# 解压Python文件
			msg = "Extracting Python3 files to %s/Python3\n"%(rmflc)
			execute_wto_deter(msg,Py_Ext_CMD,RMIP)
			
			# 安装python依赖包
			msg = "Installing Python3 dependency\n"
			execute_wto_deter(msg,Py_dep_CMD,RMIP)
			
			# 安装python3
			msg = "Installing Python3 software\n"
			execute_wto_deter(msg,Py_Inst_CMD,RMIP)
					
			# 创建python链接
			msg = "Creating link of new version of python\n"
			execute_wto_deter(msg,Ln_Py_CMD,RMIP)
			
			# 删除临时解压目录
			msg = "Removing extract directory\n"
			execute_wto_deter(msg,Py_Ext_Del_CMD,RMIP)
		
		# 检查Python3安装是否成功
		msg = "Checking Python3 installation\n"
		log_record_print(log_name,msg)
		
		result_stdout,result_errout = remote_execute('python3 -V',RMIP)
		
		if result_stdout[0].replace('\n','') == 'Python 3.7.3':
			msg = "Python3 installation succeeded\n"
			log_record_print(log_name,msg)
		else:
			msg = "Python3 installation failed\n"
			log_record_print(log_name,msg)
			Error_Counter += 1
		
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
	
	# 以下为远程主机重要系统文件备份位置，请不要修改
	Backup_Dir = '/opt/SYS_BAK'

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
	elif Initial_Config() > 0:	
		msg = "Script stopped because initial Configuration failed. Please check log file: %s\n"%(log_name)
		log_record_print(log_name,msg)
	elif Yum_Repo_Src() > 0:
		msg = "Script stopped because yum setup failed. Please check log file: %s\n"%(log_name)
		log_record_print(log_name,msg)
	elif Python_Install() > 0:
		msg = "Script stopped because python installation failed. Please check log file: %s\n"%(log_name)
		log_record_print(log_name,msg)
	
	# 结束设置远程主机
	msg = "--------------------All Setup Finished--------------------\n"
	log_record_print(log_name,msg)
	print("Log record in file: %s\n"%(log_name))