#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Summarize version 1.0

Copyright (C) 2012 Petr Nohejl, petrnohejl.net

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

This program comes with ABSOLUTELY NO WARRANTY!
"""

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
