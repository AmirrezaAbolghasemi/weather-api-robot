from telebot import types
from DataBase_bot import insert_user_data, show_user_info
import telebot
import datetime
import requests
import time

TOKEN = '<TOKEN-API>'
bot = telebot.TeleBot(TOKEN)

knownUsers = [] 

commands = {  # command description used in the "help" command
    'start'       : 'Get used to the Bot',
    'help'        : 'Gives you information about the available commands',
    'register'        : 'Register to the Bot',
    'information'        : 'show user information',
    'invit_link'        : 'invit_link to the bot',
    'weather'        : 'Get information about your city weather ',
}

hideBoard = types.ReplyKeyboardRemove()  # if sent as reply_markup, will hide the keyboard


# this variable is short memmory about data user for show one time than delete
user_data = {}

# only used for console output now
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        print(m)
        if m.content_type == 'text':
            # print the sent message to the console
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)


bot.set_update_listener(listener)  # register listener


# handle the "/start" command
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid not in knownUsers:  # if user hasn't used the "/start" command yet:
        knownUsers.append(cid)  # save user id, so you could brodcast messages to all users of this bot later
        bot.send_message(cid, "Hello, welcome to weather api Bot🔥")
        command_help(m)  # show the new user the help page
    else:
        bot.send_message(cid, "I already know you, no need for me to scan you again❗️")


# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "The following commands are available: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + " - "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page


# Get weather with city name
@bot.message_handler(commands=['weather'])
def get_weather(m):
    cid = m.chat.id
    if cid in knownUsers:
        bot.send_message(cid, 'Send me your city name please!')

        bot.register_next_step_handler(m, handle_city)
    else:
        bot.send_message(cid, 'First register to the bot❗️')
        register(m)  


def handle_city(m):
    cid = m.chat.id
    if cid in knownUsers :
        city = m.text.strip()
        api_key = "<API-KEY>" # get api key from openweather
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            date = datetime.datetime.now()
            bot.send_message(cid, f'*Status of " {city} ":*\n\t• Temperature ==> {temp}°C\n\t• Description ==> {description}\n\t• Humidity ==> {humidity}%\n\t• Wind Speed ==> {wind_speed} m/s \n\t• Date ==> {date.strftime("%Y-%m-%d")}',parse_mode='markdown')
            time.sleep(2)
            command_help(m)
        else:
            bot.send_message(cid, "City not found... Try again❌!")
            get_weather(m)
    else:
        bot.send_message(cid, 'First register to the bot❗️')
        register(m)  


# register user to the bot and save in data base
@bot.message_handler(commands=['register'])
def register(m):
    cid = m.chat.id
    bot.send_message(cid , 'Lets , Send me your name !')
    
    bot.register_next_step_handler(m , get_name)

def get_name(m):
    global name
    cid = m.chat.id
    name = m.text.strip()
    user_data[cid] = {'name' : name}
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button = types.KeyboardButton("Send my phone number📞", request_contact=True)
    markup.add(button)
    bot.send_message(cid , f'Thanks {name} !\nNow send me your phone number', reply_markup=markup)


# handle information about user for save
@bot.message_handler(content_types=['contact']) 
def handle_contact(m):
    cid = m.chat.id
    full_name = name
    contact = m.contact  # Contact info sent by user
    phone_number = contact.phone_number  # Get phone number
    username = m.chat.username
    user_data[cid]['phone'] = phone_number
    bot.send_message(cid, f"Thanks!\n I received your phone number✅",reply_markup=hideBoard)
    bot.send_message(cid , f'*Information :*\n• phone Number - {phone_number}\n• UserName - @{m.chat.username}\n• Name - {user_data[cid]['name']}', parse_mode='markdown')
    insert_user_data(cid, full_name, username, phone_number)
    user_data.clear()
    time.sleep(1)
    command_help(m)
    
    

@bot.message_handler(commands=['information'])
def show_user_information(m):
    cid = m.chat.id
    
    if cid in knownUsers:
        user_data = show_user_info(cid)
        bot.send_message(cid, f'*Information :*\n• chat id - {user_data['cid']}\n• phone Number - {user_data['phone']}\n• UserName - @{user_data['username']}\n• Name - {user_data['first_name']}', parse_mode='markdown')
        time.sleep(1)
        command_help(m)
    else:
        bot.send_message(cid, 'First register to the bot❗️')
        register(m)
    
    

# invite anyone to bot with this command
@bot.message_handler(commands=['invit_link'])
def invit_link_command(m):
    cid = m.chat.id
    if cid in knownUsers: 
        link = f'https://t.me/weather_api_testingbot?start={cid}'
        bot.send_message(cid, f'Your invite link: {link}')
    else:
        bot.send_message(cid, 'First register to the bot❗️ ')
        register(m)
    

# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    cid = m.chat.id
    bot.send_message(m.chat.id, "I don't understand \"" + m.text + "\"\nMaybe try the help page at /help")


bot.infinity_polling()
