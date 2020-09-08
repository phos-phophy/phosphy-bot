from random import randint, choice
from datetime import datetime
from connection import bot, app, db

cats = ['273364557']
size_cats = [4859]

dogs = []
size_dogs = []

pandas = []
size_pandas = []

frogs = []
size_frogs = []

anime = []
size_anime = []

easter_eggs = {'аксиома эскобара': 'Шо то хуйня, шо это хуйня. Вот это обе хуйни такие, шо я бля ебал ее маму в рот',
               'лучшая девочка': 'Алёна',
               'лучшая жопа': 'У Ярика',
               'лучший самоцвет': 'Phosphophyllite!',
               'лучший тайтл': 'Tower of God, Land of the Lustrous и OreGairu',
               'лучший жанр': 'Драма, повседневность',
               'лучшая вайфу': 'Шиноа Хиираги'}

nerd_ans = ['Ого, вы только посмотрите! А ботан дня-то - [id{0}|{1}]',
            'Кажется, ботан дня - [id{0}|{1}]',
            'Кто бы мог подумать, что ботан дня - [id{0}|{1}]',
            'Ботан дня обыкновенный, 1 шт. - [id{0}|{1}]',
            'А наш сегодняшний счастливчик - [id{0}|{1}]!',
            'Стоять! Никому не двигаться! Вы объявлены ботаном дня, [id{0}|{1}]',
            'Сканирование завершено. Ты ботан, [id{0}|{1}]',
            'Вжух и ты ботан, [id{0}|{1}]',
            'А прекрасным человеком дня объявляется [id{0}|{1}]!',
            'Что? Где? Когда? А ты ботан дня, [id{0}|{1}]',
            'Так-с, а ботаном дня сегодня становится [id{0}|{1}]',
            'Что там у нас? Надо же, ты теперь ботан дня, [id{0}|{1}]']


def get_nerd(chat_id, members):
    """return code of the answer, id and name of the nerd of the day
    0 - could not find nerd
    1 - nerd has already been selected
    2 - have found the nerd"""

    date = int(datetime.today().strftime('%d%m%Y'))
    chat_info = db.get_chat_info(chat_id)

    if len(chat_info) == 0:
        db.add_chat_info(chat_id)
        db.create_chat_members_table(chat_id)
    elif chat_info[0][4] == date:
        return 1, chat_info[0][2], chat_info[0][3]

    users_id = list()
    for member in members:
        if member['member_id'] > 0:
            users_id.append(member['member_id'])

    try:
        nerd_id = choice(users_id)
    except IndexError as exc:
        print(exc)
        return 0, 0, 0

    nerd_info = bot.get_user_info(nerd_id)
    nerd_name = nerd_info[0]['last_name'] + ' ' + nerd_info[0]['first_name']
    user_info = db.get_chat_member(chat_id=chat_id, user_id=nerd_id)

    if len(user_info) == 0:
        if nerd_id == 146693136:
            db.add_chat_member(chat_id, nerd_id, 0, 10)
        else:
            db.add_chat_member(chat_id, nerd_id, 0, 10)
    elif nerd_id == 146693136:
        db.update_nerd_count(chat_id, nerd_id, user_info[0][2] + 10)
    else:
        db.update_nerd_count(chat_id, nerd_id, user_info[0][2] + 1)

    db.update_nerd_info(chat_id, nerd_id=nerd_id, nerd_name=nerd_name, nerd_date=date)

    return 2, nerd_id, nerd_name


def get_nerd_history(chat_id):
    """return the list of names with nerd_counts """

    ans = list()
    members = db.get_all_chat_members(chat_id)

    for member in members:
        member_id = member[0]
        nerd_count = member[2]

        if member_id > 0 and nerd_count > 0:
            user_info = bot.get_user_info(member_id)
            ans.append((user_info[0]['last_name'] + ' ' + user_info[0]['first_name'], nerd_count))

    ans.sort(key=lambda x: x[1], reverse=True)
    return ans


def get_cat():
    """return a random photo of a cat"""

    index_of_album = randint(0, len(cats) - 1)
    index_of_photo = randint(0, size_cats[index_of_album] - 1)

    album = app.vk_app.photos.get(owner_id=-bot.group_id, album_id=cats[index_of_album],
                                  offset=(index_of_photo // 1000) * 1000, count=1000)

    return 'photo-' + str(bot.group_id) + '_' + str(album['items'][index_of_photo % 1000]['id'])


def get_dog():
    """return a random photo of a dog"""

    index_of_album = randint(0, len(dogs) - 1)
    index_of_photo = randint(0, size_dogs[index_of_album] - 1)

    album = app.vk_app.photos.get(owner_id=-bot.group_id, album_id=dogs[index_of_album],
                                  offset=(index_of_photo // 1000) * 1000, count=1000)

    return 'photo-' + str(bot.group_id) + '_' + str(album['items'][index_of_photo % 1000]['id'])


def get_panda():
    """return a random photo of a panda"""

    index_of_album = randint(0, len(pandas) - 1)
    index_of_photo = randint(0, size_pandas[index_of_album] - 1)

    album = app.vk_app.photos.get(owner_id=-bot.group_id, album_id=pandas[index_of_album],
                                  offset=(index_of_photo // 1000) * 1000, count=1000)

    return 'photo-' + str(bot.group_id) + '_' + str(album['items'][index_of_photo % 1000]['id'])


def get_frog():
    """return a random photo of a panda"""

    index_of_album = randint(0, len(frogs) - 1)
    index_of_photo = randint(0, size_frogs[index_of_album] - 1)

    album = app.vk_app.photos.get(owner_id=-bot.group_id, album_id=frogs[index_of_album],
                                  offset=(index_of_photo // 1000) * 1000, count=1000)

    return 'photo-' + str(bot.group_id) + '_' + str(album['items'][index_of_photo % 1000]['id'])


def get_anime():
    """return a random photo of a panda"""

    index_of_album = randint(0, len(anime) - 1)
    index_of_photo = randint(0, size_anime[index_of_album] - 1)

    album = app.vk_app.photos.get(owner_id=-bot.group_id, album_id=anime[index_of_album],
                                  offset=(index_of_photo // 1000) * 1000, count=1000)

    return 'photo-' + str(bot.group_id) + '_' + str(album['items'][index_of_photo % 1000]['id'])
