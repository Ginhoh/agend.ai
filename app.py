import telebot
from agent.brain import main
import asyncio

bot = telebot.TeleBot('9106630394:AAEr0Hti694M1yyMghJSP-Dc9GgMToVteGo')

@bot.message_handler(['start'])
def start(msg:telebot.types.Message):
    bot.reply_to(msg, "Bot Funcionando!")

@bot.message_handler(content_types=['text'])
def agent(call: telebot.types.Message):
    try:
        resposta = asyncio.run(main(call.text))
        bot.reply_to(call, resposta)
    except Exception as e:
        bot.reply_to(call, f"ERRO: {e}")

bot.infinity_polling()