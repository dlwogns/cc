from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import stopwords
import zmq


# 텍스트 밀도 추출
def get_text_density(soup):
    text = soup.get_text(separator=' ')
    total_text_length = len(text.strip())
    total_tag_count = len(soup.find_all())

    if total_tag_count > 0:
        text_density = total_text_length / total_tag_count
    else:
        text_density = 0

    return {
        'text_length': total_text_length,
        'tag_count': total_tag_count,
        'text_density': text_density
    }
# 메타 태그 분석
def get_meta_features(soup):
    author_meta = soup.find('meta', {'name': 'author'})
    date_meta = soup.find('meta', {'property': 'article:published_time'}) or soup.find('meta', {'name': 'date'})
    description_meta = soup.find('meta', {'name': 'description'})

    return {
        'has_author': bool(author_meta),
        'has_date': bool(date_meta),
        'has_description': bool(description_meta)
    }

# 미디어 요소 빈도 분석
def get_media_features(soup):
    links = soup.find_all('a')
    images = soup.find_all('img')
    videos = soup.find_all('video')

    return {
        'link_count': len(links),
        'image_count': len(images),
        'video_count': len(videos)
    }
    
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def clean_text(text):
    # 특수 문자 제거
    text = re.sub(r'[^\w\s]', '', text)

    # 소문자로 변환
    text = text.lower()

    # 불용어 제거
    tokens = text.split()
    filtered_tokens = [word for word in tokens if word not in stop_words]

    return ' '.join(filtered_tokens)

def extract_features_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # 텍스트 밀도, 메타 태그, 미디어 요소 등의 특징 추출
    density_features = get_text_density(soup)
    meta_features = get_meta_features(soup)
    media_features = get_media_features(soup)

    # 페이지의 텍스트 추출 및 NLP 처리
    text = soup.get_text(separator=' ')
    cleaned_text = clean_text(text)

    # 모든 특징 결합
    features = {**density_features, **meta_features, **media_features}
    return features, cleaned_text

if __name__ == "__main__":
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.connect("tcp://127.0.0.1:5555")
    
    while True:
        html_content = socket.recv_string()
        print(html_content)
        features, cleaned_text = extract_features_from_html(html_content)
        
        