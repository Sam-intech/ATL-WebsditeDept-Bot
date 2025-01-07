# Importations
from typing import final
from telegram import Bot, Update
# from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, ContextTypes, Application
from datetime import datetime, timedelta, time as dt_time
# from datetime import datetime, timezone, timedelta
import pytz
import schedule
# import time
import threading
from apscheduler.schedulers.background import BackgroundScheduler


# importation ends here
# -----========================================================-----
# Bot Api and username 
TOKEN:final = '8192400793:AAHy4YGrwN7UfTa5r7tHbiXRhINEMKkt8cE'
BOT_USERNAME:final = '@ATL_WebsiteDept_Bot'


# ------------==================================================-------------------------
# Variables
# Define team members, their usernames, teams and role
members = [
    {"name": "Samuel Sonowo", "username": "@Sam_intech", "team": "Design Team, Development Team", "teamlead": False, "leader": True},
    {"name": "AbdulMalik Mukhtar", "username": "@malikmukhtar", "team": "Development Team", "teamlead": True, "leader": False},
    {"name": "Gbemisola Ajibade", "username": "@GbemmyA", "team": "Database Team", "teamlead": True, "leader": True},
    {"name": "Olushola Ogunkelu", "username": "@BeauNaturals", "team": "SEO/Content Writing Team", "teamlead": True, "leader": False},
    {"name": "Onyema Emmanuel Kelechi", "username": "@Mint04", "team": "Support Team", "teamlead": False, "leader": False},
    {"name": "Ebunoluwa Oladunjoye", "username": "@OmololaGift", "team": "Support Team", "teamlead": True, "leader": False},
    {"name": "Omoruyi Aiyudu", "username": "@UyiAiyudu", "team": "Database Team", "teamlead": False, "leader": False},
    {"name": "Awosolu Dayo", "username": "@Holadayur", "team": "Database Team", "teamlead": False, "leader": False},
    {"name": "Azubuike Utuh", "username": "@Zubi_007", "team": "SEO/Content Writing Team", "teamlead": False, "leader": False},
    {"name": "Omowumi Esther", "username": "@Soughtout22", "team": "SEO/Content Writing Team", "teamlead": False, "leader": False},
    {"name": "Tina Ozieh", "username": "@Teee_nah", "team": "SEO/Content Writing Team", "teamlead": False, "leader": False},
    {"name": "Seunfunmi Moses", "username": "@seunfunmianna", "team": "Design Team", "teamlead": True, "leader": False}
    # Add more members as needed
]


# Define teams with members, leaders, and meeting links
teams_data = {
    "Leadership Team": {
        "leader": [member['name'] for member in members if member['leader'] ==  True],
        "members": [member['name'] for member in members if member['teamlead'] == True or member['leader'] == True],
        "meeting_link": "https://meet.google.com/ohw-juya-xxd",
        # "meeting-time": "First Friday of the month (8pm - UTC+01:00)"
        "meeting_time": (datetime.now(pytz.timezone('Africa/Lagos')) + timedelta(seconds=5)).time(),  # Testing: 15 mins from now
        "group_topic_id": 100  # Example topic ID


    },
    "Design Team": {
        "leader": [member['name'] for member in members if member['team'] == "Design Team" and member['teamlead'] == True],
        "members": [member['name'] for member in members if member['team'] == "Design Team"],
        "meeting_link": "https://meet.google.com/rfb-cogx-nwv",
        "meeting_time": datetime.now(pytz.timezone('Africa/Lagos')).time(),  # Example time
        # "group_topic_id": 
    },
    "Development Team": {
        "leader": [member['name'] for member in members if member['team'] == "Development Team" and member['teamlead'] == True],
        "members": [member['name'] for member in members if member['team'] == "Development Team"],
        "meeting_link": "https://meet.google.com/nux-bfvh-gvf",
        "meeting_time": datetime.now(pytz.timezone('Africa/Lagos')).time(),  # Example time
        # "group_topic_id": 
    },
    "SEO/Content Writing Team": {
        "leader": [member['name'] for member in members if member['team'] == "SEO/Content Writing Team" and member['teamlead'] == True],
        "members": [member['name'] for member in members if member['team'] == "SEO/Content Writing Team"],
        "meeting_link": "https://meet.google.com/fzb-dejs-mtm",
        "meeting_time": datetime.now(pytz.timezone('Africa/Lagos')).time(),  # Example time
        # "group_topic_id": 
    },
    "Support Team": {
        "leader": [member['name'] for member in members if member['team'] == "Support Team" and member['teamlead'] == True],
        "members": [member['name'] for member in members if member['team'] == "Support Team"],
        "meeting_link": "Meeting link not set yet",
        "meeting_time": datetime.now(pytz.timezone('Africa/Lagos')).time(),  # Example time
        # "group_topic_id": 
    },
    "Database Team": {
        "leader": [member['name'] for member in members if member['team'] == "Database Team" and member['teamlead'] == True],
        "members": [member['name'] for member in members if member['team'] == "Database Team"],
        "meeting_link": "Meeting link not set yet",
        "meeting_time": datetime.now(pytz.timezone('Africa/Lagos')).time(),  # Example time
        # "group_topic_id":
    }
}


# messages variables
meetingsMessage = "MEETING TIMES \n\n\nTeam Leads - Every 1st Friday of the Month(8pm - UTC+01:00) \n**Design Team** - Every last Saturday of the month(7pm - UTC+01:00) \n**Development Team** - Every last Saturday of the month(8pm - UTC+01:00) \n**Database Team** - Unknown \n**SEO/Content Writing Team** - Unknown \n**Support Team** - Unknown"
rulesMessage = "🧑‍⚖️ DEPARTMENT RULES \n\n\n1. Any member that uses or shares the website's sensitive information outside of the department without the EXPRESS AUTHORIZATION of the team leads or the co-directors of the Department will be immediately REMOVED from the group and possibly from the department.\n\n2. Any team member who fails to perform or deliver on the task given to them without an explicitly convincing reason will pay a fine of #1000\n\n3. Any team member that has been inactive for more than 8 weeks will be EXPELLED from the department.\n\n4. Any team lead that doesn't attend a meeting without a valid reason to give at least 12 hours for meeting time will be subjected to a fine #2000.\n\nAll fine are to be paid to: \n7082236694 \nPalmpay \nAjibade Gbemisola \n\n5. A third strike mean automatic EXPULSION."
# teamsMessage = "**TEAMS & THEIR LEADS** \n\n\n1. Design Team - Seunfunmi \n2. Development Team - Mr Malik \n3. Database Team - Mrs Gbemi \n4. Content/SEO Team - Shola \n5. Support Team - Ebunoluwa"
membersMessage = "**MEMBERS LIST** \n\n" + "\n".join(
    [f"{i + 1}. {member['name']} ({member['username']}) - {member['team']}" for i, member in enumerate(members)]
)
helpMessage = "I run minor errand in the Department. I can help you with a list of the following:\n\n1. Get Department rules.\n2. Check Meeting times for all teams.\n3. List of teams in the department and their team leads.\n4. List of Website department team member"

# Define meeting links for each team using teams_data
meetingLinks = "MEETING LINKS\n" + "-" * 15 + "\n" + "\n".join(
    [f"{team}: {data['meeting_link']}" for team, data in teams_data.items()]
)

# teamleadMessage = "TEAM LEADS\n\n" + "-" * 10 + "\n".join(
#     [f"{team}: {data['leader']}" for team, data in teams_data.items()]
# )


# teams = ["Desgin Team", "Development Team", "Database Team", "SEO/Content Writing Team", "Support Team"]





# variables ends here
# -------==================================================---------------

# objects

# Update team_leads to populate from members list
# team_leads = {member['team']: member['name'] for member in members if member['is_lead']}

# Function to generate teamsMessage dynamically
def generate_teams_message() -> str:
    teams_message = "TEAMS & THEIR LEADS \n\n"
    for team, lead in team_leads.items():
        teams_message += f"{team} - {lead} (Leader) \n"
    return teams_message.strip()


async def list_topics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    topics = await context.bot.get_forum_topics(chat_id)
    for topic in topics:
        print(f"Topic Name: {topic.name}, Topic ID: {topic.message_thread_id}")
        await update.message.reply_text(
            f"Topic: {topic.name}, ID: {topic.message_thread_id}"
        )



# --------====================================================----------
# creating commands for the bots
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hi!, This is ATL Website Department Bot. I run minor arrand in the department. If you are not a member, i doubt i will be off any use to you. If you are an ATL Website team member, HEY!, What can i do for you?')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # helpMessage = "I run minor errand in the Department. I can help you with a list of the following:\n\n1. Get Department rules.\n2. Check Meeting times for all teams.\n3. List of teams in the department and their team leads.\n4. List of Website department team member"
    await update.message.reply_text(helpMessage)


async def rules_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # rulesMessage = "🧑‍⚖️DEPARTMENT RULES \n\n1. Any member that uses or shares the website's sensitive information outside of the department without the EXPRESS AUTHORIZATION of the team leads or the co-directors of the Department will be immediately REMOVED from the group and possibly from the department.\n2. Any team member who fails to perform or deliver on the task given to them without an explicitly convincing reason will pay a fine of #1000\n3. Any team member that has been inactive for more than 8 weeks will be EXPELLED from the department.\n4. Any team lead that doesn't attend a meeting without a valid reason to give at least 12 hours for meeting time will be subjected to a fine #2000.\n\nAll fine are to paid to: \n7082236694 \nPalmpay \nAjibade Gbemisola \n\n6. A third strike mean automatic EXPULSION."
    await update.message.reply_text(rulesMessage)


async def meetings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # meetingMessage = "MEETING TIMES \n\nTeam Leads - Every 1st Friday of the Month(8pm) \nDesign Team - Every last Saturday of the month(7pm) \nDevelopment Team - Every last Saturday of the month(8pm) \nDatabase Team - Unknown \nContent/SEO Team - Unknown \nSupport Team - Unknown"
    await update.message.reply_text(meetingsMessage)


# Update teams_command to use the new function
async def teams_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(generate_teams_message())


async def members_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # membersMessage = "MEMBERS LIST \n\nStill Compiling..."
    await update.message.reply_text(membersMessage)




# ------------------------
# Responding to messages from users
def handle_responses(text: str) -> str:
    processed: str = text.lower()

    # if all or any(keyword in processed for keyword in ['department', 'rules']):
    #     return rulesMessage

    if 'rules' in processed:
        return rulesMessage
    
    # -----
    # greatings and general words
    if any(keyword in processed for keyword in ['hello', 'hi']):
        return 'Hey Hi!, What can i do for you?'

    if any(keyword in processed for keyword in ['purpose', 'why']):
        return 'I am an Assistant Bot for ATL Website department. I perform minor tasks in the department like keeping infos and sending reminders promptly.'

    if any(keyword in processed for keyword in ['what can you do', 'help']):
        return helpMessage
    
    # -----
    # list of members
    if all(keyword in processed for keyword in ['list', 'members', 'all']):
        return membersMessage
    
    # -----
    # list of teamleads
    if all(keyword in processed for keyword in ['list', 'team', 'leads']):
        return teamleadMessage

    
    
    # --------
    # meeings
    if 'all meeting links' in processed:
        return meetingLinks

    # -----
    #teamleads 
    if all(keyword in processed for keyword in ['team lead', 'meeting', 'link']):
        return teams_data["Leadership Team"]["meeting_link"]
    
    if all(keyword in processed for keyword in ['team', 'leads', 'meeting', 'time']):
        return teams_data["Leadership Team"]["meeting-time"]
    
    if all(keyword in processed for keyword in ['team', 'leads', 'meeting', 'link', 'time']):
        return f"{teams_data['Leadership Team']['meeting-time']}\n\n{teams_data['Leadership Team']['meeting_link']}"

    # -----
    # design
    if all(keyword in processed for keyword in ['design', 'team', 'meeting', 'link']):
        return teams_data["Design Team"]["meeting_link"]

    if all(keyword in processed for keyword in ['design', 'team', 'meeting', 'time']):
        return teams_data["Design Team"]["meeting-time"]

    if all(keyword in processed for keyword in ['design', 'team', 'meeting', 'link', 'time']):
        return f"{teams_data['Design Team']['meeting-time']}\n{teams_data['Design Team']['meeting_link']}"
    
    if all(keyword in processed for keyword in ['list', 'members', 'design']):
        return {teams_data['Design Team']['members']}
    
    # -----
    # dev with an or
    if all(keyword in processed for keyword in ['development', 'meeting', 'link']):
        return teams_data["Development Team"]["meeting_link"]
    
    if all(keyword in processed for keyword in ['development', 'meeting', 'time']):
        return teams_data["Development Team"]["meeting-time"]
    
    if all(keyword in processed for keyword in ['dev', 'meeting', 'time']):
        return teams_data["Development Team"]["meeting-time"]
    
    if all(keyword in processed for keyword in ['dev', 'meeting', 'link']):
        return teams_data["Development Team"]["meeting_link"]
    
    if all(keyword in processed for keyword in ['list', 'members', 'development']):
        return {teams_data['Development Team']['members']}
    
    if all(keyword in processed for keyword in ['list', 'members', 'dev']):
        return {teams_data['Development Team']['members']}




    return 'I am sorry. I can not make out what you mean'




# ---------------------------
# handling of messages and send back user either in a group or in private chat
async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'user ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type in ['group', 'supergroup']:
        if update.message.entities:
            for entity in update.message.entities:
                if entity.type == 'mention':
                    mention_text = text[entity.offset: entity.offset + entity.length]
                    if mention_text == BOT_USERNAME:  # Check if the bot is mentioned correctly
                        new_text: str = text.replace(BOT_USERNAME, '').strip()
                        response: str = handle_responses(new_text)
                        print('Bot:', response)
                        await update.message.reply_text(response)
                        return
        print("Bot was not tagged in the group message.")

    elif message_type == 'private':
        response: str = handle_responses(text)
        print('Bot:', response)
        await update.message.reply_text(response)

    else:
        print(f"Unsupported message type: {message_type}")




# --------------------
# handling errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update (update) caused error {context.error}')


# ------------====================================================================================-----------------
# scheduling meeting
def schedule_reminders(bot, job_queue):
    nigeria_tz = pytz.timezone('Africa/Lagos')

    for team, data in teams_data.items():
        print(f"Processing team: {team}, Data: {data}")

        meeting_time = data.get("meeting_time")
        if not meeting_time:
            print(f"Skipping team {team} due to missing 'meeting_time'")
            continue

        # Handle both string and datetime.time types
        if isinstance(data["meeting_time"], dt_time):  # Use 'time' directly
            meeting_time = datetime.now(nigeria_tz).replace(
                hour=data["meeting_time"].hour,
                minute=data["meeting_time"].minute,
                second=0,
                microsecond=0,
            )
        elif isinstance(data["meeting_time"], str):
            meeting_time = datetime.strptime(data["meeting_time"], "%H:%M").replace(
                year=datetime.now().year,
                month=datetime.now().month,
                day=datetime.now().day,
                tzinfo=nigeria_tz,
            )
        else:
            print(f"Unsupported meeting_time format for team: {team}")
            continue

        # Schedule reminders
        reminders = [
            ("1 week before", meeting_time - timedelta(days=7)),
            ("2 days before", meeting_time - timedelta(days=2)),
            ("24 hours before", meeting_time - timedelta(hours=24)),
            ("5 hours before", meeting_time - timedelta(hours=5)),
        ]

        for desc, reminder_time in reminders:
            if reminder_time > datetime.now(nigeria_tz):  # Only schedule future reminders
                job_queue.run_once(
                    send_reminder,
                    when=(reminder_time - datetime.now(nigeria_tz)).total_seconds(),
                    context={"team": team, "data": data},
                    name=f"{team}_{desc}",
                )



# Send reminder message
async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    team = context.job.context["team"]
    data = context.job.context["data"]

    mentions = " ".join([f"@{member}" for member in data["members"]])
    message = (
        f"🚨 Reminder for {team} Meeting 🚨\n\n"
        f"Meeting Link: {data['meeting_link']}\n"
        f"Time: {data['meeting_time']}\n\n"
        f"Team Members: {mentions}"
    )

    await context.bot.send_message(
        chat_id="-1001898213670",  # Replace with actual group chat ID
        text=message,
        message_thread_id=data["group_topic_id"]
    )

# sending meeting reminders to team leads
# def send_reminder(context):
#     team_leads_names = [member['name'] for member in members if member['teamlead']]
#     team_leads_mentions = " ".join([f"@{member['username'][1:]}" for member in members if member['teamlead']])  # Remove '@' for mention
#     message = f"MEETING TIME 🚨\n\n\nDear Team leads\n{team_leads_mentions}\nKindly join the meeting! \n\nHere is a link to the meeting: {teams_data['Leadership Team']['meeting_link']}"
#     context.bot.send_message(chat_id='YOUR_GROUP_CHAT_ID', text=message)

# def schedule_reminders():
#     # Set timezone to Nigeria
#     nigeria_tz = pytz.timezone('Africa/Lagos')
    
#     # Calculate the time for the next reminder (15 minutes from now)
#     reminder_time = datetime.now(nigeria_tz) + timedelta(minutes=15)

#     # Schedule the reminder
#     schedule.every().day.at(reminder_time.strftime("%H:%M")).do(send_reminder)  # Send reminder at the calculated time

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








# ----------============================================---------------------
# Compilation..
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


    app.add_handler(CommandHandler("list_topics", list_topics))


    # error
    app.add_error_handler(error)


    # Schedule reminders
    scheduler = BackgroundScheduler()
    scheduler.start()
    schedule_reminders(app.bot, app.job_queue)


    # polling the pot
    print('polling...')

    # checks for new message every 5 seconds
    app.run_polling(poll_interval=5)



    