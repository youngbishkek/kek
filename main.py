from telethon import TelegramClient, events

api_id = '20904033'
api_hash = '76d5b1af83337d4a2129aed1456dc2b7'

source_channel_ids = [-1001394050290, -1001101170442, -1001050820672, -1001099860397, -1001117628569, -1001708761316, -1001741877871]
destination_channel_id = -1001988868149

# Создаем клиента Telegram
client = TelegramClient('session_name', api_id, api_hash)


# Обработчик событий для новых входящих сообщений в исходных каналах
@client.on(events.NewMessage(chats=source_channel_ids))
async def handle_new_message(event):
    # Получаем новое сообщение
    message = event.message
    
    # Проверяем, содержит ли сообщение файлы
    if message.media and hasattr(message.media, 'document'):
        # Получаем все файлы из сообщения
        files = message.media.document.attributes
        if len(files) > 1:
            # Сортируем файлы по размеру в порядке убывания
            sorted_files = sorted(files, key=lambda attr: attr.file_size, reverse=True)
            largest_file = sorted_files[0]
            
            # Создаем новое сообщение только с самым большим файлом
            new_message = await client.send_file(destination_channel_id, file=largest_file)
            
            # Удаляем оригинальное сообщение из исходного канала
            await message.delete()
        else:
            # Отправляем сообщение с единственным файлом в целевой канал
            await client.send_file(destination_channel_id, file=files[0])
    else:
        # Отправляем сообщение без файлов в целевой канал
        await message.forward_to(destination_channel_id)


# Запускаем клиента Telegram
client.start()

# Запускаем бесконечный цикл для ожидания новых сообщений
client.run_until_disconnected()
