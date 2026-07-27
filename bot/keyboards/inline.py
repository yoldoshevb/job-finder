from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def role_selection_keyboard():
    """Rol tanlash tugmalari"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🏢 Ish beruvchi", callback_data="role_employer"),
            InlineKeyboardButton(text="👷 Ishchi", callback_data="role_worker")
        ]
    ])

def employer_menu_keyboard():
    """Ish beruvchi menyusi"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📝 Yangi e'lon", callback_data="create_job"),
            InlineKeyboardButton(text="📋 Mening e'lonlarim", callback_data="my_jobs")
        ],
        [
            InlineKeyboardButton(text="👥 Ishchilar", callback_data="find_workers"),
            InlineKeyboardButton(text="📊 Statistika", callback_data="employer_stats")
        ],
        [
            InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="settings"),
            InlineKeyboardButton(text="💬 Xabarlar", callback_data="messages")
        ],
        [
            InlineKeyboardButton(text="❓ Yordam", callback_data="help")
        ]
    ])

def worker_menu_keyboard():
    """Ishchi menyusi"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📝 Profil yaratish", callback_data="create_profile"),
            InlineKeyboardButton(text="📋 Mening profilim", callback_data="my_profile")
        ],
        [
            InlineKeyboardButton(text="💼 Ish qidirish", callback_data="find_jobs"),
            InlineKeyboardButton(text="📊 Mening statistikam", callback_data="worker_stats")
        ],
        [
            InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="settings"),
            InlineKeyboardButton(text="💬 Xabarlar", callback_data="messages")
        ],
        [
            InlineKeyboardButton(text="❓ Yordam", callback_data="help")
        ]
    ])

def back_to_menu_keyboard():
    """Bosh menyuga qaytish"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Bosh menyu", callback_data="main_menu")]
    ])

def cancel_keyboard():
    """Bekor qilish"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel")]
    ])

def settings_keyboard():
    """Sozlamalar menyusi"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🌐 Til", callback_data="settings_lang"),
            InlineKeyboardButton(text="🔔 Eslatmalar", callback_data="settings_notif")
        ],
        [
            InlineKeyboardButton(text="🔙 Bosh menyu", callback_data="main_menu")
        ]
    ])
