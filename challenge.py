# -*- coding: utf-8 -*-
#from urllib.request import urlopen,sys,re,Request
from urllib.request import urlopen,sys,re,Request
import csv

domain = "www.epocacosmeticos.com.br"
dictionary = {}
stack=[]

def safeprint(msg):
	print(msg.encode(sys.getdefaultencoding(), 'replace'))

def urlInDomain(url):
	p = re.search(domain, url)
	return p != None

def isAProductPage(url):
	p = re.search("/p$", url)
	return p != None

def findTitle(content):
	p = re.search("<title>(.*)</title>",content)
	return p.group(1)

def findProductName(content):
	p = re.search("fn productName[^>]*\">([^<]*)</div>",content)
	return p.group(1)
	
def urlStartsWithSlash(url):
	p = re.search("^/", url)
	return p != None

def addUrl(url):
	stack.append(url)
	dictionary[url]=0

def urlWasVisited(url):
	return url in dictionary and dictionary[url] == 1
	
def visitPage(url):
	print("Has got " + url)
	
	writer = csv.writer(open("urls.csv", "w"))
	
	#Mark as visited
	dictionary[url] = 1
	
	#Get page content
	req = Request(
		url,
		headers={'User-Agent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"}) 
	try :
		html = urlopen( req ).read().decode('utf-8')
	except Exception  :
		print("Erro em: "+url)
		return
	
	#Get links
	p = re.compile('href="([^"]*)"')

	productsOnPage=[]
	
	iterator = p.finditer(html)
	for match in iterator:
		newUrl = match.group(1)
		
		if isAProductPage(newUrl) :
			productsOnPage.append(newUrl)
		
		if urlStartsWithSlash(newUrl) and not urlWasVisited("http://"+domain+newUrl):
			addUrl("http://"+domain+newUrl)
		elif (urlWasVisited(newUrl) or not urlInDomain(newUrl)) :
			pass
		else :
			addUrl(newUrl)
	
	if isAProductPage(url) :
		title=findTitle(html)
		productName=findProductName(html)
		test=[title, productName,'|'.join(productsOnPage)]
		writer.writerow(test)

visitPage("http://"+domain)

while (len(stack) > 0):
	actualUrl = stack.pop()
	print("Analyze: "+actualUrl)
	if not urlWasVisited(actualUrl) :
		visitPage(actualUrl)	
   