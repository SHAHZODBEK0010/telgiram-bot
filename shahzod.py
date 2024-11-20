from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os
import nest_asyncio
import asyncio

# nest_asyncio ni ishga tushirish
nest_asyncio.apply()

# Bot tokenini qo'shing
BOT_TOKEN = "5650860925:AAHs-MlgGc8ynR6PslnymdMhrRNmfLPOMzw"

# Foydali fayllar
schedule_image_path = "photo_2024-11-20_10-19-58.jpg"  # Dars jadvali rasmi joylashgan manzil
homework_file_path = "Sayyora Rahmonqulova. Kompyuter olamiga sayohat.pdf"  # Uyga vazifa fayli manzili
ebooks = {
    "Python asoslari": "GqIpOwhkoxw3HtvyNikcpython_basics.pdf",
    "Kompyuter savodxonligi": "21352_2_65D77B7B9DD95C36F22F90F3BEF95F5A76A0DDF7.pdf",
    "Matematika qo'llanmasi": "2023-11-10-10-42-53_3a5ab7ae17ff5ce1bac4eb32ea7001e1.pdf",
}

# Start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! O‘quv markazi botiga xush kelibsiz! Quyidagilarni tanlang:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📅 Dars jadvali", callback_data="schedule")],
            [InlineKeyboardButton("📚 Uyga vazifa", callback_data="homework")],
            [InlineKeyboardButton("📖 Elektron kitoblar", callback_data="ebooks")],
        ])
    )

# Callback funksiyalar
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "schedule":
        # Dars jadvali rasmini yuborish
        if os.path.exists(schedule_image_path):
            with open(schedule_image_path, "rb") as f:
                await query.message.reply_photo(photo=f, caption="Dars jadvali")
        else:
            await query.message.reply_text("Dars jadvali rasmini topib bo'lmadi.")
    
    elif query.data == "homework":
        # Uyga vazifa faylini yuborish
        if os.path.exists(homework_file_path):
            with open(homework_file_path, "rb") as f:
                await query.message.reply_document(document=f, caption="Uyga vazifa")
        else:
            await query.message.reply_text("Uyga vazifa faylini topib bo'lmadi.")

    elif query.data == "ebooks":
        # Elektron kitoblar ro'yxati
        buttons = [
            [InlineKeyboardButton(name, callback_data=f"ebook_{name}")]
            for name in ebooks.keys()
        ]
        await query.message.reply_text(
            "Quyidagi elektron kitoblardan birini tanlang:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif query.data.startswith("ebook_"):
        # Elektron kitobni yuborish
        book_name = query.data.split("_", 1)[1]
        file_path = ebooks.get(book_name)
        if file_path and os.path.exists(file_path):
            with open(file_path, "rb") as f:
                await query.message.reply_document(document=f, caption=book_name)
        else:
            await query.message.reply_text(f"{book_name} kitobini topib bo'lmadi.")

# Botni ishga tushirish
async def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Komandalarni ro'yxatga olish
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    # Botni ishga tushirish
    print("Bot ishlamoqda...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
