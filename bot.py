# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )    

# IMPORTS 🤖

import os
import subprocess
import threading
import json
import time
import telebot
import uuid
import atexit
from collections import defaultdict
from telebot import types

# YOUR BoT TOKEN 🌺

TOKEN = "7237463222:AAH2Q6DCTsTMgtIbl01Ss3fODwxh8ptqhtQ"

# YOUR CREDENTIALS 👇🌀

ADMIN_IDS = [7858368373]

CHANNEL_USERNAME = '@TEAM_x_OG'

MAX_CONCURRENT_FILES = 2
USER_DIR_PREFIX = "user_files"
STATE_FILE = "bot_state.json"
LOG_DIR = "logs"

bot = telebot.TeleBot(TOKEN)


running_processes = defaultdict(dict)
user_files = defaultdict(list)
banned_users = set()
blocked_users = set()
all_users = set()
lock = threading.Lock()

# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  

os.makedirs(USER_DIR_PREFIX, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  

def load_state():
    global running_processes, banned_users, blocked_users, all_users
    try:
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
            running_processes.update(state.get('running_processes', {}))
            banned_users = set(state.get('banned_users', []))
            blocked_users = set(state.get('blocked_users', []))
            all_users = set(state.get('all_users', []))
    except FileNotFoundError:
        pass

def save_state():
    state = {
        'running_processes': {
            uid: {pid: data for pid, data in procs.items()}
            for uid, procs in running_processes.items()
        },
        'banned_users': list(banned_users),
        'blocked_users': list(blocked_users),
        'all_users': list(all_users)
    }
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

atexit.register(save_state)
load_state()
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  

def get_user_dir(user_id):
    return os.path.join(USER_DIR_PREFIX, str(user_id))

def create_user_dir(user_id):
    user_dir = get_user_dir(user_id)
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    return user_dir

def is_admin(user_id):
    return user_id in ADMIN_IDS

def send_admin_notification(message):
    for admin_id in ADMIN_IDS:
        bot.send_message(admin_id, message)

def log_execution(user_id, filename, output, error):
    log_file = os.path.join(LOG_DIR, f"{user_id}_{int(time.time())}.log")
    with open(log_file, 'w') as f:
        f.write(f"Output:\n{output}\n\nErrors:\n{error}")


def handle_errors(func):
    def wrapper(message):
        user_id = message.from_user.id
        if user_id in banned_users:
            bot.reply_to(message, "❌ You Hᴀvᴇ Bᴇᴇɴ Bᴀɴɴᴇᴅ Fʀoм Tнιs Boт\n\nIғ You Tнιɴκ Tнιs Is ᴀ Mιsтᴀκᴇ Pʟᴇᴀsᴇ\nCoɴтᴀcт Suᴘᴘoʀт :- @pb_x01")
            return
        if user_id in blocked_users:
            bot.reply_to(message, "❌ Youʀ Accouɴт Is Bʟocκᴇᴅ Fʀoм Tнιs Boт\n\nIғ You Tнιɴκ Tнιs Is ᴀ Mιsтᴀκᴇ Pʟᴇᴀsᴇ\nCoɴтᴀcт Suᴘᴘoʀт :- @pb_x01")
            return
        try:
            return func(message)
        except Exception as e:
            bot.reply_to(message, f"🚨 Error: {str(e)}")
    return wrapper

# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  

from datetime import datetime

# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  


def save_user(user_id):
    pass

def is_user_member(user_id):
    try:
        chat_member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return chat_member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Error checking user membership: {e}")
        return False

# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  

@bot.message_handler(commands=['start'])
def send_welcome(message):
    save_user(message.chat.id)
    user_id = message.chat.id
    if not is_user_member(user_id):
        markup = types.InlineKeyboardMarkup()
        join_button = types.InlineKeyboardButton("⨀ Jᴏɪɴ Cʜᴀɴɴᴇʟ ⨀", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")
        markup.add(join_button)
        bot.send_message(user_id, "⚠️ Yᴏᴜ Mᴜsᴛ Jᴏɪɴ Oᴜʀ Cʜᴀɴɴᴇʟ Tᴏ Cᴏɴᴛɪɴᴜᴇ ⚠️", reply_markup=markup)
        return
        
    save_user(user_id)
    current_time = datetime.now().strftime("Dᴀтᴇ :-  %d/%m/%y  ⌚ %I:%M %p")
    
    caption = f"""
◈◈◈  🅱🅾🆃 🅷🅾🆂🆃🅸🅽🅶 🅿🆁🅾  ◈◈◈

╔═➣  ✦ 𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝗠𝗲𝘀𝘀𝗮𝗴𝗲 ✦
║
╠═➤ 𝗛𝗼𝘀𝘁𝗶𝗻𝗴 𝗙𝗲𝗮𝘁𝘂𝗿𝗲𝘀:
║   ├─ 24*7 𝗨𝗽𝘁𝗶𝗺𝗲 𝗚𝘂𝗮𝗿𝗮𝗻𝘁𝗲𝗲ᴅ
║   ├─ 𝗙ᴜʟʟ 𝗔ᴜᴛᴏᴍᴀᴛᴇᴅ 𝗦ᴇʀᴠᴇʀ
║   └─ 𝗙ʀᴇᴇ 𝗙ᴏʀ 2 𝗕ᴏᴛs 𝗦ɪᴍᴜʟᴛᴀɴᴇᴏᴜsʟʏ
║
╠═➣ 𝗨𝘀𝗮𝗴𝗲 𝗡𝗼𝘁𝗲𝘀:
║   ├─ 𝗡𝗼 𝗣𝗮𝘆𝗺𝗲𝗻𝘁 𝗥𝗲𝗾𝘂𝗶𝗿𝗲ᴅ
║   ├─ 𝗠ᴀʟɪᴄɪᴏᴜs 𝗙ɪʟᴇs = 𝗣ᴇʀᴍᴀɴᴇɴᴛ 𝗕ᴀɴ
║   └─ 𝗔ᴜᴛᴏ 𝗖ʟᴇᴀɴᴜᴘ 𝗘ᴠᴇʀʏ 24ʜ
║
╠═➤ 𝗦𝘂𝗽𝗽𝗼𝗿𝘁 𝗜𝗻𝗳𝗼:
║   └─ @pb_x01
║
╠═➣ 𝗧𝗶𝗺𝗲 𝗦𝘁𝗮𝗺𝗽:
║   └─ {current_time}
║
◈◈◈  𝗧𝗘𝗔𝗠 𝗫 𝗢𝗚  ◈◈◈
    """.strip()

# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  

    markup = types.InlineKeyboardMarkup()
    
    btn1 = types.InlineKeyboardButton("🌹 ʀᴇᴅɪʀᴇᴄᴛ ➰", url="t.me/TEAM_X_OG")
    btn2 = types.InlineKeyboardButton("🌀 ᴅᴇᴠᴇʟᴏᴘᴇʀ", url="t.me/pb_x01")
    btn3 = types.InlineKeyboardButton("💎 sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ 💎", url="tg://resolve?domain=pb_x01&text=нιι%20I%20ɴᴇᴇᴅ%20sтιcκᴇʀ%20ιᴅ%20ʙoт%20souʀcᴇ%20coᴅᴇ%0A%0Aιтs%20ᴘᴀιᴅ%20souʀcᴇ%20%3F")
    
    markup.row(btn1, btn2)
    markup.row(btn3)
    
    photo_url = "https://graph.org/file/deea1849022f8b7f1a98a-374d2c9e15e0fd666b.jpg"
    bot.send_photo(user_id, photo_url, 
                 caption=caption, 
                 parse_mode="HTML",
                 reply_markup=markup)
    
    sticker_id = "CAACAgUAAyEFAASJBV1rAAEBaopnzOJgXYo8ZGMh-IGi17cs2HSuFgACBRYAAkYYaVZwjUHDOtNa5TYE"
    bot.send_sticker(user_id, sticker_id)

# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  

@bot.message_handler(commands=['help'])
@handle_errors
def show_help(message):
    save_user(message.chat.id)
    help_text = f"""
◈◈◈🌀  🅷🅴🅻🅿 🅼🅴🅽🆄  🌀◈◈◈

╔═➣  ✦ 𝗖𝗼𝗿𝗲 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀 ✦
║
╠═➤ 𝗕𝗮𝘀𝗶𝗰 𝗙𝘂𝗻𝗰𝘁𝗶𝗼𝗻𝘀:
║   ├
║   ├─ /sᴛᴀʀᴛ ➔ Iɴιтιᴀʟιzᴇ Boт
║   ├─ /ʜᴇʟᴘ  ➔ Sнow тнιs мᴇɴυ
║   └─ /ʟs  ➔  Lιsт Aʟʟ Fιʟᴇs
║
╠═➣ 𝗙𝗶𝗹𝗲 𝗠𝗮𝗻𝗮𝗴𝗲𝗺𝗲𝗻𝘁:
║   ├
║   ├─ /ᴜᴘʟᴏᴀᴅ  ➔  Uᴘʟoᴀᴅ Nᴇw Fιʟᴇ
║   ├─ /ᴅᴇʟᴇᴛᴇ file_name  ➔  Rᴇмovᴇ Sᴘᴇcιғιc Fιʟᴇ
║   └─ /ᴅᴏᴡɴʟᴏᴀᴅ file_name  ➔  Gᴇт Fιʟᴇ Froм Sᴇʀvᴇʀ
║
╠═➤ 𝗣𝗿𝗼𝗰𝗲𝘀𝘀 𝗖𝗼𝗻𝘁𝗿𝗼𝗹:
║   ├
║   ├─ /ʀᴜɴ ғɪʟᴇ  ➔  Exᴇcυтᴇ Sᴄʀιᴘт
║   └─ /sᴛᴏᴘ ғɪʟᴇ  ➔  Hᴀʟт Rυɴɴιɴɢ Pʀᴏᴄᴇss
║
╠═➣ 𝗣𝗮𝗰𝗸𝗮𝗴𝗲 𝗠𝗴𝗺𝘁:
║   └─ Pɪᴘ Iɴsᴛᴀʟʟ Pᴀᴄᴋᴀɢᴇ  ➔  Aᴅᴅ Nᴇw Pᴀᴄκᴀɢᴇ
║
╠═➤ 𝗦𝗲𝗰𝘂𝗿𝗶𝘁𝘆 𝗡𝗼𝘁𝗲𝘀:
║   ├
║   ├─ Mᴀx 2 Sιмυʟтᴀɴᴇoυs Rυɴs
║   ├─ Mᴀʟιcιoυs Fιʟᴇs = Pᴇʀмᴀɴᴇɴт Bᴀɴ
║   └─ Aυтo Fιʟᴇ Cʟᴇᴀɴυᴘ Evᴇʀʏ 199999ʜ
║
╠═➣ 𝗦𝘂𝗽𝗽𝗼𝗿𝘁:
║   └─ @pb_x01
║
◈◈◈  𝗧𝗘𝗔𝗠 𝗫 𝗢𝗚  ◈◈◈
    """.strip()

    bot.send_message(message.chat.id, help_text, 
                   parse_mode='HTML',
                   disable_web_page_preview=True)
    
    # Send sticker after help message
    sticker_id = "CAACAgUAAyEFAASJBV1rAAEBaopnzOJgXYo8ZGMh-IGi17cs2HSuFgACBRYAAkYYaVZwjUHDOtNa5TYE"
    bot.send_sticker(message.chat.id, sticker_id)

# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  

ADMIN_ID = "7858368373"
USER_FILE = "2.txt"

def save_user(chat_id):
    with open(USER_FILE, "a+") as file:
        file.seek(0)
        if str(chat_id) not in file.read().split():
            file.write(f"{chat_id}\n")





@bot.message_handler(commands=['bdcast'])
def handle_broadcast(message):
    if str(message.from_user.id) != ADMIN_ID:
        bot.reply_to(message, "🚫 *Access Denied!*", parse_mode='Markdown')
        return

    args = message.text.split(' ', 1)
    if len(args) < 2:
        bot.reply_to(message, "📝 *Usage:* /broadcast _<message>_", parse_mode='Markdown')
        return

    with open(USER_FILE, "r") as file:
        users = [line.strip() for line in file]

    success = 0
    failed = 0
    deleted = 0
    blocked = 0
    broadcast_msg = args[1]

    for user_id in users:
        try:
            bot.send_message(user_id, broadcast_msg)
            success += 1
        except Exception as e:
            if "Forbidden" in str(e):
                blocked += 1
            elif "chat not found" in str(e):
                deleted += 1
            else:
                failed += 1

    stats = f"""
    📢 *Broadcast Report* 📢
    
    ✅ Success: {success}
    ❌ Failed: {failed}
    🗑 Deleted: {deleted}
    🚫 Blocked: {blocked}
    """
    bot.reply_to(message, stats, parse_mode='Markdown')

@bot.message_handler(commands=['s'])
def handle_users(message):
    if str(message.from_user.id) != ADMIN_ID:
        bot.reply_to(message, "🚫 *Access Denied!*", parse_mode='Markdown')
        return

    with open(USER_FILE, "r") as file:
        users = [line.strip() for line in file]

    user_list = []
    for user_id in users:
        try:
            chat = bot.get_chat(user_id)
            if chat.username:
                user_entry = f"👤 @{chat.username} (`{user_id}`)"
            else:
                user_entry = f"👤 [No Username] (`{user_id}`)"
            user_list.append(user_entry)
        except:
            user_list.append(f"❌ Invalid User (`{user_id}`)")

    response = "📊 *Registered Users* 📊\n\n" + "\n".join(user_list)
    bot.send_message(message.chat.id, response, parse_mode='Markdown')

@bot.message_handler(commands=['run'])
@handle_errors
def run_file(message):
    save_user(message.chat.id)
    user_id = message.from_user.id
    if len(message.text.split()) < 2:
        bot.reply_to(message, "Usage: /run <filename>")
        return
    
    filename = message.text.split()[1]
    user_dir = get_user_dir(user_id)
    file_path = os.path.join(user_dir, filename)
    
    if not os.path.exists(file_path):
        bot.reply_to(message, "╠══➤❌ Fιʟᴇ Noт Fouɴᴅ\n║  └─ Mᴀκᴇ suʀᴇ тнᴇ ғιʟᴇ ɴᴀмᴇ ιs coʀʀᴇcт\n║  └─ Oʀ Ruɴ /ʟs тo sнow ʟιsт ᴀʟʟ ғιʟᴇs\n╠══➤ 𝗦𝘂𝗽𝗽𝗼𝗿𝘁 𝗜𝗻𝗳𝗼:\n║  └─ @pb_x01\n║")
        return
    
    with lock:
        if len(running_processes[user_id]) >= MAX_CONCURRENT_FILES:
            bot.reply_to(message, "❌ You Cᴀɴ Oɴʟʏ Ruɴ 2 Fιʟᴇs Aт ᴀ Tιмᴇ\n\nCoɴтᴀcт Suᴘᴘoʀт :- @pb_x01")
            return
        
        try:
            process = subprocess.Popen(
                ['python', file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            process_id = str(uuid.uuid4())
            
            running_processes[user_id][process_id] = {
                'process': process,
                'filename': filename,
                'start_time': time.time()
            }
            
            # Notify admin
            admin_msg = (f"🚀 NEW FILE RUNNING\n"
                          f"User: @{message.from_user.username}\n"
                          f"ID: {user_id}\n"
                          f"File: {filename}\n"
                          f"Running files: {len(running_processes[user_id])}")
            send_admin_notification(admin_msg)
            
            # Start monitoring thread
            threading.Thread(target=monitor_process, 
                             args=(user_id, process_id)).start()
            
            bot.reply_to(message, f"Oκ Youʀ Fιʟᴇ Is Ruɴɴιɴԍ\n\nWᴀʀɴιɴԍ Do Noтᴇ Ruɴ Hᴀʀм Fuʟʟ Fιlᴇs Eʟsᴇ You Gᴇт Bᴀɴɴᴇᴅ Fʀoм Tнιs Boт\n\nRUNNING THIS FILE {filename}\n/stop to stop this\n\nCoɴтᴀcт Suᴘᴘoʀт :- @pb_x01")
            
            sticker_id = "CAACAgUAAyEFAASJBV1rAAEBaopnzOJgXYo8ZGMh-IGi17cs2HSuFgACBRYAAkYYaVZwjUHDOtNa5TYE"
            bot.send_sticker(user_id, sticker_id)

        except Exception as e:
            bot.reply_to(message, f"❌ Error starting process: {str(e)}\n\nCoɴтᴀcт Suᴘᴘoʀт :- @pb_x01")

# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  

def monitor_process(user_id, process_id):
    process_data = running_processes[user_id][process_id]
    process = process_data['process']
    
    stdout, stderr = process.communicate()
    return_code = process.poll()
    
    with lock:
        del running_processes[user_id][process_id]
    
    log_execution(user_id, process_data['filename'], stdout, stderr)
    
    if return_code != 0:
        error_msg = f"❌ Error in {process_data['filename']}:\n{stderr[:4000]}"
        bot.send_message(user_id, error_msg)
        
        admin_msg = (f"⚠️ Process Failed\n"
                    f"User: {user_id}\n"
                    f"File: {process_data['filename']}\n"
                    f"Error: {stderr[:1000]}")
        send_admin_notification(admin_msg)

# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  

#  DON'T CHANGE VARNA ERROR AYEGA 💯%
expected_hash = "f95261a257bfd38c5fbfbcdf036da5affb4503eebbd5cbf1ab2d7b98ce997d9b"
@bot.message_handler(commands=['stop'])
@handle_errors
def stop_file(message):
    user_id = message.from_user.id
    if len(message.text.split()) < 2:
        bot.reply_to(message, "Usᴀԍᴇ: /sтoᴘ ")
        return
    
    filename = message.text.split()[1]
    
    with lock:
        to_remove = []
        for pid, data in running_processes[user_id].items():
            if data['filename'] == filename:
                data['process'].terminate()
                to_remove.append(pid)
        
        for pid in to_remove:
            del running_processes[user_id][pid]
        
        if to_remove:
            bot.reply_to(message, f"Sтoᴘᴘᴇᴅ {len(to_remove)} Iɴsтᴀɴcᴇs Oғ {filename}\n\nCoɴтᴀcт Suᴘᴘoʀт :- @pb_x01")
        else:
            bot.reply_to(message, "╔═════════════════\n║❌ 𝗦𝗧𝗢𝗣 𝗙𝗔𝗜𝗟𝗘𝗗\n║\n║ 𝗡𝗼 𝗿𝘂𝗻𝗻𝗶𝗻𝗴 𝗶𝗻𝘀𝘁𝗮𝗻𝗰𝗲𝘀 𝗳𝗼𝘂𝗻𝗱\n║\n║𝗣𝗼𝘀𝘀𝗶𝗯𝗹𝗲 𝗥𝗲𝗮𝘀𝗼𝗻𝘀:\n║\n║ ➲ File already stopped\n║ ➲ Incorrect filename\n║ ➲ Process completed\n║\n╚═════════════════\n\nCoɴтᴀcт Suᴘᴘoʀт :- @pb_x01")

# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  

@bot.message_handler(commands=['upload'])
@handle_errors
def handle_upload(message):
    user_id = message.from_user.id
    msg = bot.reply_to(message, "📤 Pʟᴇᴀsᴇ Sᴇɴᴅ Tнᴇ Fιʟᴇ You Wᴀɴт To Uᴘʟoᴀᴅ")
    bot.register_next_step_handler(msg, process_upload)

def process_upload(message):
    user_id = message.from_user.id
    try:
        if not message.document:
            bot.reply_to(message, "❌ Pʟᴇᴀsᴇ Sᴇɴᴅ ᴀ Fιʟᴇ\n\nCoɴтᴀcт Suᴘᴘoʀт :- @pb_x01")
            return
        
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        filename = message.document.file_name
        
        user_dir = create_user_dir(user_id)
        file_path = os.path.join(user_dir, filename)
        
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        user_files[user_id].append(filename)
        bot.reply_to(message, f"✅ Fιʟᴇ {filename} Uᴘʟoᴀᴅᴇᴅ Succᴇssғuʟʟʏ")
        
    except Exception as e:
        bot.reply_to(message, f"❌ Upload failed: {str(e)}\n\nCoɴтᴀcт Suᴘᴘoʀт :- @pb_x01")

# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  

@bot.message_handler(commands=['users'])
@handle_errors
def handle_users(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        return
    
    response = ["👥 Users:"]
    for uid in all_users:
        user = bot.get_chat(uid)
        running = len(running_processes.get(uid, []))
        response.append(
            f"{user.first_name} (@{user.username}) ID: {uid} - Running: {running}"
        )
    
    bot.reply_to(message, "\n".join(response))

# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  

@bot.message_handler(commands=['broadcast'])
@handle_errors
def handle_broadcast(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        return
    
    if len(message.text.split()) < 2:
        bot.reply_to(message, "Usage: /broadcast <message>")
        return
    
    msg = ' '.join(message.text.split()[1:])
    for uid in all_users:
        try:
            bot.send_message(uid, f"📢 ~~   Aᴅмιɴ Bʀoᴀᴅcᴀsт ~~\n👇👇👇👇👇👇\n\n{msg}")
        except Exception as e:
            print(f"Failed to send to {uid}: {str(e)}")
    
    bot.reply_to(message, f"✅ Broadcast sent to {len(all_users)} users")

# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  

@bot.message_handler(commands=['stopall'])
@handle_errors
def stop_all(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        return
    
    count = 0
    with lock:
        for uid in list(running_processes.keys()):
            for pid, data in running_processes[uid].items():
                data['process'].terminate()
                count += 1
            running_processes[uid].clear()
    
    bot.reply_to(message, f"✅ Stopped {count} processes across all users")

# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  

@bot.message_handler(commands=['ban'])
@handle_errors
def handle_ban(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        return
    
    if len(message.text.split()) < 2:
        bot.reply_to(message, "Usage: /ban <user_id>")
        return
    
    target_id = int(message.text.split()[1])
    banned_users.add(target_id)
    bot.reply_to(message, f"✅ User {target_id} banned")

# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  


@bot.message_handler(commands=['block'])
@handle_errors
def handle_block(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        return
    
    if len(message.text.split()) < 2:
        bot.reply_to(message, "Usage: /block <user_id>")
        return
    
    target_id = int(message.text.split()[1])
    blocked_users.add(target_id)
    bot.reply_to(message, f"✅ User {target_id} blocked")

# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  

@bot.message_handler(commands=['show'])
@handle_errors
def handle_show(message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        return
    
    response = ["🏃♂️ Running Processes:"]
    for uid, procs in running_processes.items():
        user = bot.get_chat(uid)
        response.append(f"User: @{user.username} ({uid})")
        for pid, data in procs.items():
            response.append(f"  - {data['filename']} (PID: {pid[:8]})")
    
    bot.reply_to(message, "\n".join(response))

# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  


@bot.message_handler(commands=['download'])
@handle_errors
def handle_download(message):
    user_id = message.from_user.id
    if len(message.text.split()) < 2:
        bot.reply_to(message, "Usᴀԍᴇ: /Dowɴʟoᴀᴅ ")
        return
    
    filename = message.text.split()[1]
    user_dir = get_user_dir(user_id)
    file_path = os.path.join(user_dir, filename)
    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            bot.send_document(user_id, f)
    else:
        bot.reply_to(message, "❌ Fιʟᴇ Noт Fouɴᴅ\n\nCнᴇcκ Fιʟᴇs Lιsт Usιɴԍ /ʟs")

# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  

@bot.message_handler(commands=['delete'])
@handle_errors
def handle_delete(message):
    user_id = message.from_user.id
    if len(message.text.split()) < 2:
        bot.reply_to(message, "usᴀԍᴇ: /ᴅᴇʟᴇтᴇ <ғιʟᴇɴᴀмᴇ>")
        return
    
    filename = message.text.split()[1]
    user_dir = get_user_dir(user_id)
    file_path = os.path.join(user_dir, filename)
    
    if os.path.exists(file_path):
        os.remove(file_path)
        bot.reply_to(message, f"Dᴇʟᴇтᴇᴅ 🌀 {filename}")
    else:
        bot.reply_to(message, "❌ File not found")

@bot.message_handler(commands=['ls'])
@handle_errors
def handle_ls(message):
    user_id = message.from_user.id
    user_dir = get_user_dir(user_id)
    files = os.listdir(user_dir)
    response = "📁 Youʀ Fιʟᴇs :\n" + "\n".join(files) if files else "No Fιʟᴇs Fouɴᴅ"
    bot.reply_to(message, response)


# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  

import re



EDIT_INTERVAL = 2


# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  

@bot.message_handler(func=lambda msg: msg.text.lower().startswith("pip"))
def install_package(message):
    match = re.match(r"pip\s*([\w\-]*)", message.text.strip(), re.IGNORECASE)
    
    if not match or match.group(1) == "":
        bot.send_message(message.chat.id, "**Usage:** `pip install <package_name>`", parse_mode="Markdown")
        return  

    package_name = match.group(1)
    install_msg = bot.send_message(message.chat.id, f"Iɴsтᴀʟʟιɴԍ {package_name}...")

    def run_install():
        try:
            process = subprocess.Popen(
                ["pip", "install", package_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            output_lines = []
            last_edit_time = time.time()

            for line in process.stdout:
                output_lines.append(line.strip())
                if time.time() - last_edit_time >= EDIT_INTERVAL:
                    try:
                        bot.edit_message_text(
                            f"Iɴsтᴀʟʟιɴԍ {package_name}...\n\n```python\n{chr(10).join(output_lines[-10:])}```",
                            chat_id=message.chat.id,
                            message_id=install_msg.message_id,
                            parse_mode="Markdown"
                        )
                        last_edit_time = time.time()
                    except:
                        break  

            process.wait()

            final_status = "Iɴsтᴀʟʟᴀтιoɴ Succᴇssғuʟ !" if process.returncode == 0 else "❌ Iɴsтᴀʟʟᴀтιoɴ Fᴀιʟᴇᴅ!"
            bot.edit_message_text(
                f"{final_status}\n\n```python\n{chr(10).join(output_lines[-15:])}```",
                chat_id=message.chat.id,
                message_id=install_msg.message_id,
                parse_mode="Markdown"
            )

        except Exception as e:
            bot.edit_message_text(f"❌ Error: `{str(e)}`", chat_id=message.chat.id, message_id=install_msg.message_id, parse_mode="Markdown")

    threading.Thread(target=run_install).start()

# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  


@bot.message_handler(commands=['mylogs'])
@handle_errors
def handle_logs(message):
    user_id = message.from_user.id
    logs = [f for f in os.listdir(LOG_DIR) if f.startswith(str(user_id))]
    
    if not logs:
        bot.reply_to(message, "No logs found")
        return
    
    logs.sort(reverse=True)
    response = ["📜 Your last 5 logs:"]
    for log in logs[:5]:
        with open(os.path.join(LOG_DIR, log), 'r') as f:
            content = f.read(200) + "..." if len(f.read()) > 200 else f.read()
            response.append(f"{log}: {content}")
    
    bot.reply_to(message, "\n".join(response))

# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  # THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  

import hashlib
import sys


# DON'T CHANGE VARNA ERROR AYEGA 💯%

original_text = "THIS FILE IS MADE BYE :- @pb_x01\nTHIS FILE IS MADE BYE :- @pb_x01\nTHIS FILE IS MADE BYE :- @pb_x01"

# DON'T CHANGE VARNA ERROR AYEGA 💯%

def generate_hash(text):
    hash_object = hashlib.sha256(text.encode())
    return hash_object.hexdigest()

# DON'T CHANGE VARNA ERROR AYEGA 💯%

current_hash = generate_hash(original_text)

# DON'T CHANGE VARNA ERROR AYEGA 💯%

if current_hash == expected_hash:
    print(original_text)
else:
    print("DONT CHANGE THE DEVELOPER NAME\n\nRG ~~ @pb_x01")
    sys.exit()

# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  

if __name__ == "__main__":
    print("Bot started...")
    bot.infinity_polling()
    
    


























































































































































































































































































































































































































































































































































































# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )  
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )
# THIS FILE IS MADE BYE :- @pb_x01 ( on tg )