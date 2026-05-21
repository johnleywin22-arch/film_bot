import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from database import create_table, get_film, add_film, update_film, delete_film, get_all_films, get_stats

# ===================== SOZLAMALAR =====================
BOT_TOKEN =  "8952846799:AAFO5rQaERgEgeDt_JXyshRLgjt8H75jtF0"  # @BotFather dan olingan token
ADMIN_IDS = [8103333488]            # Admin Telegram ID raqamlari

# ===================== LOGGING =====================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===================== BOT VA DISPATCHER =====================
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# ===================== FSM HOLATLARI =====================
class AddFilm(StatesGroup):
    waiting_code = State()
    waiting_title = State()
    waiting_file = State()
    waiting_description = State()

class DeleteFilm(StatesGroup):
    waiting_code = State()

# ===================== YORDAMCHI FUNKSIYALAR =====================
def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

# ===================== BUYRUQLAR =====================

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "🎬 <b>Film Bot</b>ga xush kelibsiz!\n\n"
        "Film kodini yuboring va men sizga filmni topib beraman.\n\n"
        "Misol: <code>F001</code>",
        parse_mode="HTML"
    )

@dp.message(Command("help"))
async def cmd_help(message: Message):
    text = (
        "📖 <b>Yordam</b>\n\n"
        "🎬 Film olish uchun shunchaki <b>kodni</b> yuboring.\n"
        "Misol: <code>F001</code>\n\n"
    )
    if is_admin(message.from_user.id):
        text += (
            "👮 <b>Admin buyruqlari:</b>\n"
            "/add — Yangi film qo'shish\n"
            "/delete — Film o'chirish\n"
            "/list — Barcha filmlar\n"
            "/stats — Statistika\n"
        )
    await message.answer(text, parse_mode="HTML")

# ===================== FILM QIDIRISH =====================

@dp.message(F.text & ~F.text.startswith("/"))
async def search_film(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        return  # FSM holati aktiv bo'lsa, bu handlerni o'tkazib yuborish

    code = message.text.strip()
    film = get_film(code)

    if film:
        caption = f"🎬 <b>{film['title']}</b>\n📌 Kod: <code>{film['code']}</code>"
        if film["description"]:
            caption += f"\n\n📝 {film['description']}"

        await bot.send_video(
            chat_id=message.chat.id,
            video=film["file_id"],
            caption=caption,
            parse_mode="HTML"
        )
    else:
        await message.answer(
            f"❌ <b>{code}</b> kodi bo'yicha film topilmadi.\n"
            "Kodni to'g'ri kiritganingizni tekshiring.",
            parse_mode="HTML"
        )

# ===================== ADMIN: FILM QO'SHISH =====================

@dp.message(Command("add"))
async def cmd_add(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Bu buyruq faqat adminlar uchun.")
        return
    await state.set_state(AddFilm.waiting_code)
    await message.answer("🎬 Yangi film qo'shish\n\n1️⃣ Film kodini kiriting (masalan: <code>F001</code>):", parse_mode="HTML")

@dp.message(AddFilm.waiting_code)
async def process_code(message: Message, state: FSMContext):
    code = message.text.strip().upper()
    existing = get_film(code)
    if existing:
        await message.answer(f"⚠️ <b>{code}</b> kodi allaqachon mavjud. Boshqa kod kiriting:", parse_mode="HTML")
        return
    await state.update_data(code=code)
    await state.set_state(AddFilm.waiting_title)
    await message.answer("2️⃣ Film nomini kiriting:")

@dp.message(AddFilm.waiting_title)
async def process_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text.strip())
    await state.set_state(AddFilm.waiting_file)
    await message.answer("3️⃣ Film faylini yuboring (video):")

@dp.message(AddFilm.waiting_file, F.video)
async def process_file(message: Message, state: FSMContext):
    file_id = message.video.file_id
    await state.update_data(file_id=file_id)
    await state.set_state(AddFilm.waiting_description)
    await message.answer("4️⃣ Film haqida qisqacha tavsif kiriting (o'tkazib yuborish uchun <code>-</code> yuboring):", parse_mode="HTML")

@dp.message(AddFilm.waiting_description)
async def process_description(message: Message, state: FSMContext):
    description = "" if message.text.strip() == "-" else message.text.strip()
    data = await state.get_data()
    await state.clear()

    success = add_film(data["code"], data["title"], data["file_id"], description)
    if success:
        await message.answer(
            f"✅ Film muvaffaqiyatli qo'shildi!\n\n"
            f"🎬 <b>{data['title']}</b>\n"
            f"📌 Kod: <code>{data['code']}</code>",
            parse_mode="HTML"
        )
    else:
        await message.answer("❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.")

# ===================== ADMIN: FILM O'CHIRISH =====================

@dp.message(Command("delete"))
async def cmd_delete(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Bu buyruq faqat adminlar uchun.")
        return
    await state.set_state(DeleteFilm.waiting_code)
    await message.answer("🗑 O'chirmoqchi bo'lgan film kodini kiriting:")

@dp.message(DeleteFilm.waiting_code)
async def process_delete(message: Message, state: FSMContext):
    code = message.text.strip().upper()
    await state.clear()
    success = delete_film(code)
    if success:
        await message.answer(f"✅ <b>{code}</b> kodi bo'yicha film o'chirildi.", parse_mode="HTML")
    else:
        await message.answer(f"❌ <b>{code}</b> kodi topilmadi.", parse_mode="HTML")

# ===================== ADMIN: RO'YXAT =====================

@dp.message(Command("list"))
async def cmd_list(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Bu buyruq faqat adminlar uchun.")
        return
    films = get_all_films()
    if not films:
        await message.answer("📭 Bazada hali film yo'q.")
        return

    text = "🎬 <b>Barcha filmlar:</b>\n\n"
    for film in films:
        text += f"📌 <code>{film['code']}</code> — {film['title']}\n"
    await message.answer(text, parse_mode="HTML")

# ===================== ADMIN: STATISTIKA =====================

@dp.message(Command("stats"))
async def cmd_stats(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Bu buyruq faqat adminlar uchun.")
        return
    stats = get_stats()
    await message.answer(
        f"📊 <b>Statistika:</b>\n\n"
        f"🎬 Jami filmlar: <b>{stats['total_films']}</b>",
        parse_mode="HTML"
    )

# ===================== ISHGA TUSHIRISH =====================

async def main():
    create_table()
    logger.info("Bot ishga tushmoqda...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
