#!/usr/bin/python
# -*- coding: utf-8 -*-


import string
import re
import glob
import os
import sys


# CONFIG
OUTPUT = "summarize.txt"


# SUMMARIZE FILES
class Summarize():
	def __init__(self):
		self.summarize()


	def summarize(self):
		os.chdir("./")
		output = open(OUTPUT,"w")
		for file in glob.glob("*.html"):
			result = self.parse_file(file)
			output.write(result)
			sys.stdout.write(result)
		output.close
			
			
	def parse_file(self, file_name):
		file = open(file_name,"r")
		lines = file.readlines()
		file.close
		
		content = string.join(lines)
		parsed = string.join(re.compile("<span>[0-9 ]+<\/span>", re.DOTALL).findall(content))
		parsed = string.replace(parsed," ","")
		values = re.compile("\d+", re.DOTALL).findall(parsed)

		return self.create_line(file_name, values)
		
		
	def create_line(self, file_name, values):
		result = file_name[8:10] + "." + file_name[5:7] + "." + file_name[0:4] + " " + file_name[11:13] + ":" + file_name[14:16] + "\t" + values[0] + "\t" + values[1] + "\t" + values[2] + "\t" + values[3] + "\t" + values[4] + "\n"
		return result
		
					
# MAIN
if (__name__=="__main__"): 
	Summarize()
