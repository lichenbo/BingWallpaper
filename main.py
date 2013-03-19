import xml.etree.ElementTree as ET
import urllib2
import os
import errno
import sys

if len(sys.argv) > 1 and sys.argv[1] == '-clear':
	try:
		os.remove('config.dat')
	except OSError as exception:
		print "config file removed." 
try:	
	local = open('config.dat','r+')
except IOError as exception:
	local = open('config.dat','w+')

dest = local.read()
if dest=="":
		dest = raw_input("Please enter the directory:")
		try:
				os.makedirs(dest)
		except OSError as exception:
				if exception.errno != errno.EEXIST:
						print "Error during creating directory"

		if dest[-1] != '/' and dest[-1] != '\\':
				dest+='/'
		local.write(dest)
local.close()

for i in range(10):
	tree = ET.parse(urllib2.urlopen('http://www.bing.com/HPImageArchive.aspx?format=xml&idx='+str(i)+'&n=1&mkt=en-US'))
	root = tree.getroot()
	user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.160 Safari/537.22'
	dlink = str('http://www.bing.com'+root.find('image').find('url').text)
	dname = str(root.find('image').find('startdate').text)
	print ('Downloading ' + dname + ' to ' + dest)
	pic = urllib2.urlopen(urllib2.Request(dlink.replace(" ","%20"),None,{'User-Agent' : user_agent}))
	output = open(dest+dname+'.jpg','wb+')
	output.write(pic.read())
	output.close()
