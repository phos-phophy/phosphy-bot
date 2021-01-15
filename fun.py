from random import randint, choice
from datetime import datetime
from connection import bot, app, db
import json

leg_group_id = 125649011
kpt_group_id = 184860963
mlu_group_id = 92876084
mnu_group_id = 152671561
haiku_group_id = 92597394
anitype_group_id = 102297515

cats = ['273364557']
size_cats = [4859]

dogs = ['276575090']
size_dogs = [1645]

pandas = []
size_pandas = []

frogs = []
size_frogs = []

anime = []
size_anime = []

jew = ['97564662_457244986',
       '97564662_457244986',
       '97564662_457243883',
       '97564662_457243883',
       '97564662_456240982',
       '97564662_379252144',
       '97564662_367744740',
       '156310742_457242428',
       '156310742_456241121',
       '156310742_456239284',
       '156310742_456239984',
       '154781321_456245857',
       '154781321_410669548',
       '154781321_273116912',
       '154781321_456241330',
       '154781321_456241031',
       '182115778_457244426',
       '182115778_457243319',
       '182115778_456240259',
       '182115778_456240202',
       '182115778_456240254',
       '182115778_456240255',
       '182115778_456240258',
       '182115778_457244431',
       '182115778_457244430',
       '182115778_457244429',
       '182115778_457244429']

adyg = ['498558144_457251555',
        '498558144_457244224',
        '498558144_456241809',
        '498558144_456239219',
        '498558144_456242087',
        '498558144_456242086',
        '498558144_456242093',
        '498558144_456242089',
        '498558144_456242088',
        '498558144_456239216']

easter_eggs = {'аксиома эскобара': 'Шо то хуйня, шо это хуйня. Вот это обе хуйни такие, шо я бля ебал ее маму в рот',
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
            db.add_chat_member(chat_id, nerd_id, 0, 1)
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
                                  offset=index_of_photo, count=1)

    return 'photo-' + str(bot.group_id) + '_' + str(album['items'][0]['id'])


def get_dog():
    """return a random photo of a dog"""

    index_of_album = randint(0, len(dogs) - 1)
    index_of_photo = randint(0, size_dogs[index_of_album] - 1)

    album = app.vk_app.photos.get(owner_id=-bot.group_id, album_id=dogs[index_of_album],
                                  offset=index_of_photo, count=1)

    return 'photo-' + str(bot.group_id) + '_' + str(album['items'][0]['id'])


def get_panda():
    """return a random photo of a panda"""

    index_of_album = randint(0, len(pandas) - 1)
    index_of_photo = randint(0, size_pandas[index_of_album] - 1)

    album = app.vk_app.photos.get(owner_id=-bot.group_id, album_id=pandas[index_of_album],
                                  offset=index_of_photo, count=1)

    return 'photo-' + str(bot.group_id) + '_' + str(album['items'][0]['id'])


def get_frog():
    """return a random photo of a panda"""

    index_of_album = randint(0, len(frogs) - 1)
    index_of_photo = randint(0, size_frogs[index_of_album] - 1)

    album = app.vk_app.photos.get(owner_id=-bot.group_id, album_id=frogs[index_of_album],
                                  offset=index_of_photo, count=10)

    return 'photo-' + str(bot.group_id) + '_' + str(album['items'][0]['id'])


def get_anime():
    """return a random photo of a panda"""

    index_of_album = randint(0, len(anime) - 1)
    index_of_photo = randint(0, size_anime[index_of_album] - 1)

    album = app.vk_app.photos.get(owner_id=-bot.group_id, album_id=anime[index_of_album],
                                  offset=index_of_photo, count=1)

    return 'photo-' + str(bot.group_id) + '_' + str(album['items'][0]['id'])


def get_jew():
    """return a random photo of jew"""

    return 'photo' + choice(jew)


def get_adyg():
    """return a random photo of adyg"""

    return 'photo' + choice(adyg)


def get_legs():
    """return a random photo of women legs"""

    res = app.vk_app.wall.get(owner_id=-leg_group_id, offset=randint(0, 5000), count=10)
    ans = []

    for item in res["items"]:
        if item["marked_as_ads"]:
            continue

        if "attachments" in item:
            for attach in item["attachments"]:
                if attach["type"] == "photo":
                    ans.append("photo" + str(attach["photo"]["owner_id"]) + "_" + str(attach["photo"]["id"]))
            if len(ans) != 0:
                break

    return ans


def get_kpt():
    """return a random meme from public 'комочек пушистой тьмы'"""

    res = app.vk_app.wall.get(owner_id=-kpt_group_id, offset=randint(0, 6000), count=10)
    ans = []

    for item in res["items"]:
        if item["marked_as_ads"]:
            continue

        if "attachments" in item:
            for attach in item["attachments"]:
                if attach["type"] == "photo":
                    ans.append("photo" + str(attach["photo"]["owner_id"]) + "_" + str(attach["photo"]["id"]))
            if len(ans) != 0:
                break

    return ans


def get_mlu():
    """return a random meme from public 'мои любимые юморески'"""

    res = app.vk_app.wall.get(owner_id=-mlu_group_id, offset=randint(0, 6000), count=1)

    return "wall" + str(-mlu_group_id) + "_" + str(res["items"][0]["id"])


def get_mnu():
    """return a random meme from public 'мои нейронные юморески'"""

    res = app.vk_app.wall.get(owner_id=-mnu_group_id, offset=randint(0, 6000), count=1)

    return "wall" + str(-mnu_group_id) + "_" + str(res["items"][0]["id"])


def get_haiku():
    """return a random meme from public 'мои нейронные юморески'"""

    res = app.vk_app.wall.get(owner_id=-haiku_group_id, offset=randint(0, 6000), count=1)

    return "wall" + str(-haiku_group_id) + "_" + str(res["items"][0]["id"])


def get_hyxpk():
    """return a random picture of @hyxpk"""

    res = app.vk_app.wall.search(owner_id=-anitype_group_id, query='hyxpk', offset=randint(0, 80))
    ans = []

    for item in res["items"]:
        if "attachments" in item:
            for attach in item["attachments"]:
                if attach["type"] == "photo":
                    ans.append("photo" + str(attach["photo"]["owner_id"]) + "_" + str(attach["photo"]["id"]))
            if len(ans) != 0:
                break

    return ans
