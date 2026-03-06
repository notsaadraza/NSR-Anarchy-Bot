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
PASSWORD = 'NSRBOT1'
VERSION = '1.20.1'

def create_bot():
    print(f"🚀 Starting Bot: {USERNAME} on Port: {PORT}")
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
        # 1. Automatic Login/Register
        time.sleep(2)
        bot.chat(f"/register {PASSWORD} {PASSWORD}")
        time.sleep(1)
        bot.chat(f"/login {PASSWORD}")
        
        print(f"✅ {bot.username} is online and logged in!")
        
        # Start background tasks
        Thread(target=announcer, daemon=True).start()
        Thread(target=ultra_movement, daemon=True).start()

    # --- 1. SMART ANNOUNCER (Har 5 Min) ---
    def announcer():
        while True:
            time.sleep(300) # 5 Minutes
            if bot.entity:
                bot.chat("This is 24/7 Anarchy server, That mean no rules.")

    # --- 2. ULTRA HUMAN-LIKE MOVEMENT ---
    def ultra_movement():
        actions = ['jump', 'sneak', 'forward', 'back', 'left', 'right']
        while True:
            if not bot.pvp.target:
                # Randomly perform actions
                act = random.choice(actions)
                bot.setControlState(act, True)
                time.sleep(random.uniform(0.5, 2.0))
                bot.setControlState(act, False)
                
                # Randomly look around
                bot.look(random.uniform(0, 360), random.uniform(-30, 30))
            
            time.sleep(random.randint(2, 7))

    # --- 3. AUTO-REVENGE (Defend itself) ---
    @On(bot, 'entityHurt')
    def handle_hurt(this, entity, *args):
        if entity.username == bot.username:
            enemy = bot.nearestEntity(lambda e: e.type == 'player')
            if enemy:
                bot.chat(f"Oye {enemy.username}! Badla toh lena parega!")
                bot.pvp.attack(enemy)

    # --- 4. RECONNECT SYSTEM ---
    @On(bot, 'end')
    def handle_end(*args):
        print("🔄 Connection lost. Reconnecting in 20s...")
        time.sleep(20)
        create_bot()

create_bot()
