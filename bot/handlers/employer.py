from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.utils.database import db
from bot.keyboards.inline import back_to_menu_keyboard, cancel_keyboard
from bot.config import Config

router = Router()

# Ish beruvchi uchun state'lar (10 qadam)
class EmployerStates(StatesGroup):
    waiting_photos = State()        # 1. Rasmlar
    waiting_title = State()          # 2. Ish nomi
    waiting_description = State()    # 3. Ish haqida
    waiting_age = State()            # 4. Yosh oralig'i
    waiting_gender = State()         # 5. Jinsi
    waiting_requirements = State()   # 6. Talablar
    waiting_salary = State()         # 7. Oylik maosh
    waiting_work_type = State()      # 8. Ishlash tartibi
    waiting_meal_type = State()      # 9. Ovqatlanish
    waiting_location = State()       # 10. Manzil
    waiting_phone = State()          # 11. Telefon
    waiting_username = State()       # 12. Username

@router.callback_query(F.data == "create_job")
async def start_create_job(callback: CallbackQuery, state: FSMContext):
    """Yangi e'lon yaratish - 1-qadam"""
    user = await db.get_user(callback.from_user.id)
    
    if not user or user['user_type'] != 'employer':
        await callback.answer("❌ Siz ish beruvchi emassiz!", show_alert=True)
        return
    
    await callback.message.edit_text(
        "📝 <b>Yangi e'lon yaratish (1/10)</b>\n\n"
        "1️⃣ <b>Kompaniya rasmi</b>\n"
        "Iltimos, 1-3 tagacha rasm yuboring.\n"
        "(Ixtiyoriy, o'tkazib yuborish uchun /skip)",
        reply_markup=cancel_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(EmployerStates.waiting_photos)
    await callback.answer()

@router.message(EmployerStates.waiting_photos)
async def process_photos(message: Message, state: FSMContext):
    """1-qadam: Rasmlar"""
    if message.text and message.text == "/skip":
        await state.update_data(photos=[])
        await goto_next_step(message, state, 2)
        return
    
    if not message.photo:
        await message.answer("❌ Iltimos, rasm yuboring yoki /skip deb o'tkazib yuboring.")
        return
    
    # Rasmlarni saqlash
    data = await state.get_data()
    photos = data.get('photos', [])
    
    # Maksimal 3 ta rasm
    if len(photos) >= Config.MAX_PHOTOS:
        await message.answer(
            f"✅ {Config.MAX_PHOTOS} ta rasm yuklandi! Davom etamiz."
        )
        await goto_next_step(message, state, 2)
        return
    
    photo_id = message.photo[-1].file_id
    photos.append(photo_id)
    await state.update_data(photos=photos)
    
    remaining = Config.MAX_PHOTOS - len(photos)
    await message.answer(
        f"✅ Rasm qabul qilindi! ({len(photos)}/{Config.MAX_PHOTOS})\n"
        f"Yana {remaining} ta rasm yuborishingiz mumkin yoki /skip"
    )

async def goto_next_step(message: Message, state: FSMContext, step: int):
    """Keyingi qadamga o'tish"""
    data = await state.get_data()
    
    if step == 2:
        await message.answer(
            "📝 <b>Yangi e'lon yaratish (2/10)</b>\n\n"
            "2️⃣ <b>Ish nomi</b>\n"
            "Iltimos, ishning nomini kiriting.\n"
            "Masalan: <i>Cho'pon</i>",
            reply_markup=cancel_keyboard(),
            parse_mode="HTML"
        )
        await state.set_state(EmployerStates.waiting_title)
    
    elif step == 3:
        await message.answer(
            "📝 <b>Yangi e'lon yaratish (3/10)</b>\n\n"
            "3️⃣ <b>Ish haqida</b>\n"
            "Ish haqida batafsil ma'lumot kiriting.\n"
            "Masalan: <i>Sigirlarga qarash, sog'ish, boqish</i>",
            reply_markup=cancel_keyboard(),
            parse_mode="HTML"
        )
        await state.set_state(EmployerStates.waiting_description)
    
    elif step == 4:
        await message.answer(
            "📝 <b>Yangi e'lon yaratish (4/10)</b>\n\n"
            "4️⃣ <b>Ishchi yosh oralig'i</b>\n"
            "Format: <i>25-45</i> yoki <i>18-50</i>\n"
            "Yoki <i>60</i> - 60 yoshgacha",
            reply_markup=cancel_keyboard(),
            parse_mode="HTML"
        )
        await state.set_state(EmployerStates.waiting_age)
    
    elif step == 5:
        await message.answer(
            "📝 <b>Yangi e'lon yaratish (5/10)</b>\n\n"
            "5️⃣ <b>Jinsi</b>\n"
            "Quyidagi tugmalardan birini tanlang:",
            reply_markup=gender_keyboard(),
            parse_mode="HTML"
        )
        await state.set_state(EmployerStates.waiting_gender)
    
    elif step == 6:
        await message.answer(
            "📝 <b>Yangi e'lon yaratish (6/10)</b>\n\n"
            "6️⃣ <b>Talablar</b>\n"
            "Ishchiga qo'yiladigan talablarni kiriting.\n"
            "Masalan: <i>Chorvachilik tajribasi, veterinariya bilimi</i>",
            reply_markup=cancel_keyboard(),
            parse_mode="HTML"
        )
        await state.set_state(EmployerStates.waiting_requirements)
    
    elif step == 7:
        await message.answer(
            "📝 <b>Yangi e'lon yaratish (7/10)</b>\n\n"
            "7️⃣ <b>Oylik maosh</b>\n"
            "Maoshni kiriting (so'mda).\n"
            "Masalan: <i>5 000 000</i>",
            reply_markup=cancel_keyboard(),
            parse_mode="HTML"
        )
        await state.set_state(EmployerStates.waiting_salary)
    
    elif step == 8:
        await message.answer(
            "📝 <b>Yangi e'lon yaratish (8/10)</b>\n\n"
            "8️⃣ <b>Ishlash tartibi</b>\n"
            "Quyidagi tugmalardan birini tanlang:",
            reply_markup=work_type_keyboard(),
            parse_mode="HTML"
        )
        await state.set_state(EmployerStates.waiting_work_type)
    
    elif step == 9:
        await message.answer(
            "📝 <b>Yangi e'lon yaratish (9/10)</b>\n\n"
            "9️⃣ <b>Ovqatlanish</b>\n"
            "Quyidagi tugmalardan birini tanlang:",
            reply_markup=meal_type_keyboard(),
            parse_mode="HTML"
        )
        await state.set_state(EmployerStates.waiting_meal_type)
    
    elif step == 10:
        await message.answer(
            "📝 <b>Yangi e'lon yaratish (10/10)</b>\n\n"
            "🔟 <b>Manzil</b>\n"
            "Ish joyining manzilini kiriting.\n"
            "Masalan: <i>Toshkent viloyati, Chinoz tumani</i>",
            reply_markup=cancel_keyboard(),
            parse_mode="HTML"
        )
        await state.set_state(EmployerStates.waiting_location)
    
    elif step == 11:
        await message.answer(
            "📝 <b>Yangi e'lon yaratish (11/10)</b>\n\n"
            "1️⃣1️⃣ <b>Telefon raqam</b>\n"
            "Telefon raqamingizni kiriting.\n"
            "Masalan: <i>+998901234567</i>",
            reply_markup=cancel_keyboard(),
            parse_mode="HTML"
        )
        await state.set_state(EmployerStates.waiting_phone)
    
    elif step == 12:
        await message.answer(
            "📝 <b>Yangi e'lon yaratish (12/10)</b>\n\n"
            "1️⃣2️⃣ <b>Telegram username</b>\n"
            "Telegram username'ingizni kiriting (ixtiyoriy).\n"
            "Masalan: <i>@username</i>\n"
            "O'tkazib yuborish uchun /skip",
            reply_markup=cancel_keyboard(),
            parse_mode="HTML"
        )
        await state.set_state(EmployerStates.waiting_username)

def gender_keyboard():
    """Jins tanlash tugmalari"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🧑 Erkak", callback_data="gender_male"),
            InlineKeyboardButton(text="👩 Ayol", callback_data="gender_female"),
            InlineKeyboardButton(text="👥 Farqi yo'q", callback_data="gender_any")
        ],
        [InlineKeyboardButton(text="🔙 Bekor qilish", callback_data="cancel")]
    ])

def work_type_keyboard():
    """Ishlash tartibi tugmalari"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🏠 Yotib ishlash", callback_data="work_live_in"),
            InlineKeyboardButton(text="🚶 Kelib-ketish", callback_data="work_live_out")
        ],
        [InlineKeyboardButton(text="🔙 Bekor qilish", callback_data="cancel")]
    ])

def meal_type_keyboard():
    """Ovqatlanish tugmalari"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="👨‍🍳 Ish beruvchi hisobidan", callback_data="meal_employer"),
            InlineKeyboardButton(text="🍽️ Ishchi o'z hisobidan", callback_data="meal_worker")
        ],
        [InlineKeyboardButton(text="🔙 Bekor qilish", callback_data="cancel")]
    ])

# Qolgan handler'lar keyingi xabarlarda...
