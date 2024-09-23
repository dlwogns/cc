import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from get_res import worker
import threading
import traceback

url_queue = Queue()
checkqueue = Queue()
visited_urls = set()
lock = threading.Lock()
max_workers = 2

if __name__ == "__main__":
    url = "https://edition.cnn.com/"  
    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for i in range(max_workers):
                executor.submit(worker, i, url_queue, visited_urls, lock)            # set default url
            url_queue.put(url)
            checkqueue.put(url) 
    except:
        print(traceback.format_exc())
        
        
        
    
