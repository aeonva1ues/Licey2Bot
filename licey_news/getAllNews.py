# import telebot
# from threading import Thread
# import time
# import urls
# import parsing_news

# ID = '-1001618657766'
# TOKEN = '5188618612:AAFGjZmT9Z3_9o8CGd0jpqmQRNIb0dDmX6M'


# def getAllNews():
#     cards_on_page_arg = 140
#     count = 0
#     while cards_on_page_arg >= 0:
#         # сразу вывод
#         url = f'http://oren-licey2.ru/?start={cards_on_page_arg}'
#         cards_array = parsing_news.parseMainPage(url)
#         for card_num in range(len(cards_array)-1, -1, -1):
#             news_title = cards_array[card_num]['title']
#             img_link = cards_array[card_num]['image_link']
#             news_description = cards_array[card_num]['description']
#             news_data = cards_array[card_num]['publication_data']
#             news_link = cards_array[card_num]['link']
#             if news_description == '!!':
#                 news_description = 'Подробности по ссылке ниже'
#             bot.send_message(ID, f'❗️ Новость с сайта лицея\n📌 Заголовок: "{news_title}"\n©️ {news_description}\n🧷 Ссылка: {news_link}\n🕐 {news_data}\n\n#новости_лицея')
#             if img_link == '!!':
#                 pass
#             else:
#                 bot.send_photo(ID, img_link)
#             count+=1
#             print(f'{count}/140')
#             time.sleep(30)
#         cards_on_page_arg -= 7

# # bot = telebot.TeleBot(TOKEN)

# if __name__ == '__main__':
#     bot = telebot.TeleBot(TOKEN)
#     while True:
#         try:
#             print('Delete commits if you decide to re-create the channel')
#             # t=Thread(target=getAllNews)
#             # t.start()
#             bot.polling()
#         except Exception as bot_error:
#             print(f'Упс, ошибка: {bot_error}')

        
