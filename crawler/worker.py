from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import zmq

import traceback

# selenium chrome driver
driver = webdriver.Chrome()


context2 = zmq.Context()
socket2 = context2.socket(zmq.PULL)
socket2.connect("tcp://127.0.0.1:5555")

def worker(thread_id, url_queue, visited_urls, lock, disallowed_list, zmq_port):
    print("worker start")
    # zmq context
    context = zmq.Context()
    # if preprocessor modified, pub-sub have to be considered
    socket = context.socket(zmq.PUSH)
    socket.bind(f"tcp://127.0.0.1:{zmq_port}")
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Headless 모드
        chrome_options.add_argument("--disable-dev-shm-usage")  # 메모리 사용량 감소
        driver = webdriver.Chrome(options=chrome_options)
        
        
        while True:
            print(len(visited_urls))
            url = socket2.recv_string()
            driver.get(url)
            
            # get all url from <a> 
            links = driver.find_elements(By.TAG_NAME, "a")
            
            for link in links:
                href = link.get_attribute("href")
                with lock:
                    if href:
                        if href not in visited_urls:
                            url_queue.put(href)
                            visited_urls[href] = 1
            
            # html preprocessing for define whether page contains article info
            html_content = driver.page_source
            print("zmq push")
            html_json = {"html_content":html_content, "url":url}
            #socket.send_string(html_content)
            socket.send_json(html_json)
            
        driver.quit()
    except:
        print(traceback.format_exc())
    