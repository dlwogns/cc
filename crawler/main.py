import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
from worker import worker
import utils.url_allowed_checker as ac
import threading
import traceback
from multiprocessing import Lock, Queue, Manager, Process
from url_checker import check_url

allowed_domain = ["https://edition.cnn.com"]
disallowed_list = []
max_workers = 4

if __name__ == "__main__":
    manager = Manager()
    
    visited_urls = manager.dict()
    url_queue = manager.Queue()    
    lock = manager.Lock()
    zmq_bind_list = ["5556", "5557", "5558", "5559"]
    
    disallowed_list = ac.get_disallowed_list(domain_list = allowed_domain)
    #url = "https://edition.cnn.com/"  
    # 이 부분도 나중에 domain 기준으로 탐색할 수 있도록 바꿔야됨.
    url = "https://edition.cnn.com/2024/09/22/politics/mark-robinson-campaign-resignations/index.html"
    try:
        p = Process(target=check_url, args=(visited_urls, url_queue, disallowed_list, allowed_domain, lock))
        p.start()
        print("pstart")
        
        print("put url in queue")
        url_queue.put(url)
        
        # Worker Process 
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            for i in range(max_workers):
                executor.submit(worker, i, url_queue, visited_urls, lock, disallowed_list, zmq_bind_list[i])            # set default url
                
    except:
        print(traceback.format_exc())
        
        
        
    
