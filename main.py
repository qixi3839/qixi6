import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from game import BlackjackGame

# 初始化游戏逻辑对象
game = BlackjackGame()

# 从环境变量获取 Token（在 Render 设置 TOKEN）
TOKEN = os.getenv("TOKEN")

# /start 命令：欢迎信息
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎲 欢迎来到21点游戏！\n👉 输入 /join 加入游戏\n👉 输入 /startgame 开始游戏"
    )

# /join 命令：玩家加入
async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.full_name
    game.add_player(user_id, username)
    await update.message.reply_text(f"✅ {username} 已加入游戏！")

# /startgame 命令：开始游戏，向每个玩家发牌
async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    game.start_game()
    for user_id in game.players:
        await context.bot.send_message(chat_id=user_id, text=game.get_player_initial_cards(user_id))
    await update.message.reply_text("🃏 游戏开始，所有玩家已收到初始牌！")

# /hit 命令：玩家要牌
async def hit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = game.player_hit(user_id)
    await update.message.reply_text(text)

# /stand 命令：玩家停牌
async def stand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = game.player_stand(user_id)
    await update.message.reply_text(text)

# 启动机器人
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("join", join))
    app.add_handler(CommandHandler("startgame", start_game))
    app.add_handler(CommandHandler("hit", hit))
    app.add_handler(CommandHandler("stand", stand))
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
