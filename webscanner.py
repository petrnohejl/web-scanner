#!/usr/bin/python
# -*- coding: utf-8 -*-


import time
import re
import urllib2
import socket
import random


# CONFIG
URL = "https://play.google.com/store/apps/details?id=net.jestrab.slevolapka" # web page URL
SLEEP_TIME = 7200 # in seconds
SLEEP_TIME_SALT = 1800 # maximum of random value added to SLEEP_TIME


# SUPPORT CLASSES AND METHODS
def load_content_from_url(source_url, timeout=20, **kwargs):
	"""
	Loads content from url address

	@param source_url: source URL from which to download a content
	@param timeout: time in seconds until connection is consider dead
	"""
	
	# set random browser agents
	agents = [ 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
				'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/125.2 (KHTML, like Gecko) Safari/125.8',
				'Opera/9.80 (Windows NT 6.1; U; es-ES) Presto/2.9.181 Version/12.00',
				'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6']

	# set default timeout for request
	socket.setdefaulttimeout(timeout)

	# make request with random agent (ban protection)
	request = urllib2.Request(source_url)
	request.add_header('User-Agent', random.choice(agents))

	# open file, read its content and store it
	opener = urllib2.build_opener()

	return opener.open(request).read()


# SCANNER
class WebScanner():
	def __init__(self):
		self.loop()


	def loop(self):
		while(1):
			try:
				# get web content
				content = load_content_from_url(URL, timeout=60)
				
				# parse content
				parsed = re.compile("<div class=.histogram-table.+?<\/div>", re.DOTALL).findall(content)
				
				# file output
				if(len(parsed)>0):
					filename = time.strftime("%Y_%m_%d_%H_%M", time.localtime()) + ".html"
					file = open(filename, "w")
					file.write("<html><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" /></head><body>\n")
					file.write(parsed[0] + "\n")
					file.write("</body></html>\n")
					file.close()
			
			except:
				print "Error!"
	
			# sleep
			time.sleep(SLEEP_TIME + random.randint(0, SLEEP_TIME_SALT))
		
			
# MAIN
if (__name__=="__main__"): 
	WebScanner()
