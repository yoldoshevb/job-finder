import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import Config
from bot.handlers.start import router as start_router
from bot.handlers.employer import router as employer_router
from bot.handlers.worker import router as worker_router
from bot.utils.database import Database

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Bot va dispatcher
bot = Bot(
    token=Config.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# Database
db = Database()

async def setup_commands():
    """Bot komandalarini sozlash"""
    commands = [
        BotCommand(command="start", description="🚀 Botni ishga tushirish"),
        BotCommand(command="help", description="❓ Yordam"),
        BotCommand(command="menu", description="📋 Bosh menyu"),
    ]
    await bot.set_my_commands(commands)

async def on_startup():
    """Bot ishga tushganda"""
    logger.info("🔄 Database ga ulanish...")
    await db.connect()
    logger.info("✅ Database ulandi!")
    
    logger.info("🔄 Bot komandalari sozlanmoqda...")
    await setup_commands()
    
    logger.info("🚀 SmartJobBot ishga tushdi!")

async def on_shutdown():
    """Bot to'xtaganda"""
    logger.info("🔄 Database dan uzilish...")
    await db.close()
    logger.info("✅ Database uzildi!")
    logger.info("⏹️ Bot to'xtatildi.")

async def main():
    """Asosiy funksiya"""
    # Router'larni ulash
    dp.include_router(start_router)
    dp.include_router(employer_router)
    dp.include_router(worker_router)
    
    # Start va shutdown eventlari
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    # Botni ishga tushirish
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"❌ Bot ishlamadi: {e}")
        raise
