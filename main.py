import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import msg_score
import foward
import credit

# 替換成你自己的 Telegram Bot API Token
bot_token = '6475926933:AAFQ1ybI-L1sSX22gpqHZdYi0VcMoKBTF-c'
 
# 建立 Telegram Bot 物件
bot = telebot.TeleBot(bot_token)
target_admin_id = '6091149500'
target_channel_id = '-1001944967974'

foward.start(bot, target_admin_id, target_channel_id)
credit.start(bot)

def getUserCredit(id: int) -> float:
    return 0.5

def getTextScore(text: str) -> float:
    message_score = msg_score.getTextScore(text)
    return message_score
 
def get_score(message) -> float:
    UserCredit = getUserCredit(message.from_user.id)
    TextScore = getTextScore(message.text)
    score = UserCredit * TextScore
    return score
 
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
        bot.reply_to(message, """\
Hi 我是 message guardian bot 
我是一個你們專屬的群組管理員，以下是我的功能
1.我將會幫你們篩選重要訊息
2.如果我有遺漏也可以手動轉傳重要訊息給我
3.也可以透過投票 讓我的之後的判斷更加準確
4.每個群組成員都將有一個 social credit(威望) 會隨著成員在群組的行為 進行分數的更動
希望能為您打造一個乾淨的重點整理頻道 和 友善的群組環境

指令:
/help        顯示指令列表
/start       顯示我的介紹
/showcredit  顯示大家的信譽積分
""")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    score = getTextScore(message.text)
    usercredit = credit.getUserCredit(message.from_user.id)

    print(score, usercredit)
 
    finalScore = score * usercredit

    reply_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("👍", callback_data="like_like"),
            InlineKeyboardButton("👎", callback_data="like_dis")
        ]
    ])
 
    if finalScore >= 0.6:
 
        new_msg = bot.forward_message(
            target_channel_id,
            from_chat_id=message.chat.id,
            message_id=message.message_id
        )
    
        bot.reply_to(new_msg, 'react', reply_markup=reply_markup)
        credit.whenFOWARD(message.from_user.id)

 
    
    word_listt = msg_score.cut_text(message.text)
    bot.reply_to(message, f'這則訊息的分數: {score}')
    bot.reply_to(message, f'這則訊息的分析: {word_listt}')
 
 
# 開始接收並處理來自 Telegram 的訊息
print('bot is online')
bot.infinity_polling()