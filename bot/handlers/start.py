from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from bot.utils.database import db
from bot.config import Config
from bot.keyboards.inline import (
    role_selection_keyboard,
    employer_menu_keyboard,
    worker_menu_keyboard
)

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """/start komandasi"""
    user_id = message.from_user.id
    username = message.from_user.username
    
    # Foydalanuvchini tekshirish
    user = await db.get_user(user_id)
    
    if user:
        # Agar ro'yxatdan o'tgan bo'lsa
        if user['user_type'] == 'employer':
            await message.answer(
                "🏢 <b>Xush kelibsiz, Ish beruvchi!</b>\n\n"
                "Quyidagi menyudan kerakli bo'limni tanlang:",
                reply_markup=employer_menu_keyboard(),
                parse_mode="HTML"
            )
        else:
            await message.answer(
                "👷 <b>Xush kelibsiz, Ishchi!</b>\n\n"
                "Quyidagi menyudan kerakli bo'limni tanlang:",
                reply_markup=worker_menu_keyboard(),
                parse_mode="HTML"
            )
    else:
        # Yangi foydalanuvchi
        await message.answer(
            "🤖 <b>SmartJobBot ga xush kelibsiz!</b>\n\n"
            "Bu yerda siz:\n"
            "✅ Ish e'lonlarini joylay olasiz\n"
            "✅ Ish topishingiz mumkin\n"
            "✅ AI sizga eng mos variantlarni topib beradi\n\n"
            "Iltimos, kim sifatida ro'yxatdan o'tmoqchisiz?",
            reply_markup=role_selection_keyboard(),
            parse_mode="HTML"
        )

@router.message(Command("menu"))
async def cmd_menu(message: Message):
    """Bosh menyu"""
    user = await db.get_user(message.from_user.id)
    
    if user:
        if user['user_type'] == 'employer':
            await message.answer(
                "🏢 <b>Bosh menyu</b>",
                reply_markup=employer_menu_keyboard(),
                parse_mode="HTML"
            )
        else:
            await message.answer(
                "👷 <b>Bosh menyu</b>",
                reply_markup=worker_menu_keyboard(),
                parse_mode="HTML"
            )
    else:
        await cmd_start(message, None)

@router.message(Command("help"))
async def cmd_help(message: Message):
    """Yordam"""
    await message.answer(
        "❓ <b>Yordam</b>\n\n"
        "Bot haqida: SmartJobBot - ish topish va ishchi topish uchun AI asosidagi bot.\n\n"
        "📋 <b>Asosiy komandalar:</b>\n"
        "/start - Botni ishga tushirish\n"
        "/menu - Bosh menyu\n"
        "/help - Yordam\n\n"
        "📞 <b>Aloqa:</b> @support_username\n"
        "📄 <b>GitHub:</b> github.com/username/smart-job-bot",
        parse_mode="HTML"
    )

@router.callback_query(F.data == "main_menu")
async def callback_main_menu(callback: CallbackQuery):
    """Bosh menyu tugmasi"""
    user = await db.get_user(callback.from_user.id)
    
    if user:
        if user['user_type'] == 'employer':
            await callback.message.edit_text(
                "🏢 <b>Bosh menyu</b>",
                reply_markup=employer_menu_keyboard(),
                parse_mode="HTML"
            )
        else:
            await callback.message.edit_text(
                "👷 <b>Bosh menyu</b>",
                reply_markup=worker_menu_keyboard(),
                parse_mode="HTML"
            )
    await callback.answer()

@router.callback_query(F.data == "role_employer")
async def callback_role_employer(callback: CallbackQuery, state: FSMContext):
    """Ish beruvchi rolini tanlash"""
    user_id = callback.from_user.id
    username = callback.from_user.username
    
    # Foydalanuvchini yaratish yoki yangilash
    user = await db.create_user(user_id, username, 'employer')
    
    await callback.message.edit_text(
        "✅ <b>Siz Ish beruvchi sifatida ro'yxatdan o'tdingiz!</b>\n\n"
        "Endi siz yangi e'lon yaratishingiz yoki ishchilarni qidirishingiz mumkin.",
        reply_markup=employer_menu_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == "role_worker")
async def callback_role_worker(callback: CallbackQuery, state: FSMContext):
    """Ishchi rolini tanlash"""
    user_id = callback.from_user.id
    username = callback.from_user.username
    
    # Foydalanuvchini yaratish yoki yangilash
    user = await db.create_user(user_id, username, 'worker')
    
    await callback.message.edit_text(
        "✅ <b>Siz Ishchi sifatida ro'yxatdan o'tdingiz!</b>\n\n"
        "Endi siz profilingizni yaratishingiz va ish qidirishingiz mumkin.",
        reply_markup=worker_menu_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()
