from bot import Bot
from app import App
from database import Database
import os


# information about group
token = str(os.environ.get('BOT_TOKEN'))
group_id = 196764812

# information about app
client_id = os.environ.get('CLIENT_ID')
client_secret = str(os.environ.get('CLIENT_SECRET'))
access_token = str(os.environ.get('ACCESS_TOKEN'))

# basic commands
basic_commands = {'-help': 'photo-196764812_457244024',
                  '-кафедры': 'photo-196764812_457244025',
                  '-чилл': 'photo-196764812_457244026',
                  '-матан': 'photo-196764812_457244027'}

# information about bot
bot_inf = 'Бот создан при моральной поддержке \"Дримтим\" и \"Групповуха\"\n\n' \
          'Для просмотра остальных команд введите \'-help\''

# creation bot and app, connect to database
bot = Bot(token, group_id)
app = App(client_id, client_secret, access_token)
db = Database('bot_db')
