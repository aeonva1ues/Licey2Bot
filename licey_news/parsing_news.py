from bs4 import BeautifulSoup
import requests
from . import urls
# ПАРСИНГ САЙТА С ВЫВОДОМ МАССИВА СЛОВАРЕЙ, СОДЕРЖАЩИХ ЗАГОЛОВКИ КАРТОЧЕК, ССЫЛКИ НА КАРТИНКИ, А ТАКЖЕ ССЫЛКИ НА НОВОСТЬ
def parseMainPage(url):
    r_text = requests.get(url, headers=urls.HEADERS).text
    soup = BeautifulSoup(r_text, 'lxml')
    all_cards = soup.find_all('div', class_='col-xs-12 col-sm-12 col-md-12 col-lg-12 article_news')
    full_news_card = []
    for card in all_cards:
        link_on_news = card.find('a').get('href')
        news_image = card.find('img')
        if not news_image:
            news_image_link = "!!"
        else:
            # news_image_link = card.find('img').get('src')
            news_image_link = news_image.get('src')
        news_title_find = card.find('a')
        if not news_title_find:
            news_title = "!!"
        else:
            news_title = news_title_find.text
        news_description_find = card.find('div', class_='annotation')
        if not news_description_find:
            news_description = "!!"
        else:
            news_description = news_description_find.text
        news_data_publication = card.find('div', class_='col-md-6 col-sm-6 col-xs-8').text
        full_news_card.append(
            {
                'title': news_title,
                'image_link': news_image_link,
                'description': news_description,
                'publication_data': news_data_publication,
                'link': urls.DOMEN+link_on_news   
            }
        )
    if len(full_news_card) == 0:
        print('ПАРСЕР НИЧЕГО НЕ НАШЕЛ! pasing_news.py')
    return full_news_card
