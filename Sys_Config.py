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

#----------创建日志文件----------#

def log_creation():
	print(
