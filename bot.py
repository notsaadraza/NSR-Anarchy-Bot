from javascript import require, On, AsyncTask
import time

mineflayer = require('mineflayer')

# --- ATERNOS SERVER SETTINGS ---
bot_args = {
    'host': 'nsranarchy.aternos.me', 
    'port': 44441,                     
    'username': 'NSRAnarchy_Bot1',      
    'version': '1.21.1',               
    'hideErrors': True
}

def create_bot():
    bot = mineflayer.createBot(bot_args)

    @On(bot, 'spawn')
    def handle_spawn(*args):
        print(f"✅ [ATERNOS] Bot {bot.username} has joined!")
        print("💡 Server status: STAYS ONLINE 24/7")
        
        # Anti-AFK Movement (Aternos specific)
        @AsyncTask(start=True)
        def anti_kick(task):
            while True:
                # Thoda aage peeche chalna
                bot.setControlState('forward', True)
                time.sleep(1)
                bot.setControlState('forward', False)
                bot.setControlState('back', True)
                time.sleep(1)
                bot.setControlState('back', False)
                
                # Jump karna
                bot.setControlState('jump', True)
                time.sleep(0.5)
                bot.setControlState('jump', False)
                
                # Wait for 30 seconds
                time.sleep(30)

    # Login & Register System
    @On(bot, 'chat')
    def handle_chat(this, username, message, *args):
        msg = message.lower()
        # Aapka bataya hua password 'NSRAnarchy_Bot1'
        if "/register" in msg:
            bot.chat("/register NSRAnarchy_Bot1 NSRAnarchy_Bot1")
        elif "/login" in msg:
            bot.chat("/login NSRAnarchy_Bot1")

    # Agar bot kick ho jaye (Server restart/lag)
    @On(bot, 'kicked')
    def handle_kicked(this, reason, *args):
        print(f"⚠️ Kicked from server. Reason: {reason}")

    @On(bot, 'end')
    def handle_end(*args):
        print("🔄 Reconnecting in 20 seconds...")
        time.sleep(20)
        create_bot()

create_bot()