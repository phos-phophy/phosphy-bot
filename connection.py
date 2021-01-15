from bot import Bot
from app import App
from database import Database


# information about group
token = ...
group_id = ...

# information about app
client_id = ...
client_secret = ...
access_token = ...

# basic commands
basic_commands = {'-help': 'photo-196764812_457244080',
                  '-control': 'photo-196764812_457244081',
                  '-кафедры': 'photo-196764812_457244025',
                  '-чилл': 'photo-196764812_457244082',
                  '-матан': 'photo-196764812_457244027'}

# information about bot
bot_inf = 'Бот создан при моральной поддержке \"Дримтим\" и \"Групповуха\"\n\n' \
          'Для просмотра остальных команд введите \'-help\''

# creation bot and app, connect to database
bot = Bot(token, group_id)
app = App(client_id, client_secret, access_token)
db = Database('bot_db')
