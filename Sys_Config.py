#!/usr/bin/python
# coding=UTF-8
# 需要先安装argparse和paramiko模块

import os
import sys
import argparse
import paramiko
import xml.dom.minidom

#----------参数导入----------#

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
nhnls = []
for c in range(len(RMIPLS)):
	rmipls.append(RMIPLS[c].firstChild.data)
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

# 以下为配置文件存放文件夹，请不要修改，除非修改安装包
OSimagedir = 'OS_Image'
Yumdir = 'Yum_Repo'
Pydir = 'Python'

# 打印提取结果
print('remote host IP list:\n',rmipls)
print('new host name list:\n',nhnls)	
print('loginuser:\n',lgusn)
print('loginpassword:\n',lgpsw)
print('sshport:\n',lgsshp)
print('newusergroup:\n',nusg)
print('newuser:\n',nusn)
print('newpassword:\n',nupsw)
print('remotefileslocation:\n',rmflc)
print('yum source location:\n',yumlc)
print('OS image name:\n',OSimagename)
print('yum repo name:\n',Yumname)
print('python installer name:\n',Pyname)

#----------定义函数：ssh远程执行命令 & 上传下载文件----------#

# 定义远程执行批量命令的函数，作用是在一台远程主机执行多条命令。命令须是列表类型，远程IP须是字符串
def remote_execute(exe_cmd,remote_ip):

	# 远程连接主机
	ssh = paramiko.SSHClient()

	# 自动添加主机名和主机密钥保存到本地的HostKeys
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	
	# 输入关键SSH参数：主机名(可以是IP)，端口号，用户名，密码
	ssh.connect(hostname=remote_ip,port=lgsshp,username=lgusn,password=lgpsw)

	# 顺序执行命令，无报错则认为成功
	for n in range(len(exe_cmd)):
		print("Running CMD: %s\n"%(exe_cmd[n]))
		stdin,stdout,stderr = ssh.exec_command(exe_cmd[n])
		result = stderr.read()
		if result:
			print("error: %s"%result)
		else:
			print("Succeeded\n")
	
	# 关闭ssh连接
	ssh.close()

# 定义远程传送文件的函数，作用是往一台远程主机传输文件。本地路径和远端路径必须是列表类型，远程IP必须是字符串
def remote_put(Localpath,Remotepath,remote_IP):

	# 指定远程登录主机和登录端口
	trans = paramiko.Transport((remote_IP,int(lgsshp)))
	
	# 连接远端主机
	trans.connect(username=lgusn,password=lgpsw)
	
	# 指定对象sftp
	sftp = paramiko.SFTPClient.from_transport(trans)
	
	for n in range(len(Localpath)):
		
		print("Transporting files to remote host: %s\n"%(Localpath[n]))
		
		# 上传文件到远端主机
		sftp.put(Localpath[n],Remotepath[n])
		
		print("Transport succeeded. File locates at %s\n"%(Remotepath[n]))
	
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
	
	# 轮流传输多个文件到远端
	for n in range(len(Localpath)):
		
		print("Downloading files from remote host: %s\n"%(Remotepath[n]))
		
		# 上传文件到远端主机
		sftp.get(Remotepath[n],Localpath[n])
		
		print("Transport succeeded. File locates at %s\n"%(Localpath[n]))
	
	# 结束连接
	trans.close()

#----------基本配置----------#

def Initial_Config():
	c = 0
	for c in range(len(rmipls)):
		
		MachineNo = c + 1
		
		print("--------------------Machine%s configuration--------------------"%(MachineNo))
		
		# 定义远程执行的命令(基本配置)
		Initial_CMD = [
					   'hostname %s'%(nhnls[c]),
					   'groupadd %s'%(nusg),
					   'useradd -g %s %s'%(nusg,nusn),
					   'echo %s | passwd %s --stdin'%(nupsw,nusn),
					   'mkdir %s'%(rmflc)
					  ]
		RMIP = rmipls[c]	
		remote_execute(Initial_CMD,RMIP)

#----------上传文件----------#

def Trans_File():	
	# 传输文件至远端
	c = 0

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
			
	for c in range(len(rmipls)):
		
		MachineNo = c + 1
			
		print("--------------------Machine%s Transporting--------------------"%MachineNo)
		
		RMIP = rmipls[c]	
		remote_put(lcp_put,rmp_put,RMIP)

#----------配置Yum本地源----------#

def Yum_Repo_Src():
	# 定义yum配置命令
	Yum_CMD = [
				 'mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.bak',
				 'cp %s /etc/yum.repos.d/CentOS-Base.repo'%(os.path.join(rmflc,Yumname)),
				 'mkdir %s'%(yumlc),
				 'mkdir /tmp/CentOS7;mount %s /tmp/CentOS7'%(os.path.join(rmflc,OSimagename)), #创建临时目录挂载镜像
				 'cp -r /tmp/CentOS7/* %s'%(yumlc),
				 'umount /tmp/CentOS7;rm -rf /tmp/CentOS7' #取消挂载并删除临时目录
			  ]

	c = 0
	for c in range(len(rmipls)):
		
		MachineNo = c + 1
		
		print("--------------------Machine%s Yum config--------------------"%(MachineNo))
		
		RMIP = rmipls[c]
		
		remote_execute(Yum_CMD,RMIP)

#----------安装python----------#

def Python_Install():
	# 定义python安装命令
	PySetup_CMD = [
				   'mkdir %s/Python3'%(rmflc),
				   'tar -zxvf %s -C %s/Python3'%(os.path.join(rmflc,Pyname),rmflc),
				   'yum install -y zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel libffi-devel gcc make',
				   'cd %s/Python3/Python-3.7.3 && ./configure --prefix=/usr/local/python3 && make && make install'%(rmflc), 
				   'mv /usr/bin/python /usr/bin/python.bak',
				   'ln /usr/local/python3/bin/python3.7 /usr/bin/python',
				   'ln -s /usr/local/python3/bin/pip3 /usr/bin/pip',
				   'cp /usr/bin/yum /usr/bin/yum.bak;sed -i '1c\#! /usr/bin/python2' /usr/bin/yum',
				   'cp /usr/libexec/urlgrabber-ext-down /usr/libexec/urlgrabber-ext-down.bak;sed -i '1c\#! /usr/bin/python2' /usr/libexec/urlgrabber-ext-down'
				  ]
	c = 0
	for c in range(len(rmipls)):
		
		MachineNo = c + 1
		
		print("--------------------Machine%s Python installation--------------------"%(MachineNo))
		
		RMIP = rmipls[c]
		
		remote_execute(PySetup_CMD,RMIP)

#----------程序主体----------#

Initial_Config()
Trans_File()
Yum_Repo_Src()
Python_Install()
print("--------------------Finished--------------------")


