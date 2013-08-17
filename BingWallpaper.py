# Author: Chenbo Li, http://www.binarythink.net
# Description: The code is to download the background images of bing.com of last 10 days as wallpaper for windows 7. 
# It automatically renew the entire pictures directory with exactly 10 pictures up-to-date.
# Configs are written in config.dat which shares the same directory with BingWallpaper.py or BingWallpaper.exe.
import xml.etree.ElementTree as ET
import urllib2
import os
import errno
import sys
import Tkinter

top = Tkinter.Tk()
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
print 'Your current image library is at '+ dest+'. Please run this program with parameter `-clear` to reset the location'
local.close()

filelist = os.listdir(dest)
currentlist = []

# get the last 10 xml files.
for i in range(10):
	tree = ET.parse(urllib2.urlopen('http://www.bing.com/HPImageArchive.aspx?format=xml&idx='+str(i)+'&n=1&mkt=en-US'))
	root = tree.getroot()
	# add user_agent in case the Bing site detects the robot.
	user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.160 Safari/537.22'
	try:
			dlink = str('http://www.bing.com'+root.find('image').find('url').text)
	except urllib2.URLError as exception:
			print 'cannot find xml file, check your internet connection'
	dname = str(root.find('image').find('startdate').text+'.jpg')
	currentlist.append(dname)
	if dname in filelist:
			print dname + ' already in directory.'
	else:
			print ('Downloading ' + dname + ' to ' + dest)
			pic = urllib2.urlopen(urllib2.Request(dlink.replace(" ","%20"),None,{'User-Agent' : user_agent}))
			try:
					output = open(dest+dname,'wb+')
			except urllib2.URLError as exception:
					print 'cannot find jpg file, check your internet connection'
			output.write(pic.read())
			output.close()

for imgfile in filelist:
		if imgfile not in currentlist:
				os.remove(dest+imgfile)
print 'update successfully.'
def main():
		checkPath()
		path = getPath()
		downloadFiles()

if __name__ == '__main__':
		main()
