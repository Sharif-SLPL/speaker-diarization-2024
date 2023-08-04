import os
import io
import zipfile
import logging
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackContext, MessageHandler, filters

import diarization as d


proxy = 'http://127.0.0.1:1082'
proxy = 'socks5://127.0.0.1:1081'

os.environ['http_proxy'] = proxy
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hi\send me a vocie, i recognize speackers in that vocie :)")

async def handle_voice(update: Update, context: CallbackContext):
    new_file = await context.bot.get_file(update.message.voice.file_id)
    # await new_file.download_to_drive("voice_note.wav")
    out = io.BytesIO()
    await new_file.download_to_memory(out)
    out.seek(0)
    result = d.diarize(out)
    # await update.message.reply_text(result)
    await context.bot.send_photo(update.message.chat_id, photo=result)
    out.close()
    # resultFile = io.StringIO(result)
    # await context.bot.send_document(update.message.chat_id, resultFile)


async def handle_audio(update: Update, context: CallbackContext):
    # await context.bot.send_message(chat_id=update.effective_chat.id, text="Hi\send me a vocie, i recognize speackers in that vocie :)))))))))")
    new_file = await context.bot.get_file(update.message.audio.file_id)
    # await new_file.download_to_drive("voice_note.wav")
    out = io.BytesIO()
    await new_file.download_to_memory(out)
    out.seek(0)
    result = d.diarize(out)
    # await update.message.reply_text(result)
    await context.bot.send_photo(update.message.chat_id, photo=result)
    out.close()
    # resultFile = io.StringIO(result)
    # await context.bot.send_document(update.message.chat_id, resultFile)


async def handle_audio_file(update: Update, context: CallbackContext):
    # await context.bot.send_message(chat_id=update.effective_chat.id, text="Hi\send me a vocie, i recognize speackers in that vocie :)))))))))")
    new_file = await context.bot.get_file(update.message.effective_attachment.file_id)
    # await new_file.download_to_drive("voice_note.wav")
    out = io.BytesIO()
    await new_file.download_to_memory(out)
    out.seek(0)
    result = d.diarize(out)
    # await update.message.reply_text(result)
    await context.bot.send_photo(update.message.chat_id, photo=result)
    out.close()
    # resultFile = io.StringIO(result)
    # await context.bot.send_document(update.message.chat_id, resultFile)


if __name__ == '__main__':
    load_dotenv()
    token = os.getenv('TELEGRAM_TOKEN')
    
    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.VOICE, handle_voice))
    application.add_handler(MessageHandler(filters.AUDIO, handle_audio))
    application.add_handler(MessageHandler(filters.Document.Category("audio/"), handle_audio_file))

    application.run_polling()
