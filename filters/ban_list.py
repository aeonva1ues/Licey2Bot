import telebot

class BannedUser(telebot.custom_filters.SimpleCustomFilter):
    key='is_banned'
    @staticmethod
    def check(message):
        # ОТКРЫВАЕТСЯ ФАЙЛ channel_admins.txt ИЗ SETTINGS ДЛЯ ЧТЕНИЯ
        with open('./admin_panel/ban_list.txt', 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    if str(line).strip() == str(message.from_user.id).strip():
                        return True # banned user
                except:
                    print('Ошибка при обработке файла ban_list.txt')
            return False # not banned user
        
            
