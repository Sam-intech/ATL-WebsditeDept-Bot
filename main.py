from typing import final
from telegram import Bot
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, ContextTypes, Application
# import schedule
# import time
# import threading
# from datetime import datetime
# import pytz

# Bot Api and username 
TOKEN:final = '8192400793:AAHy4YGrwN7UfTa5r7tHbiXRhINEMKkt8cE'
BOT_USERNAME:final = '@ATL_WebsiteDept_Bot'


# ------------------
# creating commands for the bots
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hi!, This is ATL Website Department Bot. I run minor arrand in the department. If you are not a member, i doubt i will be off any use to you. If you are an ATL Website team member, HEY!, What can i do for you?')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    helpMessage = "I run minor errand in the Department. I can help you with a list of the following:\n\n1. Get Department rules.\n2. Check Meeting times for all teams.\n3. List of teams in the department and their team leads.\n4. List of Website department team member"
    await update.message.reply_text(helpMessage)


async def rules_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rulesMessage = "🧑‍⚖️DEPARTMENT RULES \n\n1. Any member that uses or shares the website's sensitive information outside of the department without the EXPRESS AUTHORIZATION of the team leads or the co-directors of the Department will be immediately REMOVED from the group and possibly from the department.\n2. Any team member who fails to perform or deliver on the task given to them without an explicitly convincing reason will pay a fine of #1000\n3. Any team member that has been inactive for more than 8 weeks will be EXPELLED from the department.\n4. Any team lead that doesn't attend a meeting without a valid reason to give at least 12 hours for meeting time will be subjected to a fine #2000.\n\nAll fine are to paid to: \n7082236694 \nPalmpay \nAjibade Gbemisola \n\n6. A third strike mean automatic EXPULSION."
    await update.message.reply_text(rulesMessage)


async def meetings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    meetingMessage = "MEETING TIMES \n\nTeam Leads - Every 1st Friday of the Month(8pm) \nDesign Team - Every last Saturday of the month(7pm) \nDevelopment Team - Every last Saturday of the month(8pm) \nDatabase Team - Unknown \nContent/SEO Team - Unknown \nSupport Team - Unknown"
    await update.message.reply_text(meetingMessage)


async def teams_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teamsMessage = "TEAMS & THEIR LEADS \n\n1. Design Team - Seunfunmi \n2. Development Team - Mr Malik \n3. Database Team - Mrs Gbemi \n4. Content/SEO Team - Shola \n5. Support Team - Ebunoluwa"
    await update.message.reply_text(teamsMessage)


async def members_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    membersMessage = "MEMBERS LIST \n\nStill Compiling..."
    await update.message.reply_text(membersMessage)




# ------------------------
# Responding to messages from users
def handle_responses(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hey Hi!'

    if 'hi' in processed:
        return 'Hello!'

    if 'ATL website member' in processed:
        return 'Great! Kindly tell me your username please'

    if 'ATL member' in processed:
        return 'Oh right. Glad to have you here ATLite. However, this bot is for the IT Department'

    if 'Alpha training lab member' in processed: 
        return 'Oh right. Glad to have you here ATLite. However, this bot is for the IT Department'

    return 'I am an assistant bot for ATL Website department. If you are not a member of ATL website department, I am afraid i will be of no use to you. If you are a member of ATL website department, kindly tell me your telegram username please.'




# ---------------------------
# handling of messages and send back user either in a group or in private chat
async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'user ({update.message.chat.id}) in {message.type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_reponses(new_text)
        else:
            return
    else:
        response: str = handle_reponses(text)

    print('Bot:', response)
    await update.message.reply_text(response)



# --------------------
# handling errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update (update) caused error {context.error}')


# ------------====================================================================================-----------------
# sending meeting reminders to team leads
# def send_reminder(context):
#     context.bot.send_message(chat_id='YOUR_GROUP_CHAT_ID', text="Reminder: Team leaders, please prepare for the meeting!")

# def schedule_reminders():
#     # Set timezone to Nigeria
#     nigeria_tz = pytz.timezone('Africa/Lagos')
    
#     # Schedule the reminder for the first Friday of every month at 8 PM
#     schedule.every().month.at("20:00").do(send_reminder)

#     while True:
#         schedule.run_pending()
#         time.sleep(1)

# def start(update, context):
#     update.message.reply_text("Bot started! Reminders will be sent every first Friday of the month.")

# def main():
#     updater = Updater(token, use_context=True)
#     dp = updater.dispatcher

#     dp.add_handler(CommandHandler("start", start))

#     # Start the reminder scheduling in a separate thread
#     threading.Thread(target=schedule_reminders).start()

#     updater.start_polling()
#     updater.idle()







if __name__ == '__main__':
    print('starting bot...')
    # main()
    app = Application.builder().token(TOKEN).build()


    # the commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('rules', rules_command))
    app.add_handler(CommandHandler('meetings', meetings_command))
    app.add_handler(CommandHandler('teams', teams_command))
    app.add_handler(CommandHandler('members', members_command))


    # the messages
    app.add_handler(MessageHandler(filters.TEXT, handle_messages))


    # error
    app.add_error_handler(error)


    # polling the pot
    print('polling...')

    # checks for new message every 5 seconds
    app.run_polling(poll_interval=5)