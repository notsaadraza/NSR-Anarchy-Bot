import time
import random
from threading import Thread
from javascript import require, On

mineflayer = require('mineflayer')
pathfinder = require('mineflayer-pathfinder')
pvp = require('mineflayer-pvp').plugin
autoeat = require('mineflayer-auto-eat').plugin
armorManager = require('mineflayer-armor-manager')

# --- SETTINGS ---
IP = 'nsranarchy.aternos.me'
PORT = 44441
USERNAME = 'Corona_Virus'
VERSION = '1.20.1'

def create_bot():
    print("🚀 Bot starting...")
    bot = mineflayer.createBot({
        'host': IP,
        'port': PORT,
        'username': USERNAME,
        'version': VERSION
    })

    # Plugins Load Karein
    bot.loadPlugin(pathfinder.pathfinder)
    bot.loadPlugin(pvp)
    bot.loadPlugin(autoeat)
    bot.loadPlugin(armorManager)

    @On(bot, 'spawn')
    def handle_spawn(*args):
        print(f"✅ {bot.username} is online!")
        bot.chat("NSR Ultra Bot is here! No Rules, Just Anarchy.")

    # 1. AUTO CHAT (Har 5 minute baad)
    def announcer():
        while True:
            time.sleep(300) # 5 minutes
            try:
                bot.chat("This is a 24/7 Anarchy server, That mean no rules.")
            except: pass

    # 2. RANDOM MOVEMENT (Jump, Sneak, Walk)
    def start_moving():
        actions = ['jump', 'sneak', 'forward', 'back', 'left', 'right']
        while True:
            if not bot.pvp.target:
                act = random.choice(actions)
                bot.setControlState(act, True)
                time.sleep(random.uniform(0.5, 1.5))
                bot.setControlState(act, False)
                bot.look(random.uniform(0, 360), random.uniform(-20, 20))
            time.sleep(1)

    # 3. SELF DEFENSE (Revenge)
    @On(bot, 'entityHurt')
    def handle_hurt(this, entity, *args):
        if entity.username == bot.username:
            enemy = bot.nearestEntity(lambda e: e.type == 'player')
            if enemy:
                bot.pvp.attack(enemy)

    # 4. RECONNECT SYSTEM
    @On(bot, 'end')
    def handle_end(*args):
        print("🔄 Server off or kicked. Reconnecting in 20s...")
        time.sleep(20)
        create_bot()

    # background tasks start karein
    Thread(target=announcer, daemon=True).start()
    Thread(target=start_moving, daemon=True).start()

create_bot()
