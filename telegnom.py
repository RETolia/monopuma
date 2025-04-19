from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
from aiogram.enums import ChatType
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import WebAppInfo
from aiogram import Bot
from aiogram.types import ForumTopic
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
bot = Bot(token="")
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("start_cmd_Привет!")

async def main():
    await dp.start_polling(bot)


def is_allowed_chat(message: types.Message) -> bool:
    return (
        message.chat.type == ChatType.PRIVATE or  # Личные сообщения
        message.message_thread_id is None or  # General (не топик)
        message.message_thread_id is not None  # и топик ----------------------временно
    )


#-------------------------------------------
from aiogram import Bot
from aiogram.types import ChatFullInfo
from aiogram.enums import ChatType
@dp.message(Command("chat_info"))
async def cmd_chat_info(message: types.Message):
    await print_full_chat_info(bot, message.chat.id)
async def print_full_chat_info(bot: Bot, chat_id: int):
    try:
        chat_info: ChatFullInfo = await bot.get_chat(chat_id)
        
        info = f"""
        🔍 Полная информация о чате:
        
        ID: {chat_info.id}
        Тип: {chat_info.type} ({ChatType(chat_info.type).name})
        Название: {chat_info.title}
        Юзернейм: @{chat_info.username if chat_info.username else 'N/A'}
        Описание: {chat_info.description if chat_info.description else 'N/A'}
        
        👥 Участники:
        - Количество: {chat_info.members_count if hasattr(chat_info, 'members_count') else 'N/A'}
        
        
        ⚙️ Настройки:
        - Форум: {'Да' if chat_info.is_forum else 'Нет'}
        - Защита от спама: {'Включена' if chat_info.has_protected_content else 'Выключена'}
        - Анонимные админы: {'Да' if chat_info.has_aggressive_anti_spam_enabled else 'Нет'}
        
        🌐 Связанные чаты:
        - Основной чат: {chat_info.linked_chat_id if chat_info.linked_chat_id else 'N/A'}
        
        
        🕒 Время создания: {chat_info.birthdate if hasattr(chat_info, 'birthdate') else 'N/A'}
        Эмодзи статуса: {chat_info.emoji_status_custom_emoji_id or 'N/A'}
        """
        
        print(info)
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
#-------------------------------------------


async def check_topics(bot: Bot, target_chat_id: int):
    existing_topics = []
    
    for thread_id in range(1, 301):  # Проверяем ID от 1 до 300
        try:
            # Пытаемся отправить "тихое" сообщение
            await bot.send_message(
                chat_id=target_chat_id,
                message_thread_id=thread_id,
                text="...",  # Пустое сообщение
                disable_notification=True
            )
            existing_topics.append(thread_id)
            print(f"Топик {thread_id} существует!")
            
        except TelegramBadRequest as e:
            if "message thread not found" in str(e).lower():
                print(f"Топик {thread_id} не существует.")
            else:
                print(f"Ошибка для {thread_id}: {e}")
        
        except Exception as e:
            print(f"Критическая ошибка: {e}")
            break
        
        await asyncio.sleep(0.01)  # Задержка для соблюдения лимитов
    
    return existing_topics

@dp.message(Command("scan_topics"))
async def scan_topics(message: types.Message):
    target_chat_id = -1001471637496  # Замените на ID вашей группы
    
    # Проверяем, что команда вызвана в нужном чате
    if message.chat.id != target_chat_id:
        return await message.answer("Команда доступна только в целевой группе!")
    
    result = await check_topics(bot, target_chat_id)
    await message.answer(f"Найдено топиков: {len(result)}\nID: {result}")




"""
пользователь вводит id для разрешения/закрытипя 
бан id топика && id чата 

"""



#----------------------------Reply-клавиатура:
def get_reply_kb():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Кнопка 1")
    builder.button(text="Кнопка 2")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

@dp.message(Command("keyboard"), is_allowed_chat)
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

@dp.message(Command("inline"), is_allowed_chat)
async def show_inline_kb(message: types.Message):
    await message.answer("Пример inline-клавиатуры:", reply_markup=get_inline_kb())


#----------------------------отправка фотопо ссылке:
@dp.message(Command("photo"), is_allowed_chat)
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

    
@dp.message(Command("hi"), is_allowed_chat)
async def hi(message: types.Message):
    await message.answer("hi")

@dp.message(Command("get_thread_id"))
async def get_thread_id(message: types.Message):
    # Получаем ID топика (если сообщение отправлено в топике)
    thread_id = message.message_thread_id
    chat_id = message.chat.id  
    if thread_id:
        await message.reply(f"ID этого топика: {thread_id} в чате с id {chat_id}")
    else:
        await message.reply("Это сообщение не в топике! Отправьте команду в нужном подчате.")
# Команда для запуска
@dp.message(Command("game"), is_allowed_chat)
async def cmd_game(message: types.Message):
    await message.answer(
        "Нажмите кнопку, чтобы открыть игру:",
        reply_markup=get_game_keyboard()
    )

if __name__ == "__main__":
    asyncio.run(main())
