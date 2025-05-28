import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from game import BlackjackGame

game = BlackjackGame()

TOKEN = "YOUR_BOT_TOKEN"  # 请替换为你自己的 BotFather 提供的 Token

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "欢迎来到21点游戏！使用 /join 加入游戏，/startgame 开始游戏。"
    )

async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.full_name
    game.add_player(user_id, username)
    await update.message.reply_text(f"{username} 已加入游戏！")

async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    game.start_game()
    for user_id in game.players:
        await context.bot.send_message(chat_id=user_id, text=game.get_player_initial_cards(user_id))
    await update.message.reply_text("游戏已开始，所有玩家已收到初始牌。")

async def hit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = game.player_hit(user_id)
    await update.message.reply_text(text)

async def stand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = game.player_stand(user_id)
    await update.message.reply_text(text)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("join", join))
    app.add_handler(CommandHandler("startgame", start_game))
    app.add_handler(CommandHandler("hit", hit))
    app.add_handler(CommandHandler("stand", stand))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()