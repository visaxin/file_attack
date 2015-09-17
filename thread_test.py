import threading
import thread
import time
conn = threading.Condition()
def t1():
    global conn
    if onn.acquire():
        while 1:

            print "this is t1 thread"
            conn.wait(2)
            conn.notify()
            conn.release()


def t2():
    global conn
    conn.acquire()
    while 1:
        print "this is t2 thread"
        conn.wait(2)
        conn.notify()
        conn.release()
if __name__ == '__main__':
    t1 = threading.Thread(target=t1())
    t2 = threading.Thread(target=t2())

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    # thread.start_new_thread(t1,())
    # time.sleep(2)
    # thread.start_new_thread(t2,())
    # time.sleep(2)
    #
    #
