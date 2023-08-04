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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hi\send me a vocie, i recognize speackers in that vocie :)")


async def handle_diarization(update: Update, context: CallbackContext, file):
    out = io.BytesIO()
    await file.download_to_memory(out)
    out.seek(0)
    result = d.diarize(out)
    await context.bot.send_photo(update.message.chat_id, photo=result)
    out.close()


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
