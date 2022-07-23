import telebot
import time
from datetime import datetime
from settings.chatID import ID as CHAT_ID
from settings.token import TOKEN
from licey_news import autoupdate
from content_for_user import site_parser


running = False

def updateHeadSquad():
    url = 'http://oren-licey2.ru/rukovodstvo.html'
    answer = site_parser.headSqdParse(url)
    # info_content = HeadSquadInfo()
    if len(answer) != 0:
        content = ''
        for i in range(len(answer)-2):
            content = content + '\n' + answer[i]
        content = content + '\n\n\nОзнакомиться можно по ссылке: http://oren-licey2.ru/rukovodstvo.html'
        with open('./content_for_user/head_squad.txt', 'w', encoding='utf-8') as file:
            return file.write(content)
    else:
        return print('Руководящий состав выведен неудачно, отправил альтернативное сообщение')

if __name__ == '__main__':
    bot = telebot.TeleBot(TOKEN)
    running = True # запуск главного цикла
    print('Автоматический парсер сайта запущен')
    updating = False # флаг для отправки новости


while running:
    try:
        date = str(datetime.today()) 
        time_to_update = date.split()[1].split('.')[0]
        if time_to_update == '06:00:00':
            updateHeadSquad()
        if (time_to_update == '08:00:00' or time_to_update == '10:00:00' or time_to_update == '14:00:00' or time_to_update == '16:00:00' or time_to_update == '18:00:00') and updating == False:
            updating = True
            print('Началась проверка на наличие обновлений на сайте лицея..')
        # ЕСЛИ ОБНОВЛЕНИЙ НЕТ
            time.sleep(3)
            if autoupdate.get_actual_news():
                print('Обновление новостей не найдено')
        # ЕСЛИ ОБНОВЛЕНИЯ ЕСТЬ
            else:
                array_of_content = autoupdate.new_actual_news()
                news_title = array_of_content[0]
                img_link = array_of_content[1]
                news_link = array_of_content[2]
                news_data = array_of_content[3]
                news_description = array_of_content[4]                   
                bot.send_message(CHAT_ID, f'❗️ Новость с сайта лицея\n📌 Заголовок: "{news_title}"\n©️ {news_description}\n🧷 Ссылка: {news_link}\n🕐 {news_data}\n\n#новости_лицея')
                bot.send_photo(CHAT_ID, img_link)
                print('Последняя новость отправлена ботом')
                with open('./admin_info/logs.txt', 'a', encoding='utf-8') as log:
                    date = str(datetime.today())
                    display_date = date.split()[1].split(".")[0]
                    log_text = f'{display_date} || Отправлена новость "{news_title}"\n'
                    log.write(log_text)
            updating = False
    except Exception as second_thread_error:
        print(f'Ошибка: {second_thread_error}')

