import telebot
import google.generativeai as genai
import hashlib
import sys
import sqlite3
from telebot import types

# THIS CODE IS MADE BYE - @MR_INDIAN_OWNER_1

# Configuration
BOT_TOKEN = "7690937386:AAG5BY6X4nzbz0jmtAWxVYWsFSFxW7tV6IE"
GEMINI_API_KEY = "AIzaSyCLWwTnaGsnwqIPtaz1FP2AnNwS86trVeY"
OWNER_ID = 7858368373
MAX_FREE_USERS = 100

# Initialize Gemini AI
genai.configure(api_key=GEMINI_API_KEY)
text_model = genai.GenerativeModel("gemini-pro")
vision_model = genai.GenerativeModel('gemini-pro-vision')

# Initialize Telegram Bot
bot = telebot.TeleBot(BOT_TOKEN)

# Initialize Database
conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (user_id INTEGER PRIMARY KEY,
              username TEXT,
              is_premium INTEGER DEFAULT 0,
              referral_count INTEGER DEFAULT 0,
              referred_by INTEGER)''')
conn.commit()

# THIS CODE IS MADE BYE - @MR_INDIAN_OWNER_1

def get_gemini_response(prompt, image=None):
    try:
        if image:
            response = vision_model.generate_content([prompt, image])
        else:
            response = text_model.generate_content(prompt)
        return response.text if response.text else "No response generated."
    except Exception as e:
        return f"Error: {str(e)}"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    args = message.text.split()
    referrer_id = int(args[1]) if len(args) > 1 else None
    
    user_id = message.chat.id
    username = message.from_user.username
    
    # Check existing user
    c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    if c.fetchone():
        bot.send_message(user_id, "🌟 Welcome back! Use /help to see available commands.")
        return

    # Check user limit
    if referrer_id:
        c.execute('SELECT is_premium FROM users WHERE user_id = ?', (referrer_id,))
        referrer_status = c.fetchone()
        premium_referral = referrer_status and referrer_status[0] == 1
    else:
        premium_referral = False

    c.execute('SELECT COUNT(*) FROM users WHERE is_premium = 0')
    free_users = c.fetchone()[0]
    
    if free_users >= MAX_FREE_USERS and not premium_referral:
        bot.send_message(user_id, "🚫 User limit reached. Get a premium user's referral link!")
        return

    # Register new user
    c.execute('INSERT INTO users (user_id, username, referred_by) VALUES (?, ?, ?)',
              (user_id, username, referrer_id))
    if referrer_id:
        c.execute('UPDATE users SET referral_count = referral_count + 1 WHERE user_id = ?', (referrer_id,))
    conn.commit()

    # Welcome message with referral link
    referral_link = f"https://t.me/{bot.get_me().username}?start={user_id}"
    welcome_msg = f"""🤖 Welcome to Gemini AI Pro!

🔑 Your Premium Status: {'Active 🎖️' if premium_referral else 'Basic'}
📤 Your Referral Link: {referral_link}
🎯 Referrals Count: 0

Use /help for commands"""
    bot.send_message(user_id, welcome_msg)

@bot.message_handler(commands=['referral'])
def show_referral(message):
    user_id = message.chat.id
    c.execute('SELECT referral_count, is_premium FROM users WHERE user_id = ?', (user_id,))
    user_data = c.fetchone()
    
    if user_data:
        count, premium = user_data
        link = f"https://t.me/{bot.get_me().username}?start={user_id}"
        response = f"""📊 Your Referral Stats:

🔗 Your Link: {link}
👥 Total Referrals: {count}
🎖️ Premium Status: {'Active' if premium else 'Inactive'}
        
Every 5 referrals earns you 1 week of premium!"""
        bot.send_message(user_id, response)
    else:
        bot.send_message(user_id, "❌ Please /start first")

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
        c.execute('SELECT user_id, username, is_premium, referral_count FROM users')
        users = c.fetchall()
        
        response = "📊 Registered Users:\n\n"
        for user in users:
            response += f"ID: {user[0]}\nUser: @{user[1]}\nPremium: {'✅' if user[2] else '❌'}\nReferrals: {user[3]}\n\n"
        
        # Split long messages
        for i in range(0, len(response), 3000):
            bot.send_message(message.chat.id, response[i:i+3000])
    else:
        bot.send_message(message.chat.id, "❌ Owner-only command")

@bot.message_handler(content_types=['text', 'photo'])
def handle_messages(message):
    user_id = message.chat.id
    bot.send_chat_action(user_id, 'typing')
    
    # Check registration
    c.execute('SELECT is_premium FROM users WHERE user_id = ?', (user_id,))
    user = c.fetchone()
    if not user:
        bot.send_message(user_id, "❌ Please /start first")
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

# THIS CODE IS MADE BYE - @MR_INDIAN_OWNER_1

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
# THIS CODE IS MADE BYE - @MR_INDIAN_OWNER_1