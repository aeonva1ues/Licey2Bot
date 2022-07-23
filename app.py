import time
from datetime import datetime
# from threading import Thread
import telebot
from telebot import types
from settings import token
from settings import admin
from settings import chatID
from filters import check_admin
from filters import ban_list
from licey_news import autoupdate
from licey_news import admins_news


bot = telebot.TeleBot(token.TOKEN)
running = False
updating = False


# СОЗДАНИЕ ЛОГА В ФАЙЛЕ
def makeLog(activity):
    with open('./admin_info/logs.txt', 'a', encoding='utf-8') as log:
        try:
            date = str(datetime.today())
            display_date = date.split(".")[0]
            log_text = f'{display_date} || {activity}\n'
            return log.write(log_text)
        except Exception as logging_error:
            return print(f'Ошибка при логировании // {logging_error}')

# 
def sendImage(chatId: str, status: bool, path: str) -> bool:
    if status == True:
        img = open(path, 'rb')
        bot.send_photo(chatId, img)
        img.close()
    else:
        print('Отправка новости без фото')

# ГЛАВНАЯ КЛАВИАТУРА
def mainKeyboard():
    main_btn_head_sqd = types.KeyboardButton('Руководящий состав')
    main_btn_to_first_class = types.KeyboardButton('Приём в первый класс')
    main_btn_licey_contacts = types.KeyboardButton('Контакты лицея')
    main_btn_licey_location = types.KeyboardButton('Расположение')
    main_btn_write_quest = types.KeyboardButton('Задать вопрос')
    main_keyboard = types.ReplyKeyboardMarkup(row_width=2)
    return main_keyboard.add(main_btn_head_sqd, main_btn_to_first_class, main_btn_licey_location, main_btn_licey_contacts).add(main_btn_write_quest)
# ПРОВЕРКА НА ОТМЕНУ ДЕЙСТВИЯ (/CANCEL)
def cancelCommand(message: str) -> bool:
    try:
        if str(message.text.strip().lower()) == '/cancel' or str(message.text.strip().lower()) == '/отмена':
            bot.send_message(message.chat.id, ('Действие отменено'))
            return True
        return False
    except:
        return False

# ФУНКЦИИ ДЛЯ ЛС БОТА
    # ЕСЛИ АККАУНТ ЗАБЛОКИРОВАН
@bot.message_handler(is_banned = True)
def messageForBannedUser(message):
    bot.send_message(message.chat.id, 'Вы были заблокированы администратором. Все функции бота для вас закрыты')

    # СТАРТ
@bot.message_handler(commands=['start'], is_banned = False)
def startCommand(message):
    print(f'{message.from_user.id} использовал /start')
    makeLog(f'{message.from_user.id} использовал /start')
    date = str(datetime.today()) 
    actual_time = date.split()[1].split('.')[0][:2]
    actual_time_int = int(actual_time)
    welcome_word = 'Здравствуйте'
    if actual_time[0] == '0':
        actual_time_int = int(actual_time[1])
    if actual_time_int >= 6 and actual_time_int <= 13:
        welcome_word = 'Доброго утра'
    elif actual_time_int > 13 and actual_time_int <= 17:
        welcome_word = 'Добрый день'
    elif actual_time_int > 17 and actual_time_int < 22:
        welcome_word = 'Добрый вечер'
    elif actual_time_int >= 22 or actual_time_int < 6:
        welcome_word = 'Доброй ночи' 
    bot.send_message(message.chat.id, f'👋 {welcome_word}, {message.from_user.first_name}! \nСнизу у вас появилась телеграмм-клавиатура, которую вы можете использовать для того, чтобы узнать все то, что вам необходимо', reply_markup=mainKeyboard())
    # НАВИГАЦИЯ БОТОМ
@bot.message_handler(is_banned = False, content_types=['text'], func=lambda message: message.text[0] != '/')
def navigation(message):
    if message.text == 'Руководящий состав':
        # global content
        with open('./content_for_user/head_squad.txt', 'r', encoding='utf-8') as file:
            head_squad_content = file.read()
            head_squad_content = str(head_squad_content).strip()
        try:
            if head_squad_content != '':
                bot.send_message(message.chat.id, head_squad_content)
            else:
                bot.send_message(message.chat.id, 'Ознакомиться с руководящим и педагогическим составом можно по ссылке: http://oren-licey2.ru/rukovodstvo.html')
        except:
            bot.send_message(message.chat.id, 'Ознакомиться с руководящим и педагогическим составом можно по ссылке: http://oren-licey2.ru/rukovodstvo.html')
    elif message.text == 'Приём в первый класс':
        bot.send_message(message.chat.id, 'Вся информация предоставлена по ссылке: http://oren-licey2.ru/post/priyom-v-1-klass1.html')
    elif message.text == 'Контакты лицея':
        contacts = 'Адрес: г. Оренбург ул. Уральская, 1\nНомер телефона: (3532) 43-07-13\nEmail: l2@orenschool.ru'
        bot.send_message(message.chat.id, f'📗 Контактная информация:\n{contacts}')
    elif message.text == 'Задать вопрос':
        if questions_count <= 4:
            user_fullname = f'{message.from_user.first_name} {message.from_user.last_name} ({message.from_user.username})'
            msg = bot.send_message(message.chat.id, 'Напишите мне ваш вопрос. Он будет передан администраторам.\nЕсли вы хотите отменить действия - отправьте в чат /cancel')
            bot.register_next_step_handler(msg, getQuestionText)
        else:
            bot.send_message(message.chat.id, 'Очередь переполнена, попробуйте обратиться немного позже')
    elif message.text == 'Расположение':
        bot.send_location(message.chat.id, 51.765715459216764, 55.13461504705226)

def getQuestionText(message):
    print(f'Пользователь {message.from_user.username} ({message.from_user.id}) написал текст: {message.text}')
    makeLog(f'Пользователь {message.from_user.username} ({message.from_user.id}) задал вопрос: {message.text}')
    if cancelCommand(message):
        return
    global questions_count
    global questions_array
    global requests_count
    messagesIdInAdmChats = []
    admChatsId = []
    questions_count+=1
    user_fullname = f'{message.from_user.first_name} {message.from_user.last_name} ({message.from_user.username})'
    user_question_text = f'(ADMIN) Вопрос от пользователя {user_fullname}:\n\n{message.text}'
    with open('./settings/channel_admins.txt', 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    inlineButton_answer = types.InlineKeyboardButton('Дать ответ', callback_data='AnswerIt')
                    inlineButton_del = types.InlineKeyboardButton('Удалить вопрос', callback_data='DeleteIt')
                    admin_reaction_keyboard = types.InlineKeyboardMarkup(row_width=2)
                    admin_reaction_keyboard.add(inlineButton_answer,inlineButton_del)
                    arr = line.split(':')
                    admin_id = str(arr[1].strip())
                    admin_msg = bot.send_message(admin_id, user_question_text, reply_markup=admin_reaction_keyboard)
                    # ДОБАВЛЕНИЕ В СПИСОК ИД СООБЩЕНИЯ В ЛИЧКЕ С АДМИНОМ ДЛЯ ДАЛЬНЕЙШЕГО УДАЛЕНИЯ У ВСЕХ
                    messagesIdInAdmChats.append(admin_msg.message_id)
                    admChatsId.append(admin_msg.chat.id)
                except:
                    print('Ошибка при обработке файла channel_admins.txt (в app.py при отправке вопроса пользователем)')
    # МАССИВ СОДЕРЖИТ В СЕБЕ ВСЕ НЕОБХОДИМЫЕ ИД, ХРАНЯ ИХ ВМЕСТЕ В СЛОВАРЯХ
    questions_array.append({'number': requests_count, 'm_id': messagesIdInAdmChats, 'c_id': admChatsId, 'user_c_id': message.chat.id, 'question_text': message.text, 'user_fullname': user_fullname})
    requests_count +=1
    bot.send_message(message.chat.id, f'Ваш вопрос успешно отправлен! В ближайшее время вы получите ответ.\nВопросов в очереди (включая ваш): {questions_count}')

# КАЛЛБЕК АДМИНИСТРАТОРА
@bot.callback_query_handler(func=lambda callback: True)
def adminAnswer(callback):
    global admin_answer_message_id
    global admin_start_writing_answer
    if admin_start_writing_answer:
        bot.send_message(callback.message.chat.id, '(ADMIN) Один из администраторов уже начал отвечать на вопрос. Пожалуйста, дождитесь его ответа, иначе могут возникнуть программные ошибки. В случае возникновения ошибки обратитесь к разработчику.')
    else:
        admin_start_writing_answer = True
        if callback.data == 'AnswerIt':
            admin_answer_message_id = callback.message.id # ид сообщения, на которое отреагировал админ
            msg = bot.send_message(callback.from_user.id, '(ADMIN) Введите ваш ответ для пользователя (одним сообщением).')
            bot.register_next_step_handler(msg, adminAnswer)
        elif callback.data == 'DeleteIt':
            admin_answer_message_id = callback.message.id
            msg = bot.send_message(callback.from_user.id, '(ADMIN) Введите причину удаления вопроса для пользователя')
            bot.register_next_step_handler(msg, deleteQuestion)

def adminAnswer(message):
    if cancelCommand(message):
        return
    global admin_answer_message_id
    global questions_array
    global questions_count
    global admin_start_writing_answer # ФЛАГ, ОБОЗНАЧАЮЩИЙ ДЕЙСТВУЮЩЕЕ НАПИСАНИЕ ОТВЕТА НА ВОПРОС АДМИНИСТРАТОРОМ
    admins_answer = message.text
    questions_count-=1
    admin_start_writing_answer = False
    for k in range(len(questions_array)):
        if admin_answer_message_id in questions_array[k]['m_id']:
            date = str(datetime.today())
            bot.send_message(questions_array[k]['user_c_id'], f'Пришел ответ на ваш вопрос: "{questions_array[k]["question_text"]}"\n\n{admins_answer}')
            bot.send_message(message.chat.id, f'(ADMIN) Ответ пользователю {questions_array[k]["user_fullname"]} отправлен!\n\nТекст вопроса: "{questions_array[k]["question_text"]}"\nВаш ответ: "{admins_answer}"\n\nДата:{date.split()[1].split(".")[0]}')
            makeLog(f'Ответ пользователю {questions_array[k]["user_fullname"]} отправлен администратором {message.from_user.first_name} {message.from_user.last_name} ({message.from_user.username}) || Текст вопроса: "{questions_array[k]["question_text"]}" || Ответ администратора: "{admins_answer}"')
            for i in range(len(questions_array[k]["c_id"])):
                bot.delete_message(questions_array[k]['c_id'][i], questions_array[k]['m_id'][i])
            del questions_array[k]
            break

def deleteQuestion(message):
    if cancelCommand(message):
        return
    global admin_answer_message_id
    global questions_array
    global questions_count
    global admin_start_writing_answer
    admins_answer = message.text
    questions_count-=1
    admin_start_writing_answer = False
    for k in range(len(questions_array)):
        if admin_answer_message_id in questions_array[k]['m_id']:
            date = str(datetime.today())
            bot.send_message(questions_array[k]['user_c_id'], f'Ваш вопрос: "{questions_array[k]["question_text"]}" был удален администратором. Причина: {admins_answer}')
            bot.send_message(message.chat.id, f'(ADMIN) Вопрос был удален. Ответ пользователю {questions_array[k]["user_fullname"]} отправлен!\n\nТекст вопроса: "{questions_array[k]["question_text"]}"\nВаш ответ: "{admins_answer}"\n\nДата:{date.split()[1].split(".")[0]}')
            makeLog(f'Вопрос пользователя {questions_array[k]["user_fullname"]} был удален администратором {message.from_user.first_name} {message.from_user.last_name} ({message.from_user.username}) || Текст вопроса: "{questions_array[k]["question_text"]}" || Причина, указанная администратором: "{admins_answer}"')
            for i in range(len(questions_array[k]["c_id"])):
                bot.delete_message(questions_array[k]['c_id'][i], questions_array[k]['m_id'][i])
            del questions_array[k]
            break


# Жалоба по тех состовляющему
@bot.message_handler(commands=['report'])
def report(message):
    msg = bot.send_message(message.chat.id, 'Опишите вашу жалобу, касающуюся бота или канала. Она будет передана напрямую разработчику на исправление.\nЕсли же у вас возникла претензия или вопрос к руководству лицея, то вы можете воспользоваться функцией "Задать вопрос", однако прежде, нажмите на /cancel для отмены технической жалобы.')
    bot.register_next_step_handler(msg, report_text)


def report_text(message):
    if cancelCommand(message):
        return
    bot.send_message(admin.DEV_ADMIN_ID, f'(DEV) ЖАЛОБА от {message.from_user.first_name} {message.from_user.last_name} ({message.from_user.username}):\n"{message.text}"')
    makeLog('(DEV) ЖАЛОБА от {message.from_user.first_name} {message.from_user.last_name} ({message.from_user.username}):\n"{message.text}"')
    bot.send_message(message.chat.id, 'Ваша жалоба успешно отправлена. Обратный ответ не предусмотрен. Если у вас остались вопросы лично к разработчику или вы хотите предоставить скриншот ошибки, то обратитесь в личные сообщения: https://t.me/aeonva1ues')
    return makeLog(f'{message.from_user.first_name} {message.from_user.last_name} ({message.from_user.username}) создал жалобу: {message.text}')


# СПИСОК АДМИНИСТРАЦИИ БОТА
@bot.message_handler(commands=['admins'])
def show_admins(message):
    if str(message.from_user.id) == admin.DEV_ADMIN_ID:
        with open('./settings/channel_admins.txt', 'r', encoding='utf-8') as txt_file:
            admin_list: str = txt_file.read()
        return bot.send_message(message.chat.id, f'(DEV ADMIN) Состав администрации бота:\n{admin_list}')


# БАН ПОЛЬЗОВАТЕЛЯ КОМАНДОЙ /fastban userid
@bot.message_handler(commands=['fastban'])
def fastban(message):
    if str(message.from_user.id) == admin.DEV_ADMIN_ID:
        command_text_arr = message.text.split()
        if len(command_text_arr) == 2:
            arg = command_text_arr[1] # ИД пользователя для блокировки
            with open('./admin_panel/ban_list.txt', 'a', encoding='utf-8') as banlist_file:
                banlist_file.write('\n'+arg)
            bot.send_message(message.chat.id, f'(DEV) Пользователь {arg} заблокирован.')
            makeLog('(DEV) Пользователь {arg} заблокирован')
        else:
            bot.send_message(message.chat.id, '(DEV) Используйте /fastban id для быстрой блокировки пользователя')


# ПРОСМОТР ЛОГА (/logs count)
@bot.message_handler(commands=['logs'])
def show_logs(message):
    if str(message.from_user.id) == admin.DEV_ADMIN_ID:
        try:
            commands_arr = message.text.split()
            if len(commands_arr) == 2:
                arg: int = int(commands_arr[1])
                try:
                    with open('./admin_info/logs.txt', 'r', encoding='utf-8') as logs:
                        log_content = logs.read() # ПОЛНЫЙ ЛОГ
                        log_strings_arr = log_content.split('\n') # МАССИВ ИЗ СТРОЧЕК ЛОГОВ
                        log_strings_arr.reverse()
                    logs_to_send_arr = log_strings_arr[0:arg+1]
                    logs_ready_to_send = "\n\n".join(logs_to_send_arr)
                    bot.send_message(message.chat.id, f'(DEV) Последние строчки логов ({arg}):\n{logs_ready_to_send}')
                except:
                    bot.send_message(message.chat.id,'(DEV) Ошибка в выгрузке логов')
            else:
                return bot.send_message(message.chat.id, '(DEV) Используйте /logs count, где count - кол-во строчек из логов')
        except:
            return bot.send_message(message.chat.id, '(DEV) Ошибка при использовании команды')


# ОЧИСТКА ОЧЕРЕДИ ОТВЕТОВ НА ВОПРОСЫ (/wasc - writing answer status change)
@bot.message_handler(commands=['wasc'])
def writing_answer_status_change(message):
    global admin_start_writing_answer
    if str(message.from_user.id) == admin.DEV_ADMIN_ID:
        admin_start_writing_answer = False
        makeLog('DEV очистил очередь ответа на вопросы')
        return bot.send_message(message.chat.id, '(DEV ADMIN) Очередь администрации на ответы пользователям успешно очищена.')


# СТАТУС ОЧЕРЕДИ ОТВЕТОВ НА ВОПРОСЫ (/was - writing answer status)
@bot.message_handler(commands=['was'])
def writing_answer_status(message):
    global admin_start_writing_answer
    if str(message.from_user.id) == admin.DEV_ADMIN_ID:
        if admin_start_writing_answer:
            return bot.send_message(message.chat.id, '(DEV ADMIN) Очередь администрации на ответ пользователям занята')
        else:
            return bot.send_message(message.chat.id, '(DEV ADMIN) Очередь администрации на ответ пользователям свободна')


# СТАТУС ОЧЕРЕДИ НА СОЗДАНИЕ НОВОСТИ С АККАУНТА РАЗРАБОТЧИКА
@bot.message_handler(commands=['qstatus'])
def queque_status(message):
    global making_news
    if str(message.from_user.id) == admin.DEV_ADMIN_ID:
        if making_news == 0:
            return bot.send_message(message.chat.id, '(DEV ADMIN) Очередь на создание новостей свободна')
        elif making_news == 1:
            return bot.send_message(message.chat.id, '(DEV ADMIN) Очередь на создание новостей занята')
# ОЧИСТКА ОЧЕРЕДИ С АККАУНТА РАЗРАБОТЧИКА
@bot.message_handler(commands=['clearq'])
def clear_queque(message):
    global making_news
    if str(message.from_user.id) == admin.DEV_ADMIN_ID:
        making_news = 0
        makeLog('DEV очистил очередь создания новостей')
        return bot.send_message(message.chat.id, '(DEV ADMIN) Очередь успешно очищена.')
# СОЗДАНИЕ НОВОСТИ
@bot.message_handler(is_admin=True, commands=['makenews'])
def get_text(message):
    makeLog(f'Администратор ({message.from_user.id}) {message.from_user.username} - {message.from_user.first_name} начал создание новости')
    global making_news
    if making_news == 0:
        making_news = 1
        remove_keyboard = telebot.types.ReplyKeyboardRemove()
        print(f'{message.from_user.id} - {message.from_user.username} - {message.from_user.first_name} | начал создание новости для канала')
        bot.send_message(message.chat.id, '(ADMIN) Отлично, вы начали создание новости для канала. Следуйте всем инструкциям.', reply_markup=remove_keyboard)
        msg = bot.send_message(message.chat.id, '(ADMIN) Введите заголовок новости. Не используйте эмодзи! Украсить свое сообщение вы сможете позже.\nДля отмены действия вы можете использовать /cancel.')
        bot.register_next_step_handler(msg, makeNewsHeader)
    elif making_news == 1:
        bot.send_message(message.chat.id, '(ADMIN) В данный момент другой администратор создает новость. Пожалуйста, подождите')

    # СОЗДАНИЕ ЗАГОЛОВКА НОВОСТИ
def makeNewsHeader(message):
    global making_news
    if cancelCommand(message):
        making_news = 0
        return print('Создание новости отменено (выбор заголовка новости)')
    print(f'{message.from_user.id} - {message.from_user.username} - {message.from_user.first_name} | создал заголовок новости')
    global admin_news_message
    admin_news_message = admins_news.CreatingAdminsNews()
    # ПОЛУЧЕНИЕ ИМЕНИ АВТОРА
    with open('./settings/channel_admins.txt', 'r', encoding='utf-8') as file:
        for line in file:
            try:
                arr = line.split(':')
                if str(arr[1].strip()) == f'{str(message.from_user.id)}':
                    admin_news_message.news_author = str(arr[0].strip())
            except:
                pass
    try:
        admin_news_message.news_header = message.text.strip()
    except:
        return bot.register_next_step_handler(bot.send_message(message.chat.id, '(ADMIN) Недопустимый заголовок. Введите текст'), makeNewsHeader)
    bot.send_message(message.chat.id, '(ADMIN) Заголовок успешно установлен!')
    msg = bot.send_message(message.chat.id, '(ADMIN) Выберите эмодзи для заголовка. Оно будет установлено перед заголовком. Используйте стандартные эмодзи телеграма.')
    bot.register_next_step_handler(msg, makeHeaderEmoji)

def makeHeaderEmoji(message):
    global making_news
    try:
        message_length = len(message.text)
    except:
        return bot.register_next_step_handler(bot.send_message(message.chat.id, '(ADMIN) Ошибка. Выберите эмодзи из стандартных эмодзи в Телеграм'), makeHeaderEmoji)
    if cancelCommand(message):
        making_news = 0
        return print('Создание новости отменено (выбор эмодзи заголовка новости)')
    elif message_length > 1:
        msg = bot.send_message(message.chat.id, '(ADMIN) Ошибка при выборе эмодзи...')
        bot.send_message(message.chat.id, '(ADMIN) Прогресс не сброшен. Введите эмодзи заново или же используйте /cancel для полной отмены')
        print(f'{message.from_user.id} - {message.from_user.username} - {message.from_user.first_name} | ошибка при выборе эмодзи - {message.text}')
        bot.register_next_step_handler(msg, makeHeaderEmoji)
    else:
        bot.send_message(message.chat.id, '(ADMIN) Эмодзи успешно установлено!')
        global admin_news_message
        admin_news_message.news_head_emoji = message.text.strip()
        msg = bot.send_message(message.chat.id, '(ADMIN) Введите основной текст новости. Можете использовать отступы, символы. Не используйте эмодзи в начале своего сообщения - выбор эмодзи будет предложен вам в следующих шагах.')
        bot.register_next_step_handler(msg, makeNewsBody)

def makeNewsBody(message):
    global making_news
    try:
        message_length = len(message.text)
    except:
        return bot.register_next_step_handler(bot.send_message(message.chat.id, '(ADMIN) Ошибка. Если вы хотите прикрепить фотографию, то сможете это сделать позже. Для прикрепления видеороликов их требуется загрузить на YouTube'), makeNewsBody)
    if cancelCommand(message):
        making_news = 0
        return print('Создание новости отменено (выбор текста новости)')
    elif message_length < 5:
        msg = bot.send_message(message.chat.id, '(ADMIN) Я предполагаю, что вы ошиблись... Если это не так и на самом деле существуют объявления или новости такой длины - отпишите https://t.me/aeonva1ues')
        bot.send_message(message.chat.id, '(ADMIN) Прогресс не сброшен. Такая ошибка появляется, если ваш текст состоит менее, чем из 6 символов. Если хотите остановить создание новости, то используйте /cancel')
        print(f'{message.from_user.id} - {message.from_user.username} - {message.from_user.first_name} | ошибка при создании текста - {message.text}')
        bot.register_next_step_handler(msg, makeNewsBody)
    else:
        bot.send_message(message.chat.id, '(ADMIN) Текст объявления сохранен!')
        global admin_news_message
        admin_news_message.news_body = message.text.strip()
        msg = bot.send_message(message.chat.id, '(ADMIN) Выберите эмодзи в начале текста новости. Обратите внимание, пробел между текстом и новостью ставится АВТОМАТИЧЕСКИ!')
        bot.register_next_step_handler(msg, makeBodyEmoji)

def makeBodyEmoji(message):
    global making_news
    try:
        message_length = len(message.text)
    except:
        return bot.register_next_step_handler(bot.send_message(message.chat.id, '(ADMIN) Ошибка. Выберите эмодзи из стандартных эмодзи в Телеграм'), makeBodyEmoji)
    if cancelCommand(message):
        making_news = 0
        return print('Создание новости отменено (выбор эмодзи около текста новости)')
    elif message_length > 1:
        msg = bot.send_message(message.chat.id, '(ADMIN) Возможно, вы ошиблись при выборе эмодзи. Частая ошибка - выбор стикера или использование нескольких эмодзи')
        bot.send_message(message.chat.id, '(ADMIN) Прогресс не сброшен. Введите эмодзи заново или же используйте /cancel для полной отмены')
        print(f'{message.from_user.id} - {message.from_user.username} - {message.from_user.first_name} | ошибка при выборе эмодзи - {message.text}')
        bot.register_next_step_handler(msg, makeBodyEmoji)
    else: 
        bot.send_message(message.chat.id, '(ADMIN) Эмодзи успешно установлено!')
        global admin_news_message
        admin_news_message.news_body_emoji = message.text.strip()
        default_news_tag = types.KeyboardButton('#новости_лицея')
        event_news_tag = types.KeyboardButton('#мероприятия_в_лицее')
        special_event_news_tag = types.KeyboardButton('#10класс_дискотека')
        tag_keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard= True)
        tag_keyboard.add(default_news_tag, event_news_tag, special_event_news_tag)
        msg = bot.send_message(message.chat.id, '(ADMIN) Отлично, почти все! Выберите хэш-тэг к новости. Вы можете воспользоваться предложенными примерами или указать свой. Всегда используйте один хэш-тэг на новости одного типа.\n\nПри вводе начните с знака #', reply_markup=tag_keyboard)
        bot.register_next_step_handler(msg, makeNewsTag)

def makeNewsTag(message):
    global making_news
    remove_keyboard = telebot.types.ReplyKeyboardRemove()
    try:
        if cancelCommand(message):
            making_news = 0
            return print('Создание новости отменено (выбор тэга)')
        elif message.text[0] != '#':
            bot.register_next_step_handler(bot.send_message(message.chat.id,'(ADMIN) Сообщение должно начинаться с #\nПопробуйте выбрать тэг заново.'), makeNewsTag)
        else:
            global admin_news_message
            admin_news_message.news_tag = message.text.strip()
            msg = bot.send_message(message.chat.id, '(ADMIN) Хотели ли бы вы загрузить фото? Отправьте мне фотографию или напишите "Нет"', reply_markup=remove_keyboard)
            bot.register_next_step_handler(msg, addPhoto)
    except:
        return bot.register_next_step_handler(bot.send_message(message.chat.id, '(ADMIN) Введите тэг.'), makeNewsTag)

def addPhoto(message):
    global making_news
    global admin_news_message
    global withPhoto
    withPhoto = False
    remove_keyboard = telebot.types.ReplyKeyboardRemove()
    next_step = False
    try:
        if cancelCommand(message):
            making_news = 0
            return print('Создание новости отменено (отправка фото))')
        elif message.content_type == 'photo':
            photo = message.photo[-1].file_id
            path = f'./licey_news/img/news_pic.png'
            admin_news_message.news_image_path = path
            file_info = bot.get_file(photo)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(path,'wb') as new_file:
                new_file.write(downloaded_file)
                bot.send_message(message.chat.id, '(ADMIN) Фото загружено успешно!')
                withPhoto = True
                next_step = True
        elif message.text.lower() == 'нет':
            next_step = True
        elif message.text.lower() != 'нет':
            bot.register_next_step_handler(bot.send_message(message.chat.id,'(ADMIN) В ответ вы должны прислать либо фото, либо ответить "Нет" (без ковычек)'), addPhoto)
        if next_step == True:
            admin_news_message.createNews()
            bot.send_message(message.chat.id, '(ADMIN) Новость готова к публикации. Выглядеть она будет таким образом:', reply_markup=remove_keyboard)
            bot.send_message(message.chat.id, f'{admin_news_message.news_content}')
            sendImage(message.chat.id, withPhoto, admin_news_message.news_image_path)
            last_creating_msg = bot.send_message(message.chat.id, '(ADMIN) Все ли вас устраивает? Чтобы опубликовать новость, напишите мне в ответ "Да". Если вы хотите вернуться и изменить какую-либо часть, напишите "Нет", тогда вам будет предложен выбор быстрого исправления!')
            bot.register_next_step_handler(last_creating_msg, userAcceptForMakingNews)
    except:
        return bot.register_next_step_handler(bot.send_message(message.chat.id,'(ADMIN) Возникла ошибка, попробуйте еще раз'), addPhoto)

def userAcceptForMakingNews(message):
    global admin_news_message
    global making_news
    try:
        if cancelCommand(message):
            making_news = 0
            return print('Создание новости отменено (согласие на публикацию)')
        elif message.text.lower() == 'да':
            bot.send_message(message.chat.id, '(ADMIN) Отлично, отправляю вашу новость в канал.')
            bot.send_message(chatID.ID, admin_news_message.news_content)
            sendImage(chatID.ID, withPhoto, admin_news_message.news_image_path)
            bot.send_message(message.chat.id, '(ADMIN) Новость отправлена!')
            makeLog(f'Администратор ({message.from_user.id}) {message.from_user.username} - {message.from_user.first_name} создал новость')
            making_news = 0
        elif message.text.lower() == 'нет':
            btn_change_header = types.KeyboardButton('Заголовок')
            btn_change_header_emoji = types.KeyboardButton('Эмодзи перед заголовком')
            btn_change_body = types.KeyboardButton('Текст новости')
            btn_change_body_emoji = types.KeyboardButton('Эмодзи перед текстом новости')
            btn_change_tag = types.KeyboardButton('Тэг')
            btn_change_image = types.KeyboardButton('Фото')
            keyboard_back_step = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard_back_step.add(btn_change_header,btn_change_header_emoji,btn_change_body,btn_change_body_emoji,btn_change_tag, btn_change_image)
            msg = bot.send_message(message.chat.id, '(ADMIN) Выберите раздел, в котором вы хотите что-то поменять. Используйте клавиатуру.', reply_markup=keyboard_back_step)
            bot.register_next_step_handler(msg, choosePlaceInNewsToChange)
        else:
            msg = bot.send_message(message.chat.id, '(ADMIN) Похоже, вы ошиблись. Введите в ответ "Да" или "Нет" (ковычки использовать не нужно)')
            bot.register_next_step_handler(msg, userAcceptForMakingNews)
    except:
        msg = bot.send_message(message.chat.id, '(ADMIN) Похоже, вы ошиблись. Введите в ответ "Да" или "Нет" (ковычки использовать не нужно)')
        bot.register_next_step_handler(msg, userAcceptForMakingNews)

def choosePlaceInNewsToChange(message):
    global placeToChangeText
    global withPhoto
    global making_news
    remove_keyboard = telebot.types.ReplyKeyboardRemove()
    try:
        if cancelCommand(message):
            making_news = 0
            return print('Создание новости отменено (согласие на публикацию)')
        elif message.text == 'Заголовок':
            msg = bot.send_message(message.chat.id, '(ADMIN) Введите новый текст заголовка')
            placeToChangeText = 'Head'
            bot.register_next_step_handler(msg, changeText)
        elif message.text == 'Эмодзи перед заголовком':
            placeToChangeText = 'HeadEmoji'
            msg = bot.send_message(message.chat.id, '(ADMIN) Выберите новое эмодзи')
            bot.register_next_step_handler(msg, changeText)
        elif message.text == 'Текст новости':
            msg = bot.send_message(message.chat.id, '(ADMIN) Выберите новый текст новости')
            placeToChangeText = 'Body'
            bot.register_next_step_handler(msg, changeText)
        elif message.text == 'Эмодзи перед текстом новости':
            msg = bot.send_message(message.chat.id, '(ADMIN) Выберите новое эмодзи')
            placeToChangeText = 'BodyEmoji'
            bot.register_next_step_handler(msg, changeText)
        elif message.text == 'Тэг':
            msg = bot.send_message(message.chat.id, '(ADMIN) Выберите новый тэг')
            placeToChangeText = 'Tag'
            bot.register_next_step_handler(msg, changeText)
        elif message.text == 'Фото':
            btn_delete_photo = types.KeyboardButton('Удалить')
            btn_change_photo = types.KeyboardButton('Заменить')
            btn_add_photo = types.KeyboardButton('Добавить')
            keyboard_photo_changing = types.ReplyKeyboardMarkup(resize_keyboard=True)
            if withPhoto == False:
                keyboard_photo_changing.add(btn_add_photo)
                bot.send_message(message.chat.id, '✅', reply_markup=remove_keyboard)
                msg = bot.send_message(message.chat.id, '(ADMIN)Нажмите на кнопку чтобы добавить фото\n', reply_markup=keyboard_photo_changing)
            else:
                bot.send_message(message.chat.id, '✅', reply_markup=remove_keyboard)
                keyboard_photo_changing.add(btn_delete_photo, btn_change_photo)
                msg = bot.send_message(message.chat.id, '(ADMIN) Вы хотите удалить фотографию или заменить ее на другую?\n', reply_markup=keyboard_photo_changing)
            placeToChangeText = 'Photo'
            bot.register_next_step_handler(msg, changeText)
        else:
            msg = bot.send_message(message.chat.id, '(ADMIN) Вам нужно нажать на одну из этих кнопок!')
            bot.register_next_step_handler(msg, choosePlaceInNewsToChange)
    except:
        msg = bot.send_message(message.chat.id, '(ADMIN) Вам нужно нажать на одну из этих кнопок!')
        return bot.register_next_step_handler(msg, choosePlaceInNewsToChange)

def changeText(message):
    global making_news
    global admin_news_message
    global placeToChangeText
    global withPhoto
    next_step = False
    remove_keyboard = telebot.types.ReplyKeyboardRemove()
    try:
        if cancelCommand(message):
            making_news = 0
            return print('Создание новости отменено (изменение)')
        elif placeToChangeText == 'Head':
            admin_news_message.news_header = message.text.strip()
            next_step = True
        elif placeToChangeText == 'HeadEmoji':
            if len(message.text) > 1:
                bot.register_next_step_handler(bot.send_message(message.chat.id, '(ADMIN) Ошибка, выберите другое эмодзи', reply_markup=remove_keyboard), changeText)
            else:
                admin_news_message.news_head_emoji = message.text.strip()
                next_step = True
        elif placeToChangeText == 'Body':
            if len(message.text) < 5:
                bot.register_next_step_handler(bot.send_message(message.chat.id, '(ADMIN) Ошибка, текст слишком короткий', reply_markup=remove_keyboard), changeText)
            else:
                admin_news_message.news_body = message.text.strip()
                next_step = True
        elif placeToChangeText == 'BodyEmoji':
            if len(message.text) > 1:
                bot.register_next_step_handler(bot.send_message(message.chat.id, '(ADMIN) Ошибка, выберите другое эмодзи', reply_markup=remove_keyboard), changeText)
            else:
                admin_news_message.news_body_emoji = message.text.strip()
                next_step = True
        elif placeToChangeText == 'Tag':
            if message.text[0] != '#':
                bot.register_next_step_handler(bot.send_message(message.chat.id, '(ADMIN) Ошибка, тэг должен начинаться с #', reply_markup=remove_keyboard), changeText)
            else:
                admin_news_message.news_tag = message.text.strip()
                next_step = True
        elif placeToChangeText == 'Photo':
            if message.text == 'Удалить':
                withPhoto = False
                next_step = True
            elif message.text == 'Заменить' or 'Добавить':
                msg = bot.send_message(message.chat.id, '(ADMIN) Отправьте мне новую фотографию (если вы вновь передумаете, то напишите "Нет")', reply_markup=remove_keyboard)
                bot.register_next_step_handler(msg, addPhoto)
            else:
                bot.register_next_step_handler(bot.send_message(message.chat.id, '(ADMIN) Ошибка, вам нужно было нажать на кнопку'), changeText)
        if next_step == True:
            admin_news_message.createNews()
            bot.send_message(message.chat.id, f'Новый текст:\n\n\n{admin_news_message.news_content}', reply_markup=remove_keyboard)
            sendImage(message.chat.id, withPhoto, admin_news_message.news_image_path)
            msg = bot.send_message(message.chat.id, 'Если вы готовы опубликовать новость - введите "Да", если хотите что-то исправить еще - введите "Нет"')
            bot.register_next_step_handler(msg, userAcceptForMakingNews)
    except:
        return bot.register_next_step_handler(bot.send_message(message.chat.id, '(ADMIN) Ошибка, попробуйте еще раз'), changeText)
# ЗАПУСК БОТА
if __name__ == '__main__':
    print('Licey2Bot is running')
    questions_count = 0 # количество вопросов в очереди
    requests_count = 0 # номер вопроса в словаре
    making_news = 0 # 1 - другой администратор создает новость, 0 - можно создавать новость
    admin_start_writing_answer = False 
    questions_array = []
    running = True
    # ФИЛЬТР is_admin = True/False ДЛЯ ХАНДЛЕРОВ
    bot.add_custom_filter(check_admin.IsAdmin())
    bot.add_custom_filter(ban_list.BannedUser())

while running:
    try:
        # ВКЛЮЧЕНИЕ ПОСТОЯННОЙ РАБОТЫ БОТА
        bot.polling()
        
    except Exception as error_text:
        error_date = str(datetime.today()) 
        error_time = error_date.split()[1].split('.')[0]
        print(f'{error_time} Возникла ошибка: {error_text}. Бот отправлен на перезагрузку')
        time.sleep(4)