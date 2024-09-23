from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
from readability import Document
import traceback
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


driver = webdriver.Chrome()

def worker(thread_id, url_queue, visited_urls, lock):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Headless 모드
        chrome_options.add_argument("--disable-dev-shm-usage")  # 메모리 사용량 감소
        driver = webdriver.Chrome(options=chrome_options)
        
        
        while True:
            print(len(visited_urls))
            url = url_queue.get(block=True)
            driver.get(url)
            links = driver.find_elements(By.TAG_NAME, "a")
            
            for link in links:
                href = link.get_attribute("href")
                with lock:
                    if href:
                        if href not in visited_urls:
                            url_queue.put(href)
                            visited_urls.add(href)
            
        driver.quit()
    except:
        print(traceback.format_exc())
    