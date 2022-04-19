import pyautogui as gui

def mainPanel():
    main_admin_panel_button_pressed = gui.confirm(text='Добро пожаловать в панель администратора!', title='Admin Panel', buttons=['Add admin', 'Admin list', 'Delete admin', 'Ban list', 'Ban user', 'Unban user', 'Close panel'])
        # gui.prompt() # поле ввода
    if main_admin_panel_button_pressed == 'Close panel':
        sys.exit
    elif main_admin_panel_button_pressed == 'Add admin':
        addAdmin()
    elif main_admin_panel_button_pressed == 'Admin list':
        readAdminList()
    elif main_admin_panel_button_pressed == 'Delete admin':
        deleteAdmin()
    elif main_admin_panel_button_pressed == 'Ban user':
        banUser()
    elif main_admin_panel_button_pressed == 'Unban user':
        unbanUser()
    elif main_admin_panel_button_pressed == 'Ban list':
        readBanList()

def passwordCheck():
    running = True
    while running:
        admin_password = gui.password(title='Admin login', text='Для входа в систему введите пароль')
        if admin_password == '12345':
            mainPanel() # запуск главной панели
            running = False # отключение цикличного появления окна входа
        elif admin_password == None:
            running = False
            sys.exit # выход из программы
        else:
            gui.alert(title='Login error!', text='Пароль введен неверно.')

def addAdmin():
    admin_id_text = gui.prompt(title='Add administrator (1 step)', text='Введите телеграм ид администратора', default='123456')
    if admin_id_text != None:
        admin_fullname_text = gui.prompt(title='Add administrator (2 step)', text='Введите имя администратора, оно будет использоваться при создании новостей', default='Тест Тестов')
        if admin_fullname_text != None:
            with open('D:/Bots/BotLicey2/settings/channel_admins.txt', 'a', encoding='utf-8') as file:
                file.write(f'\n{str(admin_fullname_text).strip()} : {str(admin_id_text).strip()}')
    return mainPanel()

def readAdminList():
    with open('D:/Bots/BotLicey2/settings/channel_admins.txt', 'r', encoding='utf-8') as file:
        admins = file.read()
        gui.alert(title='Admin list', text=admins)
    return mainPanel()

def deleteAdmin():
    admin_to_delete = gui.prompt(title='Delete administrator', text='Введите телеграмм ид администратора или же его полное имя',default='123456')
    with open('D:/Bots/BotLicey2/settings/channel_admins.txt', 'r', encoding='utf-8') as file:
        lines_arr = file.readlines()
        for i in range(len(lines_arr)):
            if admin_to_delete in lines_arr[i]:
                agree_to_delete = gui.confirm(title='Are you sure?', text = f'Найдено совпадение: {lines_arr[i]}. Удалить данного администратора из списка?', buttons=['Да', 'Нет'])
                if agree_to_delete != None:
                    if agree_to_delete == 'Да':
                        del lines_arr[i]
                        new_file_content = "".join(lines_arr)
                        with open('D:/Bots/BotLicey2/settings/channel_admins.txt', 'w', encoding='utf-8') as file:
                            file.write(new_file_content)
                        return mainPanel()
                    if agree_to_delete == 'Нет':
                        pass
                else:
                    return mainPanel()
        gui.alert(title='Упс..', text='Пользователи не найдены')
        return mainPanel()
        
def banUser():
    user_to_ban = gui.prompt(title='Ban', text='Введите ид пользователя, которого хотите заблокировать',default='123456')
    if user_to_ban != None:
        try:
            with open('D:/Bots/BotLicey2/admin_panel/ban_list.txt', 'a', encoding='utf-8') as file:
                file.write(f'\n{user_to_ban}')      
            gui.alert(title='User is banned', text='Пользователь заблокирован')
        except Exception as error:
            print(error)
            gui.alert(title='Error', text='Ошибка при работе с файлом ban_list.txt')
    return mainPanel()

def readBanList():
    with open('D:/Bots/BotLicey2/admin_panel/ban_list.txt', 'r', encoding='utf-8') as file:
        ban_users = file.read()
        gui.alert(title='Admin list', text=ban_users)
    return mainPanel()

def unbanUser():
    user_to_unban = gui.prompt(title='Unban ID', text='Введите телеграмм ид пользователя, которого хотите разблокировать',default='123456')
    with open('D:/Bots/BotLicey2/admin_panel/ban_list.txt', 'r', encoding='utf-8') as file:
        lines_arr = file.readlines()
        for i in range(len(lines_arr)):
            if user_to_unban.strip() == lines_arr[i].strip():
                agree_to_delete = gui.confirm(title='Are you sure?', text = f'Найдено совпадение: {lines_arr[i]}.\nВы уверены, что хотите разбанить данного пользователя?', buttons=['Да', 'Нет'])
                if agree_to_delete != None:
                    if agree_to_delete == 'Да':
                        del lines_arr[i]
                        new_file_content = "".join(lines_arr)
                        with open('D:/Bots/BotLicey2/admin_panel/ban_list.txt', 'w', encoding='utf-8') as file:
                            file.write(new_file_content)
                        return mainPanel()
                    if agree_to_delete == 'Нет':
                        pass
                else:
                    return mainPanel()
        gui.alert(title='Упс..', text='Пользователи не найдены')
        return mainPanel()

def main():
    passwordCheck()


if __name__ == '__main__':
    main()
        