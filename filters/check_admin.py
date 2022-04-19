import telebot

class IsAdmin(telebot.custom_filters.SimpleCustomFilter):
    key='is_admin'
    @staticmethod
    def check(message):
        # ОТКРЫВАЕТСЯ ФАЙЛ channel_admins.txt ИЗ SETTINGS ДЛЯ ЧТЕНИЯ
        with open('./settings/channel_admins.txt', 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    arr = line.split(':')
                    if str(arr[1].strip()) == f'{str(message.from_user.id)}':
                        return True
                except:
                    print('Ошибка при обработке файла channel_admins.txt')
            return False
        
            
