import telebot, requests, json, random

bot = telebot.TeleBot("your telegram bot token")

@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    bot.send_message(message.chat.id, 'Слава Ісусу Христу!')
    bot.send_message(message.chat.id, 'Я бот, який допоможе Вам підібрати одяг залежно від погоди')

    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row("Man", "Woman")
    bot.send_message(message.chat.id, 'Введіть, будь-ласка, Вашу стать', reply_markup=user_markup)
    


gender = 0

@bot.message_handler(content_types=['text'])
def send_text(message):

    global gender

    if message.text.lower() == 'woman':
        gender = 'w'
        #bot.send_message(message.chat.id, 'Стать введено')
        bot.send_message(message.chat.id, 'Введіть, будь ласка, місто Вашого перебування (Англійською)')

    
    elif message.text.lower() == 'man':
        gender = 'm'
        #bot.send_message(message.chat.id, 'Стать введено')
        bot.send_message(message.chat.id, 'Введіть, будь ласка, місто Вашого перебування (Англійською)')
        
    try:

        if message.text.lower() != 'woman' and message.text.lower() != 'man':
            current_temperature, current_humidiy, current_pressure, weather_description = get_weath(message.text)

            if "rain" in weather_description.lower() or "snow" in weather_description.lower():
                opady = True
            else:
                opady = False

            opys = pick_clothes(int(current_temperature), opady, gender)

            bot.send_message(message.chat.id, "Місто " + str(message.text))

            
            
            bot.send_message(message.chat.id, "Сьогоднішня температура = " + str(int(current_temperature)) + "'С")
            bot.send_message(message.chat.id, "Сьогоднішня хмарність = " + str(current_humidiy) + "%")
            bot.send_message(message.chat.id, "Сьогоднішній тиск = " + str(current_pressure) + "мм.рт.ст.")
            bot.send_message(message.chat.id, opys)

            if current_humidiy < 60:
                bot.send_sticker(message.chat.id, 'CAADAgADAgQAAtJaiAECKCdNruu1MRYE')
                f = open("Sunny (Sefon.me).mp3", 'rb')
                bot.send_audio(message.chat.id, f)
                #bot.send_document(message.chat.id, 'CQADAgAD9QQAAoyLeUrtu_2vNg62WhYE')
                f.close()
            elif "rain" in weather_description.lower():
                bot.send_sticker(message.chat.id, 'CAADAgADJAEAAqZESAsL5_Fz7_gGkBYE')
                f = open("Its Raining Men (Sefon.me).mp3", 'rb')
                bot.send_audio(message.chat.id, f)
                #bot.send_document(message.chat.id, 'CQADAgAD9QQAAoyLeUrtu_2vNg62WhYE')
                f.close()
            elif "snow" in weather_description.lower():
                bot.send_sticker(message.chat.id, 'CAADAgADOAEAAqZESAvMWrzVi1b-6RYE')
                f = open("02 Snow (Hey Oh).mp3", 'rb')
                bot.send_audio(message.chat.id, f)
                #bot.send_document(message.chat.id, 'CQADAgAD9QQAAoyLeUrtu_2vNg62WhYE')
                f.close()
            elif "thun" in weather_description.lower():
                bot.send_sticker(message.chat.id, 'CAADAgADLAEAAqZESAs1JufkLCR1wxYE')
                f = open("Thunderstruck (Sefon.me).mp3", 'rb')
                bot.send_audio(message.chat.id, f)
                #bot.send_document(message.chat.id, 'CQADAgAD9QQAAoyLeUrtu_2vNg62WhYE')
                f.close()
            else:
                bot.send_sticker(message.chat.id, 'CAADAgADJAQAAtJaiAGGA7TDrrPgrxYE')
                f = open("1521528725_system-of-a-down-lonely-day-2006-www_muzonov_net.mp3", 'rb')
                bot.send_audio(message.chat.id, f)
                #bot.send_document(message.chat.id, 'CQADAgAD9QQAAoyLeUrtu_2vNg62WhYE')
                f.close()


    except:
        bot.send_message(message.chat.id, "Введено некоректні дані, будь ласка, повторіть")
    



def get_weath(city):
    # Enter your API key here 
    api_key = "your openweathermap api token"

    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    complete_url = base_url + "appid=" + api_key + "&q=" + city

    # get method of requests module 
    # return response object 
    response = requests.get(complete_url) 
    
    # json method of response object  
    # convert json format data into 
    # python format data 
    x = response.json()

    if x["cod"] != 404:

        # store the value of "main" 
        # key in variable y 
        y = x["main"]

        current_temperature = float(y["temp"]) - 273.15

        current_humidiy = y["humidity"]

        current_pressure = y["pressure"]

        z = x["weather"]

        weather_description = z[0]["main"]

        return current_temperature, current_humidiy, current_pressure, weather_description

    else:
        return False, False, False, False

def pick_clothes(tem, fall_out, sex):
    male_dct = {1:(["футболка", "сорочка", "майка", "поло"], ["шорти","бриджі", "капрі", ], ["кепка", "капелюх", "панама" , "сонячні окуляри"],  ["босоніжки", "кросівки" , "кеди" , "мешти", "мокасини"]), 2: (["светер", "світшот", "худі" , "кардиган" , "піджак" , "джинсова куртка"], ["класичні джинси", "чорні джинси", "брюки"], ["черевики", "кросівки", "кеди"]), 3: ( ["куртка", "плащ", "пуховик"], ["класичні джинси", "чорні джинси", "брюки"], ["шапка", "шалик", "рукавиці"], ["черевики", "уггі", "утеплені кросівки", "чоботи"] )}
    female_dct = { 1:(["футболка", "сорочка", "майка", "поло"], ["шорти", "бриджі", "спідниця", "капрі"], ["кепка", "капелюх", "сонячні окуляри"],  ["босоніжки", "кросівки", "туфлі"]), 2: (["светер", "світшот", "худі", "піджак", "джемпер", "джинсова куртка"], ["класичні джинси", "чорні джинси", "брюки"], ["черевики", "кросівки", "кеди", "туфлі"]), 3: ( ["куртка", "плащ", "пуховик"], ["класичні джинси", "чорні джинси", "брюки"], ["шапка", "шалик", "рукавиці"], ["черевики", "уггі", "утеплені кросівки", "чоботи"])}
    if tem in range(-30, 5): i = 3
    elif tem in range(5, 18): i = 2
    elif tem in range(18, 30): i = 1
    elif tem < -30: return 'Не виходьте з хати!'
    elif tem > 30: return 'Поспішайте на озеро!'
    
    if sex == 'm': wardrobe = male_dct
    elif sex == 'w': wardrobe = female_dct
    
    extra_advice = str()
    if fall_out:
        extra_advice = "А також не забудьте прихопити парасольку!"
    look = str("Рекомендований одяг на сьогодні:\n")
    for el in wardrobe[i]:
        look += random.choice(el) + ', '
    look = look.rstrip(', ') + '. ' + extra_advice
    return look


bot.polling()
