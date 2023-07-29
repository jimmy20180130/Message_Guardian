import json
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultPhoto

userCredit = {} #{userid: Credit}

like = {} #{message: [43434,9989898]}
#len(like[messageid])

dislike = {} #{message: [43434,9989898]}
#len(dislike[messageid])

current_moment_user_count = 0

#read everyone's scores
with open('score_userCredit.json', 'r', encoding="utf-8") as f:
    database = json.load(f)
    userCredit = database['userCredit']
    like = database['like']
    dislike = database['dislike']
    print(like, type(like))
    for i in like:
        like[i] = set(like[i])
    print(like, type(like))
    for i in dislike:
        dislike[i] = set(dislike[i])
    print('like', like)
    print("loaded data")

def element_to_list(d):
    r = d.copy()
    for k, v in r.items():
        r[k] = list(v)
    return r

#store everyone's scores
def saveScore(userCredit: dict):
    with open('score_userCredit.json', 'w', encoding='utf-8') as f:
        data = {
            'userCredit': userCredit,
            "like": element_to_list(like),
            'dislike': element_to_list(dislike),
        }
        print(data)
        json.dump(data, f, indent=2, sort_keys=False, ensure_ascii=False)

def getUserCredit(userid: str) -> float:
    userid = str(userid)
    CheckUserExist(userid)
    return userCredit[userid]

# How score changes after forwarded
def whenFOWARD(userid: int):
    userid = str(userid)
    print(1, userCredit)
    CheckUserExist(userid)
    print(2, userCredit)
    userCredit[userid] += 0.1
    print(3, userCredit)
    saveScore(userCredit)
    return userCredit[userid]


#Check if the person exist in the userCredit
def CheckUserExist(userid: str) -> float:
    userid = str(userid)
    if userid not in userCredit:
        userCredit[userid] = 0.5
    saveScore(userCredit)
    return userCredit[userid]

#event
#How score changes after message liked or disliked(now unfinished)

def message_in_like_or_not(message_id):
    message_id  = str(message_id)
    if message_id not in like:
        like[message_id] = set()
    return like[message_id]

def message_in_dislike_or_not(message_id):
    message_id  = str(message_id)
    if message_id not in dislike:
        dislike[message_id] = set()
    return dislike[message_id]
    
#a, b = message_in_like_dislike_or_not()

'''
    reply_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("like ", callback_data="like_like"),
            InlineKeyboardButton("dislike ", callback_data="like_dis"),
        ]
    ])
'''

def start(bot):
    @bot.callback_query_handler(func=lambda cb: cb.data.startswith('like_like'))
    def like_count(call):
        whoPress = str(call.from_user.id)
        fromuser = str(call.message.reply_to_message.forward_from.id)
        msg_id = str(call.message.message_id)
        print(f'fromuser: {fromuser}, whoPress: {whoPress}')
        CheckUserExist(fromuser)
        message_in_dislike_or_not(call.message.message_id)
        message_in_like_or_not(call.message.message_id)
        print('like', like, msg_id, like[msg_id])

        print('whoPress', whoPress, like[msg_id])
        if whoPress not in like[msg_id]:
            print('new user like')
            like[msg_id].add(whoPress)
            decide_score(call, 'like')
            saveScore(userCredit)
        bot.answer_callback_query(call.id, "已按讚")

    #dislike count
    @bot.callback_query_handler(func=lambda cb: cb.data.startswith('like_dis'))
    def dislike_count(call):
        whoPress = str(call.from_user.id)
        fromuser = str(call.message.reply_to_message.forward_from.id)
        msg_id = str(call.message.message_id)
        CheckUserExist(fromuser)
        message_in_dislike_or_not(call.message.message_id)
        message_in_like_or_not(call.message.message_id)

        if whoPress not in like[msg_id]:
            print('new user dislike')
            dislike[msg_id].add(whoPress)
            decide_score(call, 'dislike')
            saveScore(userCredit)
        bot.answer_callback_query(call.id, "已按倒讚")

    @bot.message_handler(commands=['showcredit'])
    def send_Credit(message):
        print(userCredit)
        data = {}
        text = "大家的信譽分數:\n"
        for k, v in userCredit.items():
            text += f'{bot.get_chat(k).first_name}:\t\t{round(v, 2)}\n'
        bot.reply_to(message, text)

def decide_score(call, mode):
    userid = str(call.message.reply_to_message.forward_from.id)
    msgid = str(call.message.id)
    print(call.from_user.id, call.message.reply_to_message.forward_from.id)
    if mode == 'like':
        userCredit[userid] += 0.02
    if mode == 'dislike':
        userCredit[userid] -= 0.02
    # if len (like[call.message.id]) == (len(userCredit) // 2) + 1 or len (dislike[call.message.id]) == (len(userCredit) // 2) + 1: 
    #     if len(like[call.message.id]) > len(dislike[call.message.id]):
    #         userCredit[userid] += 0.1
    #         saveScore(userCredit)

    #     if len(like[call.message.id]) < len(dislike[call.message.id]):
    #         userCredit[userid] -= 0.1
    #         saveScore(userCredit)