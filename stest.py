from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
from readability import Document

# ChromeDriver 경로를 설정
chrome_driver_path = "/path/to/chromedriver"  # 자신의 chromedriver 경로로 변경

# WebDriver 설정 및 브라우저 열기
driver = webdriver.Chrome()

# 특정 웹 페이지로 이동
url = "https://edition.cnn.com/"  # 링크를 추출할 페이지 URL로 변경
driver.get(url)

def extract_article_using_readability(url):
    response = requests.get(url)
    doc = Document(response.text)
    
    # 기사 제목과 본문 추출
    title = doc.short_title()
    article_content = doc.summary()

    # BeautifulSoup으로 HTML에서 텍스트만 추출
    soup = BeautifulSoup(article_content, "html.parser")
    paragraphs = soup.find_all('p')
    content = ' '.join([p.get_text() for p in paragraphs])
    
    return title, content

article_url = "https://edition.cnn.com/2024/09/20/middleeast/israel-hamas-eden-yerushalmi-sisters-interview-intl/index.html"

try:
    # 페이지의 모든 링크(a 태그의 href 속성) 추출
    links = driver.find_elements(By.TAG_NAME, "a")
    print("start")
    print(links)
    # 링크를 출력
    herf_list = []
    for link in links:
        href = link.get_attribute("href")
        if href:
            herf_list.append(href)
    print(herf_list)
    title, content = extract_article_using_readability(article_url)
    print(title)
    print(content)
            

    # 브라우저 닫기
    driver.quit()
except:
    driver.quit()