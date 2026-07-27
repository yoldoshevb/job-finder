#!/usr/bin/env python3
"""
SmartJobBot - Ish topish boti
"""

import asyncio
import sys
import os
from dotenv import load_dotenv

# .env faylini yuklash
load_dotenv()

# Bot import
from bot.main import main

if __name__ == "__main__":
    print("🚀 SmartJobBot ishga tushmoqda...")
    print(f"📡 BOT_TOKEN: {os.getenv('BOT_TOKEN', 'NOT SET')[:20]}...")
    print(f"🗄️ DATABASE_URL: {os.getenv('DATABASE_URL', 'NOT SET')[:30]}...")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("⏹️ Bot to'xtatildi.")
    except Exception as e:
        print(f"❌ Xatolik: {e}")
        sys.exit(1)
