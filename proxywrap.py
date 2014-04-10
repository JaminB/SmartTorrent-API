#!/usr/bin/python
import sys
import os
import subprocess
class Proxy:
	def __init__(self):
		print ""
	def run(self,arguments):
		f = open("logs.txt","w")
		f.write("proxychains " + arguments)
		f.close()
		proc = subprocess.Popen("proxychains "  +'"'+ arguments+'"', shell=True)
		output = proc.stdout
		print output
