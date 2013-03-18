import xml.etree.ElementTree as ET
import urllib2
import os
import errno


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
tree = ET.parse(urllib2.urlopen('http://themeserver.microsoft.com/default.aspx?p=Bing&c=Desktop&m=en-US'))
root = tree.getroot()
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.160 Safari/537.22'
for item in root.iter('item'):
		dlink = str(item.find('link').get('ref'))
		dname = str(item.find('title').text)
		print ('Downloading ' + dlink + ' to ' + dest)
		pic = urllib2.urlopen(urllib2.Request(dlink.replace(" ","%20"),None,{'User-Agent' : user_agent}))
		output = open(dest+dname+'.jpg','wb+')
		output.write(pic.read())
		output.close()
