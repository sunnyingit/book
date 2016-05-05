from time import sleep, ctime
import thread

def loop0():
    print 'start loop 0 at', ctime()
    sleep(4)
    print 'end loop 0 at', ctime()

def loop1():
    print 'start loop 1  at', ctime()
    sleep(2)
    print 'end loop 1 at', ctime()

def main():
    print 'starting at', ctime()
    thread.start_new_thread(loop0, ())
    thread.start_new_thread(loop1, ())
    print 'all Done at', ctime()


if __name__ == '__main__':
    main()
    while True:
        sleep(1)
        print "Main thread not exit"
