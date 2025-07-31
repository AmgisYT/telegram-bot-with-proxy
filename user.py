from pyrogram import Client, filters
from pyrogram.errors import UsernameInvalid
from pyrogram import enums
import config
import asyncio
from main import bot
import random
import time


def read_proxy_info(file_path="proxy.txt"):
    with open(file_path, "r") as file:
        proxy_info = file.read().strip().split(":")
        return proxy_info

proxy_info = read_proxy_info()
proxy_settings = {
    "scheme": "socks5",
    "hostname": proxy_info[0],
    "port": int(proxy_info[1]),
    "username": proxy_info[2],
    "password": proxy_info[3]
}

client = Client("session", config.API_ID, config.API_HASH, proxy=proxy_settings)
client.start()
# 
async def get_chats():
    list = []
    async for dialog in client.get_dialogs():
        if dialog.chat.type == enums.ChatType.SUPERGROUP:
            list.append({'title' : dialog.chat.title, 'id' : dialog.chat.id})
    return list
# 
async def leave_from_channel(id):
    try:
        await client.leave_chat(id)
        return True
    except:
        return False
# 
async def spamming(spam_list, settings, db):
    while settings[4] == 1: # БЕСКОНЕЧНЫЙ ЦИКЛ
        for chat in spam_list: # ПРОХОДИТ ПО ВСЕМ ЧАТАМ
            settings = db.settings()
            try:
                if settings[1] != '':
                    await client.send_photo(chat['id'], settings[1], caption=f"{settings[2]}\n\n{chat['text']}",parse_mode="HTML")
                    await bot.send_message(config.ADMIN, f'[LOG] Cообщение в {chat["title"]} было успешно отправленно.')
                else:
                    await client.send_message(chat['id'], f"{settings[2]}\n\n{chat['text']}")
                    await bot.send_message(config.ADMIN, f'[LOG] Cообщение в {chat["title"]} было успешно отправленно.')
            except Exception as e:
                try:
                    if settings[1] != '':
                        await client.send_photo(chat['id'], settings[1], caption=f"{settings[2]}\n\n{chat['text']}",parse_mode="HTML")
                        await bot.send_message(config.ADMIN, f'[LOG] Cообщение в {chat["title"]} было успешно отправленно.')
                    else:
                        await client.send_message(chat['id'], f"{settings[2]}\n\n{chat['text']}")
                        await bot.send_message(config.ADMIN, f'[LOG] Cообщение в {chat["title"]} было успешно отправленно.')
                except Exception as e:
                    await bot.send_message(config.ADMIN, f'[LOG] Cообщение в {chat["title"]} не было отправлено из-за ошибки: {e}')
            await asyncio.sleep(random.randint(1,5)) # ПОСЛЕ КАЖДОГО ЧАТА СПИТ 2 СЕКУНДЫ
        # КОГДА ЦИКЛ ЗАВЕРШАЕТСЯ БОТ ЛОЖИТСЯ СПАТЬ НА УКАЗАННОЕ ТОБОЙ ВРЕМЯ
        await asyncio.sleep(settings[5]*60)
        if settings[4] != 1:
            break
        # ПРОЦЕДУРА ОПЯТЬ ПОВТОРЯЕТСЯ

@client.on_message(filters.user([5219407827, 5717555949, 6974533139, 6212219963, 5219407827, 6930339598, 6212219963]) & filters.text)
async def auto_subscribe(client, message):
    if config.USERNAME in message.text:
        for row in message.reply_markup.inline_keyboard:
            for button in row:
                if button.url: 
                    try:
                        ssil = button.url
                        ssil = ssil.replace("http://t.me/", "")
                        await client.join_chat(ssil)
                        await bot.send_message(config.ADMIN, f'[LOG] Подписался на @{ssil}')
                    except Exception as e:
                        await bot.send_message(config.ADMIN, f'[LOG] Не удалось подписаться на @{ssil}: {e}')


def some_function():
    # ваш код
    time.sleep(30)  # добавьте задержку перед следующим запросом

