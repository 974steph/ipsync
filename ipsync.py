# ipsync.py
# Author: Andy Culler
# Date: 7/23/14
# 
# Silly little utility that will reach out to my VPS and update a file with my current home
# IP address at a given interval.

from __future__ import print_function
import paramiko
import urllib
import re
import sys

# Set up global variables
SERVER = "" # Server to connect to
USER = ""   # User to connect as

# Function to pull the actual IP
def get_ip():
	url = "http://checkip.dyndns.org"
	
	request = urllib.urlopen(url).read()
	ip = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}", request)
	return ip[0]

# Function to write to stderr
def warn(msg):
	print("WARNING: " + msg, file=sys.stderr)

#
# Main code body
#

ip = get_ip()
if ip == None:
	warn("Unable to find IP. Exiting.");
	sys.exit(-1)

else:
	print("Found IP: " + ip)

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
try:
	ssh.connect(SERVER,username=USER)
except Exception as e:
	warn("Unable to connect to server. Exiting.")
	warn("Exception: " + str(e))
	sys.exit(-1)

stdin,stdout,stderr = ssh.exec_command('echo "' + ip + '" > ~/.ipinfo')

ret = stdout.readlines()
if len(ret) != 0:
	output = "\n".join(ret)
	warn("Unable to write IP to file. Output:")
	warn(output)
	sys.exit(-1)
else:
	print("IP updated successfully")
