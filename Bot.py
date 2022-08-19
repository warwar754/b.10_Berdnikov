import telebot
from config import TOKEN, keys
from extensions import ConvertionException, converter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def start_help(message: telebot.types.Message):
    text = f"Привет {message.chat.username}. Что бы начать работать введите команду боту в формате \n<имя валюты> \
<в какую валюту перевести> \
<количество валюты>. Получить список доступных валют можно введя команду /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=["values"])
def valute(message: telebot.types.Message):
    text = "Доступные валюты:"
    for i in keys.keys():
        text = "\n".join((text, i,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text", ])
def currency_request(message: telebot.types.Message):
    try:
        values = message.text.split(" ")
        if len(values) != 3:
            raise ConvertionException(
                "Параметров Должно быть три. Введите /help для справки")
        quote, base, amount = values
        result = converter.converter(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f"Ошибка пользователя\n{e}")

    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду\n{e}")

    else:
        result = converter.get_price(quote, base, amount)
        text = f"Цена {amount} {quote} в {base} = {result}"
        bot.send_message(message.chat.id, text)


bot.polling()
