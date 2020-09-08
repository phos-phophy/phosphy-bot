from bor import Bor
from connection import db, bot


# word filter
obscene_1 = Bor()
obscene_2 = Bor()

answers = ['Маты это плохо', 'Не матерись', 'Перестань', 'По губам получишь', 'Ну хватит', 'Прекрати сейчас же',
           'Как некрасиво']
sticker_answers = [2826, 2832, 2833, 2834, 4284, 4292, 4293, 4296]

with open('text_files/obscene_1', 'r') as f:
    for line in f:
        obscene_1.add_word(line.rstrip())

with open('text_files/obscene_2', 'r') as f:
    for line in f:
        obscene_2.add_word(line.rstrip())


def switch_filters(chat_id, filter_state):
    """switch the word filter states
    0 - word filter does not work
    1 - word filter only check for using obscene words
    2 - word filter check for using obscene words and save count of using"""

    if db.get_chat_info(chat_id) is None:
        db.add_chat_info(chat_id, filter_state)
        db.create_chat_members_table(chat_id)
    else:
        db.update_filter_state(chat_id, filter_state)


def get_warn_stat(chat_id):
    """return the list of names with warn_counts """

    ans = list()
    members = db.get_all_chat_members(chat_id)

    for member in members:
        member_id = member[0]
        warn_count = member[1]

        if member_id > 0 and warn_count > 0:
            user_info = bot.get_user_info(member_id)
            ans.append((user_info[0]['last_name'] + ' ' + user_info[0]['first_name'], warn_count))

    ans.sort(key=lambda x: x[1], reverse=True)
    return ans


def word_filter(chat_id, from_id, from_id_is_admin, text):
    """find obscene words in the text
    return -1 - there are not obscene words
    return 0 - user has used obscene word (without saving warning in the database)
    return 1 - user has used obscene word and he has 1 warning
    return 2 - user has used obscene word and he has 2 warnings
    return 3 - user has used obscene word and he has 3 warnings (update user`s warning_count to 0)"""

    chat_info = db.get_chat_info(chat_id)
    filter_ = 0

    if len(chat_info) == 0:
        db.add_chat_info(chat_id)
        db.create_chat_members_table(chat_id)
    elif chat_info[0][1] == 0:
        return -1
    else:
        filter_ = chat_info[0][1]

    words = text.split()
    obscene_flag = -1

    if obscene_1.check_word(text):
        obscene_flag = 0
    else:
        for word in words:
            if obscene_2.check_for_equality(word):
                obscene_flag = 0
                break

    if filter_ == 1 or obscene_flag == -1 or from_id_is_admin:
        return obscene_flag

    # at this moment it is clear that user is not admin, he has used obscene word and chat rules forbid using ow

    return db.increase_warning_count(chat_id, from_id)
