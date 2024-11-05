from readability import Document
from bs4 import BeautifulSoup
import zmq
import os
import json
import re
import traceback

def save_data_to_json(title, contents, url, label, filename):
    new_data = {
        "title": title,
        "contents": contents,
        "url": url,
        "label": label
    }
    
    # JSON 파일로 저장
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = []
    
    # 새로운 데이터 추가
    data.append(new_data)
    
    # JSON 파일로 저장 (기존 데이터 포함)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
def check_numeric_pattern(s):
    # 정규식 패턴: /숫자/숫자/숫자/ 형식
    pattern = r'/\d+/\d+/\d+/'
    
    # 패턴이 문자열에 있으면 1, 없으면 0 반환
    if re.search(pattern, s):
        return 1
    else:
        return 0
    
def normalize_string(s):
    # Step 1: 백슬래시와 그 뒤의 문자 하나를 공백으로 치환
    s = re.sub(r'\\.', ' ', s)
    
    # Step 2: 여러 개의 공백을 하나의 공백으로 치환
    s = re.sub(r'\s+', ' ', s)
    
    # Step 3: 양쪽 공백 제거
    s = s.strip()
    
    return s

if __name__ == "__main__":
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.connect("tcp://127.0.0.1:5556")
    
    try:
        while True:
            html_content = socket.recv_json()
            url = html_content["url"]
            doc = Document(html_content["html_content"])
            
            title = doc.title()
            article_content = doc.summary()
            
            soup = BeautifulSoup(article_content, "html.parser")
            paragraphs = soup.find_all('p')
            content = " ".join([p.get_text() for p in paragraphs])
            normalized_content = normalize_string(content)
            label = check_numeric_pattern(html_content['url'])
            
            save_data_to_json(title=title, contents=normalized_content,url=url , label=label, filename="site_data.json")
            
    except:
       print(traceback.format_exc())
    