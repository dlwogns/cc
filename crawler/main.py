import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from worker import worker
import url_allowed_checker as ac
import threading
import traceback

url_queue = Queue()
visited_urls = set()
lock = threading.Lock()
allowed_domain = ["https://edition.cnn.com"]
disallowed_list = []
max_workers = 4

if __name__ == "__main__":
    disallowed_list = ac.get_disallowed_list(domain_list = allowed_domain)
    #url = "https://edition.cnn.com/"  
    # 이 부분도 나중에 domain 기준으로 탐색할 수 있도록 바꿔야됨.
    url = "https://edition.cnn.com/2024/09/22/politics/mark-robinson-campaign-resignations/index.html"
    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for i in range(max_workers):
                executor.submit(worker, i, url_queue, visited_urls, lock)            # set default url
            url_queue.put(url)
    except:
        print(traceback.format_exc())
        
        
        
    
