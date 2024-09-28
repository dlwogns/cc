import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from worker import worker
import threading
import traceback

url_queue = Queue()
visited_urls = set()
lock = threading.Lock()
max_workers = 4

if __name__ == "__main__":
    #url = "https://edition.cnn.com/"  
    url = "https://edition.cnn.com/2024/09/22/politics/mark-robinson-campaign-resignations/index.html"
    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for i in range(max_workers):
                executor.submit(worker, i, url_queue, visited_urls, lock)            # set default url
            url_queue.put(url)
    except:
        print(traceback.format_exc())
        
        
        
    
