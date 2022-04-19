import time
from datetime import datetime
from . import parsing_news
from . import urls


# 1 строчка - Название новости
# 2 строчка - Ссылка на картинку
# 3 строчка - Ссылка на новость

# ЕСЛИ НОВОСТИ АКТУАЛЬНЫЙ - TRUE, НЕАКТУАЛЬНЫЕ - FALSE
def get_actual_news():
    url = urls.DOMEN # главная страница
    main_page_news = parsing_news.parseMainPage(url)
    head_title_news = main_page_news[0]['title']
    news_img_link = main_page_news[0]['image_link']
    news_link = main_page_news[0]['link']
    news_publication_data = main_page_news[0]['publication_data']
    news_description = main_page_news[0]['description']
    # количество карточек с новостями - 7, используется только первая
    try:
        with open('./licey_news/actual_news.txt', 'r', encoding='utf-8') as file:
            content = file.readline()
        if str(content.strip()) == str(head_title_news.strip()):
            print('autoupdate.py | Обновления новостей не найдены')
            return True
        # В СЛУЧАЕ, ЕСЛИ НОВОЕ ОБНОВЛЕНИЕ НАЙДЕНО
        else:
            time.sleep(1)
            print(f'Новость "{head_title_news}" найдена! Передаю в app.py')
            # В ТЕКСТОВОЙ ФАЙЛЕ СОХРАНЯЕТСЯ НАЗВАНИЕ (ДЛЯ ПОСЛЕДУЮЩЕЙ ПРОВЕРКИ), А ТАКЖЕ НЕОБХОДИМЫЕ ДЛЯ СООБЩЕНИЯ ССЫЛКИ
            with open('./licey_news/actual_news.txt', 'w', encoding='utf-8') as file:
                file.write(head_title_news)
                file.write(f'\n{str(news_img_link)}\n{str(news_link)}\n{str(news_publication_data)}\n{str(news_description)}')
                print('Начал отправку..')
                return False
    except Exception as update_error:
        print(f'Возникла работа при работе с файлом autoupdate.py: {update_error}')

# ВЫЗЫВАЕТСЯ APP.PY ПРИ ПОЯВЛЕНИИ НОВОЙ НОВОСТИ
def new_actual_news():
    arr = []
    with open('./licey_news/actual_news.txt', 'r', encoding='utf-8') as file:
        for line in file:
            arr.append(line.strip())
    return arr


