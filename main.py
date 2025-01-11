# Importations
import os
from typing import final
from telegram import Bot, Update
# from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, ContextTypes, Application
from datetime import datetime, timedelta, time as dt_time
import pytz
import calendar
import schedule
# import time
import threading
from apscheduler.schedulers.background import BackgroundScheduler


# importation ends here
# -----========================================================-----
# Bot Api and username 
TOKEN:final = os.getenv("TELEGRAM_BOT_TOKEN") #Hide the bot token using environment
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


# ---------------------------------
# calculating meeting date
def get_meeting_date(year, month, weekday, week_index, time_of_day, timezone):
    """
    Calculate the date for a specific week and day in a given month.
    :param year: Year of the meeting
    :param month: Month of the meeting
    :param weekday: 0 = Monday, ..., 6 = Sunday
    :param week_index: 1 = First week, ..., 4 = Fourth week
    :param time_of_day: Time of the meeting (as datetime.time)
    :param timezone: pytz timezone object
    :return: datetime object of the meeting
    """
    calendar_month = calendar.monthcalendar(year, month)
    target_week = [week for week in calendar_month if week[weekday] != 0][week_index - 1]
    meeting_date = datetime(year, month, target_week[weekday], time_of_day.hour, time_of_day.minute, tzinfo=timezone)
    return meeting_date


nigeria_tz = pytz.timezone('Africa/Lagos')
now = datetime.now(nigeria_tz)


# ----------------------------------------------------------------
# Define teams with members, leaders, and meeting links
teams_data = {
    "Leadership Team": {
        "leader": [member['name'] for member in members if member['leader'] ==  True],
        "members": [member['name'] for member in members if member['teamlead'] == True or member['leader'] == True],
        "meeting_link": "https://meet.google.com/ohw-juya-xxd",
        "meeting_time": get_meeting_date(now.year, now.month, weekday=4, week_index=1, time_of_day=dt_time(20, 0), timezone=nigeria_tz),  # First Friday
        # "meeting_time": (datetime.now(nigeria_tz) + timedelta(seconds=5)).time(),  # Testing: 5 seconds
        "team_topic_id": 5043  # Example topic ID


    },
    "Design Team": {
        "leader": [member['name'] for member in members if member['team'] == "Design Team" and member['teamlead'] == True],
        "members": [member['name'] for member in members if member['team'] == "Design Team"],
        "meeting_link": "https://meet.google.com/rfb-cogx-nwv",
        "meeting_time": get_meeting_date(now.year, now.month, weekday=5, week_index=2, time_of_day=dt_time(20, 0), timezone=nigeria_tz),  # Second Saturday
        # "meeting_time": (datetime.now(nigeria_tz) + timedelta(seconds=10)).time(),  # Testing: 5 seconds
        "team_topic_id": 4914
    },
    "Development Team": {
        "leader": [member['name'] for member in members if member['team'] == "Development Team" and member['teamlead'] == True],
        "members": [member['name'] for member in members if member['team'] == "Development Team"],
        "meeting_link": "https://meet.google.com/nux-bfvh-gvf",
        "meeting_time": get_meeting_date(now.year, now.month, weekday=5, week_index=3, time_of_day=dt_time(20, 0), timezone=nigeria_tz),  # Third Saturday
        # "meeting_time": (datetime.now(nigeria_tz) + timedelta(seconds=15)).time(),  # Testing: 5 seconds
        "team_topic_id": 4934 
    },
    "SEO/Content Writing Team": {
        "leader": [member['name'] for member in members if member['team'] == "SEO/Content Writing Team" and member['teamlead'] == True],
        "members": [member['name'] for member in members if member['team'] == "SEO/Content Writing Team"],
        "meeting_link": "https://meet.google.com/fzb-dejs-mtm",
        "meeting_time": None,  # Example time
        "team_topic_id": 4936 
    },
    "Support Team": {
        "leader": [member['name'] for member in members if member['team'] == "Support Team" and member['teamlead'] == True],
        "members": [member['name'] for member in members if member['team'] == "Support Team"],
        "meeting_link": "Meeting link not set yet",
        "meeting_time": None,  # Example time
        "team_topic_id": 4911 
    },
    "Database Team": {
        "leader": [member['name'] for member in members if member['team'] == "Database Team" and member['teamlead'] == True],
        "members": [member['name'] for member in members if member['team'] == "Database Team"],
        "meeting_link": "Meeting link not set yet",
        "meeting_time": None,  # Example time
        "team_topic_id": 4901
    }
}


# messages variables
meetingsMessage = "MEETING TIMES\n" + "-" * 15 + "\nTeam Leads - Every 1st Friday of the Month(8pm - UTC+01:00) \nDesign Team - Every last Saturday of the month(7pm - UTC+01:00) \nDevelopment Team - Every last Saturday of the month(8pm - UTC+01:00) \nDatabase Team - Unknown \nSEO/Content Writing Team - Unknown \nSupport Team - Unknown"
rulesMessage = "🧑‍⚖️ DEPARTMENT RULES\n" + "-" * 15 + "\n1. Any member that uses or shares the website's sensitive information outside of the department without the EXPRESS AUTHORIZATION of the team leads or the co-directors of the Department will be immediately REMOVED from the group and possibly from the department.\n\n2. Any team member who fails to perform or deliver on the task given to them without an explicitly convincing reason will pay a fine of #1000\n\n3. Any team member that has been inactive for more than 8 weeks will be EXPELLED from the department.\n\n4. Any team lead that doesn't attend a meeting without a valid reason to give at least 12 hours for meeting time will be subjected to a fine #2000.\n\nAll fine are to be paid to: \n7082236694 \nPalmpay \nAjibade Gbemisola \n\n5. A third strike mean automatic EXPULSION."
teamsMessage = "TEAMS & THEIR LEADS\n" + "-" * 15 + "\n1. Design Team - Seunfunmi \n2. Development Team - Mr Malik \n3. Database Team - Mrs Gbemi \n4. Content/SEO Team - Shola \n5. Support Team - Ebunoluwa"
membersMessage = "MEMBERS LIST\n" + "-" * 15 + "\n".join(
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


async def topics_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    
    try:
        # Fetch chat details
        chat = await context.bot.get_chat(chat_id)
        
        if not chat.is_forum:
            await update.message.reply_text("This chat does not support topics.")
            return

        # List topics
        topics = chat.forum_topics
        if not topics:
            await update.message.reply_text("No topics found in this group.")
            return

        response = "Group Topics:\n"
        for topic in topics:
            response += f"Topic Name: {topic.name}, Topic ID: {topic.message_thread_id}\n"
            print(f"Topic Name: {topic.name}, Topic ID: {topic.message_thread_id}")
        await update.message.reply_text(response)
    except Exception as e:
        print(f"Error retrieving topics: {e}")
        await update.message.reply_text(f"Failed to list topics: {e}")



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



# -----------------------------------
async def log_thread_ids(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message:
        thread_id = message.message_thread_id
        print(f"Message received in thread ID: {thread_id}")
        await update.message.reply_text(f"Thread ID: {thread_id}")
    else:
        await update.message.reply_text("No thread ID found in this message.")





# ---------------------------
# handling of messages and send back user either in a group or in private chat
async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Received update: {update}")

    
    if update.message and hasattr(update.message, "pinned_message") and update.message.pinned_message:
        print("Pinned message detected. Ignoring.")
        return

    # Ignore non-text messages
    if not update.message or not update.message.text:
        print("Non-text message detected. Ignoring.")
        return

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









# SCHEDULING MEETINGS AND SENDING REMINDERS
# ------------====================================================================================-----------------
# scheduling meeting
def schedule_reminders(bot, job_queue):
    nigeria_tz = pytz.timezone('Africa/Lagos')

    for team, data in teams_data.items():
        # print(f"Processing team: {team}, Data: {data}")

        meeting_time = data.get("meeting_time")
        if not meeting_time:
            # print(f"No meeting time set for {team}. Skipping.")
            continue

        # Schedule reminders
        reminders = [
            ("1 week before", meeting_time - timedelta(days=7), send_reminder_message),
            ("2 days before", meeting_time - timedelta(days=2), send_reminder_message),
            ("6 hours before", meeting_time - timedelta(hours=6), send_reminder_message),
            ("on meeting day", meeting_time, send_meeting_message)
        ]

        for desc, reminder_time, func in reminders:
            if reminder_time > datetime.now(nigeria_tz):  # Only schedule future events
                job_queue.run_once(
                    func,
                    when=(reminder_time - datetime.now(nigeria_tz)).total_seconds(),
                    data={"team": team, "data": data},
                    name=f"{team}_{desc}",
                )



async def send_reminder_message(context: ContextTypes.DEFAULT_TYPE):
    job_data = context.job.data
    team = job_data["team"]
    data = job_data["data"]

    # Calculate days remaining for the meeting
    meeting_time = data["meeting_time"]
    now = datetime.now(pytz.timezone('Africa/Lagos'))
    days_remaining = (meeting_time - now).days


    # Tag team members using their Telegram usernames
    mentions = " ".join(
        [f"@{member['username'][1:]}" for member in members if member['name'] in data["members"]]
    )

    # Reminder message
    reminder_message = (
        f"🚨 GENTLE REMINDER FOR {team} MONTHLY MEETING! 🚨\n\n"
        f"📅 Date: {data['meeting_time']:%A, %B %d, %Y}\n"
        f"🕒 Time: {data['meeting_time']:%I:%M %p}\n\n"
        f"👥 Attendees: {mentions}\n\n"
        f"{days_remaining} day(s) left to the meeting. Please be on time.\nThank you!"
    )

    try:
        # Send reminder to the team topic
        await context.bot.send_message(
            chat_id="-1001898213670",  # send the message to the group using group ID
            text=reminder_message,
            message_thread_id=data["team_topic_id"] # sends message to specific topics in the group
        )
        print(f"Reminder sent for {team} meeting in topic {data['team_topic_id']}")
    except Exception as e:
        print(f"Failed to send reminder for {team}: {e}")





async def send_meeting_message(context: ContextTypes.DEFAULT_TYPE):
    job_data = context.job.data
    team = job_data["team"]
    data = job_data["data"]

    # Tag all team members
    mentions = " ".join([f"@{member.replace(' ', '_')}" for member in data["members"]])
    message = (
        f"🚨 {team} MEETING STARTS 🚨\n\n"
        # f"🕒 Time: {data['meeting_time']}\n"
        f"👥 Attendees: {mentions}\n\n"
        f"Please join in ⬇️⬇️\n"
        f"📅 Meeting Link: {data['meeting_link']}"
    )

    try:
        # Send meeting day message to the team topic
        await context.bot.send_message(
            chat_id="-1001898213670",  # send the message to the group using group ID
            text=message,
            message_thread_id=data["team_topic_id"] # send message to specific topic(teams) in the group
        )
        print(f"Meeting message sent for {team} in topic {data['team_topic_id']}")
    except Exception as e:
        print(f"Failed to send meeting message for {team}: {e}")








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
    app.add_handler(CommandHandler('topics', topics_command))


    # the messages
    app.add_handler(MessageHandler(filters.TEXT, handle_messages))
    # app.add_handler(CommandHandler("list_topics", list_topics))
    app.add_handler(MessageHandler(filters.ALL, log_thread_ids))



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



    