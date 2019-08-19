import datetime
import argparse
from argparse import RawTextHelpFormatter
from six.moves.configparser import RawConfigParser
import sys
import ccl_bplist
import plistlib
import io
import os
import glob
import datetime
import argparse
from time import process_time

start = process_time()

#load common notification parameters
with open('NotificationParams.txt', 'r') as f:
	notiparams = [line.strip() for line in f]

#calculate timestamps
unix = datetime.datetime(1970, 1, 1)  # UTC
cocoa = datetime.datetime(2001, 1, 1)  # UTC
delta = cocoa - unix 

pathfound = 0
count = 0
notdircount = 0
exportedbplistcount = 0

parser = argparse.ArgumentParser(description="\
	iOS Notifications Traige Parser\
	\n\n Process iOS notification files for triage."
, prog='iOSNotificationsParser.py'
, formatter_class=RawTextHelpFormatter)
parser.add_argument('data_dir_to_analyze',help="Path to Data Directory.")

args = parser.parse_args()
data_dir = args.data_dir_to_analyze


print("\n--------------------------------------------------------------------------------------")
print("iOS Notification Parser.")
print("Objective: Triage iOS notifications content.")
print("By: Alexis Brignoni | @AlexisBrignoni | abrignoni.com")
print("Data Directory: " + data_dir)
print("\n--------------------------------------------------------------------------------------")
print("")

for root, dirs, filenames in os.walk(data_dir):
		for f in dirs:
			if f == "UserNotifications":
				pathfound = os.path.join(root, f)

if pathfound == 0:
	print("No UserNotifications directory located")
else:
	folder = ("TriageReports_" + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')) #add the date thing from phill
	os.makedirs( folder )
	print("Processing:")
	for filename in glob.iglob(pathfound+'\**', recursive=True):
		if os.path.isfile(filename): # filter dirs
			file_name = os.path.splitext(os.path.basename(filename))[0]
			#create directory
			if 'DeliveredNotifications' in file_name:
				#create directory where script is running from
				print (filename) #full path
				notdircount = notdircount + 1				
				#print (os.path.basename(file_name)) #filename with  no extension
				openplist = (os.path.basename(os.path.normpath(filename))) #filename with extension
				#print (openplist)
				bundlepath = (os.path.basename(os.path.dirname(filename)))#previous directory
				appdirect = (folder + "\\"+ bundlepath) 
				#print(appdirect)
				os.makedirs( appdirect )
				
				#open the plist
				p = open(filename, 'rb')
				plist = ccl_bplist.load(p)
				plist2 = plist["$objects"]

				long = len(plist2)
				#print (long)
				h = open('./'+appdirect+'/DeliveredNotificationsReport.html', 'w') #write report
				h.write('<html><body>')
				h.write('<h2>iOS Delivered Notifications Triage Report </h2>')
				h.write ('<style> table, th, td {border: 1px solid black; border-collapse: collapse;}</style>')
				h.write('<br/>')
				
				h.write('<button onclick="hideRows()">Hide rows</button>')
				h.write('<button onclick="showRows()">Show rows</button>')
				
				with open("script.txt") as f:
					for line in f:
						h.write(line)
				
				h.write('<br>')
				h.write('<table name="hide">')
				h.write('<tr name="hide">')
				h.write('<th>Data type</th>')
				h.write('<th>Value</th>')
				h.write('</tr>')
								
				h.write('<tr name="hide">')
				h.write('<td>Plist</td>')
				h.write('<td>Initial Values</td>')
				h.write('</tr>')
				
				test = 0
				for i in range (0, long):
					try:
						if (plist2[i]['$classes']):
							h.write('<tr name="hide">')
							h.write('<td>$classes</td>')
							ob6 = str(plist2[i]['$classes'])
							h.write('<td>')
							h.write(str(ob6))
							h.write('</td>')
							h.write('</tr>')
							test = 1
					except:
						pass
					try:
						if (plist2[i]['$class']):
							h.write('<tr name="hide">')
							h.write('<td>$class</td>')
							ob5 = str(plist2[i]['$class'])
							h.write('<td>')
							h.write(str(ob5))
							h.write('</td>')
							h.write('</tr>')
							test = 1
					except:
						pass
					try:
						if (plist2[i]['NS.keys']):
							h.write('<tr name="hide">')
							h.write('<td>NS.keys</td>')
							ob0 = str(plist2[i]['NS.keys'])
							h.write('<td>')
							h.write(str(ob0))
							h.write('</td>')
							h.write('</tr>')
							test = 1
					except:
						pass
					try:
						if (plist2[i]['NS.objects']):
							ob1 = str(plist2[i]['NS.objects'])
							h.write('<tr name="hide">')
							h.write('<td>NS.objects</td>')
							h.write('<td>')
							h.write(str(ob1))
							h.write('</td>')
							h.write('</tr>')
							
							test = 1
					except:
						pass
					try:
						if (plist2[i]['NS.time']):
							dia = str(plist2[i]['NS.time'])
							dias = (dia.rsplit('.', 1)[0])
							timestamp = datetime.datetime.fromtimestamp(int(dias)) + delta
							#print (timestamp)
						
							h.write('<tr>')
							h.write('<td>Time UTC</td>')
							h.write('<td>')
							h.write(str(timestamp))
							#h.write(str(plist2[i]['NS.time']))
							h.write('</td>')
							h.write('</tr>')
							
							test = 1 
					except:
						pass
					try:
						if (plist2[i]['NS.base']):
							ob2 = str(plist2[i]['NS.objects'])
							h.write('<tr name="hide">')
							h.write('<td>NS.base</td>')
							h.write('<td>')
							h.write(str(ob2))
							h.write('</td>')
							h.write('</tr>')
							
							test = 1 
					except:
						pass
					try:
						if (plist2[i]['$classname']):
							ob3 = str(plist2[i]['$classname'])
							h.write('<tr name="hide">')
							h.write('<td>$classname</td>')
							h.write('<td>')
							h.write(str(ob3))
							h.write('</td>')
							h.write('</tr>')
							
							test = 1 
					except:
						pass
					try:
						if test == 0:
							if (plist2[i]) == "AppNotificationMessage":
								h.write('</table>')
								h.write('<br>')
								h.write('<table>')
								h.write('<tr>')
								h.write('<th>Data type</th>')
								h.write('<th>Value</th>')
								h.write('</tr>')
							
								h.write('<tr name="hide">')
								h.write('<td>ASCII</td>')
								h.write('<td>'+str(plist2[i])+'</td>')
								h.write('</tr>')
								
								
							else:
								if plist2[i] in notiparams:
									h.write('<tr name="hide">')
									h.write('<td>ASCII</td>')
									h.write('<td>'+str(plist2[i])+'</td>')
									h.write('</tr>')
								elif plist2[i] == " ":
									h.write('<tr name="hide">')
									h.write('<td>Null</td>')
									h.write('<td>'+str(plist2[i])+'</td>')
									h.write('</tr>')
								else:
									h.write('<tr>')
									h.write('<td>ASCII</td>')
									h.write('<td>'+str(plist2[i])+'</td>')
									h.write('</tr>')
							
					except:
						pass
						
					test = 0
								
					
					#h.write('test')
				
				
				for dict in plist2:
					liste = dict
					types = (type(liste))
					#print (types)
					try:
						for k, v in liste.items():
							if k == 'NS.data':
								chk = str(v)
								reduced = (chk[2:8])
								#print (reduced)
								if reduced == "bplist":
									count = count + 1
									binfile = open('./'+appdirect+'/incepted'+str(count)+'.bplist', 'wb')
									binfile.write(v)
									binfile.close()

									procfile = open('./'+appdirect+'/incepted'+str(count)+'.bplist', 'rb')
									secondplist = ccl_bplist.load(procfile)
									secondplistint = secondplist["$objects"]
									print('Bplist processed and exported.')
									exportedbplistcount = exportedbplistcount + 1
									h.write('<tr name="hide">')
									h.write('<td>NS.data</td>')
									h.write('<td>')
									h.write(str(secondplistint))
									h.write('</td>')
									h.write('</tr>')
									
									procfile.close()
									count = 0
								else:
									h.write('<tr name="hide">')
									h.write('<td>NS.data</td>')
									h.write('<td>')
									h.write(str(secondplistint))
									h.write('</td>')
									h.write('</tr>')
					except:
						pass
				h.close()
			elif 'AttachmentsList' in file_name:
				test = 0 #future development
end = process_time()
time = start - end
print(" ")
print("Process completed.")
print("Processing time: " + str(abs(time)) )

print("Total notification directories processed:"+str(notdircount))
print("Total exported bplists from notifications:"+str(exportedbplistcount))			
		