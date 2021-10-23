from multiprocessing import Process
import time

def fun(process_id, delay):
    print('starting fun' + str(process_id))
    time.sleep(delay)
    print('ending fun' + str(process_id))

if __name__ == '__main__':
    p1 = Process(target=fun, args=('1', 2))
    p2 = Process(target=fun, args=('2', 10))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print('ending main')