import telebot
import json
import os
from telebot.types import ReplyKeyboardMarkup
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from gazpacho import Soup, get
from youtubesearchpython import VideosSearch
TOKEN = '6006612958:AAEoHenPn-U4fYtw6ZEzyUl9s1EoojzesN0'
IN_MAIN_MENU = False
IN_INFO = False
MCI_list = []
bot = telebot.TeleBot(TOKEN)
if os.path.exists('users_data.json'):
    with open('users_data.json') as file:
        users_info = json.load(file)
else:
    users_info = {}


@bot.message_handler(commands=['start'])
def bot_start(message):
    global users_info
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}, я - бот, который поможет тебе найти '
                                      f'самые выгодные цены на товары,'
                                      f'а также подскажет тебе telegram - каналы, основываясь на своих интересах.'
                                      f'Еще в меню вы сможете послушать музыку, которую я подберу.'
                                      f'Информация будет со временем обновляться автоматически, поэтому '
                                      f'не забывайте сюда заглядывать.')

    users_info.setdefault(str(message.chat.id), {})
    if len(users_info[str(message.chat.id)]) == 0:
        films(message)
    else:
        main_menu(message)


def films(message):
    global IN_INFO
    IN_INFO = True
    users_info[str(message.chat.id)] = {}
    users_info[str(message.chat.id)].setdefault('Name', message.from_user.first_name)
    users_info[str(message.chat.id)].setdefault('Surname', message.from_user.last_name)
    bot.send_message(message.chat.id, 'Для моей корректной работы мне необходимо узнать'
                                      ' побольше о вас.')
    bot.send_chat_action(message.chat.id, 'typing')
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = 'Да ✅'
    button2 = 'Нет ❌'
    markup.row(button1, button2)
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, 'Скажите, вы любите кино? 🎬',  reply_markup=markup)
    bot.register_next_step_handler(message, music)


def music(message):
    global users_info
    users_info[str(message.chat.id)].setdefault('interests', {})
    users_info[str(message.chat.id)]['interests']['Films'] = message.text
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = 'Да ✅'
    button2 = 'Нет ❌'
    markup.row(button1, button2)
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, f'А нравится ли вам слушать музыку? 🎶', reply_markup=markup)
    bot.register_next_step_handler(message, travel)


def travel(message):
    global users_info
    users_info[str(message.chat.id)]['interests']['Music'] = message.text
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = 'Да ✅'
    button2 = 'Нет ❌'
    markup.row(button1, button2)
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, 'Скажите, любите ли вы туризм? ⛺', reply_markup=markup)
    bot.register_next_step_handler(message, sport)


def sport(message):
    global users_info
    users_info[str(message.chat.id)]['interests']['Travel'] = message.text
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = 'Да ✅'
    button2 = 'Нет ❌'
    markup.row(button1, button2)
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, 'Мне кажется, вы любите спорт, ведь так? 🏋️‍🚴', reply_markup=markup)
    bot.register_next_step_handler(message, end_interests)


def end_interests(message):
    global users_info, IN_INFO
    users_info[str(message.chat.id)]['interests']['Sport'] = message.text
    print(users_info)
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, 'Спасибо, этой информации будет достаточно, чтобы я мог работать правильно )')

    with open('users_data.json', 'w') as file:
        json.dump(users_info, file, indent=4)
    IN_INFO = False
    main_menu(message)


def main_menu(message):
    global IN_MAIN_MENU
    IN_MAIN_MENU = True
    users_info[str(message.chat.id)].setdefault('comment', '')
    bot.send_chat_action(message.chat.id, 'typing')
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    sales_button = '1. Промокоды и скидки 💲 🛒'
    telegram_button = '2. Telegram - каналы 📰'
    music_buton = '3. Музыка 🎧'
    YouTube_button = '4. YouTube (beta)▶️'
    profile_button = '5. Профиль 👤'
    info_button = '6. Info ℹ️'
    markup.row(sales_button, telegram_button).row(music_buton, YouTube_button).row(profile_button).row(info_button)
    bot.send_message(message.chat.id, f'Добро пожаловать в главное меню.'
                                      f'Здесь вам доступен основной функционал бота.', reply_markup=markup)
    bot.register_next_step_handler(message, choose)
    IN_MAIN_MENU = False


def choose(message):
    global IN_MAIN_MENU
    try:
        if '1' in message.text.lower():
            bot.send_message(message.chat.id, f'Сейчас я подберу вам предложения, основываясь на ваших интрересах)')
            if 'Да' in users_info[str(message.chat.id)]['interests']['Travel']:
                travel_sales(message)
            if 'Да' in users_info[str(message.chat.id)]['interests']['Sport']:
                sport_sales(message)
            if 'Нет' in users_info[str(message.chat.id)]['interests']['Sport'] and 'Нет' in users_info[str(message.chat.id)]['interests']['Travel']:
                bot.send_message(message.chat.id, f'К сожалению, на данный момент подходящих по вашим интересам скидок нет')
            main_menu(message)
        elif '2' in message.text.lower():
            bot.send_message(message.chat.id, f'Сейчас я поищу телеграм - каналы для вас )')
            if 'Да' in users_info[str(message.chat.id)]['interests']['Travel']:
                telegram_travel(message)
            if 'Да' in users_info[str(message.chat.id)]['interests']['Films']:
                telegram_films(message)
            if 'Да' in users_info[str(message.chat.id)]['interests']['Sport']:
                telegram_sport(message)
            if 'Да' in users_info[str(message.chat.id)]['interests']['Music']:
                telegram_music(message)
            main_menu(message)
        elif '4' in message.text.lower():
            bot.send_chat_action(message.chat.id, 'typing')
            bot.send_message(message.chat.id, f'Отправьте мне текстовый запрос,'
                                              f' и я постараюсь найти вам самое подходящее видео )')
            bot.register_next_step_handler(message, youtube_search)
        elif '5' in message.text.lower():
            markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            button1 = '1. Изменить интересы'
            button3 = '3. Назад'
            button2 = '2. Оставить отзыв'
            markup.row(button1).row(button2).row(button3)
            bot.send_message(message.chat.id, f'----Профиль----\n\n'
                                    f'Имя: {users_info[str(message.chat.id)]["Name"]}\n'
                                    f'Фамилия: {users_info[str(message.chat.id)]["Surname"]}\n'
                                    f'Никнейм: {message.from_user.username}\n\n'
                                    f'Ваши интересы:\n🎬 Фильмы - {users_info[str(message.chat.id)]["interests"]["Films"]}\n'
                                    f'🎵 Музыка - {users_info[str(message.chat.id)]["interests"]["Music"]}\n'
                                    f'🏜 Путешествия - {users_info[str(message.chat.id)]["interests"]["Travel"]}\n'
                                    f'⛹ Спорт - {users_info[str(message.chat.id)]["interests"]["Sport"]}',
                         reply_markup=markup)
            bot.register_next_step_handler(message, profile_choose)
        elif '3' in message.text.lower():
            bot.send_chat_action(message.chat.id, 'typing')
            bot.send_message(message.chat.id, f'Сейчас я пришлю вам музыкальные новинки за последний месяц 😎')
            music_top(message)
        elif '6' in message.text.lower():
            info(message)
        else:
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            IN_MAIN_MENU = True
            sales_button = '1. Промокоды и скидки 💲 🛒'
            telegram_button = '2. Тг - каналы 📰'
            music_buton = '3. Музыка 🎧'
            profile_button = '4. Профиль 👤'
            info_button = '6. Info'
            youtube_button = '5. YouTube (beta)'
            markup.row(sales_button, telegram_button).row(music_buton, youtube_button).row(profile_button).row(info_button)
            bot.send_message(message.chat.id, f'Ответ не распознан. Повторите попытку ввода.', reply_markup=markup)
            bot.register_next_step_handler(message, choose)
            IN_MAIN_MENU = False
    except Exception:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        sales_button = '1. Промокоды и скидки 💲 🛒'
        telegram_button = '2. Тг - каналы 📰'
        music_buton = '3. Музыка 🎧'
        profile_button = '4. Профиль 👤'
        info_button = '6. Info'
        youtube_button = '5. YouTube (beta)'
        markup.row(sales_button, telegram_button).row(music_buton, youtube_button).row(profile_button).row(info_button)
        bot.send_message(message.chat.id, f'Ответ не распознан. Повторите попытку ввода.', reply_markup=markup)
        bot.register_next_step_handler(message, choose)


def profile_choose(message):
    markup = ReplyKeyboardRemove()
    if '3' in message.text:
        main_menu(message)
    elif '1' in message.text:
        bot.send_message(message.chat.id, f'Я обнулил информацию о ваших интересах.')
        films(message)
    elif '2' in message.text:
        if users_info[str(message.chat.id)]['comment'] == '':
            bot.send_message(message.chat.id, f'Оставьте ваши пожелания или отзыв и я передам их разработчику:', reply_markup=markup)
            bot.register_next_step_handler(message, send_comment)
        elif users_info[str(message.chat.id)]['comment'] != '':
            bot.send_message(message.chat.id, f'Вот старый текст вашего комментария:\n\n'
                                              f'{users_info[str(message.chat.id)]["comment"]}\n\n'
                                              f'Оставьте ваши пожелания или отзыв и я передам их разработчику:', reply_markup=markup)
            bot.register_next_step_handler(message, send_comment)





def travel_sales(message):
    global current_page_travel, num_of_page_travel, link_list_travel, title_list_travel, MCI
    url = 'https://www.pepper.ru/groups/travel'
    data = get(url)
    html = Soup(data)
    a = html.find('a', {'class': 'cept-tt thread-link linkPlain thread-title--list js-thread-title'})
    a = ''.join(map(str, a))
    a = a.split('</a>')
    title_list_travel = []
    link_list_travel = []
    for i in a:
        title = i[83:i.find('href') - 2]
        title_list_travel.append(title)
        print(title)
        link_list_travel.append(i[i.find('href="') + 6: i.find('data-t') - 2])
    print(link_list_travel)
    for i in range(len(link_list_travel)):
        if len(link_list_travel[i]) == 0:
            link_list_travel.pop(i)
    print(link_list_travel)
    for j in range(len(title_list_travel)):
        if len(title_list_travel[j]) == 0:
            title_list_travel.pop(j)
    print(title_list_travel)
    num_of_page_travel = 1
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(text='⬅️', callback_data='back_travel')
    button2 = InlineKeyboardButton(text='➡️', callback_data='forward_travel')
    button3 = InlineKeyboardButton(text=f'{num_of_page_travel}/{len(link_list_travel)}', callback_data='---')
    button4 = InlineKeyboardButton(text='❌', callback_data='delete_travel')
    markup.add(button1, button3, button2).add(button4)
    current_page_travel = bot.send_message(message.chat.id, f'ПУТЕШЕСТВИЯ:\n\n'
                                                            f'{title_list_travel[num_of_page_travel - 1]}'
                                                     f'\n\n {link_list_travel[num_of_page_travel - 1]}',
                                            reply_markup=markup).message_id
    MCI = message.chat.id




@bot.callback_query_handler(func=lambda c:True)
def swap_page(message):
    global num_of_page_travel, current_page_travel, link_list_travel,\
        title_list_travel, num_of_page_sport, current_page_sport,\
        link_list_sport, title_list_sport, num_of_page_music, current_page_music,\
        link_list_music, current_page_telegram_travel, num_of_page_telegram_travel,\
        telegram_travel_link_list, current_page_telegram_films, num_of_page_telegram_films,\
        telegram_films_link_list, current_page_telegram_sport, num_of_page_telegram_sport,\
        telegram_sport_link_list, current_page_telegram_music, num_of_page_telegram_music,\
        telegram_music_link_list
    MCI = message.chat.id
    if message.data == 'back_travel' and num_of_page_travel != 1:
        num_of_page_travel -= 1
        current_title_travel = title_list_travel[num_of_page_travel - 1]
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='⬅️', callback_data='back_travel')
        button2 = InlineKeyboardButton(text='➡️', callback_data='forward_travel')
        button3 = InlineKeyboardButton(text=f'{num_of_page_travel}/{len(link_list_travel)}', callback_data='---')
        button4 = InlineKeyboardButton(text='❌', callback_data='delete_travel')
        markup.add(button1, button3, button2).add(button4)
        bot.edit_message_text(chat_id=MCI, message_id=current_page_travel, text=f'ПУТЕШЕСТВИЯ:'
                                                                                f'\n\n{current_title_travel}\n\n'
                                                                        f'{link_list_travel[num_of_page_travel - 1]}',
                              reply_markup=markup)
    elif message.data == 'back_travel' and num_of_page_travel == 1:
        num_of_page_travel = len(link_list_travel)
        current_title_travel = title_list_travel[num_of_page_travel - 1]
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='⬅️', callback_data='back_travel')
        button2 = InlineKeyboardButton(text='➡️', callback_data='forward_travel')
        button3 = InlineKeyboardButton(text=f'{num_of_page_travel}/{len(link_list_travel)}', callback_data='---')
        button4 = InlineKeyboardButton(text='❌', callback_data='delete_travel')
        markup.add(button1, button3, button2).add(button4)
        bot.edit_message_text(chat_id=MCI, message_id=current_page_travel, text=f'ПУТЕШЕСТВИЯ:'
                                                                                f'\n\n{current_title_travel}\n\n'
                                                                        f'{link_list_travel[num_of_page_travel - 1]}',
                              reply_markup=markup)
    elif message.data == 'forward_travel' and num_of_page_travel != len(link_list_travel):
        num_of_page_travel += 1
        current_title_travel = title_list_travel[num_of_page_travel - 1]
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='⬅️', callback_data='back_travel')
        button2 = InlineKeyboardButton(text='➡️', callback_data='forward_travel')
        button3 = InlineKeyboardButton(text=f'{num_of_page_travel}/{len(link_list_travel)}', callback_data='---')
        button4 = InlineKeyboardButton(text='❌', callback_data='delete_travel')
        markup.add(button1, button3, button2).add(button4)
        bot.edit_message_text(chat_id=MCI, message_id=current_page_travel, text=f'ПУТЕШЕСТВИЯ:'
                                                                                f'\n\n{current_title_travel}\n\n'
                                                                        f'{link_list_travel[num_of_page_travel - 1]}',
                              reply_markup=markup)
    elif message.data == 'forward_travel' and num_of_page_travel == len(link_list_travel):
        num_of_page_travel = 1
        current_title_travel = title_list_travel[num_of_page_travel - 1]
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='⬅️', callback_data='back_travel')
        button2 = InlineKeyboardButton(text='➡️', callback_data='forward_travel')
        button3 = InlineKeyboardButton(text=f'{num_of_page_travel}/{len(link_list_travel)}', callback_data='---')
        button4 = InlineKeyboardButton(text='❌', callback_data='delete_travel')
        markup.add(button1, button3, button2).add(button4)
        bot.edit_message_text(chat_id=MCI, message_id=current_page_travel, text=f'ПУТЕШЕСТВИЯ:'
                                                                                f'\n\n{current_title_travel}\n\n'
                                                                        f'{link_list_travel[num_of_page_travel - 1]}',
                              reply_markup=markup)
    elif message.data == 'forward_sport' and num_of_page_sport != len(link_list_sport):
        num_of_page_sport += 1
        current_title_sport = title_list_sport[num_of_page_sport - 1]
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='⬅️', callback_data='back_sport')
        button2 = InlineKeyboardButton(text='➡️', callback_data='forward_sport')
        button3 = InlineKeyboardButton(text=f'{num_of_page_sport}/{len(link_list_sport)}', callback_data='---')
        button4 = InlineKeyboardButton(text='❌', callback_data='delete_sport')
        markup.add(button1, button3, button2).add(button4)
        bot.edit_message_text(chat_id=MCI, message_id=current_page_sport, text=f'СПОРТ И АКТИВНЫЙ ОТДЫХ:\n\n'
                                                                               f'{current_title_sport}\n\n'
                                                                                f'{link_list_sport[num_of_page_sport - 1]}',
                              reply_markup=markup)
    elif message.data == 'forward_sport' and num_of_page_sport == len(link_list_sport):
        num_of_page_sport = 1
        current_title_sport = title_list_sport[num_of_page_sport - 1]
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='⬅️', callback_data='back_sport')
        button2 = InlineKeyboardButton(text='➡️', callback_data='forward_sport')
        button3 = InlineKeyboardButton(text=f'{num_of_page_sport}/{len(link_list_sport)}', callback_data='---')
        button4 = InlineKeyboardButton(text='❌', callback_data='delete_sport')
        markup.add(button1, button3, button2).add(button4)
        bot.edit_message_text(chat_id=MCI, message_id=current_page_sport, text=f'СПОРТ И АКТИВНЫЙ ОТДЫХ:\n\n'
                                                                               f'{current_title_sport}\n\n'
                                                                               f'{link_list_sport[num_of_page_sport - 1]}',
                              reply_markup=markup)

    elif message.data == 'back_sport' and num_of_page_sport != 1:
        num_of_page_sport -= 1
        current_title_sport = title_list_sport[num_of_page_sport - 1]
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='⬅️', callback_data='back_sport')
        button2 = InlineKeyboardButton(text='➡️', callback_data='forward_sport')
        button3 = InlineKeyboardButton(text=f'{num_of_page_sport}/{len(link_list_sport)}', callback_data='---')
        button4 = InlineKeyboardButton(text='❌', callback_data='delete_sport')
        markup.add(button1, button3, button2).add(button4)
        bot.edit_message_text(chat_id=MCI, message_id=current_page_sport, text=f'СПОРТ И АКТИВНЫЙ ОТДЫХ:\n\n'
                                                                               f'{current_title_sport}\n\n'
                                                                               f'{link_list_sport[num_of_page_sport - 1]}',
                              reply_markup=markup)
    elif message.data == 'back_sport' and num_of_page_sport == 1:
        num_of_page_sport = len(link_list_sport)
        current_title_sport = title_list_sport[num_of_page_sport - 1]
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='⬅️', callback_data='back_sport')
        button2 = InlineKeyboardButton(text='➡️', callback_data='forward_sport')
        button3 = InlineKeyboardButton(text=f'{num_of_page_sport}/{len(link_list_sport)}', callback_data='---')
        button4 = InlineKeyboardButton(text='❌', callback_data='delete_sport')
        markup.add(button1, button3, button2).add(button4)
        bot.edit_message_text(chat_id=MCI, message_id=current_page_sport, text=f'СПОРТ И АКТИВНЫЙ ОТДЫХ:\n\n'
                                                                               f'{current_title_sport}\n\n'
                                                                               f'{link_list_sport[num_of_page_sport - 1]}',
                              reply_markup=markup)
    elif message.data == 'back_music' and num_of_page_music != 1:
        num_of_page_music -= 1
        page = f'{num_of_page_music} / {len(link_list_music)}'
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='⬅️', callback_data='back_music')
        button2 = InlineKeyboardButton(text='➡️', callback_data='forward_music')
        button3 = InlineKeyboardButton(text=page, callback_data='---')
        button4 = InlineKeyboardButton(text='❌', callback_data='delete_music')
        markup.add(button1, button3, button2).add(button4)
        bot.delete_message(MCI, current_page_music)
        current_page_music = bot.send_audio(MCI, audio=f'{link_list_music[num_of_page_music - 1]}',
                       reply_markup=markup).message_id
    elif message.data == 'back_music' and num_of_page_music == 1:
        num_of_page_music = len((link_list_music))
        page = f'{num_of_page_music} / {len(link_list_music)}'
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='⬅️', callback_data='back_music')
        button2 = InlineKeyboardButton(text='➡️', callback_data='forward_music')
        button3 = InlineKeyboardButton(text=page, callback_data='---')
        button4 = InlineKeyboardButton(text='❌', callback_data='delete_music')
        markup.add(button1, button3, button2).add(button4)
        bot.delete_message(MCI, message_id=current_page_music)
        current_page_music = bot.send_audio(MCI, audio=f'{link_list_music[num_of_page_music - 1]}',
                       reply_markup=markup).message_id
    elif message.data == 'forward_music' and num_of_page_music == len(link_list_music):
        num_of_page_music = 1
        page = f'{num_of_page_music} / {len(link_list_music)}'
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='⬅️', callback_data='back_music')
        button2 = InlineKeyboardButton(text='➡️', callback_data='forward_music')
        button3 = InlineKeyboardButton(text=page, callback_data='---')
        button4 = InlineKeyboardButton(text='❌', callback_data='delete_music')
        markup.add(button1, button3, button2).add(button4)
        bot.delete_message(MCI, message_id=current_page_music)
        current_page_music = bot.send_audio(MCI, audio=f'{link_list_music[num_of_page_music - 1]}',
                       reply_markup=markup).message_id
    elif message.data == 'forward_music' and num_of_page_music != len(link_list_music):
        num_of_page_music += 1
        page = f'{num_of_page_music} / {len(link_list_music)}'
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='⬅️', callback_data='back_music')
        button2 = InlineKeyboardButton(text='➡️', callback_data='forward_music')
        button3 = InlineKeyboardButton(text=page, callback_data='---')
        button4 = InlineKeyboardButton(text='❌', callback_data='delete_music')
        markup.add(button1, button3, button2).add(button4)
        bot.delete_message(MCI, message_id=current_page_music)
        current_page_music = bot.send_audio(MCI, audio=f'{link_list_music[num_of_page_music - 1]}',
                       reply_markup=markup).message_id
    elif message.data == 'back_telegram_travel' and num_of_page_telegram_travel == 1:
        num_of_page_telegram_travel = len(telegram_travel_link_list)
        page = f'{num_of_page_telegram_travel}/{len(telegram_travel_link_list)}'
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='⬅️', callback_data='back_telegram_travel')
        button2 = InlineKeyboardButton(text='➡️', callback_data='forward_telegram_travel')
        button3 = InlineKeyboardButton(text=page, callback_data='---')
        button4 = InlineKeyboardButton(text='❌', callback_data='delete_telegram_travel')
        markup.add(button1, button3, button2).add(button4)
        bot.edit_message_text(chat_id=MCI, message_id=current_page_telegram_travel,
                              text=f'ПУТЕШЕСТВИЯ:\n\n'
                                   f'{telegram_travel_link_list[num_of_page_telegram_travel - 1]}',
                              reply_markup=markup)
    elif message.data == 'back_telegram_travel' and num_of_page_telegram_travel != 1:
        num_of_page_telegram_travel -= 1
        page = f'{num_of_page_telegram_travel}/{len(telegram_travel_link_list)}'
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='⬅️', callback_data='back_telegram_travel')
        button2 = InlineKeyboardButton(text='➡️', callback_data='forward_telegram_travel')
        button3 = InlineKeyboardButton(text=page, callback_data='---')
        button4 = InlineKeyboardButton(text='❌', callback_data='delete_telegram_travel')
        markup.add(button1, button3, button2).add(button4)
        bot.edit_message_text(chat_id=MCI, message_id=current_page_telegram_travel,
                              text=f'ПУТЕШЕСТВИЯ:\n\n'
                                   f'{telegram_travel_link_list[num_of_page_telegram_travel - 1]}',
                              reply_markup=markup)
    elif message.data == 'forward_telegram_travel' and num_of_page_telegram_travel != len(telegram_travel_link_list):
        num_of_page_telegram_travel += 1
        page = f'{num_of_page_telegram_travel}/{len(telegram_travel_link_list)}'
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='⬅️', callback_data='back_telegram_travel')
        button2 = InlineKeyboardButton(text='➡️', callback_data='forward_telegram_travel')
        button3 = InlineKeyboardButton(text=page, callback_data='---')
        button4 = InlineKeyboardButton(text='❌', callback_data='delete_telegram_travel')
        markup.add(button1, button3, button2).add(button4)
        bot.edit_message_text(chat_id=MCI, message_id=current_page_telegram_travel,
                              text=f'ПУТЕШЕСТВИЯ:\n\n'
                                   f'{telegram_travel_link_list[num_of_page_telegram_travel - 1]}',
                              reply_markup=markup)
    elif message.data == 'forward_telegram_travel' and num_of_page_telegram_travel == len(telegram_travel_link_list):
        num_of_page_telegram_travel = 1
        page = f'{num_of_page_telegram_travel}/{len(telegram_travel_link_list)}'
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='⬅️', callback_data='back_telegram_travel')
        button2 = InlineKeyboardButton(text='➡️', callback_data='forward_telegram_travel')
        button3 = InlineKeyboardButton(text=page, callback_data='---')
        button4 = InlineKeyboardButton(text='❌', callback_data='delete_telegram_travel')
        markup.add(button1, button3, button2).add(button4)
        bot.edit_message_text(chat_id=MCI, message_id=current_page_telegram_travel,
                              text=f'ПУТЕШЕСТВИЯ:\n\n'
                                   f'{telegram_travel_link_list[num_of_page_telegram_travel - 1]}',
                              reply_markup=markup)
    elif message.data == 'back_telegram_films' and num_of_page_telegram_films == 1:
        num_of_page_telegram_films = len(telegram_films_link_list)
        page = f'{num_of_page_telegram_films}/{len(telegram_films_link_list)}'
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='⬅️', callback_data='back_telegram_films')
        button2 = InlineKeyboardButton(text='➡️', callback_data='forward_telegram_films')
        button3 = InlineKeyboardButton(text=page, callback_data='---')
        button4 = InlineKeyboardButton(text='❌', callback_data='delete_telegram_films')
        markup.add(button1, button3, button2).add(button4)
        bot.edit_message_text(chat_id=MCI, message_id=current_page_telegram_films,
                              text=f'КИНО:\n\n'
                                   f'{telegram_films_link_list[num_of_page_telegram_films - 1]}',
                              reply_markup=markup)
    elif message.data == 'back_telegram_films' and num_of_page_telegram_films != 1:
        num_of_page_telegram_films -= 1
        page = f'{num_of_page_telegram_films}/{len(telegram_films_link_list)}'
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='⬅️', callback_data='back_telegram_films')
        button2 = InlineKeyboardButton(text='➡️', callback_data='forward_telegram_films')
        button3 = InlineKeyboardButton(text=page, callback_data='---')
        button4 = InlineKeyboardButton(text='❌', callback_data='delete_telegram_films')
        markup.add(button1, button3, button2).add(button4)
        bot.edit_message_text(chat_id=MCI, message_id=current_page_telegram_films,
                              text=f'КИНО:\n\n'
                                   f'{telegram_films_link_list[num_of_page_telegram_films - 1]}',
                              reply_markup=markup)
    elif message.data == 'forward_telegram_films' and num_of_page_telegram_films != len(telegram_films_link_list):
        num_of_page_telegram_films += 1
        page = f'{num_of_page_telegram_films}/{len(telegram_films_link_list)}'
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='⬅️', callback_data='back_telegram_films')
        button2 = InlineKeyboardButton(text='➡️', callback_data='forward_telegram_films')
        button3 = InlineKeyboardButton(text=page, callback_data='---')
        button4 = InlineKeyboardButton(text='❌', callback_data='delete_telegram_films')
        markup.add(button1, button3, button2).add(button4)
        bot.edit_message_text(chat_id=MCI, message_id=current_page_telegram_films,
                              text=f'КИНО:\n\n'
                                   f'{telegram_films_link_list[num_of_page_telegram_films - 1]}',
                              reply_markup=markup)
    elif message.data == 'forward_telegram_films' and num_of_page_telegram_films == len(telegram_films_link_list):
        num_of_page_telegram_films = 1
        page = f'{num_of_page_telegram_films}/{len(telegram_films_link_list)}'
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='⬅️', callback_data='back_telegram_films')
        button2 = InlineKeyboardButton(text='➡️', callback_data='forward_telegram_films')
        button3 = InlineKeyboardButton(text=page, callback_data='---')
        button4 = InlineKeyboardButton(text='❌', callback_data='delete_telegram_films')
        markup.add(button1, button3, button2).add(button4)
        bot.edit_message_text(chat_id=MCI, message_id=current_page_telegram_films,
                              text=f'КИНО:\n\n'
                                   f'{telegram_sport_link_list[num_of_page_telegram_films - 1]}',
                              reply_markup=markup)
    elif message.data == 'back_telegram_sport' and num_of_page_telegram_sport == 1:
        num_of_page_telegram_sport = len(telegram_sport_link_list)
        page = f'{num_of_page_telegram_sport}/{len(telegram_sport_link_list)}'
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='⬅️', callback_data='back_telegram_sport')
        button2 = InlineKeyboardButton(text='➡️', callback_data='forward_telegram_sport')
        button3 = InlineKeyboardButton(text=page, callback_data='---')
        button4 = InlineKeyboardButton(text='❌', callback_data='delete_telegram_sport')
        markup.add(button1, button3, button2).add(button4)
        bot.edit_message_text(chat_id=MCI, message_id=current_page_telegram_sport,
                              text=f'СПОРТ И ЗДОРОВЬЕ:\n\n'
                                   f'{telegram_sport_link_list[num_of_page_telegram_sport - 1]}',
                              reply_markup=markup)
    elif message.data == 'back_telegram_sport' and num_of_page_telegram_sport != 1:
        num_of_page_telegram_sport -= 1
        page = f'{num_of_page_telegram_sport}/{len(telegram_sport_link_list)}'
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='⬅️', callback_data='back_telegram_sport')
        button2 = InlineKeyboardButton(text='➡️', callback_data='forward_telegram_sport')
        button3 = InlineKeyboardButton(text=page, callback_data='---')
        button4 = InlineKeyboardButton(text='❌', callback_data='delete_telegram_sport')
        markup.add(button1, button3, button2).add(button4)
        bot.edit_message_text(chat_id=MCI, message_id=current_page_telegram_sport,
                              text=f'СПОРТ И ЗДОРОВЬЕ:\n\n'
                                   f'{telegram_sport_link_list[num_of_page_telegram_sport - 1]}',
                              reply_markup=markup)
    elif message.data == 'forward_telegram_sport' and num_of_page_telegram_sport != len(telegram_sport_link_list):
        num_of_page_telegram_sport += 1
        page = f'{num_of_page_telegram_sport}/{len(telegram_sport_link_list)}'
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='⬅️', callback_data='back_telegram_sport')
        button2 = InlineKeyboardButton(text='➡️', callback_data='forward_telegram_sport')
        button3 = InlineKeyboardButton(text=page, callback_data='---')
        button4 = InlineKeyboardButton(text='❌', callback_data='delete_telegram_sport')
        markup.add(button1, button3, button2).add(button4)
        bot.edit_message_text(chat_id=MCI, message_id=current_page_telegram_sport,
                              text=f'СПОРТ И ЗДОРОВЬЕ:\n\n'
                                   f'{telegram_sport_link_list[num_of_page_telegram_sport - 1]}',
                              reply_markup=markup)
    elif message.data == 'forward_telegram_sport' and num_of_page_telegram_sport == len(telegram_sport_link_list):
        num_of_page_telegram_sport = 1
        page = f'{num_of_page_telegram_sport}/{len(telegram_sport_link_list)}'
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='⬅️', callback_data='back_telegram_sport')
        button2 = InlineKeyboardButton(text='➡️', callback_data='forward_telegram_sport')
        button3 = InlineKeyboardButton(text=page, callback_data='---')
        button4 = InlineKeyboardButton(text='❌', callback_data='delete_telegram_sport')
        markup.add(button1, button3, button2).add(button4)
        bot.edit_message_text(chat_id=MCI, message_id=current_page_telegram_sport,
                              text=f'СПОРТ И ЗДОРОВЬЕ:\n\n'
                                   f'{telegram_sport_link_list[num_of_page_telegram_sport - 1]}',
                              reply_markup=markup)

    elif message.data == 'back_telegram_music' and num_of_page_telegram_music == 1:
        num_of_page_telegram_music = len(telegram_music_link_list)
        page = f'{num_of_page_telegram_music}/{len(telegram_music_link_list)}'
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='⬅️', callback_data='back_telegram_music')
        button2 = InlineKeyboardButton(text='➡️', callback_data='forward_telegram_music')
        button3 = InlineKeyboardButton(text=page, callback_data='---')
        button4 = InlineKeyboardButton(text='❌', callback_data='delete_telegram_music')
        markup.add(button1, button3, button2).add(button4)
        bot.edit_message_text(chat_id=MCI, message_id=current_page_telegram_music,
                              text=f'МУЗЫКА:\n\n'
                                   f'{telegram_music_link_list[num_of_page_telegram_music - 1]}',
                              reply_markup=markup)
    elif message.data == 'back_telegram_music' and num_of_page_telegram_music != 1:
        num_of_page_telegram_music -= 1
        page = f'{num_of_page_telegram_music}/{len(telegram_music_link_list)}'
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='⬅️', callback_data='back_telegram_music')
        button2 = InlineKeyboardButton(text='➡️', callback_data='forward_telegram_music')
        button3 = InlineKeyboardButton(text=page, callback_data='---')
        button4 = InlineKeyboardButton(text='❌', callback_data='delete_telegram_music')
        markup.add(button1, button3, button2).add(button4)
        bot.edit_message_text(chat_id=MCI, message_id=current_page_telegram_music,
                              text=f'МУЗЫКА:\n\n'
                                   f'{telegram_music_link_list[num_of_page_telegram_music - 1]}',
                              reply_markup=markup)
    elif message.data == 'forward_telegram_music' and num_of_page_telegram_music != len(telegram_music_link_list):
        num_of_page_telegram_music += 1
        page = f'{num_of_page_telegram_music}/{len(telegram_music_link_list)}'
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='⬅️', callback_data='back_telegram_music')
        button2 = InlineKeyboardButton(text='➡️', callback_data='forward_telegram_music')
        button3 = InlineKeyboardButton(text=page, callback_data='---')
        button4 = InlineKeyboardButton(text='❌', callback_data='delete_telegram_music')
        markup.add(button1, button3, button2).add(button4)
        bot.edit_message_text(chat_id=MCI, message_id=current_page_telegram_music,
                              text=f'МУЗЫКА:\n\n'
                                   f'{telegram_music_link_list[num_of_page_telegram_music - 1]}',
                              reply_markup=markup)
    elif message.data == 'forward_telegram_music' and num_of_page_telegram_music == len(telegram_music_link_list):
        num_of_page_telegram_music = 1
        page = f'{num_of_page_telegram_music}/{len(telegram_music_link_list)}'
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='⬅️', callback_data='back_telegram_music')
        button2 = InlineKeyboardButton(text='➡️', callback_data='forward_telegram_music')
        button3 = InlineKeyboardButton(text=page, callback_data='---')
        button4 = InlineKeyboardButton(text='❌', callback_data='delete_telegram_music')
        markup.add(button1, button3, button2).add(button4)
        bot.edit_message_text(chat_id=MCI, message_id=current_page_telegram_music,
                              text=f'МУЗЫКА:\n\n'
                                   f'{telegram_music_link_list[num_of_page_telegram_sport - 1]}',
                              reply_markup=markup)


    elif message.data == 'delete_music':
        bot.delete_message(MCI, current_page_music)
    elif message.data == 'delete_sport':
        bot.delete_message(MCI, current_page_sport)
    elif message.data == 'delete_travel':
        bot.delete_message(MCI, current_page_travel)
    elif message.data == 'delete_telegram_travel':
        bot.delete_message(MCI, current_page_telegram_travel)
    elif message.data == 'delete_telegram_sport':
        bot.delete_message(MCI, current_page_telegram_sport)
    elif message.data == 'delete_telegram_films':
        bot.delete_message(MCI, current_page_telegram_films)
    elif message.data == 'delete_telegram_music':
        bot.delete_message(MCI, current_page_telegram_music)


def sport_sales(message):
    global current_page_sport, num_of_page_sport, link_list_sport, title_list_sport, MCI
    url = 'https://www.pepper.ru/groups/sports'
    data = get(url)
    html = Soup(data)
    a = html.find('a', {'class': 'cept-tt thread-link linkPlain thread-title--list js-thread-title'})
    a = ''.join(map(str, a))
    a = a.split('</a>')
    title_list_sport = []
    link_list_sport = []
    for i in a:
        title = i[83:i.find('href') - 2]
        title_list_sport.append(title)
        link_list_sport.append(i[i.find('href="') + 6: i.find('data-t') - 2])
    for i in range(len(link_list_sport)):
        if len(link_list_sport[i]) == 0:
            link_list_sport.pop(i)
    for j in range(len(title_list_sport)):
        if len(title_list_sport[j]) == 0:
            title_list_sport.pop(j)
    num_of_page_sport = 1
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(text='⬅️', callback_data='back_sport')
    button2 = InlineKeyboardButton(text='➡️', callback_data='forward_sport')
    button3 = InlineKeyboardButton(text=f'{num_of_page_sport}/{len(link_list_sport)}', callback_data='---')
    button4 = InlineKeyboardButton(text='❌', callback_data='delete_sport')
    markup.add(button1, button3, button2).add(button4)
    current_page_sport = bot.send_message(message.chat.id, f'СПОРТ И АКТИВНЫЙ ОТДЫХ:\n\n'
                                                           f'{title_list_sport[num_of_page_sport - 1]}'
                                                     f'\n\n {link_list_sport[num_of_page_sport - 1]}',
                                            reply_markup=markup).message_id
    MCI = message.chat.id



def music_top(message):
    global current_page_music, num_of_page_music, link_list_music, MCI
    link_list_music = []
    url = 'https://wow1.supermusic.me/foreign/'
    response = get(url)
    html = Soup(response)
    text = "".join(map(str, html.find('div', {'class': 'popular-play'})))
    start_list = text.split('<a ')
    for i in start_list:
        if 'data-url' in i:
            link_list_music.append(i[10: i.find('class="') - 2])
    k = 0
    for j in link_list_music:
        j = j.replace(' ', '%20')
        link_list_music[k] = j
        k += 1

    num_of_page_music = 1
    page = f'{num_of_page_music}/{len(link_list_music)}'
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(text='⬅️', callback_data=['back_music'])
    button2 = InlineKeyboardButton(text='➡️', callback_data='forward_music')
    button3 = InlineKeyboardButton(text=page, callback_data='---')
    button4 = InlineKeyboardButton(text='❌', callback_data='delete_music')
    markup.add(button1, button3, button2).add(button4)
    current_page_music = bot.send_audio(message.chat.id, audio=f'{link_list_music[num_of_page_music - 1]}',
                                         reply_markup=markup).message_id
    MCI = message.chat.id

    main_menu(message)


def telegram_travel(message):
    global current_page_telegram_travel, num_of_page_telegram_travel, telegram_travel_link_list, MCI
    url = 'https://tlgrm.ru/channels/travel'
    data = get(url)
    html = Soup(data)
    text = " ".join(map(str, html.find('h3', {'class': 'channel-card__title'})))
    link_list = text.split('</a>')
    for i in link_list:
        if not '<a href="' in i:
            link_list.remove(i)
    nlst = []
    for j in link_list:
        nlst.append(j[j.find('<a href="') + 9: j.find('target')])
    nlst.pop(0)
    telegram_travel_link_list = []
    for k in nlst:
        telegram_travel_link_list.append(k[:k.find('"')])

    num_of_page_telegram_travel = 1
    page = f'{num_of_page_telegram_travel}/{len(telegram_travel_link_list)}'
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(text='⬅️', callback_data='back_telegram_travel')
    button2 = InlineKeyboardButton(text='➡️', callback_data='forward_telegram_travel')
    button3 = InlineKeyboardButton(text=page, callback_data='---')
    button4 = InlineKeyboardButton(text='❌', callback_data='delete_telegram_travel')
    markup.add(button1, button3, button2).add(button4)
    current_page_telegram_travel = bot.send_message(message.chat.id,
                                                    f'ПУТЕШЕСТВИЯ:\n\n'
                                                    f'{telegram_travel_link_list[num_of_page_telegram_travel - 1]}',
                                        reply_markup=markup).message_id
    MCI = message.chat.id


def telegram_films(message):
    global current_page_telegram_films, num_of_page_telegram_films, telegram_films_link_list, MCI
    url = 'https://tlgrm.ru/channels/video'
    data = get(url)
    html = Soup(data)
    text = " ".join(map(str, html.find('h3', {'class': 'channel-card__title'})))
    link_list = text.split('</a>')
    for i in link_list:
        if not '<a href="' in i:
            link_list.remove(i)
    nlst = []
    for j in link_list:
        nlst.append(j[j.find('<a href="') + 9: j.find('target')])
    nlst.pop(0)
    telegram_films_link_list = []
    for k in nlst:
        telegram_films_link_list.append(k[:k.find('"')])

    num_of_page_telegram_films = 1
    page = f'{num_of_page_telegram_films}/{len(telegram_films_link_list)}'
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(text='⬅️', callback_data='back_telegram_films')
    button2 = InlineKeyboardButton(text='➡️', callback_data='forward_telegram_films')
    button3 = InlineKeyboardButton(text=page, callback_data='---')
    button4 = InlineKeyboardButton(text='❌', callback_data='delete_telegram_films')
    markup.add(button1, button3, button2).add(button4)
    current_page_telegram_films = bot.send_message(message.chat.id,
                                                    f'КИНО:\n\n'
                                                    f'{telegram_films_link_list[num_of_page_telegram_films - 1]}',
                                        reply_markup=markup).message_id
    MCI = message.chat.id



def telegram_sport(message):
    global current_page_telegram_sport, num_of_page_telegram_sport, telegram_sport_link_list, MCI
    url = 'https://tlgrm.ru/channels/fitness'
    data = get(url)
    html = Soup(data)
    text = " ".join(map(str, html.find('h3', {'class': 'channel-card__title'})))
    link_list = text.split('</a>')
    for i in link_list:
        if not '<a href="' in i:
            link_list.remove(i)
    nlst = []
    for j in link_list:
        nlst.append(j[j.find('<a href="') + 9: j.find('target')])
    nlst.pop(0)
    telegram_sport_link_list = []
    for k in nlst:
        telegram_sport_link_list.append(k[:k.find('"')])

    num_of_page_telegram_sport = 1
    page = f'{num_of_page_telegram_sport}/{len(telegram_sport_link_list)}'
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(text='⬅️', callback_data='back_telegram_sport')
    button2 = InlineKeyboardButton(text='➡️', callback_data='forward_telegram_sport')
    button3 = InlineKeyboardButton(text=page, callback_data='---')
    button4 = InlineKeyboardButton(text='❌', callback_data='delete_telegram_sport')
    markup.add(button1, button3, button2).add(button4)
    current_page_telegram_sport = bot.send_message(message.chat.id,
                                                    f'СПОРТ И ЗДОРОВЬЕ:\n\n'
                                                    f'{telegram_sport_link_list[num_of_page_telegram_sport - 1]}',
                                        reply_markup=markup).message_id
    MCI = message.chat.id


def telegram_music(message):
    global current_page_telegram_music, num_of_page_telegram_music, telegram_music_link_list, MCI
    url = 'https://tlgrm.ru/channels/music'
    data = get(url)
    html = Soup(data)
    text = " ".join(map(str, html.find('h3', {'class': 'channel-card__title'})))
    link_list = text.split('</a>')
    for i in link_list:
        if not '<a href="' in i:
            link_list.remove(i)
    nlst = []
    for j in link_list:
        nlst.append(j[j.find('<a href="') + 9: j.find('target')])
    nlst.pop(0)
    telegram_music_link_list = []
    for k in nlst:
        telegram_music_link_list.append(k[:k.find('"')])

    num_of_page_telegram_music = 1
    page = f'{num_of_page_telegram_music}/{len(telegram_music_link_list)}'
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(text='⬅️', callback_data='back_telegram_music')
    button2 = InlineKeyboardButton(text='➡️', callback_data='forward_telegram_music')
    button3 = InlineKeyboardButton(text=page, callback_data='---')
    button4 = InlineKeyboardButton(text='❌', callback_data='delete_telegram_music')
    markup.add(button1, button3, button2).add(button4)
    current_page_telegram_music = bot.send_message(message.chat.id,
                                                    f'МУЗЫКА:\n\n'
                                                    f'{telegram_music_link_list[num_of_page_telegram_music - 1]}',
                                        reply_markup=markup).message_id
    MCI = message.chat.id


def youtube_search(message):
    try:
        link = VideosSearch(message.text.lower(), limit= 1).result()['result'][0]['link']
        bot.send_message(message.chat.id, link)
        main_menu(message)
    except Exception:
        bot.send_message(message.chat.id, 'Ошибка ввода. Повторите попытку')
        main_menu(message)


def info(message):
    global MCI
    bot.send_message(MCI, f'Привет, {message.from_user.first_name}, я - бот, который поможет тебе найти '
                                      f'самые выгодные цены на товары,'
                                      f'а также подскажет тебе telegram - каналы, основываясь на своих интересах.'
                                      f'Еще в меню вы сможете послушать музыку, которую я подберу.'
                                      f'Информация будет со временем обновляться автоматически, поэтому '
                                      f'не забывайте сюда заглядывать.')
    main_menu(message)


def send_comment(message):
    if message.content_type == 'text':
        comment = message.text.capitalize()
        bot.send_message(message.chat.id, f'Вот ваш комментарий:\n\n {comment}')
        users_info[str(message.chat.id)]['comment'] = comment
        with open('users_data.json', 'w') as file:
            json.dump(users_info, file, indent=4)
        bot.forward_message(chat_id=5182812730, from_chat_id=message.chat.id, message_id=message.message_id)
        main_menu(message)
    else:
        bot.send_message(message.chat.id, f'Комментарий или отзыв должен состоять только из текста')
        main_menu(message)


@bot.message_handler(content_types=['text'])
def isStart(message):
    global MCI
    if IN_MAIN_MENU == False and IN_INFO == False:
        MCI = message.chat.id
        main_menu(message)

while True:
    try:
        bot.polling(none_stop=True)
    except:
        bot.send_message(5182812730, f'ПРОИЗОШЛА ОШИБКА!!!!!!!')
