#!/usr/bin/python
# -*- coding: utf-8 -*-

# uses: https://2.python-requests.org/en/master/
# requires: pip install requests

import os
import re
import requests
import string
import sys
import time
import Tkinter
import webbrowser


APP_PADDING = 10
APP_FONT_DEFAULT = "Arial 11"
APP_FONT_TEXT = ("Courier", 9)
APP_FONT_STATUS = ("Arial", 9)
APP_STRING_TITLE = "SeekingA"
APP_STRING_LABEL = "Enter SeekingA URLs and ticker:"
APP_STRING_DOWNLOAD = "Download articles"
APP_STRING_OPEN = "Open articles"
APP_STRING_OPEN_ONE = "Open 1 article"
APP_STRING_OPEN_MANY = "Open {} articles"
APP_STRING_STATUS = "Entries: {}   Downloaded: {}   Failed: {}   Invalid URLs: {}"
APP_STRING_HINT = "Enter URLs and separate them by a space or a line break. Ticker is optional and is used in HTML file name."

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"


class App():
	def __init__(self):
		self.__set_root()
		self.__set_ui()
		self.sa = SeekingA()
		

	def run(self):
		self.root.mainloop()


	def __set_root(self):
		self.root = Tkinter.Tk()
		self.root.title(APP_STRING_TITLE)
		self.root.minsize(640, 480)
		self.root.option_add("*Font", APP_FONT_DEFAULT)


	def __set_ui(self):
		# frames
		self.main_frame = Tkinter.Frame(self.root)
		self.main_frame.pack(fill=Tkinter.BOTH, expand=1, padx=APP_PADDING, pady=APP_PADDING)

		self.top_frame = Tkinter.Frame(self.main_frame)
		self.top_frame.pack(fill=Tkinter.X, pady=(0, APP_PADDING))

		self.text_frame = Tkinter.Frame(self.main_frame)
		self.text_frame.pack(fill=Tkinter.BOTH, expand=1)

		self.label_frame = Tkinter.Frame(self.top_frame)
		self.label_frame.pack(fill=Tkinter.X, expand=1, side=Tkinter.LEFT)

		self.ticker_frame = Tkinter.Frame(self.root)
		self.ticker_frame.pack(fill=Tkinter.X, padx=APP_PADDING, pady=(0, APP_PADDING))

		self.status_frame = Tkinter.Frame(self.root, relief="groove", borderwidth=1)
		self.status_frame.pack(fill=Tkinter.X)

		# buttons
		self.label = Tkinter.Label(self.label_frame, text=APP_STRING_LABEL)
		self.label.pack(side=Tkinter.LEFT)

		self.download_button = Tkinter.Button(self.top_frame, text=APP_STRING_DOWNLOAD, width=16, height=1, command=self.__download)
		self.download_button.pack(side=Tkinter.LEFT, padx=APP_PADDING)

		self.open_button = Tkinter.Button(self.top_frame, text=APP_STRING_OPEN, width=16, height=1, state=Tkinter.DISABLED, command=self.__open)
		self.open_button.pack(side=Tkinter.LEFT)

		# text
		self.scrollbar = Tkinter.Scrollbar(self.text_frame)
		self.scrollbar.pack(fill=Tkinter.Y, side=Tkinter.RIGHT)

		self.text = Tkinter.Text(self.text_frame, yscrollcommand=self.scrollbar.set)
		self.text.config(font=APP_FONT_TEXT, undo=True, wrap="word")
		self.text.focus_set()
		self.text.pack(fill=Tkinter.BOTH, expand=1)

		self.scrollbar.config(command=self.text.yview)

		# ticker
		self.ticker = Tkinter.Entry(self.ticker_frame, font=APP_FONT_TEXT)
		self.ticker.pack(fill=Tkinter.X)
		
		# status
		self.status = Tkinter.Label(self.status_frame, text=APP_STRING_HINT, fg="#606060", font=APP_FONT_STATUS)
		self.status.pack(side=Tkinter.LEFT, fill=Tkinter.X)


	def __download(self):
		text = self.text.get("1.0", Tkinter.END)
		urls = text.split()
		ticker = self.ticker.get().strip()

		if(len(urls)>0):
			success_counter = 0
			fail_counter = 0
			invalid_url_counter = 0
			self.files = []

			# urls
			for i in range(len(urls)):
				url = urls[i]

				if(self.sa.validate_url(url)==False):
					invalid_url_counter += 1
					continue

				filename = self.sa.process_article_from_url(url, ticker)

				if(filename!=None):
					print "Downloaded: " + filename
					self.files.append(filename)
					success_counter += 1
				else:
					fail_counter += 1
			
			# status bar
			status = APP_STRING_STATUS.format(len(urls), success_counter, fail_counter, invalid_url_counter)
			self.status["text"] = status

			# text
			if(len(urls)==success_counter):
				self.text.delete("1.0", Tkinter.END)

			# open button
			if(len(self.files)>0):
				if(len(self.files)==1):
					open_button_text = APP_STRING_OPEN_ONE
				else:
					open_button_text = APP_STRING_OPEN_MANY.format(len(self.files))
				self.open_button["text"] = open_button_text
				self.open_button["state"] = Tkinter.NORMAL
			else:
				self.open_button["text"] = APP_STRING_OPEN
				self.open_button["state"] = Tkinter.DISABLED

		else:
			self.status["text"] = APP_STRING_HINT


	def __open(self):
		dir_path = os.path.dirname(os.path.realpath(__file__))

		for i in range(len(self.files)):
			path = os.path.join(dir_path, self.files[i])
			print "Opened: " + path
			webbrowser.open(path, new=2)


class SeekingA():
	def __init__(self):
		self.cookie_jar = None
		self.session = requests.session()


	def validate_url(self, url):
		regex = re.compile(
			r'^(?:http|ftp)s?://' # http:// or https://
			r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
			r'localhost|' #localhost...
			r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
			r'(?::\d+)?' # optional port
			r'(?:/?|[/?]\S+)$', re.IGNORECASE)
		return re.match(regex, url) is not None


	def process_directory(self, directory):
		try:
			files = os.listdir(directory)
			for file in files:
				filename = os.path.join(directory, file)
				self.process_article_from_file(filename, directory)
		except:
			print "Error: processing directory failed"


	def process_article_from_file(self, filename, ticker=None):
		# get file content
		content = self.__load_content_from_file(filename)
		
		# get url
		url = re.compile(self.__transform_sa(r"\<link href=\"https:\/\/seekingA.com.+?rel=\"amphtml\""), re.MULTILINE|re.DOTALL).findall(content)
		url = url[0][12:-15]

		return self.__process_article(content, url, ticker)


	def process_article_from_url(self, url, ticker=None):
		# get web content
		content = self.__load_content_from_url(url)
		return self.__process_article(content, url, ticker)


	def __process_article(self, content, url, ticker=None):
		# parse content
		article = re.compile(r"\<article\>.+?\<\/article\>", re.MULTILINE|re.DOTALL).findall(content)
		title = re.compile(r"\<title\>.+?\<\/title\>", re.MULTILINE|re.DOTALL).findall(content)
		style = re.compile(r"\<style.type.+?\<\/style\>", re.MULTILINE|re.DOTALL).findall(content)
		date = re.compile(r"\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ", re.MULTILINE|re.DOTALL).findall(content)

		# fix links
		if(len(article)>0):
			article[0] = article[0].replace(r"<a href='/", self.__transform_sa("<a href='https://seekingA.com/"))
			article[0] = article[0].replace(r'<a href="/', self.__transform_sa('<a href="https://seekingA.com/'))
		
		# file output
		if(len(article)>0):
			if(ticker==None or ticker==""):
				ticker = self.__get_ticker(title[0])
			filename = self.__get_filename(url, ticker, date[0])
			self.__create_html_file(filename, article[0], title[0], style[0])
			return filename
		else:
			print "Error: processing file failed"
			return None


	def __load_content_from_file(self, filename):
		content = ""
		with open(filename, "r") as file:
			content = file.read()
			print "Read " + filename
			file.close
		return content.decode('utf-8')


	def __load_content_from_url(self, url):
		headers = {"User-Agent": USER_AGENT, "cache-control": "no-cache", "Accept": "*/*", "accept-encoding": "gzip, deflate"}
		call = self.session.get(url, headers=headers, cookies=self.cookie_jar, allow_redirects=True)
		#call = self.session.get(url, headers=headers, cookies=self.cookie_jar, proxies={"http": "http://95.88.12.230:3128"}) # https://free-proxy-list.net/
		print str(call.status_code) + " " + call.reason + ": " + call.url
		#self.__print_call(call)
		
		# set cookies
		if("set-cookie" in call.headers):
			print "Cookie: " + call.cookies["machine_cookie"]
			self.cookie_jar = requests.cookies.RequestsCookieJar()
			self.cookie_jar.set("machine_cookie", call.cookies["machine_cookie"], domain=self.__transform_sa("seekingA.com"), path="/")

		result = call.text
		call.close()
		time.sleep(1)
		return result
	

	def __print_call(self, call):
		print "------------------------------------------"
		print call.request.headers
		print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
		print call.headers
		print "------------------------------------------"


	def __get_filename(self, url, ticker, date):
		url_index = string.rfind(url, "/") + 1			
		return ticker + "_" + date[:10] + "_" + url[url_index:] + ".html"


	def __get_ticker(self, title):
		ticker = re.compile(r"\(.+?\)", re.MULTILINE|re.DOTALL).findall(title)
		ticker_index = string.rfind(ticker[0], ":") + 1
		return ticker[0][ticker_index:-1]


	def __create_html_file(self, filename, content, title, style):
		file = open(filename, "w")
		file.write("<html><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />\n")
		file.write(title.encode('utf-8') + "\n")
		file.write("<style type='text/css' media='all'>body{padding:20px 0 20px 0 !important} article{width:640px;margin:auto;} #author-hd .info div.actions{width:550px}</style>\n")
		file.write(style.encode('utf-8') + "\n")
		file.write("</head><body>\n")
		file.write(content.encode('utf-8') + "\n")
		file.write("</body></html>\n")
		file.close()


	def __transform_sa(self, text):
		return text.replace("A.com", "alpha.com")

			
if (__name__=="__main__"):
	if(len(sys.argv)==1):
		App().run()
	elif(len(sys.argv)==2):
		arg = sys.argv[1]
		sa = SeekingA()
		if(sa.validate_url(arg)==True):
			sa.process_article_from_url(arg)
		else:
			sa.process_directory(arg)
	else:
		print "Error: invalid arguments"
