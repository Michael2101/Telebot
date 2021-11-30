import os
import psycopg2
import telebot
import calendar
import datetime
from datetime import *

# загружаем токен в бота. Токен надо положить в файл .env
# в .env пишем token = "ваш токен"
from dotenv import load_dotenv
load_dotenv()
bot = telebot.TeleBot(os.environ.get("token"))

conn = psycopg2.connect(database="postgres",
                        user="postgres",
                        password="1234",
                        host="localhost", port="5432")
cursor = conn.cursor()


today = datetime.today()
a = (today.strftime("%Y"))
b = float(a)
if b // 2 != 0:
    weekStatus="Нижняя"
else:
    weekStatus="Верхняя"


@bot.message_handler(commands=["start"]) # приветственное сообщение
def start(message):
    bot.send_message(message.chat.id, "Здравствуйте, Я новый бот, который может помочь вам узнать расписание\n"
                                      "чтобы узнать список моих команд пропишите /help")


@bot.message_handler(commands=["timetable"])
def timetable(message):
    inLineKeyboard = telebot.types.InlineKeyboardMarkup()
    # тут добавляем кнопки. Каждая четвертая кнопка это новая строчка снизу
    # первая строчка кнопок
    inLineKeyboard.add(telebot.types.InlineKeyboardButton(text="ПН", callback_data="Понедельник"),
                       telebot.types.InlineKeyboardButton(text="ВТ", callback_data="Вторник"))
    # вторая строчка кнопок
    inLineKeyboard.add(telebot.types.InlineKeyboardButton(text="СР", callback_data="Среда"),
                       telebot.types.InlineKeyboardButton(text="ЧТ", callback_data="Четверг"),
                       telebot.types.InlineKeyboardButton(text="ПТ", callback_data="Пятница"))
    # третья сторочка кнопок
    inLineKeyboard.add(telebot.types.InlineKeyboardButton(text="Текущая неделя", callback_data="Тн"),
                       telebot.types.InlineKeyboardButton(text="Следующая неделя", callback_data="Сн"))
    bot.send_message(chat_id=message.chat.id, text="Выберите день недели", reply_markup=inLineKeyboard)

@bot.message_handler(commands=['help'])
def start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.chat.id, '\n Комады: \n /help - Общая документация и список команд '
                                      '\n /mtuci - отправляет вам ссылку на сайт МТУСИ '
                                      '\n /timetable- Показывает расписание'
                                      '\n /week - определяет четность недели (верхняя или нижняя).')

@bot.message_handler(commands=["mtuci"])
def help(message):
    bot.send_message(message.chat.id, "https://mtuci.ru")

@bot.message_handler(commands=["week"])
def help(message):
    today = datetime.today()
    a = (today.strftime("%Y"))
    b = float(a)
    if b // 2 != 0:
        bot.send_message(message.chat.id,'Нижняя неделя')
    else:
        bot.send_message(message.chat.id,'Верхняя неделя')


@bot.message_handler(content_types=["text"])
def answer(message):
    if message.text.lower() == "/start":
        bot.send_message(message.chat.id, "Здравствуйте ,  Я новый бот , который может помочь вам узнать расписание")
    elif message.text.lower() == "/mtuci":
        bot.send_message(message.chat.id, "https://mtuci.ru")
    elif message.text.lower() == "/help":
        bot.send_message(message.chat.id, '\n Комады: \n /help - Общая документация и список команд '
                                          '\n /mtuci - отправляет вам ссылку на сайт МТУСИ '
                                          '\n /timetable- Показывает расписание'
                                          '\n /week - определяет четность недели (верхняя или нижняя).')
    else:
        bot.send_message(message.chat.id,"Извините, я Вас не понял")


@bot.callback_query_handler(func=lambda call: True)
def timetable_handler(call):
    callBackData = call.data
    cid = call.message.chat.id
    if weekStatus == "Верхняя":
        if callBackData.startswith("Понедельник"):
            # callBackData - день недели, так что создавать переменную не надо
            # teachers - массив учителей и их id. Номер учителя в массиве это id-1 в формате [(id, full_name)]
            cursor.execute("SELECT id ,full_name FROM teacher")
            teachers = list(cursor.fetchall())
            # timetableList - расписание, после where писать, какая неделя и день недели
            # выводит в формате [(пара1), (пара2), (пара3)]
            # любая (пара) = ('Предмет', 'Номер Аудитории', 'Время')
            cursor.execute("SELECT timetable.subject, room_numb, start_time FROM timetable "
                            "WHERE weekstatus='Верхняя' and day='Понедельник'")
            timetablesList = list(cursor.fetchall())
            # в {} входят все данные, которые указываются после .format( в прямом порядке.
            # т.е. Первая указанная переменная после .format( заменяет первые {}
            bot.send_message(chat_id=cid, text="{}\n--------------------------------\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n".format(
                callBackData,
                timetablesList[0][0], timetablesList[0][1], timetablesList[0][2], teachers[14][1],
                timetablesList[1][0], timetablesList[1][1], timetablesList[1][2], teachers[12][1],
                timetablesList[2][0], timetablesList[2][1], timetablesList[2][2], teachers[10][1],
                timetablesList[3][0], timetablesList[3][1], timetablesList[3][2], teachers[10][1]))

        elif callBackData.startswith("Вторник"):
            # callBackData - день недели, так что создавать переменную не надо
            # teachers - массив учителей и их id. Номер учителя в массиве это id-1 в формате [(id, full_name)]
            cursor.execute("SELECT id ,full_name FROM teacher")
            teachers = list(cursor.fetchall())
            # timetableList - расписание, после where писать, какая неделя и день недели
            # выводит в формате [(пара1), (пара2), (пара3)]
            # любая (пара) = ('Предмет', 'Номер Аудитории', 'Время')
            cursor.execute("SELECT timetable.subject, room_numb, start_time FROM timetable "
                           "WHERE weekstatus='Верхняя' and day='Вторник'")
            timetablesList = list(cursor.fetchall())
            # в {} входят все данные, которые указываются после .format( в прямом порядке.
            # т.е. Первая указанная переменная после .format( заменяет первые {}
            bot.send_message(chat_id=cid, text="{}\n--------------------------------\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n".format(
                callBackData,
                timetablesList[0][0], timetablesList[0][1], timetablesList[0][2], teachers[2][1],
                timetablesList[1][0], timetablesList[1][1], timetablesList[1][2], teachers[2][1],
                timetablesList[2][0], timetablesList[2][1], timetablesList[2][2], teachers[0][1],
                timetablesList[3][0], timetablesList[3][1], timetablesList[3][2], teachers[7][1],
                timetablesList[4][0], timetablesList[4][1], timetablesList[4][2], teachers[11][1],
            ))
        elif callBackData.startswith("Среда"):
            # callBackData - день недели, так что создавать переменную не надо
            # teachers - массив учителей и их id. Номер учителя в массиве это id-1 в формате [(id, full_name)]
            cursor.execute("SELECT id ,full_name FROM teacher")
            teachers = list(cursor.fetchall())
            # timetableList - расписание, после where писать, какая неделя и день недели
            # выводит в формате [(пара1), (пара2), (пара3)]
            # любая (пара) = ('Предмет', 'Номер Аудитории', 'Время')
            cursor.execute("SELECT timetable.subject, room_numb, start_time FROM timetable "
                           "WHERE weekstatus='Верхняя' and day='Среда'")
            timetablesList = list(cursor.fetchall())
            # в {} входят все данные, которые указываются после .format( в прямом порядке.
            # т.е. Первая указанная переменная после .format( заменяет первые {}
            bot.send_message(chat_id=cid, text="{}\n--------------------------------\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n".format(

                callBackData,
                timetablesList[0][0], timetablesList[0][1], timetablesList[0][2], teachers[15][1],
                timetablesList[1][0], timetablesList[1][1], timetablesList[1][2], teachers[9][1],
            ))
        elif callBackData.startswith("Четверг"):
            # callBackData - день недели, так что создавать переменную не надо
            # teachers - массив учителей и их id. Номер учителя в массиве это id-1 в формате [(id, full_name)]
            cursor.execute("SELECT id ,full_name FROM teacher")
            teachers = list(cursor.fetchall())
            # timetableList - расписание, после where писать, какая неделя и день недели
            # выводит в формате [(пара1), (пара2), (пара3)]
            # любая (пара) = ('Предмет', 'Номер Аудитории', 'Время')
            cursor.execute("SELECT timetable.subject, room_numb, start_time FROM timetable "
                           "WHERE weekstatus='Верхняя' and day='Четверг'")
            timetablesList = list(cursor.fetchall())
            # в {} входят все данные, которые указываются после .format( в прямом порядке.
            # т.е. Первая указанная переменная после .format( заменяет первые {}
            bot.send_message(chat_id=cid, text="{}\n--------------------------------\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n".format(

                callBackData,
                timetablesList[0][0], timetablesList[0][1], timetablesList[0][2], teachers[1][1],
                timetablesList[1][0], timetablesList[1][1], timetablesList[1][2], teachers[2][1],
                timetablesList[2][0], timetablesList[2][1], timetablesList[2][2], teachers[2][1],
                timetablesList[3][0], timetablesList[3][1], timetablesList[3][2], teachers[13][1],
            ))
        elif callBackData.startswith("Пятница"):
            # callBackData - день недели, так что создавать переменную не надо
            # teachers - массив учителей и их id. Номер учителя в массиве это id-1 в формате [(id, full_name)]
            cursor.execute("SELECT id ,full_name FROM teacher")
            teachers = list(cursor.fetchall())
            # timetableList - расписание, после where писать, какая неделя и день недели
            # выводит в формате [(пара1), (пара2), (пара3)]
            # любая (пара) = ('Предмет', 'Номер Аудитории', 'Время')
            cursor.execute("SELECT timetable.subject, room_numb, start_time FROM timetable "
                           "WHERE weekstatus='Верхняя' and day='Пятница'")
            timetablesList = list(cursor.fetchall())
            # в {} входят все данные, которые указываются после .format( в прямом порядке.
            # т.е. Первая указанная переменная после .format( заменяет первые {}
            bot.send_message(chat_id=cid, text="{}\n--------------------------------\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n".format(

                callBackData,
                timetablesList[0][0], timetablesList[0][1], timetablesList[0][2], teachers[9][1],
                timetablesList[1][0], timetablesList[1][1], timetablesList[1][2], teachers[6][1],

            ))
        elif callBackData.startswith("Тн"):
            cursor.execute("SELECT id ,full_name FROM teacher")
            teachers = list(cursor.fetchall())

            cursor.execute("SELECT timetable.subject, room_numb, start_time FROM timetable "
                           "WHERE weekstatus='Верхняя' and day='Понедельник'")
            timetablesMonday = list(cursor.fetchall())

            cursor.execute("SELECT timetable.subject, room_numb, start_time FROM timetable "
                           "WHERE weekstatus='Верхняя' and day='Вторник'")
            timetablesThuesday = list(cursor.fetchall())

            cursor.execute("SELECT timetable.subject, room_numb, start_time FROM timetable "
                           "WHERE weekstatus='Верхняя' and day='Среда'")
            timetablesWednesday = list(cursor.fetchall())

            cursor.execute("SELECT timetable.subject, room_numb, start_time FROM timetable "
                           "WHERE weekstatus='Верхняя' and day='Четверг'")
            timetablesThursday = list(cursor.fetchall())

            cursor.execute("SELECT timetable.subject, room_numb, start_time FROM timetable "
                           "WHERE weekstatus='Верхняя' and day='Пятница'")
            timetablesFriday = list(cursor.fetchall())

            bot.send_message(chat_id=cid, text="Понедельник\n--------------------------------\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nВторник\n-------------------------------------\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nСреда\n--------------------------------\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nЧетверг\n--------------------------------\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПятница\n--------------------------------\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n".format(

                timetablesMonday[0][0], timetablesMonday[0][1], timetablesMonday[0][2], teachers[14][1],
                timetablesMonday[1][0], timetablesMonday[1][1], timetablesMonday[1][2], teachers[12][1],
                timetablesMonday[2][0], timetablesMonday[2][1], timetablesMonday[2][2], teachers[10][1],
                timetablesMonday[3][0], timetablesMonday[3][1], timetablesMonday[3][2], teachers[10][1],

                timetablesThuesday[0][0], timetablesThuesday[0][1], timetablesThuesday[0][2], teachers[2][1],
                timetablesThuesday[1][0], timetablesThuesday[1][1], timetablesThuesday[1][2], teachers[2][1],
                timetablesThuesday[2][0], timetablesThuesday[2][1], timetablesThuesday[2][2], teachers[0][1],
                timetablesThuesday[3][0], timetablesThuesday[3][1], timetablesThuesday[3][2], teachers[7][1],
                timetablesThuesday[4][0], timetablesThuesday[4][1], timetablesThuesday[4][2], teachers[11][1],

                timetablesWednesday[0][0], timetablesWednesday[0][1], timetablesWednesday[0][2], teachers[15][1],
                timetablesWednesday[1][0], timetablesWednesday[1][1], timetablesWednesday[1][2], teachers[9][1],

                timetablesThursday[0][0], timetablesThursday[0][1], timetablesThursday[0][2], teachers[1][1],
                timetablesThursday[1][0], timetablesThursday[1][1], timetablesThursday[1][2], teachers[2][1],
                timetablesThursday[2][0], timetablesThursday[2][1], timetablesThursday[2][2], teachers[2][1],
                timetablesThursday[3][0], timetablesThursday[3][1], timetablesThursday[3][2], teachers[13][1],

                timetablesFriday[0][0], timetablesFriday[0][1], timetablesFriday[0][2], teachers[9][1],
                timetablesFriday[1][0], timetablesFriday[1][1], timetablesFriday[1][2], teachers[6][1],
            ))


        elif callBackData.startswith("Сн"):
            cursor.execute("SELECT id ,full_name FROM teacher")
            teachers = list(cursor.fetchall())

            cursor.execute("SELECT timetable.subject, room_numb, start_time FROM timetable "
                           "WHERE weekstatus='Нижняя' and day='Понедельник'")
            timetablesMonday = list(cursor.fetchall())

            cursor.execute("SELECT timetable.subject, room_numb, start_time FROM timetable "
                           "WHERE weekstatus='Нижняя' and day='Вторник'")
            timetablesThuesday = list(cursor.fetchall())

            cursor.execute("SELECT timetable.subject, room_numb, start_time FROM timetable "
                           "WHERE weekstatus='Нижняя' and day='Среда'")
            timetablesWednesday = list(cursor.fetchall())

            cursor.execute("SELECT timetable.subject, room_numb, start_time FROM timetable "
                           "WHERE weekstatus='Нижняя' and day='Четверг'")
            timetablesThursday = list(cursor.fetchall())

            cursor.execute("SELECT timetable.subject, room_numb, start_time FROM timetable "
                           "WHERE weekstatus='Нижняя' and day='Пятница'")
            timetablesFriday = list(cursor.fetchall())

            bot.send_message(chat_id=cid, text="Понедельник\n--------------------------------\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nВторник\n-------------------------------------\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"                                               
                                               "\nСреда\n--------------------------------\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nЧетверг\n--------------------------------\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПятница\n--------------------------------\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n".format(

                timetablesMonday[0][0], timetablesMonday[0][1], timetablesMonday[0][2], teachers[14][1],
                timetablesMonday[1][0], timetablesMonday[1][1], timetablesMonday[1][2], teachers[12][1],
                timetablesMonday[2][0], timetablesMonday[2][1], timetablesMonday[2][2], teachers[10][1],
                timetablesMonday[3][0], timetablesMonday[3][1], timetablesMonday[3][2], teachers[10][1],

                timetablesThuesday[0][0], timetablesThuesday[0][1], timetablesThuesday[0][2], teachers[2][1],
                timetablesThuesday[1][0], timetablesThuesday[1][1], timetablesThuesday[1][2], teachers[2][1],

                timetablesWednesday[0][0], timetablesWednesday[0][1], timetablesWednesday[0][2], teachers[7][1],
                timetablesWednesday[1][0], timetablesWednesday[1][1], timetablesWednesday[1][2], teachers[9][1],

                timetablesThursday[0][0], timetablesThursday[0][1], timetablesThursday[0][2], teachers[0][1],
                timetablesThursday[1][0], timetablesThursday[1][1], timetablesThursday[1][2], teachers[0][1],

                timetablesFriday[0][0], timetablesFriday[0][1], timetablesFriday[0][2], teachers[9][1],
                timetablesFriday[1][0], timetablesFriday[1][1], timetablesFriday[1][2], teachers[6][1],
            ))
        else: bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Ты как это сделал чёрт?")

    elif weekStatus == "Нижняя":
        if callBackData.startswith("Понедельник"):
            # callBackData - день недели, так что создавать переменную не надо
            # teachers - массив учителей и их id. Номер учителя в массиве это id-1 в формате [(id, full_name)]
            cursor.execute("SELECT id ,full_name FROM teacher")
            teachers = list(cursor.fetchall())
            # timetableList - расписание, после where писать, какая неделя и день недели
            # выводит в формате [(пара1), (пара2), (пара3)]
            # любая (пара) = ('Предмет', 'Номер Аудитории', 'Время')
            cursor.execute("SELECT timetable.subject, room_numb, start_time FROM timetable "
                           "WHERE weekstatus='Нижняя' and day='Понедельник'")
            timetablesList = list(cursor.fetchall())
            # в {} входят все данные, которые указываются после .format( в прямом порядке.
            # т.е. Первая указанная переменная после .format( заменяет первые {}
            bot.send_message(chat_id=cid, text="{}\n--------------------------------\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n".format(

                callBackData,
                timetablesList[0][0], timetablesList[0][1], timetablesList[0][2], teachers[14][1],
                timetablesList[1][0], timetablesList[1][1], timetablesList[1][2], teachers[12][1],
                timetablesList[2][0], timetablesList[2][1], timetablesList[2][2], teachers[10][1],
                ))

        elif callBackData.startswith("Вторник"):
            # callBackData - день недели, так что создавать переменную не надо
            # teachers - массив учителей и их id. Номер учителя в массиве это id-1 в формате [(id, full_name)]
            cursor.execute("SELECT id ,full_name FROM teacher")
            teachers = list(cursor.fetchall())
            # timetableList - расписание, после where писать, какая неделя и день недели
            # выводит в формате [(пара1), (пара2), (пара3)]
            # любая (пара) = ('Предмет', 'Номер Аудитории', 'Время')
            cursor.execute("SELECT timetable.subject, room_numb, start_time FROM timetable "
                           "WHERE weekstatus='Нижняя' and day='Вторник'")
            timetablesList = list(cursor.fetchall())
            # в {} входят все данные, которые указываются после .format( в прямом порядке.
            # т.е. Первая указанная переменная после .format( заменяет первые {}
            bot.send_message(chat_id=cid, text="{}\n--------------------------------\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n".format(
                callBackData,
                timetablesList[0][0], timetablesList[0][1], timetablesList[0][2], teachers[2][1],
                timetablesList[1][0], timetablesList[1][1], timetablesList[1][2], teachers[2][1],))
        elif callBackData.startswith("Среда"):
            # callBackData - день недели, так что создавать переменную не надо
            # teachers - массив учителей и их id. Номер учителя в массиве это id-1 в формате [(id, full_name)]
            cursor.execute("SELECT id ,full_name FROM teacher")
            teachers = list(cursor.fetchall())
            # timetableList - расписание, после where писать, какая неделя и день недели
            # выводит в формате [(пара1), (пара2), (пара3)]
            # любая (пара) = ('Предмет', 'Номер Аудитории', 'Время')
            cursor.execute("SELECT timetable.subject, room_numb, start_time FROM timetable "
                           "WHERE weekstatus='Верхняя' and day='Среда'")
            timetablesList = list(cursor.fetchall())
            # в {} входят все данные, которые указываются после .format( в прямом порядке.
            # т.е. Первая указанная переменная после .format( заменяет первые {}
            bot.send_message(chat_id=cid, text="{}\n--------------------------------\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n".format(

                callBackData,
                timetablesList[0][0], timetablesList[0][1], timetablesList[0][2], teachers[7][1],
                timetablesList[1][0], timetablesList[1][1], timetablesList[1][2], teachers[9][1],
            ))
        elif callBackData.startswith("Четверг"):
            # callBackData - день недели, так что создавать переменную не надо
            # teachers - массив учителей и их id. Номер учителя в массиве это id-1 в формате [(id, full_name)]
            cursor.execute("SELECT id ,full_name FROM teacher")
            teachers = list(cursor.fetchall())
            # timetableList - расписание, после where писать, какая неделя и день недели
            # выводит в формате [(пара1), (пара2), (пара3)]
            # любая (пара) = ('Предмет', 'Номер Аудитории', 'Время')
            cursor.execute("SELECT timetable.subject, room_numb, start_time FROM timetable "
                           "WHERE weekstatus='Нижняя' and day='Четверг'")
            timetablesList = list(cursor.fetchall())
            # в {} входят все данные, которые указываются после .format( в прямом порядке.
            # т.е. Первая указанная переменная после .format( заменяет первые {}
            bot.send_message(chat_id=cid, text="{}\n--------------------------------\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n".format(


                callBackData,
                timetablesList[0][0], timetablesList[0][1], timetablesList[0][2], teachers[0][1],
                timetablesList[1][0], timetablesList[1][1], timetablesList[1][2], teachers[0][1],

            ))
        elif callBackData.startswith("Пятница"):
            # callBackData - день недели, так что создавать переменную не надо
            # teachers - массив учителей и их id. Номер учителя в массиве это id-1 в формате [(id, full_name)]
            cursor.execute("SELECT id ,full_name FROM teacher")
            teachers = list(cursor.fetchall())
            # timetableList - расписание, после where писать, какая неделя и день недели
            # выводит в формате [(пара1), (пара2), (пара3)]
            # любая (пара) = ('Предмет', 'Номер Аудитории', 'Время')
            cursor.execute("SELECT timetable.subject, room_numb, start_time FROM timetable "
                           "WHERE weekstatus='Верхняя' and day='Пятница'")
            timetablesList = list(cursor.fetchall())
            # в {} входят все данные, которые указываются после .format( в прямом порядке.
            # т.е. Первая указанная переменная после .format( заменяет первые {}
            bot.send_message(chat_id=cid, text="{}\n--------------------------------\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n".format(

                callBackData,
                timetablesList[0][0], timetablesList[0][1], timetablesList[0][2], teachers[9][1],
                timetablesList[1][0], timetablesList[1][1], timetablesList[1][2], teachers[6][1],

            ))

        elif callBackData.startswith("Тн"):
            cursor.execute("SELECT id ,full_name FROM teacher")
            teachers = list(cursor.fetchall())

            cursor.execute("SELECT timetable.subject, room_numb, start_time FROM timetable "
                           "WHERE weekstatus='Верхняя' and day='Понедельник'")
            timetablesMonday = list(cursor.fetchall())

            cursor.execute("SELECT timetable.subject, room_numb, start_time FROM timetable "
                           "WHERE weekstatus='Верхняя' and day='Вторник'")
            timetablesThuesday = list(cursor.fetchall())

            cursor.execute("SELECT timetable.subject, room_numb, start_time FROM timetable "
                           "WHERE weekstatus='Верхняя' and day='Среда'")
            timetablesWednesday = list(cursor.fetchall())

            cursor.execute("SELECT timetable.subject, room_numb, start_time FROM timetable "
                           "WHERE weekstatus='Верхняя' and day='Четверг'")
            timetablesThursday = list(cursor.fetchall())

            cursor.execute("SELECT timetable.subject, room_numb, start_time FROM timetable "
                           "WHERE weekstatus='Верхняя' and day='Пятница'")
            timetablesFriday = list(cursor.fetchall())

            bot.send_message(chat_id=cid, text="Понедельник\n--------------------------------\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nВторник\n-------------------------------------\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nСреда\n--------------------------------\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nЧетверг\n--------------------------------\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПятница\n--------------------------------\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n".format(

                timetablesMonday[0][0], timetablesMonday[0][1], timetablesMonday[0][2], teachers[14][1],
                timetablesMonday[1][0], timetablesMonday[1][1], timetablesMonday[1][2], teachers[12][1],
                timetablesMonday[2][0], timetablesMonday[2][1], timetablesMonday[2][2], teachers[10][1],
                timetablesMonday[3][0], timetablesMonday[3][1], timetablesMonday[3][2], teachers[10][1],

                timetablesThuesday[0][0], timetablesThuesday[0][1], timetablesThuesday[0][2], teachers[2][1],
                timetablesThuesday[1][0], timetablesThuesday[1][1], timetablesThuesday[1][2], teachers[2][1],
                timetablesThuesday[2][0], timetablesThuesday[2][1], timetablesThuesday[2][2], teachers[0][1],
                timetablesThuesday[3][0], timetablesThuesday[3][1], timetablesThuesday[3][2], teachers[7][1],
                timetablesThuesday[4][0], timetablesThuesday[4][1], timetablesThuesday[4][2], teachers[11][1],

                timetablesWednesday[0][0], timetablesWednesday[0][1], timetablesWednesday[0][2], teachers[15][1],
                timetablesWednesday[1][0], timetablesWednesday[1][1], timetablesWednesday[1][2], teachers[9][1],

                timetablesThursday[0][0], timetablesThursday[0][1], timetablesThursday[0][2], teachers[1][1],
                timetablesThursday[1][0], timetablesThursday[1][1], timetablesThursday[1][2], teachers[2][1],
                timetablesThursday[2][0], timetablesThursday[2][1], timetablesThursday[2][2], teachers[2][1],
                timetablesThursday[3][0], timetablesThursday[3][1], timetablesThursday[3][2], teachers[13][1],

                timetablesFriday[0][0], timetablesFriday[0][1], timetablesFriday[0][2], teachers[9][1],
                timetablesFriday[1][0], timetablesFriday[1][1], timetablesFriday[1][2], teachers[6][1],
            ))
        elif callBackData.startswith("Сн"):
            cursor.execute("SELECT id ,full_name FROM teacher")
            teachers = list(cursor.fetchall())

            cursor.execute("SELECT timetable.subject, room_numb, start_time FROM timetable "
                           "WHERE weekstatus='Нижняя' and day='Понедельник'")
            timetablesMonday = list(cursor.fetchall())

            cursor.execute("SELECT timetable.subject, room_numb, start_time FROM timetable "
                           "WHERE weekstatus='Нижняя' and day='Вторник'")
            timetablesThuesday = list(cursor.fetchall())

            cursor.execute("SELECT timetable.subject, room_numb, start_time FROM timetable "
                           "WHERE weekstatus='Нижняя' and day='Среда'")
            timetablesWednesday = list(cursor.fetchall())

            cursor.execute("SELECT timetable.subject, room_numb, start_time FROM timetable "
                           "WHERE weekstatus='Нижняя' and day='Четверг'")
            timetablesThursday = list(cursor.fetchall())

            cursor.execute("SELECT timetable.subject, room_numb, start_time FROM timetable "
                           "WHERE weekstatus='Нижняя' and day='Пятница'")
            timetablesFriday = list(cursor.fetchall())

            bot.send_message(chat_id=cid, text="Понедельник\n--------------------------------\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nВторник\n-------------------------------------\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nСреда\n--------------------------------\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nЧетверг\n--------------------------------\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПятница\n--------------------------------\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n"
                                               "\nПредмет: {}\nАудитория: {}\nВремя: {}\nПреподаватель: {}\n".format(

                timetablesMonday[0][0], timetablesMonday[0][1], timetablesMonday[0][2], teachers[14][1],
                timetablesMonday[1][0], timetablesMonday[1][1], timetablesMonday[1][2], teachers[12][1],
                timetablesMonday[2][0], timetablesMonday[2][1], timetablesMonday[2][2], teachers[10][1],


                timetablesThuesday[0][0], timetablesThuesday[0][1], timetablesThuesday[0][2], teachers[2][1],
                timetablesThuesday[1][0], timetablesThuesday[1][1], timetablesThuesday[1][2], teachers[2][1],

                timetablesWednesday[0][0], timetablesWednesday[0][1], timetablesWednesday[0][2], teachers[7][1],
                timetablesWednesday[1][0], timetablesWednesday[1][1], timetablesWednesday[1][2], teachers[9][1],

                timetablesThursday[0][0], timetablesThursday[0][1], timetablesThursday[0][2], teachers[0][1],
                timetablesThursday[1][0], timetablesThursday[1][1], timetablesThursday[1][2], teachers[0][1],

                timetablesFriday[0][0], timetablesFriday[0][1], timetablesFriday[0][2], teachers[9][1],
                timetablesFriday[1][0], timetablesFriday[1][1], timetablesFriday[1][2], teachers[6][1],
            ))
        else: bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Ты как это сделал чёрт?")

bot.infinity_polling()