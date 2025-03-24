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

@bot.message_handler(commands=['start'])
def send_welcome(message):
    args = message.text.split()
    referrer_id = int(args[1]) if len(args) > 1 and args[1].isdigit() else None
    
    user_id = message.chat.id
    username = message.from_user.username
    
    # Check if user exists
    c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    if c.fetchone():
        c.execute('UPDATE users SET username = ? WHERE user_id = ?', (username, user_id))
        conn.commit()
        
        # Photo for returning users
        return_photo = "https://graph.org/file/1f0b433f5ed109a29eed1-c705cfa8a799cd69b3.jpg"  # Replace with your image URL
        return_caption = "𝗛𝗘𝗬 𝗧𝗘𝗥𝗘 𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗕𝗔𝗖𝗞!\n\nI'м Tᴇᴀм x Gᴘт 🌟\nHow Cᴀɴ ι Hᴇʟᴘ You?\n\nTʏᴘᴇ /help To Sᴇᴇ How To Usᴇ Mᴇ!"
        bot.send_photo(user_id, return_photo, caption=return_caption, parse_mode='Markdown')
        return

    # Check user limit
    c.execute('SELECT COUNT(*) FROM users WHERE is_premium = 0')
    free_users = c.fetchone()[0]
    
    # Check referrer status
    premium_referral = False
    if referrer_id:
        c.execute('SELECT is_premium FROM users WHERE user_id = ?', (referrer_id,))
        referrer_status = c.fetchone()
        premium_referral = referrer_status and referrer_status[0] == 1

    if free_users >= MAX_FREE_USERS and not premium_referral:
        limit_photo = "https://graph.org/file/c1e9651525a14a4674e3f-6d1b0aa8557a108c83.jpg"  # Replace with your image URL
        limit_caption = "Usᴇʀ Lιмιт Rᴇᴀcнᴇᴅ. Gᴇт ᴀ Pʀᴇмιuм Usᴇʀ's Rᴇғᴇʀʀᴀʟ Lιɴκ To Joιɴ!"
        bot.send_photo(user_id, limit_photo, caption=limit_caption, parse_mode='Markdown')
        return

    # Register new user
    c.execute('INSERT INTO users (user_id, username, referred_by) VALUES (?, ?, ?)',
              (user_id, username, referrer_id))
    
    # Handle referrals
    if referrer_id:
        c.execute('UPDATE users SET referral_count = referral_count + 1 WHERE user_id = ?', (referrer_id,))
        c.execute('SELECT referral_count FROM users WHERE user_id = ?', (referrer_id,))
        new_count = c.fetchone()[0]
        
        if new_count >= 5:
            c.execute('UPDATE users SET is_premium = 1 WHERE user_id = ?', (referrer_id,))
            
            # Congratulations photo for premium upgrade
            congrats_photo = "https://graph.org/file/7cf9e9e7825ae53f23e70-bba988b143b3878d91.jpg"  # Replace with your image URL
            congrats_caption = "🎊 𝗖𝗢𝗡𝗚𝗥𝗔𝗧𝗨𝗟𝗔𝗧𝗜𝗢𝗡𝗦 🎊\n\nYou've unlocked Premium Status!\nEnjoy your new benefits! 🎉"
            bot.send_photo(referrer_id, congrats_photo, caption=congrats_caption, parse_mode='Markdown')

    conn.commit()

    # Welcome photo for new users
    welcome_photo = "https://graph.org/file/1f0b433f5ed109a29eed1-c705cfa8a799cd69b3.jpg"  # Replace with your image URL
    referral_link = f"https://t.me/{bot.get_me().username}?start={user_id}"
    welcome_caption = f"""**🤖 Welcome to {stylize_text('Gemini AI Pro')}!**

🔗 *Your Referral Link*: [Click Here]({referral_link})
🎖️ *Status*: {'Premium 🎖️' if premium_referral else 'Basic'}

Suᴘᴘoʀт: [TEAM X OG](https://t.me/TEAM_X_OG)
Powᴇʀᴇᴅ Bʏ: [PB_X01](https://t.me/PB_X01)

Use /help for commands"""
    
    bot.send_photo(user_id, welcome_photo, caption=welcome_caption, parse_mode='Markdown')

# Referral command with tree-like structure
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

        # Photo URL (replace with your actual image URL)
        photo_url = "https://graph.org/file/c1e9651525a14a4674e3f-6d1b0aa8557a108c83.jpg"
        
        # Caption text with fixed formatting
        caption = f"""**📊 {stylize_text('Your Referral Stats')}:**

🔗 *Your Referral Link*: [CLICK HERE]({link})
👥 *Total Referrals*: {count}
🎖️ *Premium Status*: {'Active' if premium else 'Inactive'}

**Referral Tree:**

Support: [TEAM X OG](https://t.me/TEAM_X_OG)
Powered By: [PB_X01](https://t.me/PB_X01)"""
        
        # Send photo with caption
        bot.send_photo(
            user_id,
            photo_url,
            caption=caption,
            parse_mode='Markdown'
        )
    else:
        bot.send_message(
            user_id,
            "First start the bot then you can use this feature\n\n/start",
            disable_web_page_preview=True
        )

# Help command with stylized text
@bot.message_handler(commands=['help'])
def send_help(message):
    # Photo URL (replace with your actual image URL)
    photo_url = "https://graph.org/file/2f97981b929255f1576ae-2909d37d07d37ce8a2.jpg"
    
    # Caption text with fixed Markdown formatting
    caption = f"""🤖 {stylize_text('Gemini AI Pro Bot Commands')}:

🌟 /start - *Start The Bot And Get Your Referral Link*
📊 /referral - *View Your Referral Stats And Tree*
❓ /help - *Show This Help Message*
📈 /status - *Check Your Status And Referrals*
💬 /feedback - *Send Feedback To The Owner*

*For Premium Users:*

🎖️ *Premium Features Are Available Automatically*

*Owner Commands:*
👑 /approve - *Approve Premium Access*
🚫 /remove - *Remove Premium Access*
📋 /users - *List All Users*
🚫 /ban - *Ban a User*
✅ /unban - *Unban a User*
📢 /broadcast - *Send a Message To All Users*
📊 /stats - *Show Bot Statistics*

Support: [TEAM X OG](https://t.me/TEAM_X_OG)
Powered By: [PB_X01](https://t.me/PB_X01)

*💬 Simply Send a Message or Photo To Get AI Responses!*"""
    
    # Send photo with caption (REMOVED disable_web_page_preview)
    bot.send_photo(
        message.chat.id,
        photo_url,
        caption=caption,
        parse_mode='Markdown'
    )

# Status command
@bot.message_handler(commands=['status'])
def show_status(message):
    user_id = message.chat.id
    c.execute('SELECT is_premium, referral_count FROM users WHERE user_id = ?', (user_id,))
    user_data = c.fetchone()
    if user_data:
        premium, referrals = user_data
        status_text = "🎖️ Premium" if premium else "🆓 Basic"
        
        # Photo URL and caption
        photo_url = "https://graph.org/file/06bd520593fa701763c37-e08b5f90b29d4ab86e.jpg"  # Replace with your actual image URL
        caption = f"""**📊 {stylize_text('Your Status')}:**

🔑 Status: {status_text}
👥 Referrals: {referrals}

Rᴇғᴇᴇʀ 5 Usᴇʀs тo Gᴇт Pʀᴇмιuм!

Suᴘᴘoʀт :- [TEAM X OG](https://t.me/TEAM_X_OG)
Powᴇʀᴇᴇᴅ Bʏ :- [PB_X01](https://t.me/PB_X01)"""
        
        # Send photo with caption (REMOVED disable_web_page_preview)
        bot.send_photo(user_id, photo_url, caption=caption, parse_mode='Markdown')
    else:
        # This part is fine since it uses send_message()
        bot.send_message(user_id, "Fιʀsт Sтᴀʀт Tнᴇ Boт Tнᴇɴ You Cᴀɴ Usᴇ Tнιs Boт\n\n/start", disable_web_page_preview=True)
# Feedback command
@bot.message_handler(commands=['feedback'])
def send_feedback(message):
    user_id = message.chat.id
    try:
        feedback_text = message.text.split(maxsplit=1)[1]
        user_tag = f"@{message.from_user.username}" if message.from_user.username else f"ID: {user_id}"
        owner_msg = f"**📝 Feedback from {user_tag}:**\n{feedback_text}"
        bot.send_message(OWNER_ID, owner_msg, parse_mode='Markdown', disable_web_page_preview=True)
        bot.send_message(user_id, "✅", disable_web_page_preview=True)
    except:
        bot.send_message(user_id, "𝗨𝘀𝗮𝗴𝗲: /𝗳𝗲𝗲𝗱𝗯𝗮𝗰𝗸 <𝗺𝗲𝘀𝘀𝗮𝗴𝗲>", disable_web_page_preview=True)

# Admin commands
@bot.message_handler(commands=['approve'])
def approve_premium(message):
    if message.from_user.id == OWNER_ID:
        try:
            target_id = int(message.text.split()[1])
            c.execute('UPDATE users SET is_premium = 1 WHERE user_id = ?', (target_id,))
            conn.commit()
            bot.send_message(message.chat.id, f"✅ User {target_id} approved as premium!", disable_web_page_preview=True)
        except:
            bot.send_message(message.chat.id, "❌ Usage: /approve <user_id>", disable_web_page_preview=True)
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
            bot.send_message(message.chat.id, "❌ Usage: /remove <user_id>", disable_web_page_preview=True)
    else:
        bot.send_message(message.chat.id, "🙅", disable_web_page_preview=True)

@bot.message_handler(commands=['users'])
def list_users(message):
    if message.from_user.id == OWNER_ID:
        c.execute('SELECT user_id, username, is_premium, referral_count, is_banned FROM users')
        users = c.fetchall()
        
        response = f"**📊 {stylize_text('Registered Users')}:**\n\n"
        for user in users:
            response += f"ID: {user[0]}\nUser: @{user[1]}\nPremium: {'✅' if user[2] else '❌'}\nReferrals: {user[3]}\nBanned: {'✅' if user[4] else '❌'}\n\n"
        
        for i in range(0, len(response), 3000):
            bot.send_message(message.chat.id, response[i:i+3000], parse_mode='Markdown', disable_web_page_preview=True)
    else:
        bot.send_message(message.chat.id, "🙅 ", disable_web_page_preview=True)

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.from_user.id == OWNER_ID:
        try:
            target_id = int(message.text.split()[1])
            c.execute('UPDATE users SET is_banned = 1 WHERE user_id = ?', (target_id,))
            conn.commit()
            bot.send_message(message.chat.id, f"✅ User {target_id} has been banned.", disable_web_page_preview=True)
        except:
            bot.send_message(message.chat.id, "❌ Usage: /ban <user_id>", disable_web_page_preview=True)
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
            bot.send_message(message.chat.id, "❌ Usage: /unban <user_id>", disable_web_page_preview=True)
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
                    bot.send_message(user[0], broadcast_text, parse_mode='Markdown', disable_web_page_preview=True)
                except:
                    pass
            bot.send_message(message.chat.id, "✅ Broadcast sent to all users.", disable_web_page_preview=True)
        except:
            bot.send_message(message.chat.id, "❌ Usage: /broadcast <message>", disable_web_page_preview=True)
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
        response = f"""**📊 {stylize_text('Bot Statistics')}:**

👥 Total Users: {total_users}
🎖️ Premium Users: {premium_users}
🚫 Banned Users: {banned_users}"""
        bot.send_message(message.chat.id, response, parse_mode='Markdown', disable_web_page_preview=True)
    else:
        bot.send_message(message.chat.id, "🙅", disable_web_page_preview=True)

# Message handler with ban check and username update
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
        bot.send_message(user_id, "Fιʀsт Sтᴀʀт Tнᴇ Boт Tнᴇɴ You Cᴀɴ Usᴇ Tнιs Boт\n\n/start", disable_web_page_preview=True)
        return
    if user[1]:
        bot.send_message(user_id, "Yuoʀ Bᴀɴɴᴇᴅ Fʀoм Tнιs Boт Iғ Yuo Tнιɴκ Tнιs Is Mιsтᴀκᴇ Pʟᴇᴀsᴇ Coɴтᴀcт Us :- @PB_X01", disable_web_page_preview=True)
        return
    
    prompt = message.text or message.caption
    image = None
    
    if message.photo:
        try:
            file_id = message.photo[-1].file_id
            file_info = bot.get_file(file_id)
            image = bot.download_file(file_info.file_path)
        except Exception as e:
            bot.send_message(user_id, f"❌ Error processing image: {str(e)}", disable_web_page_preview=True)
            return

    processing_msg = bot.send_message(user_id, "🔎", disable_web_page_preview=True)
    response = get_gemini_response(prompt, image)
    bot.delete_message(user_id, processing_msg.message_id)

    # Split response into text and code blocks
    parts = response.split('```')
    for i, part in enumerate(parts):
        if i % 2 == 0:  # Text part
            if part.strip():
                bot.send_message(user_id, f"{part.strip()}", parse_mode='Markdown', disable_web_page_preview=True)
        else:  # Code part
            if part.strip():
                bot.send_message(user_id, f"```\n{part.strip()}\n```", parse_mode='Markdown', disable_web_page_preview=True)

    user_tag = f"@{message.from_user.username}" if message.from_user.username else f"ID: {user_id}"
    owner_msg = f"**📩 New request from {user_tag}**\n🗒️ Query: {prompt[:100]}..."
    bot.send_message(OWNER_ID, owner_msg, parse_mode='Markdown', disable_web_page_preview=True)

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