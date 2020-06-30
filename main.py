import asyncio
import io
import logging
import threading
import time

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InputMediaDocument, ReplyKeyboardRemove, \
     KeyboardButton, ReplyKeyboardMarkup,  InlineKeyboardMarkup, InlineKeyboardButton
from urllib.request import urlopen
import json
import sqlite3

#--------------------Настройки бота-------------------------

# Ваш токен от BotFather
TOKEN = '1119195878:AAHvwsweXzZmmzQOUsAF1FLKOyhsF8XRV-M'

# Логирование
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Ваш айди аккаунта администратора и айди сообщения где хранится файл с данными
admin_id=264616288
config_id=191
conn = sqlite3.connect(":memory:")  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()


# #--------------------Получение данных-------------------------
async def get_data():
    to = time.time()
    # Пересылаем сообщение с данными от админа к админу
    forward_data = await bot.forward_message(admin_id, admin_id, config_id)
    # Получаем путь к файлу, который переслали
    file_data = await bot.get_file(forward_data.document.file_id)
    # Получаем файл по url
    file_url_data = bot.get_file_url(file_data.file_path)
    # Считываем данные с файла
    json_file= urlopen(file_url_data).read()
    print('Время получения бекапа :=' + str(time.time() - to))
    # Переводим данные из json в словарь и возвращаем
    return json.loads(json_file)
#--------------------Настройки аргументов sqlite3-------------------------
sql_ins = "INSERT INTO users VALUES ({}, '{}', {},{},'{}',{},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')"
sql_insert_many = "INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
sql_create = '''CREATE TABLE users(
chatid INTEGER,name TEXT, progress INTEGER, state INTEGER, password TEXT, activDate FLOAT, passwordStatus TEXT,
place1 TEXT,  place2 TEXT, place3 TEXT, place4 TEXT, place5 TEXT, place6 TEXT, place7 TEXT, place8 TEXT, place9 TEXT, place10 TEXT)'''
sql_insert_test_user = '''INSERT INTO users VALUES (0,'test', 0, 0, 'password', 0.0000000, 'passwordstatus',
'place1',  'place2', 'place3', 'place4', 'place5', 'place6', 'place7', 'place8', 'place9', 'place10')'''

#--------------------Сохранение данных-------------------------
async def save_data():
    to = time.time()
    sql = "SELECT * FROM users "
    cursor.execute(sql)
    data = cursor.fetchall()  # or use fetchone()
    try:
        # Переводим словарь в строку
        str_data=json.dumps(data)
        # Обновляем  наш файл с данными
        await bot.edit_message_media(InputMediaDocument(io.StringIO(str_data)), admin_id, config_id)
    except Exception as ex:
        print(ex)
    print('Время сохранения бекапа:='+str(time.time() - to))
  
#--------------------Метод при нажатии start-------------------------
@dp.message_handler(commands='start')
async def start(message: types.Message):
#--------------------Настройки аргументов sqlite3-------------------------
    sql_select = "SELECT * FROM users where chatid={}".format(message.chat.id)
    sql_insert = sql_ins.format(message.chat.id,message.chat.first_name, 0, 0, 'password', 0, 'passwordStatus',
                                'place1', 'place2', 'place3', 'place4', 'place5', 'place6', 'place7', 'place8', 'place9', 'place10')

    # Добавляем нового пользователя
    try:
        cursor.execute(sql_select)
        data = cursor.fetchone()
        if data is None:
            cursor.execute(sql_insert)
            conn.commit()
            await save_data()
    except Exception:
        data = await get_data()
        cursor.execute(sql_create)
        cursor.executemany(sql_insert_many, data)
        conn.commit()
        cursor.execute(sql_select)
        data = cursor.fetchone()
        if data is  None:
            cursor.execute(sql_insert)
            conn.commit()
            await save_data()
            
    await bot.send_message(message.chat.id,'Здравствуйте, вы кто? Напишите пароль!')
    
##-------------------Обработчик списка мест-----------------------------------------
    
@dp.callback_query_handler(lambda call: call.data.startswith('place')) 
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    global mode
    code = callback_query.data[-1]
    if code.isdigit():
        code = int(code)
    if code == 1:
        await bot.answer_callback_query(callback_query.id, text='Редактируем первое место')
        await bot.send_message(callback_query.from_user.id,'Введите первое место')
        mode = 'AskForPlaceMode_1'
    if code == 2:
        await bot.answer_callback_query(callback_query.id, text='Редактируем второе место')
        await bot.send_message(callback_query.from_user.id,'Введите второе место')
        mode = 'AskForPlaceMode_2'
    if code == 3:
        await bot.answer_callback_query(callback_query.id, text='Редактируем третье место')
        await bot.send_message(callback_query.from_user.id,'Введите третье место')
        mode = 'AskForPlaceMode_3'
    if code == 4:
        await bot.answer_callback_query(callback_query.id, text='Редактируем четвертое место')
        await bot.send_message(callback_query.from_user.id,'Введите четвертое место')
        mode = 'AskForPlaceMode_4'
    if code == 5:
        await bot.answer_callback_query(callback_query.id, text='Редактируем пятое место')
        await bot.send_message(callback_query.from_user.id,'Введите пятое место')
        mode = 'AskForPlaceMode_5'
    if code == 6:
        await bot.answer_callback_query(callback_query.id, text='Редактируем шестое место')
        await bot.send_message(callback_query.from_user.id,'Введите шестое место')
        mode = 'AskForPlaceMode_6'
    if code == 7:
        await bot.answer_callback_query(callback_query.id, text='Редактируем седьмое место')
        await bot.send_message(callback_query.from_user.id,'Введите седьмое место')
        mode = 'AskForPlaceMode_7'
    if code == 8:
        await bot.answer_callback_query(callback_query.id, text='Редактируем восьмое место')
        await bot.send_message(callback_query.from_user.id,'Введите восьмое место')
        mode = 'AskForPlaceMode_8'
    if code == 9:
        await bot.answer_callback_query(callback_query.id, text='Редактируем девятое место')
        await bot.send_message(callback_query.from_user.id,'Введите девятое место')
        mode = 'AskForPlaceMode_9'
    if code == 0:
        await bot.answer_callback_query(callback_query.id, text='Редактируем десятое место')
        await bot.send_message(callback_query.from_user.id,'Введите десятое место')
        mode = 'AskForPlaceMode_10'

    
#--------------------Основная логика бота-------------------------
@dp.message_handler()
async def main_logic(message: types.Message):
    #--------------------Настройки аргументов sqlite3-------------------------
    sql_select = "SELECT * FROM users where chatid={}".format(message.chat.id)    
    sql_insert = sql_ins.format(message.chat.id,message.chat.first_name, 0, 0, 'password', 0, 'passwordStatus',
                                'place1', 'place2', 'place3', 'place4', 'place5', 'place6', 'place7', 'place8', 'place9', 'place10')
    to=time.time()
# Логика для администратора
    if message.text == 'admin':
        cursor.execute(sql_create)
        cursor.execute(sql_insert_test_user)
        conn.commit() 
        cursor.execute("SELECT * FROM users ")
        data = cursor.fetchall()
        str_data = json.dumps(data)
        await bot.send_document(message.chat.id, io.StringIO(str_data))
        await bot.send_message(message.chat.id, 'admin_id = {}'.format(message.chat.id))
        await bot.send_message(message.chat.id, 'config_id = {}'.format(message.message_id+1))
        
# Логика для пользователя
    try:        
        cursor.execute("SELECT * FROM users where chatid={}".format(message.chat.id))
        data = cursor.fetchone()  # or use fetchone()
    except Exception:
        data = await get_data()
        cursor.execute(sql_create)
        cursor.executemany(sql_insert_many, data)
        conn.commit()        
        cursor.execute("SELECT * FROM users where chatid={}".format(message.chat.id))
        data = cursor.fetchone()  # or use fetchone()

        
#########################################################################        
##---------------------Админка для родителей---------------------------##
#########################################################################

        
    if data is not None:
        if message.text == 'Creator':
            global mode
            mode = 'CreatorMode'
            markup = types.InlineKeyboardMarkup() ##кнопка ссылка на сайт
            btn_my_site= types.InlineKeyboardButton(text='Generoom.ru', url='https://generoom.ru/kvest-dlya-detej-doma.html')
            markup.add(btn_my_site)
            await bot.send_message(message.chat.id,'''
{}, вы перешли в режим создателя игры.
Введите пароль для активации, полученный Вами на  e-mail при оплате.
Если вы еще не оплачивали, посетите наш сайт:'''.format(message.chat.first_name), reply_markup = markup)


##            ReplyKeboardRemove: ##убрать кнопки
##                @dp.message_handler(commands=['rm'])
##                async def process_rm_command(message: types.Message):
##                    await message.reply("Убираем шаблоны сообщений", reply_markup=kb.ReplyKeyboardRemove())

        if mode == 'CreatorMode':
            if message.text == 'Рейтинг': ## выводим вообще все данные из базы
                sql = "SELECT * FROM users ORDER BY progress" # DESC LIMIT 15
    ##            sql = "SELECT * FROM users where place1='в жопе'"
                cursor.execute(sql)
                newlist = cursor.fetchall()  # or use fetchone()
                sql_count = "SELECT COUNT(chatid) FROM users"
                cursor.execute(sql_count)
                count=cursor.fetchone()
                amount='Всего: {}\n'.format(count[0])
                await bot.send_message(message.chat.id, amount)
                i=0
                while i<count[0]:
                    await bot.send_message(message.chat.id, newlist[i])                
                    i+=1

            elif message.text == 'Доб':
                cursor.execute(sql_insert_test_user)
                conn.commit()
                await save_data()
            elif message.text == 'Дел':
                
                sql_insert = "DELETE FROM users WHERE name = '0'"
                cursor.execute(sql_insert)
                conn.commit()
                await save_data()
            elif message.text == 'DelAll':
                sql_insert = "DELETE FROM users"
                cursor.execute(sql_insert)
                conn.commit()
                await save_data()    
            elif message.text == 'Time':
                await bot.send_message(message.chat.id, time.time())

## Проверяем введенный пароль
            elif message.text != 'Creator':
                global pas
                pas=message.text
                try:##если пароль существует
                    cursor.execute('SELECT * FROM users WHERE password = ?', (pas,)) ## проверяем, есть ли такой пароль в базе
                    data = cursor.fetchone()
                    global PeriodTime
                    periodTime=14*24*60*60
 
                    
                    #активируем правильный пароль
                    if data[6]=='pStatus':                            
                        cursor.execute("UPDATE users SET activDate = ?, passwordStatus = ?, progress = ?, place1 = ?, place2 = ?, place3 = ?, place4 = ?, \
place5 = ?, place6 = ?, place7 = ?, place8 = ?, place9 = ?, place10 = ? WHERE password = ?", (time.time(), '1', 1, \
'в холодильнике', 'на окне', 'в шкафу', 'в рюкзаке', 'в ботинке', 'в кастрюле', 'в капюшоне куртки', 'под раковиной', 'под дверью', 'на столе', pas,))
                        conn.commit()
                        cursor.execute('SELECT * FROM users WHERE password = ?', (pas,)) ## загружаем обновленные данные
                        data = cursor.fetchone()
                        ##await bot.send_message(message.chat.id,''' {}, ваш пароль успешно активирован. '''.format(message.chat.first_name))
                        mode = 'AskForPlaceMode'




                    #пароль уже активирован, еще не истекло время с момента активации
                    if data[6]=='1':
                        if time.time()-data[5]>periodTime:  #проверяем, не истек ли срок действия пароля
                            cursor.execute("UPDATE users SET passwordStatus = ? WHERE password = ?", ('2', pas,))
                            conn.commit()
                            cursor.execute('SELECT * FROM users WHERE password = ?', (pas,)) ## проверяем, есть ли такой пароль в базе
                            data = cursor.fetchone()
                        global remainingTime ##оставшееся время
                        remainingTime=round((periodTime-time.time()+data[5])/60/60/24)
##                        await bot.send_message(message.chat.id,remainingTime)
                        text=message.chat.first_name+', ваш пароль принят. Срок активации истекает через '+str(remainingTime)
                        if remainingTime==0 or remainingTime>=5:
                            text=text+' дней'
                        if remainingTime>=2 and remainingTime<=4:
                            text=text+' дня'
                        if remainingTime==1:
                            text=text+' день'   
##                        await bot.send_message(message.chat.id,'''    {}, ваш пароль принят. '''.format(message.chat.first_name))
                        await bot.send_message(message.chat.id,text)
                        mode = 'AskForPlaceMode'

                        
                    # пароль есть, но уже закончил свое действие  passwordStatus = 2
                    if data[6] == '2':
                        await bot.send_message(message.chat.id,'''Истек срок действия пароля (2 недели с момента активации).
        Приобретите новый пароль на сайте https://generoom.ru/kvest-dlya-detej-doma.html''')
                        
                        

                        
                except Exception as ex: #пароль не существует
                    print(ex)
                    await bot.send_message(message.chat.id,' Пароль неверный. Попробуйте ещё раз')



                    
        if mode == 'AskForPlaceMode_1':
            cursor.execute("UPDATE users SET place1 = ? WHERE password = ?", (message.text, pas,))
        if mode == 'AskForPlaceMode_2':
            cursor.execute("UPDATE users SET place2 = ? WHERE password = ?", (message.text, pas,))
        if mode == 'AskForPlaceMode_3':
            cursor.execute("UPDATE users SET place3 = ? WHERE password = ?", (message.text, pas,))
        if mode == 'AskForPlaceMode_4':
            cursor.execute("UPDATE users SET place4 = ? WHERE password = ?", (message.text, pas,))
        if mode == 'AskForPlaceMode_5':
            cursor.execute("UPDATE users SET place5 = ? WHERE password = ?", (message.text, pas,))
        if mode == 'AskForPlaceMode_6':
            cursor.execute("UPDATE users SET place6 = ? WHERE password = ?", (message.text, pas,))
        if mode == 'AskForPlaceMode_7':
            cursor.execute("UPDATE users SET place7 = ? WHERE password = ?", (message.text, pas,))
        if mode == 'AskForPlaceMode_8':
            cursor.execute("UPDATE users SET place8 = ? WHERE password = ?", (message.text, pas,))
        if mode == 'AskForPlaceMode_9':
            cursor.execute("UPDATE users SET place9 = ? WHERE password = ?", (message.text, pas,))
        if mode == 'AskForPlaceMode_10':
            cursor.execute("UPDATE users SET place10 = ? WHERE password = ?", (message.text, pas,))





            
        if mode == 'AskForPlaceMode' or mode == 'AskForPlaceMode_1' or mode == 'AskForPlaceMode_2'\
           or mode == 'AskForPlaceMode_3' or mode == 'AskForPlaceMode_4' or mode == 'AskForPlaceMode_5' or mode == 'AskForPlaceMode_6'\
           or mode == 'AskForPlaceMode_7' or mode == 'AskForPlaceMode_8' or mode == 'AskForPlaceMode_9' or mode == 'AskForPlaceMode_10':

            conn.commit()
            cursor.execute('SELECT * FROM users WHERE password = ?', (pas,))
            data = cursor.fetchone()       
        
            markup = types.InlineKeyboardMarkup(row_width=2) ##кнопки список мест
            btn_place_1 = types.InlineKeyboardButton(text='1: '+data[7],  callback_data='place1')
            btn_place_2 = types.InlineKeyboardButton(text='2: '+data[8],  callback_data='place2')
            btn_place_3 = types.InlineKeyboardButton(text='3: '+data[9],  callback_data='place3')
            btn_place_4 = types.InlineKeyboardButton(text='4: '+data[10], callback_data='place4')
            btn_place_5 = types.InlineKeyboardButton(text='5: '+data[11], callback_data='place5')
            btn_place_6 = types.InlineKeyboardButton(text='6: '+data[12], callback_data='place6')
            btn_place_7 = types.InlineKeyboardButton(text='7: '+data[13], callback_data='place7')
            btn_place_8 = types.InlineKeyboardButton(text='8: '+data[14], callback_data='place8')
            btn_place_9 = types.InlineKeyboardButton(text='9: '+data[15], callback_data='place9')
            btn_place_10= types.InlineKeyboardButton(text='10: '+data[16], callback_data='place10')  
            markup.add(btn_place_1, btn_place_2, btn_place_3, btn_place_4, btn_place_5, btn_place_6, btn_place_7, btn_place_8, btn_place_9, btn_place_10)
            await bot.send_message(message.chat.id,'''
Вот список мест, нажмите на место, чтобы отредактировать его'''.format(message.chat.first_name), reply_markup = markup)


            
## Запрашиваем список мест

##                    if data[2]==1: # 1 место
##                        cursor.execute("UPDATE users SET place1 = ?, progress = ? WHERE password = ?", (message.text, 2, pas,))
##                        conn.commit()
##                        cursor.execute('SELECT * FROM users WHERE password = ?', (pas,)) ## загружаем обновленные данные
##                        data = cursor.fetchone()                        
##                    if data[2]==2: # 2 место
##                        cursor.execute("UPDATE users SET place2 = ?, progress = ? WHERE password = ?", (message.text, 3, pas,))
##                        conn.commit()                        
##                        cursor.execute('SELECT * FROM users WHERE password = ?', (pas,)) ## загружаем обновленные данные
##                        data = cursor.fetchone()
                        
##                await bot.send_message(message.chat.id, 'Отлично, первую подсказку положите {}'.format(str.lower(message.text),message.chat.id))
##                await bot.send_message(message.chat.id,'''
##Отлично, список мест готов! Вот он:
##1. {}
##Чтобы ввести все заново, нажмите кнопку /Creator
##Если все устраивает, нажмите /Save и перейдите в режим игрока
##Если игра будет на этом же устройстве, советуем сначала очистить историю сообщений, чтобы сохранить список мест в секрете. Пока что в секрете))
##'''.format(str.lower(message.text)))

                  

#------------------Создание паролей----------------
        if message.text == 'ДобПар':
            allpasswords  = [
                
            (0,'0', 0, 0, '1v2uea0v', 0, 'pStatus','на столе', 'на окне', 'в шкафу', 'в рюкзаке', 'в ботинке', 'в кастрюле', 'в капюшоне куртки', 'под раковиной', 'под дверью', 'в холодильнике'),
            (0,'0', 0, 0, 'qcr2a648', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'), 
            (0,'0', 0, 0, '26ymb9yg', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'y1xltpqc', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'l4nalvzy', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, '2cmp8k3j', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'), 
            (0,'0', 0, 0, 'w90hhdnw', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'cnfrhoss', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'db8ifc1x', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, '18infsmo', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'e993rrd6', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'avc3litp', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'), 
            (0,'0', 0, 0, 'ykogakfp', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, '5m8veix3', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'vd1gkwn6', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, '9fvphk1f', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'), 
            (0,'0', 0, 0, '3woprf75', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'sl5j7fy4', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, '3ql1qens', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 's00fnbsc', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'kmye9llx', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, '4txa63gh', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'), 
            (0,'0', 0, 0, 'grqxzbgf', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'olxle1js', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'hoa3858k', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, '6whe4q4b', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'), 
            (0,'0', 0, 0, '1i62lrj2', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'cznjfuac', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'v8jmqckj', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, '11zmjo7a', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'xhtosw3y', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'q6hzww0k', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'), 
            (0,'0', 0, 0, 'pa8xg3vk', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'k5zhx0wm', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'g93t7xfx', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'lgo1vxi6', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'), 
            (0,'0', 0, 0, 'cs0wlkxy', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'sijoslbz', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'fdwpuo22', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'buueznz3', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'p8s2jbon', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'xx64gw9t', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'), 
            (0,'0', 0, 0, 'ug5hdi64', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, '6vx5o3sx', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'zp74hio1', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'qwz684vg', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'), 
            (0,'0', 0, 0, 'rwn59438', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, '6tyd283t', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'ozxb2mzf', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, '8mdb7gro', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'm5sddnfl', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'n8rgw9h5', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'), 
            (0,'0', 0, 0, 'io0ocbbl', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'my1cwkew', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, '3lmvwrc5', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'zy93c554', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'), 
            (0,'0', 0, 0, '8700eof6', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, '990qca67', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, '8bvtg0jx', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'c3ah2q4z', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'k412whuh', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'poyzahwf', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'), 
            (0,'0', 0, 0, 'qs7dqiaf', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, '9ifopa5b', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, '1tcs65v4', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, '7ioxci9r', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'), 
            (0,'0', 0, 0, 'qexngt0u', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'dca9cd1x', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, '09bvvhin', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'pq03fopc', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'rjko5yj1', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'qyjrenvv', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'), 
            (0,'0', 0, 0, 'lgeyvp9g', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'zg3rnouf', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'ma70bd6q', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, '23tkli6q', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'), 
            (0,'0', 0, 0, 'p1iy8owo', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, '1brfkitl', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, '664ouaz9', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'yeswwjyn', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 's7ixedpa', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'y6d4szkh', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'), 
            (0,'0', 0, 0, 'j6y4la1c', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'mxl5nmt0', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'l68tm3z5', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'd8jgz94k', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'), 
            (0,'0', 0, 0, 'olox1njy', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, '2oe8fw51', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'qitp3r08', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'y9f4ga2d', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, '5c3c5bfo', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'ngcajh5y', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'), 
            (0,'0', 0, 0, 'yepc72lm', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'x9ewgmvu', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'vj13jmhy', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'rdh7v316', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'), 
            (0,'0', 0, 0, 'ahywbbp8', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'y6xc99pc', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 's71thngx', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            (0,'0', 0, 0, 'n6gyi6u4', 0, 'pStatus','1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            ]
            cursor.executemany(sql_insert_many, allpasswords)
            conn.commit()
            await save_data()

            
    else:
        await bot.send_message(message.chat.id, 'Вы не зарегистрированы')

        

            
    print(time.time()-to)
    

def timer_start():
    threading.Timer(30.0, timer_start).start()
    try:
        asyncio.run_coroutine_threadsafe(save_data(),bot.loop)
    except Exception as exc:
        pass

#--------------------Запуск бота-------------------------
if __name__ == '__main__':
    timer_start()
    executor.start_polling(dp, skip_updates=True)
print(data)

#------------------Проверка пароля----------------
##def check_password(password):
##        try:        
##        cursor.execute("SELECT * FROM users where chatid={}".format(message.chat.id))
##        data = cursor.fetchone()  # or use fetchone()
##    except Exception:
##        data = await get_data()
##        cursor.execute(sql_create)
##        cursor.executemany(sql_insert_many, data)
##        conn.commit()        
##        cursor.execute("SELECT * FROM users where chatid={}".format(message.chat.id))
##        data = cursor.fetchone()  # or use fetchone()


