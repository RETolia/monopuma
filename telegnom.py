from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import WebAppInfo
bot = Bot(token="")
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("start_cmd_Привет!")

async def main():
    await dp.start_polling(bot)

#----------------------------Reply-клавиатура:
def get_reply_kb():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Кнопка 1")
    builder.button(text="Кнопка 2")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

@dp.message(Command("keyboard"))
async def kb_cmd(message: types.Message):
    await message.answer("Выберите:", reply_markup=get_reply_kb())

#----------------------------inline-клавиатура:
def get_inline_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Нажми меня", callback_data="btn_press")
    return builder.as_markup()

@dp.callback_query(lambda c: c.data == "btn_press")
async def process_callback(callback: types.CallbackQuery):
    await callback.answer("Вы нажали кнопку!", show_alert=True)

@dp.message(Command("inline"))
async def show_inline_kb(message: types.Message):
    await message.answer("Пример inline-клавиатуры:", reply_markup=get_inline_kb())


#----------------------------отправка фотопо ссылке:
@dp.message(Command("photo"))
async def send_photo(message: types.Message):
    await message.answer_photo(
        photo="https://images.app.goo.gl/iTFdnTdK4SNGNwHMA",
        caption="Это тестовое изображение девочки-гитлера взятое по ссылке из амино"
    )
#----------------------------Web App:

def get_game_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🎮 Играть", 
        web_app=WebAppInfo(url="https://island-purring-butterkase.glitch.me/")  # Замените на URL вашей игры
    )
    return builder.as_markup()

# Команда для запуска
@dp.message(Command("game"))
async def cmd_game(message: types.Message):
    await message.answer(
        "Нажмите кнопку, чтобы открыть игру:",
        reply_markup=get_game_keyboard()
    )

if __name__ == "__main__":
    asyncio.run(main())
