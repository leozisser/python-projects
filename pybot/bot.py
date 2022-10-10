from aiogram import Bot, types 
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor 
from config import TOKEN 

bot = Bot(token = TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Hey! drop me a few lines")

@dp.message_handler(commands = ['help'])
async def process_help_command(message: types.Message):
    await message.reply ("drop me a line or two and I'll sennd you back this")

@dp.message_handler()
async def echo_message(message: types.Message):
    print(message.text)
    await bot.send_message(message.from_user.id, message.text + ' my ass')


if __name__ == '__main__':
    executor.start_polling(dp)