import requests
from bs4 import BeautifulSoup


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }

def headSqdParse(url: str) -> list:
    req = requests.get(url, headers=HEADERS).text
    soup = BeautifulSoup(req, 'lxml')
    block_with_text = soup.find('div', class_='col-xs-12 col-sm-12 col-md-12 col-lg-12')
    buffer = []
    for text in block_with_text:
        try:
            text_line = text.get_text()
            if text_line == '\n':
                pass
            else:
                buffer.append(text_line)
        except:
            pass
    return buffer
