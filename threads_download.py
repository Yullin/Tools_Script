#!/usr/bin/env python3

import requests
import csv, sys, os
import threading
import time, queue

def download_worker(thread_num):
    while True:
        url = q.get()
        if url is None:
            print("Thread %s has no task, have a break" %thread_num)
            break
        # do_work(url) Doing Job
        time.sleep(0.5)
        uri = url.split('?')[0]
        file_name_to_save = uri.split('/')[-1]
        r = requests.get(url)
        print("Thread %s is doing Job %s" %(thread_num, url))
        with open(file_name_to_save, 'wb') as f:
            f.write(r.content)
            print("save to: {}".format(file_name_to_save))
        q.task_done()

if __name__ == "__main__":
    num_of_threads = 10
    file_path = sys.argv[1]
    # Create FIFO queue
    q = queue.Queue()
    # Create a thread pool
    threads = []
    if not os.path.exists(file_path):
        print("file not found!")
    else:
        # Create specific number threads, and put them in pool `threads`
        for i in range(1, num_of_threads+1):
            t = threading.Thread(target=download_worker, args=(i,))
            threads.append(t)
            t.start()

        file_cont = open(file_path, 'r')
        csv_cont = csv.reader(file_cont)
        # print(csv_cont)
        # put task in queue
        for line in csv_cont:
            l = line[0]
            q.put(l)
        # hold the queue until all task been finished
        q.join()
        # stop working thread
        for i in range(num_of_threads):
            q.put(None)
        for t in threads:
            t.join()
        print(threads)
