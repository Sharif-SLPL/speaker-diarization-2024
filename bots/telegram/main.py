from email.mime import audio
import os
import io
import zipfile
import logging
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackContext, MessageHandler, filters

import diarization as d


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

MAX_MESSAGE_LENGTH = 4096

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hi\nsend me a vocie, i recognize speackers in the vocie :)")


async def handle_diarization(update: Update, context: CallbackContext, file):
    print("processing request ...")
    out = io.BytesIO()
    await file.download_to_memory(out)
    out.seek(0)
    result = d.async_diarize(out)
    out.close()
    if result == None:
        await context.bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=update.message.message_id, text='timeout reached!')
        return
    parsed = d.parse_diarize_result(result)
    
    if len(parsed) <= MAX_MESSAGE_LENGTH:
        await context.bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=update.message.message_id, text=parsed)
    else:
        file_like_object = io.BytesIO()
        file_like_object.write(parsed.encode('utf-8'))
        file_like_object.seek(0)
        await context.bot.send_document(chat_id=update.effective_chat.id, reply_to_message_id=update.message.message_id, document=file_like_object, filename="result.txt")


async def handle_voice(update: Update, context: CallbackContext):
    voice = await context.bot.get_file(update.message.voice.file_id)
    await handle_diarization(update, context, voice)


async def handle_audio(update: Update, context: CallbackContext):
    audio = await context.bot.get_file(update.message.audio.file_id)
    await handle_diarization(update, context, audio)


async def handle_audio_file(update: Update, context: CallbackContext):
    audio_file = await context.bot.get_file(update.message.effective_attachment.file_id)
    await handle_diarization(update, context, audio_file)


if __name__ == '__main__':
    load_dotenv()
    proxy = os.getenv('PROXY')

    os.environ['http_proxy'] = proxy
    os.environ['HTTP_PROXY'] = proxy
    os.environ['https_proxy'] = proxy
    os.environ['HTTPS_PROXY'] = proxy

    
    token = os.getenv('TELEGRAM_TOKEN')

    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.VOICE, handle_voice))
    application.add_handler(MessageHandler(filters.AUDIO, handle_audio))
    application.add_handler(MessageHandler(
        filters.Document.Category("audio/"), handle_audio_file))

    application.run_polling()
