import telebot
import google.generativeai as genai
import hashlib
import sys
import sqlite3
from telebot import types

# Configuration
BOT_TOKEN = "7690937386:AAG5BY6X4nzbz0jmtAWxVYWsFSFxW7tV6IE"
GEMINI_API_KEY = "AIzaSyCLWwTnaGsnwqIPtaz1FP2AnNwS86trVeY"
OWNER_ID = 7858368373
MAX_FREE_USERS = 100

# Initialize Gemini AI with corrected model names
genai.configure(api_key=GEMINI_API_KEY)
text_model = genai.GenerativeModel("gemini-1.5-pro")  # Updated from "gemini-pro"
vision_model = genai.GenerativeModel("gemini-1.5-pro-vision")  # Updated from "gemini-pro-vision"

# Initialize Telegram Bot
bot = telebot.TeleBot(BOT_TOKEN)

# Initialize Database with added 'is_banned' column
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

# Function to stylize text (e.g., ᴇxᴀмᴘʟᴇ тᴇxт)
def stylize_text(text):
    mapping = {
        'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ғ', 'g': 'ɢ', 'h': 'ʜ', 'i': 'ɪ',
        'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ', 'p': 'ᴘ', 'q': 'ǫ', 'r': 'ʀ',
        's': 's', 't': 'ᴛ', 'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x', 'y': 'ʏ', 'z': 'ᴢ',
        '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄', '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉',
    }
    return ''.join(mapping.get(c.lower(), c) for c in text)

# Function to get Gemini AI response
def get_gemini_response(prompt, image=None):
    try:
        if image:
            response = vision_model.generate_content([prompt, image])
        else:
            response = text_model.generate_content(prompt)
        return response.text if response.text else "No response generated."
    except Exception as e:
        return f"Error: {str(e)}"

# Welcome command with referral and premium logic
@bot.message_handler(commands=['start'])
def send_welcome(message):
    args = message.text.split()
    referrer_id = int(args[1]) if len(args) > 1 and args[1].isdigit() else None
    
    user_id = message.chat.id
    username = message.from_user.username
    
    # Update username if user exists
    c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    if c.fetchone():
        c.execute('UPDATE users SET username = ? WHERE user_id = ?', (username, user_id))
        conn.commit()
        bot.send_message(user_id, "🌟 Welcome back! Use /help to see available commands.")
        return

    # Check user limit
    c.execute('SELECT COUNT(*) FROM users WHERE is_premium = 0')
    free_users = c.fetchone()[0]
    
    if referrer_id:
        c.execute('SELECT is_premium FROM users WHERE user_id = ?', (referrer_id,))
        referrer_status = c.fetchone()
        premium_referral = referrer_status and referrer_status[0] == 1
    else:
        premium_referral = False

    if free_users >= MAX_FREE_USERS and not premium_referral:
        bot.send_message(user_id, "🚫 User limit reached. Get a premium user's referral link to join!")
        return

    # Register new user
    c.execute('INSERT INTO users (user_id, username, referred_by) VALUES (?, ?, ?)',
              (user_id, username, referrer_id))
    if referrer_id:
        c.execute('UPDATE users SET referral_count = referral_count + 1 WHERE user_id = ?', (referrer_id,))
        c.execute('SELECT referral_count FROM users WHERE user_id = ?', (referrer_id,))
        new_count = c.fetchone()[0]
        if new_count >= 5:
            c.execute('UPDATE users SET is_premium = 1 WHERE user_id = ?', (referrer_id,))
            bot.send_message(referrer_id, "🎉 Congratulations! You've reached 5 referrals and earned premium status!")
    conn.commit()

    # Welcome message with referral link
    referral_link = f"https://t.me/{bot.get_me().username}?start={user_id}"
    welcome_msg = f"""🤖 Welcome to {stylize_text('Gemini AI Pro')}!

🔑 Your Premium Status: {'Active 🎖️' if premium_referral else 'Basic'}
📤 Your Referral Link: {referral_link}
🎯 Referrals Count: 0

Use /help for commands"""
    bot.send_message(user_id, welcome_msg)

# Referral command with tree-like structure
@bot.message_handler(commands=['referral'])
def show_referral(message):
    user_id = message.chat.id
    c.execute('SELECT referral_count, is_premium, referred_by FROM users WHERE user_id = ?', (user_id,))
    user_data = c.fetchone()
    
    if user_data:
        count, premium, referred_by = user_data
        link = f"https://t.me/{bot.get_me().username}?start={user_id}"
        
        # Get referrer's username
        if referred_by:
            c.execute('SELECT username FROM users WHERE user_id = ?', (referred_by,))
            referrer = c.fetchone()
            referrer_text = f"└── Referred by: @{referrer[0]}" if referrer else "└── Referred by: None"
        else:
            referrer_text = "└── Referred by: None"
        
        # Get referred users
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
        
        response = f"""📊 {stylize_text('Your Referral Stats')}:

🔗 Your Link: {link}
👥 Total Referrals: {count}
🎖️ Premium Status: {'Active' if premium else 'Inactive'}

Referral Tree:
{referrer_text}
{referred_text}"""
        bot.send_message(user_id, response)
    else:
        bot.send_message(user_id, "❌ Please /start first")

# Help command with stylized text
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = f"""🤖 {stylize_text('Gemini AI Pro Bot Commands')}:

🌟 /start - Start the bot and get your referral link
📊 /referral - View your referral stats and tree
❓ /help - Show this help message
📈 /status - Check your status and referrals
💬 /feedback <message> - Send feedback to the owner

For premium users:
🎖️ Premium features are available automatically

Owner commands:
👑 /approve <user_id> - Approve premium access
🚫 /remove <user_id> - Remove premium access
📋 /users - List all users
🚫 /ban <user_id> - Ban a user
✅ /unban <user_id> - Unban a user
📢 /broadcast <message> - Send a message to all users
📊 /stats - Show bot statistics

💬 Simply send a message or photo to get AI responses!"""
    bot.send_message(message.chat.id, help_text)

# Status command
@bot.message_handler(commands=['status'])
def show_status(message):
    user_id = message.chat.id
    c.execute('SELECT is_premium, referral_count FROM users WHERE user_id = ?', (user_id,))
    user_data = c.fetchone()
    if user_data:
        premium, referrals = user_data
        status_text = "🎖️ Premium" if premium else "🆓 Basic"
        response = f"""📊 {stylize_text('Your Status')}:

🔑 Status: {status_text}
👥 Referrals: {referrals}

Refer 5 users to get premium!"""
        bot.send_message(user_id, response)
    else:
        bot.send_message(user_id, "❌ Please /start first")

# Feedback command
@bot.message_handler(commands=['feedback'])
def send_feedback(message):
    user_id = message.chat.id
    try:
        feedback_text = message.text.split(maxsplit=1)[1]
        user_tag = f"@{message.from_user.username}" if message.from_user.username else f"ID: {user_id}"
        owner_msg = f"📝 Feedback from {user_tag}:\n{feedback_text}"
        bot.send_message(OWNER_ID, owner_msg)
        bot.send_message(user_id, "✅ Feedback sent to the owner. Thank you!")
    except:
        bot.send_message(user_id, "❌ Usage: /feedback <message>")

# Admin commands
@bot.message_handler(commands=['approve'])
def approve_premium(message):
    if message.from_user.id == OWNER_ID:
        try:
            target_id = int(message.text.split()[1])
            c.execute('UPDATE users SET is_premium = 1 WHERE user_id = ?', (target_id,))
            conn.commit()
            bot.send_message(message.chat.id, f"✅ User {target_id} approved as premium!")
        except:
            bot.send_message(message.chat.id, "❌ Usage: /approve <user_id>")
    else:
        bot.send_message(message.chat.id, "❌ Owner-only command")

@bot.message_handler(commands=['remove'])
def remove_premium(message):
    if message.from_user.id == OWNER_ID:
        try:
            target_id = int(message.text.split()[1])
            c.execute('UPDATE users SET is_premium = 0 WHERE user_id = ?', (target_id,))
            conn.commit()
            bot.send_message(message.chat.id, f"✅ User {target_id} premium access removed!")
        except:
            bot.send_message(message.chat.id, "❌ Usage: /remove <user_id>")
    else:
        bot.send_message(message.chat.id, "❌ Owner-only command")

@bot.message_handler(commands=['users'])
def list_users(message):
    if message.from_user.id == OWNER_ID:
        c.execute('SELECT user_id, username, is_premium, referral_count, is_banned FROM users')
        users = c.fetchall()
        
        response = f"📊 {stylize_text('Registered Users')}:\n\n"
        for user in users:
            response += f"ID: {user[0]}\nUser: @{user[1]}\nPremium: {'✅' if user[2] else '❌'}\nReferrals: {user[3]}\nBanned: {'✅' if user[4] else '❌'}\n\n"
        
        # Split long messages
        for i in range(0, len(response), 3000):
            bot.send_message(message.chat.id, response[i:i+3000])
    else:
        bot.send_message(message.chat.id, "❌ Owner-only command")

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.from_user.id == OWNER_ID:
        try:
            target_id = int(message.text.split()[1])
            c.execute('UPDATE users SET is_banned = 1 WHERE user_id = ?', (target_id,))
            conn.commit()
            bot.send_message(message.chat.id, f"✅ User {target_id} has been banned.")
        except:
            bot.send_message(message.chat.id, "❌ Usage: /ban <user_id>")
    else:
        bot.send_message(message.chat.id, "❌ Owner-only command")

@bot.message_handler(commands=['unban'])
def unban_user(message):
    if message.from_user.id == OWNER_ID:
        try:
            target_id = int(message.text.split()[1])
            c.execute('UPDATE users SET is_banned = 0 WHERE user_id = ?', (target_id,))
            conn.commit()
            bot.send_message(message.chat.id, f"✅ User {target_id} has been unbanned.")
        except:
            bot.send_message(message.chat.id, "❌ Usage: /unban <user_id>")
    else:
        bot.send_message(message.chat.id, "❌ Owner-only command")

@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    if message.from_user.id == OWNER_ID:
        try:
            broadcast_text = message.text.split(maxsplit=1)[1]
            c.execute('SELECT user_id FROM users')
            users = c.fetchall()
            for user in users:
                try:
                    bot.send_message(user[0], broadcast_text)
                except:
                    pass  # Skip users who have blocked the bot
            bot.send_message(message.chat.id, "✅ Broadcast sent to all users.")
        except:
            bot.send_message(message.chat.id, "❌ Usage: /broadcast <message>")
    else:
        bot.send_message(message.chat.id, "❌ Owner-only command")

@bot.message_handler(commands=['stats'])
def show_stats(message):
    if message.from_user.id == OWNER_ID:
        c.execute('SELECT COUNT(*) FROM users')
        total_users = c.fetchone()[0]
        c.execute('SELECT COUNT(*) FROM users WHERE is_premium = 1')
        premium_users = c.fetchone()[0]
        c.execute('SELECT COUNT(*) FROM users WHERE is_banned = 1')
        banned_users = c.fetchone()[0]
        response = f"""📊 {stylize_text('Bot Statistics')}:

👥 Total Users: {total_users}
🎖️ Premium Users: {premium_users}
🚫 Banned Users: {banned_users}"""
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "❌ Owner-only command")

# Message handler with ban check and username update
@bot.message_handler(content_types=['text', 'photo'])
def handle_messages(message):
    user_id = message.chat.id
    username = message.from_user.username
    c.execute('UPDATE users SET username = ? WHERE user_id = ?', (username, user_id))
    conn.commit()
    
    bot.send_chat_action(user_id, 'typing')
    
    # Check registration and ban status
    c.execute('SELECT is_premium, is_banned FROM users WHERE user_id = ?', (user_id,))
    user = c.fetchone()
    if not user:
        bot.send_message(user_id, "❌ Please /start first")
        return
    if user[1]:  # is_banned
        bot.send_message(user_id, "🚫 You are banned from using this bot.")
        return
    
    # Process input
    prompt = message.text or message.caption
    image = None
    
    if message.photo:
        try:
            file_id = message.photo[-1].file_id
            file_info = bot.get_file(file_id)
            image = bot.download_file(file_info.file_path)
        except Exception as e:
            bot.send_message(user_id, f"❌ Error processing image: {str(e)}")
            return

    # Get response
    processing_msg = bot.send_message(user_id, "🧠 Processing your request...")
    response = get_gemini_response(prompt, image)
    bot.delete_message(user_id, processing_msg.message_id)

    # Format code blocks
    formatted_response = response.replace('```', '```')
    
    # Split long messages
    max_length = 4096
    for i in range(0, len(formatted_response), max_length):
        chunk = formatted_response[i:i+max_length]
        if '```' in chunk:
            bot.send_message(user_id, chunk, parse_mode='Markdown')
        else:
            bot.send_message(user_id, chunk)

    # Notify owner
    user_tag = f"@{message.from_user.username}" if message.from_user.username else f"ID: {user_id}"
    owner_msg = f"📩 New request from {user_tag}\n🗒️ Query: {prompt[:100]}..."
    bot.send_message(OWNER_ID, owner_msg)

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
bot.infinity_polling()
