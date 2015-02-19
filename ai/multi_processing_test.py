from multiprocessing import Pool, Manager, Queue, Process


def atomic_worker(work_queue, done_queue):
    x = work_queue.get()

    done_queue.put(x**2)
    done_queue.put(x**3)
    print(done_queue.qsize())
    if x<100:
        work_queue.put(x**2)
        work_queue.put(x**3)




def main():
    work_queue = Queue()
    done_queue = Queue()
    processes = []

    for x in [2,4,5,6,]:
        work_queue.put(x)

    for w in range(2):
        p = Process(target=atomic_worker, args=(work_queue, done_queue))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()


    #done_queue.put('STOP')
    #for status in iter(done_queue.get, 'STOP'):
    #    print status


if __name__ == '__main__':
    main()

#def test_multiprocessing(self):
#    manager = Manager()
#    process = manager.list([1])
#    comleted = manager.list([])
#
#
#    results = []
#
#
#    pool = Pool(processes=4)              # start 4 worker processes
#    while process:
#        x = process.pop()
#        results.append(x)
#        if x<100:
#            result = pool.apply_async(f, [x])    # evaluate "f(10)" asynchronously
#            print result.get()
#            process.append(result.get(timeout=1))
#
#    print results