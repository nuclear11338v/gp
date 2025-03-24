import telebot
import google.generativeai as genai
import hashlib
import sys
import sqlite3
from telebot import types

BOT_TOKEN = "7690937386:AAG5BY6X4nzbz0jmtAWxVYWsFSFxW7tV6IE"
GEMINI_API_KEY = "AIzaSyCLWwTnaGsnwqIPtaz1FP2AnNwS86trVeY"
OWNER_ID = 7858368373
MAX_FREE_USERS = 100

genai.configure(api_key=GEMINI_API_KEY)
text_model = genai.GenerativeModel("gemini-1.5-pro")
vision_model = genai.GenerativeModel("gemini-1.5-pro-vision")

bot = telebot.TeleBot(BOT_TOKEN)

conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (user_id INTEGER PRIMARY KEY,
              username TEXT,
              is_premium INTEGER DEFAULT 0,
              referral_count INTEGER DEFAULT 0,
              referred_by INTEGER,
              is_banned INTEGER DEFAULT 0)''')
conn.commit()

def stylize_text(text):
    mapping = {
        'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ғ', 'g': 'ɢ', 'h': 'ʜ', 'i': 'ɪ',
        'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ', 'p': 'ᴘ', 'q': 'ǫ', 'r': 'ʀ',
        's': 's', 't': 'ᴛ', 'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x', 'y': 'ʏ', 'z': 'ᴢ',
        '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄', '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉',
    }
    return ''.join(mapping.get(c.lower(), c) for c in text)

def get_gemini_response(prompt, image=None):
    try:
        if image:
            response = vision_model.generate_content([prompt, image])
        else:
            response = text_model.generate_content(prompt)
        return response.text if response.text else "No response generated."
    except Exception as e:
        return f"Error: {str(e)}"

def send_long_message(chat_id, text, parse_mode='HTML'):
    """Split and send long messages if they exceed Telegram's limit"""
    MAX_LENGTH = 4096
    if len(text) <= MAX_LENGTH:
        bot.send_message(chat_id, text, parse_mode=parse_mode, disable_web_page_preview=True)
    else:
        parts = []
        current_part = ""
        for line in text.split('\n'):
            if len(current_part) + len(line) + 1 > MAX_LENGTH:
                parts.append(current_part)
                current_part = line
            else:
                current_part += "\n" + line if current_part else line
        if current_part:
            parts.append(current_part)
        
        for part in parts:
            bot.send_message(chat_id, part.strip(), parse_mode=parse_mode, disable_web_page_preview=True)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    args = message.text.split()
    referrer_id = int(args[1]) if len(args) > 1 and args[1].isdigit() else None
    
    user_id = message.chat.id
    username = message.from_user.username
    
    c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    if c.fetchone():
        c.execute('UPDATE users SET username = ? WHERE user_id = ?', (username, user_id))
        conn.commit()
        bot.send_message(user_id, "<b>HEY THERE WELCOME!</b>\n\nI'm Team x Gpt 🌟\nHow Can I Help You?\n\nType /help To See How To Use Me!", parse_mode='HTML', disable_web_page_preview=True)
        return

    c.execute('SELECT COUNT(*) FROM users WHERE is_premium = 0')
    free_users = c.fetchone()[0]
    
    if referrer_id:
        c.execute('SELECT is_premium FROM users WHERE user_id = ?', (referrer_id,))
        referrer_status = c.fetchone()
        premium_referral = referrer_status and referrer_status[0] == 1
    else:
        premium_referral = False

    if free_users >= MAX_FREE_USERS and not premium_referral:
        bot.send_message(user_id, "User Limit Reached. Get a Premium User's Referral Link To Join!", parse_mode='HTML', disable_web_page_preview=True)
        return

    c.execute('INSERT INTO users (user_id, username, referred_by) VALUES (?, ?, ?)',
              (user_id, username, referrer_id))
    if referrer_id:
        c.execute('UPDATE users SET referral_count = referral_count + 1 WHERE user_id = ?', (referrer_id,))
        c.execute('SELECT referral_count FROM users WHERE user_id = ?', (referrer_id,))
        new_count = c.fetchone()[0]
        if new_count >= 5:
            c.execute('UPDATE users SET is_premium = 1 WHERE user_id = ?', (referrer_id,))
            bot.send_message(referrer_id, "🎊 <b>CONGRATULATIONS</b> 🎊\n\nThank You For Choosing Me!\nI hope you're enjoying 🌟👀🥳", parse_mode='HTML', disable_web_page_preview=True)
    conn.commit()

    referral_link = f"https://t.me/{bot.get_me().username}?start={user_id}"
    welcome_msg = f"""<b>🤖 Welcome to {stylize_text('Gemini AI Pro')}!</b>\n\n
<i>Premium Status</i>: {'Active 🎖️' if premium_referral else 'Basic'}\n
<i>Total Referrals</i>: <a href='{referral_link}'>CLICK HERE</a>\n
🎯 Referrals Count: [implementing]\n\n
Support: <a href='https://t.me/TEAM_X_OG'>TEAM X OG</a>\n
Powered By: <a href='https://t.me/PB_X01'>PB_X01</a>\n\n
Use /help for commands"""
    bot.send_message(user_id, welcome_msg, parse_mode='HTML', disable_web_page_preview=True)

@bot.message_handler(commands=['referral'])
def show_referral(message):
    user_id = message.chat.id
    c.execute('SELECT referral_count, is_premium, referred_by FROM users WHERE user_id = ?', (user_id,))
    user_data = c.fetchone()
    
    if user_data:
        count, premium, referred_by = user_data
        link = f"https://t.me/{bot.get_me().username}?start={user_id}"
        
        if referred_by:
            c.execute('SELECT username FROM users WHERE user_id = ?', (referred_by,))
            referrer = c.fetchone()
            referrer_text = f"└── Referred by: @{referrer[0]}" if referrer else "└── Referred by: None"
        else:
            referrer_text = "└── Referred by: None"
        
        c.execute('SELECT username FROM users WHERE referred_by = ?', (user_id,))
        referred_users = c.fetchall()
        referred_text = ""
        if referred_users:
            referred_text += "    ├── Referred users:\n"
            for i, user in enumerate(referred_users):
                if i == len(referred_users) - 1:
                    referred_text += f"    └── @{user[0]}\n"
                else:
                    referred_text += f"    ├── @{user[0]}\n"
        
        response = f"""<b>📊 {stylize_text('Your Referral Stats')}:</b>\n\n
<i>Your Link</i>: <a href='{link}'>CLICK HERE</a>\n
<i>Total Referrals</i>: {count}\n
<i>Premium Status</i>: {'Active' if premium else 'Inactive'}\n\n
Support: <a href='https://t.me/TEAM_X_OG'>TEAM X OG</a>\n
Powered By: <a href='https://t.me/PB_X01'>PB_X01</a>\n\n
<b>Referral Tree:</b>\n
<pre>{referrer_text}\n{referred_text}</pre>"""
        send_long_message(user_id, response)
    else:
        bot.send_message(user_id, "First Start The Bot Then You Can Use This Bot\n\n/start", parse_mode='HTML', disable_web_page_preview=True)

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = f"""<b>🤖 {stylize_text('Gemini AI Pro Bot Commands')}:</b>\n\n
<i>/start</i> - Start The Bot And Get Your Referral Link\n
<i>/referral</i> - View Your Referral Stats And Tree\n
<i>/help</i> - Show This Help Message\n
<i>/status</i> - Check Your Status And Referrals\n
<i>/feedback</i> - Send Feedback To The Owner\n\n
<b>For Premium Users:</b>\n
🎖️ Premium Features Are Available Automatically\n\n
<b>Owner Commands:</b>\n
👑 /approve - Approve Premium Access\n
🚫 /remove - Remove Premium Access\n
📋 /users - List All users\n
🚫 /ban - Ban a User\n
✅ /unban - Unban a User\n
📢 /broadcast - Send a Message To All Users\n
📊 /stats - Show Bot Statistics\n\n
Support: <a href='https://t.me/TEAM_X_OG'>TEAM X OG</a>\n
Powered By: <a href='https://t.me/PB_X01'>PB_X01</a>\n\n
💬 Simply Send a Message Or Photo To Get AI Responses!"""
    send_long_message(message.chat.id, help_text)

@bot.message_handler(commands=['status'])
def show_status(message):
    user_id = message.chat.id
    c.execute('SELECT is_premium, referral_count FROM users WHERE user_id = ?', (user_id,))
    user_data = c.fetchone()
    if user_data:
        premium, referrals = user_data
        status_text = "🎖️ Premium" if premium else "🆓 Basic"
        response = f"""<b>📊 {stylize_text('Your Status')}:</b>\n\n
<i>Status</i>: {status_text}\n
<i>Referrals</i>: {referrals}\n\n
Refer 5 Users to Get Premium!\n\n
Support: <a href='https://t.me/TEAM_X_OG'>TEAM X OG</a>\n
Powered By: <a href='https://t.me/PB_X01'>PB_X01</a>"""
        bot.send_message(user_id, response, parse_mode='HTML', disable_web_page_preview=True)
    else:
        bot.send_message(user_id, "First Start The Bot Then You Can Use This Bot\n\n/start", parse_mode='HTML', disable_web_page_preview=True)

@bot.message_handler(commands=['feedback'])
def send_feedback(message):
    user_id = message.chat.id
    try:
        feedback_text = message.text.split(maxsplit=1)[1]
        user_tag = f"@{message.from_user.username}" if message.from_user.username else f"ID: {user_id}"
        owner_msg = f"<b>📝 Feedback from {user_tag}:</b>\n{feedback_text}"
        bot.send_message(OWNER_ID, owner_msg, parse_mode='HTML', disable_web_page_preview=True)
        bot.send_message(user_id, "✅", disable_web_page_preview=True)
    except:
        bot.send_message(user_id, "Usage: /feedback <message>", parse_mode='HTML', disable_web_page_preview=True)

@bot.message_handler(commands=['approve'])
def approve_premium(message):
    if message.from_user.id == OWNER_ID:
        try:
            target_id = int(message.text.split()[1])
            c.execute('UPDATE users SET is_premium = 1 WHERE user_id = ?', (target_id,))
            conn.commit()
            bot.send_message(message.chat.id, f"✅ User {target_id} approved as premium!", disable_web_page_preview=True)
        except:
            bot.send_message(message.chat.id, "❌ Usage: /approve <user_id>", parse_mode='HTML', disable_web_page_preview=True)
    else:
        bot.send_message(message.chat.id, "🙅", disable_web_page_preview=True)

@bot.message_handler(commands=['remove'])
def remove_premium(message):
    if message.from_user.id == OWNER_ID:
        try:
            target_id = int(message.text.split()[1])
            c.execute('UPDATE users SET is_premium = 0 WHERE user_id = ?', (target_id,))
            conn.commit()
            bot.send_message(message.chat.id, f"✅ User {target_id} premium access removed!", disable_web_page_preview=True)
        except:
            bot.send_message(message.chat.id, "❌ Usage: /remove <user_id>", parse_mode='HTML', disable_web_page_preview=True)
    else:
        bot.send_message(message.chat.id, "🙅", disable_web_page_preview=True)

@bot.message_handler(commands=['users'])
def list_users(message):
    if message.from_user.id == OWNER_ID:
        c.execute('SELECT user_id, username, is_premium, referral_count, is_banned FROM users')
        users = c.fetchall()
        
        response = f"<b>📊 {stylize_text('Registered Users')}:</b>\n\n"
        for user in users:
            response += f"ID: {user[0]}\nUser: @{user[1]}\nPremium: {'✅' if user[2] else '❌'}\nReferrals: {user[3]}\nBanned: {'✅' if user[4] else '❌'}\n\n"
        
        send_long_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "🙅", disable_web_page_preview=True)

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.from_user.id == OWNER_ID:
        try:
            target_id = int(message.text.split()[1])
            c.execute('UPDATE users SET is_banned = 1 WHERE user_id = ?', (target_id,))
            conn.commit()
            bot.send_message(message.chat.id, f"✅ User {target_id} has been banned.", disable_web_page_preview=True)
        except:
            bot.send_message(message.chat.id, "❌ Usage: /ban <user_id>", parse_mode='HTML', disable_web_page_preview=True)
    else:
        bot.send_message(message.chat.id, "❌ Owner-only command", disable_web_page_preview=True)

@bot.message_handler(commands=['unban'])
def unban_user(message):
    if message.from_user.id == OWNER_ID:
        try:
            target_id = int(message.text.split()[1])
            c.execute('UPDATE users SET is_banned = 0 WHERE user_id = ?', (target_id,))
            conn.commit()
            bot.send_message(message.chat.id, f"✅ User {target_id} has been unbanned.", disable_web_page_preview=True)
        except:
            bot.send_message(message.chat.id, "❌ Usage: /unban <user_id>", parse_mode='HTML', disable_web_page_preview=True)
    else:
        bot.send_message(message.chat.id, "🙅", disable_web_page_preview=True)

@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    if message.from_user.id == OWNER_ID:
        try:
            broadcast_text = message.text.split(maxsplit=1)[1]
            c.execute('SELECT user_id FROM users')
            users = c.fetchall()
            for user in users:
                try:
                    send_long_message(user[0], broadcast_text)
                except:
                    pass
            bot.send_message(message.chat.id, "✅ Broadcast sent to all users.", disable_web_page_preview=True)
        except:
            bot.send_message(message.chat.id, "❌ Usage: /broadcast <message>", parse_mode='HTML', disable_web_page_preview=True)
    else:
        bot.send_message(message.chat.id, "🙅", disable_web_page_preview=True)

@bot.message_handler(commands=['stats'])
def show_stats(message):
    if message.from_user.id == OWNER_ID:
        c.execute('SELECT COUNT(*) FROM users')
        total_users = c.fetchone()[0]
        c.execute('SELECT COUNT(*) FROM users WHERE is_premium = 1')
        premium_users = c.fetchone()[0]
        c.execute('SELECT COUNT(*) FROM users WHERE is_banned = 1')
        banned_users = c.fetchone()[0]
        response = f"""<b>📊 {stylize_text('Bot Statistics')}:</b>\n\n
<i>Total Users</i>: {total_users}\n
<i>Premium Users</i>: {premium_users}\n
<i>Banned Users</i>: {banned_users}"""
        bot.send_message(message.chat.id, response, parse_mode='HTML', disable_web_page_preview=True)
    else:
        bot.send_message(message.chat.id, "🙅", disable_web_page_preview=True)

@bot.message_handler(content_types=['text', 'photo'])
def handle_messages(message):
    user_id = message.chat.id
    username = message.from_user.username
    c.execute('UPDATE users SET username = ? WHERE user_id = ?', (username, user_id))
    conn.commit()
    
    bot.send_chat_action(user_id, 'typing')
    
    c.execute('SELECT is_premium, is_banned FROM users WHERE user_id = ?', (user_id,))
    user = c.fetchone()
    if not user:
        bot.send_message(user_id, "First Start The Bot Then You Can Use This Bot\n\n/start", parse_mode='HTML', disable_web_page_preview=True)
        return
    if user[1]:
        bot.send_message(user_id, "You are Banned From This Bot. If You Think This Is A Mistake Please Contact Us: @PB_X01", parse_mode='HTML', disable_web_page_preview=True)
        return
    
    prompt = message.text or message.caption
    image = None
    
    if message.photo:
        try:
            file_id = message.photo[-1].file_id
            file_info = bot.get_file(file_id)
            image = bot.download_file(file_info.file_path)
        except Exception as e:
            bot.send_message(user_id, f"❌ Error processing image: {str(e)}", parse_mode='HTML', disable_web_page_preview=True)
            return

    processing_msg = bot.send_message(user_id, "🔎", disable_web_page_preview=True)
    response = get_gemini_response(prompt, image)
    bot.delete_message(user_id, processing_msg.message_id)

    # Split response into text and code blocks
    parts = response.split('```')
    for i, part in enumerate(parts):
        if i % 2 == 0:  # Text part
            if part.strip():
                send_long_message(user_id, part.strip())
        else:  # Code part
            if part.strip():
                send_long_message(user_id, f"<pre>{part.strip()}</pre>")

    user_tag = f"@{message.from_user.username}" if message.from_user.username else f"ID: {user_id}"
    owner_msg = f"<b>📩 New request from {user_tag}</b>\nQuery: {prompt[:100]}..."
    bot.send_message(OWNER_ID, owner_msg, parse_mode='HTML', disable_web_page_preview=True)

# Developer credit check
original_text = """THIS FILE IS MADE BYE -> @MR_ARMAN_OWNER\nTHIS FILE IS MADE BYE -> @MR_ARMAN_OWNER\nTHIS FILE IS MADE BYE -> @MR_ARMAN_OWNER\n\nDM TO BUY PAID FILES"""
expected_hash = "dfcb19d1592200db6b5202025e4b67ba6fc43d9dad9e3eb26e2edb3db71b1921"
generated_hash = hashlib.sha256(original_text.encode()).hexdigest()

if generated_hash != expected_hash:
    print("Please don't change the developer name")
    sys.exit(1)
else:
    print(original_text)

# Start the bot
print("Bot is running...")
bot.infinity_polling(
