#!/usr/bin/python
import json
from settings import config
ipList= []
ipLoc = 0
def set_ip_list():
	global ipList
	ips = open(config.variables.get("ip_list"), "r")
	for ip in ips:
		ipList.append(ip.strip())

def _get_ip_list():
	global ipList
	return ipList

def get_next_ip():
	global ipsList
	try:
		tmpFile = open(config.variables.get("utility_data") + "tmp","r")
		ipLoc = int(tmpFile.readline())
		tmpFile.close()
	except (IOError,ValueError):
		tmpFile = open(config.variables.get("utility_data") + "tmp","w")
		tmpFile.write("0")
		ipLoc = 0
		tmpFile.close()
		return	
	tmpFile = open(config.variables.get("utility_data") + "tmp","w")
	ipLoc += 1
	if int(ipLoc) > len(ipList) - 1:
		ipLoc = 0
	tmpFile.write(str(ipLoc))	
	tmpFile.close()
	return ipList[ipLoc]

def get_next_ip_json():
		return json.dumps({"current_ip": get_next_ip()},sort_keys=True, indent=4)
