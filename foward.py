import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultPhoto
import credit


def start(bot, target_admin_id, target_channel_id):
    """
    bot: 機器人
    target_admin_id: 管理員id
    target_channel_id: 重要訊息頻道id
    credit_fc(user_id): 更新user_id的social credit
    """
    @bot.callback_query_handler(func=lambda cb: cb.data.startswith('throw_'))
    def throw_to_channel(call):
        call_info = call.data.split("_")
        text = ""
        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("👍", callback_data="like_like"),
                InlineKeyboardButton("👎", callback_data="like_dis")
            ]
        ])
        if call_info[1] == "Yes":
            new_msg = bot.forward_message(target_channel_id, from_chat_id=call_info[2], message_id=call_info[3])
            bot.reply_to(new_msg, "Vote", reply_markup=reply_markup)
            bot.answer_callback_query(call.id, "已成功轉傳")
            text = "已成功轉傳"
            print(bot.get_chat(call.message.reply_to_message.forward_from.id))
            credit.whenFOWARD(call.message.reply_to_message.forward_from.id)
        elif call.data == "throw_No":
            bot.answer_callback_query(call.id, "已阻止轉傳")
            text = "已阻止轉傳"
        bot.edit_message_text(text=text,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup = None)

    # 接收來自使用者的訊息，並轉發到目標頻道中
    @bot.message_handler(func=lambda message: message.json['chat']['type'] == 'private')
    def forward_to_channel(message):
        if message.json['chat']['type'] == 'private':
            # try:
                # 獲取訊息內容
                text = message.text
                reply_markup = InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("⭕️", callback_data=f"throw_Yes_{message.chat.id}_{message.message_id}_{message.forward_from.id}"),
                        InlineKeyboardButton("❌", callback_data="throw_No"),
                    ]
                ])
                # 轉發訊息到目標頻道
                new_msg = bot.forward_message(target_admin_id, from_chat_id=message.chat.id, message_id=message.message_id)
                bot.reply_to(new_msg, "請問以上是否為重要訊息？", reply_markup=reply_markup)
                bot.reply_to(message, "已轉傳給管理員")

            # except Exception as e:
            #     print(f"轉發訊息時出現錯誤：{e}")