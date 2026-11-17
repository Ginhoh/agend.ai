import os
from dotenv import load_dotenv  
import telebot
from agent.brain import main
import asyncio

load_dotenv()
TELEBOT_API_KEY = os.getenv("TELEBOT_API_KEY")

bot = telebot.TeleBot(TELEBOT_API_KEY)

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