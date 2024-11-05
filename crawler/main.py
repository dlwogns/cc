import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
from worker import worker
import utils.url_allowed_checker as ac
import threading
import traceback
from multiprocessing import Lock, Queue, Manager, Process, Event
from url_checker import check_url

allowed_domain = ["https://edition.cnn.com"]
disallowed_list = []
max_workers = 1
zmq_bind_list = [f"{5555+i}" for i in range(max_workers)]


if __name__ == "__main__":
    manager = Manager()
    
    visited_urls = manager.dict()
    url_queue = manager.Queue()
    lock = manager.Lock()
    ready_event = manager.Event()
    
    disallowed_list = ac.get_disallowed_list(domain_list = allowed_domain)
    url = "https://edition.cnn.com"
    
    try:
        p = Process(target=check_url, args=(visited_urls, url_queue, disallowed_list, allowed_domain, lock, ready_event))
        p.start()
        
        # send Initial URL to check_url
        url_queue.put(url)
        
        # Worker Process 
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            for i in range(max_workers):
                executor.submit(worker, i, url_queue, visited_urls, lock, disallowed_list, zmq_bind_list[i], ready_event)
                
    except:
        print(traceback.format_exc())
        
        
        
    
