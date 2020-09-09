import fun
import random
import math_an
import word_filter as wf
from vk_api.bot_longpoll import VkBotEventType
from connection import bot, bot_inf, basic_commands


while True:
    try:  # need to improve try-except
        for event in bot.long_poll.listen():
            # print(event.type)  # ________________________
            # print(event.object.items())  # ________________________

            if event.type == VkBotEventType.MESSAGE_NEW:
                # print(event.object.items())  # ________________________

                processed_flag = False

                original_text = event.object['text']
                text = original_text.lower().replace('ё', 'е')
                from_id = event.object['from_id']  # who
                peer_id = event.object['peer_id']  # where from

                it_is_chat = from_id != peer_id
                chat_id = peer_id - 2000000000  # it is necessary if from_id != peer_id

                if text:
                    # processing the simplest messages

                    if not it_is_chat and text.find('привет') != -1:
                        processed_flag = bot.send_message(peer_id, 'Привет)\n' + bot_inf)
                    elif text == '-info':
                        processed_flag = bot.send_message(peer_id, bot_inf)

                    elif text == '-cat':
                        processed_flag = bot.send_message(peer_id, attachment=[fun.get_cat()])
                    elif text == '-dog':
                        # processed_flag = bot.send_message(peer_id, attachment=[fun.get_dog()])
                        processed_flag = True
                    elif text == '-panda':
                        # processed_flag = bot.send_message(peer_id, attachment=[fun.get_panda()])
                        processed_flag = True
                    elif text == '-frog':
                        # processed_flag = bot.send_message(peer_id, attachment=[fun.get_frog()])
                        processed_flag = True
                    elif text == '-anime':
                        # processed_flag = bot.send_message(peer_id, attachment=[fun.get_anime()])
                        processed_flag = True

                    elif text in basic_commands:
                        processed_flag = bot.send_message(peer_id, attachment=[basic_commands[text]])
                    elif text in math_an.inf_m:
                        processed_flag = bot.send_message(peer_id, attachment=[math_an.inf_m[text]])
                        print(math_an.inf_m[text])
                    elif text in fun.easter_eggs:
                        processed_flag = bot.send_message(peer_id, fun.easter_eggs[text])

                    elif text.find('тупой бот') != -1:
                        processed_flag = bot.send_message(peer_id, 'Ого! пашол нахуй')
                    elif text == 'нихуевый бот':
                        processed_flag = bot.send_message(peer_id, 'Еще бы')
                    elif text == 'прекрасный бот':
                        processed_flag = bot.send_sticker(peer_id, 4279)

                    if processed_flag:
                        continue

                    # предел и непрерывность функций одной переменной
                    for element in math_an.lim_con_fun_sing_var:
                        if text == element[0]:
                            processed_flag = bot.send_message(peer_id, attachment=[element[2]])
                            break

                    if processed_flag:
                        continue

                    # дифференцируемость функций одной переменной
                    for element in math_an.dif_fun_sing_var:
                        if text == element[0]:
                            processed_flag = bot.send_message(peer_id, attachment=[element[2]])
                            break

                    if processed_flag:
                        continue

                    members = bot.get_members(peer_id)
                    # print(members)  # ________________________

                    from_id_is_admin = bot.is_admin(from_id, peer_id, members)

                    # nerd of the day and warn_stat
                    if text == '-nerd' and it_is_chat:
                        code, nerd_id, nerd_name = fun.get_nerd(chat_id, members)

                        if code == 0:
                            continue
                        elif code == 1:
                            processed_flag = bot.send_message(peer_id, 'Согласно моей информации, '
                                                                       'сегодня ботан дня - {0}'.format(nerd_name))
                        else:
                            processed_flag = bot.send_message(peer_id,
                                                              random.choice(fun.nerd_ans).format(nerd_id, nerd_name))
                    elif text == '-nerd_stat' and it_is_chat:
                        nerds = fun.get_nerd_history(chat_id)

                        if not nerds:
                            processed_flag = bot.send_message(peer_id, 'Еще не было ни одного розыгрыша. '
                                                                       'Хотите попробовать?)')
                        else:
                            stat = 'Топ ботанов за всё время:\n'
                            for index, nerd in enumerate(nerds, 1):
                                stat += '\n{0}. {1} - {2} раз(а)'.format(index, nerd[0], nerd[1])
                            processed_flag = bot.send_message(peer_id, stat)

                    elif text == '-warn_stat' and it_is_chat:
                        warn_stat = wf.get_warn_stat(chat_id)

                        if not warn_stat:
                            processed_flag = bot.send_message(peer_id, 'Еще никто не получал '
                                                                       'предупреждений, так держать)')
                        else:
                            stat = 'Статистика предупреждений:\n'
                            for index, nerd in enumerate(warn_stat, 1):
                                stat += '\n{0}. {1} - {2} раз(а)'.format(index, nerd[0], nerd[1])
                            processed_flag = bot.send_message(peer_id, stat)

                    # checking for the use of obscene vocabulary
                    if it_is_chat:
                        word_filter = wf.word_filter(chat_id, from_id, from_id_is_admin, text)

                        if word_filter == 0:
                            bot.send_message(peer_id, random.choice(wf.answers))
                            bot.send_sticker(peer_id, random.choice(wf.sticker_answers))
                        elif word_filter == 1:
                            bot.send_message(peer_id, '❗[id{0}|Первое предупреждение]. '
                                                      'Не стоит в этом чате употреблять маты'.format(from_id))
                            bot.send_sticker(peer_id, random.choice(wf.sticker_answers))
                        elif word_filter == 2:
                            bot.send_message(peer_id, '❗[id{0}|Второе предупреждение]. Следующий раз станет последним.'
                                                      ' Не стоит в этом чате употреблять маты'.format(from_id))
                            bot.send_sticker(peer_id, random.choice(wf.sticker_answers))
                        elif word_filter == 3:
                            bot.remove_user(chat_id, from_id)
                            bot.send_message(peer_id, 'So sad')

                        if word_filter != -1:
                            continue

                    # commands for admins
                    if text == '-маты это круто' and from_id_is_admin:
                        wf.switch_filters(chat_id, 0)
                        processed_flag = bot.send_message(peer_id, 'Уровень дискуссий в Восточной '
                                                                   'Европе вновь упал')
                    elif text == '-маты это плохо' and from_id_is_admin:
                        wf.switch_filters(chat_id, 1)
                        processed_flag = bot.send_message(peer_id, 'Мудро')
                    elif text == '-маты это ужасно' and from_id_is_admin:
                        wf.switch_filters(chat_id, 2)
                        processed_flag = bot.send_message(peer_id, 'Радикальненько')

                    elif text[0:4] == '-all' and from_id_is_admin:

                        all_ = ''
                        pat = '[id{0}|#]'

                        for member in members:
                            if member['member_id'] > 0:
                                all_ += pat.format(member['member_id'])

                        processed_flag = bot.send_message(peer_id, all_ + '\n' + original_text[4:])

                    elif text[0:8] == '-members' and from_id_is_admin:

                        all_ = ''
                        pat = '[id{0}|#]'

                        for member in members:
                            if member['member_id'] > 0 and not bot.is_admin(member['member_id'], peer_id, members):
                                all_ += pat.format(member['member_id'])

                        processed_flag = bot.send_message(peer_id, all_ + '\n' + original_text[8:])

                    elif text[0:7] == '-admins' and from_id_is_admin:

                        all_ = ''
                        pat = '[id{0}|#]'

                        for member in members:
                            if member['member_id'] > 0 and bot.is_admin(member['member_id'], peer_id, members):
                                all_ += pat.format(member['member_id'])

                        processed_flag = bot.send_message(peer_id, all_ + '\n' + original_text[7:])

                    elif (text[:8] == '-кик [id' or text[:9] == '-warn [id') and it_is_chat:

                        if text[1] == 'к':
                            user_id = int(text[8:17])
                            command_id = 1
                        else:
                            user_id = int(text[9:18])
                            command_id = 2

                        if user_id == from_id:
                            processed_flag = bot.send_message(peer_id, 'Самобичевание не выход')
                        elif not from_id_is_admin:
                            processed_flag = bot.send_message(peer_id, 'Кажется, ты слишком слаб для этого\n'
                                                                       'Ешь с утреца побольше каши')
                        elif bot.is_owner(user_id, peer_id, members):
                            processed_flag = bot.send_message(peer_id, 'Попытка переворота?')
                        elif bot.is_admin(user_id, peer_id, members):
                            processed_flag = bot.send_message(peer_id, 'Умно-умно, но нет')
                        elif command_id == 1:
                            bot.remove_user(chat_id, user_id)
                            processed_flag = bot.send_message(peer_id, 'Хех')
                        else:
                            warning_count = fun.db.increase_warning_count(chat_id, user_id)

                            if warning_count == 1:
                                processed_flag = bot.send_message(peer_id, '❗[id{0}|Первое '
                                                                           'предупреждение]'.format(user_id))
                            elif warning_count == 2:
                                processed_flag = bot.send_message(peer_id, '❗[id{0}|Второе предупреждение]. Следующий '
                                                                           'раз станет последним.'.format(user_id))
                            else:
                                bot.remove_user(chat_id, user_id)
                                processed_flag = bot.send_message(peer_id, 'Хех')

                    if processed_flag:
                        continue

                    # processing the more complex context
                    if text.find('нефедов') != -1:
                        processed_flag = bot.send_message(peer_id, 'Неф лапочка ^_^')

                    if processed_flag:
                        continue

                # processing the attachments
                attachments = event.object['attachments']

                if attachments:
                    for attach in attachments:
                        attach_type = attach['type']

                        if attach_type == 'sticker':
                            sticker_id = attach['sticker']['sticker_id']

                            if sticker_id == 4275:
                                processed_flag = bot.send_message(peer_id, 'Приветик)')
                            elif sticker_id == 4280:
                                processed_flag = bot.send_message(peer_id, 'Mya')
                            elif sticker_id == 2823:
                                processed_flag = bot.send_message(peer_id, 'Волшебно))')
                            elif sticker_id == 14405:
                                processed_flag = bot.send_message(peer_id, 'Хуй в очо')
                            elif 14369 <= sticker_id <= 14408 or sticker_id == 4525:
                                processed_flag = bot.send_message(peer_id, 'Ужасный стикер. Не отправляй больше это')
                            elif 18560 <= sticker_id <= 18587 or sticker_id == 19650:
                                processed_flag = bot.send_message(peer_id, 'Прекрасный стикер)')

                if processed_flag:
                    continue

                # processing the actions
                if 'action' in event.object:
                    action = event.object['action']

                    if action['type'].find('chat_invite_user') != -1:
                        processed_flag = bot.send_message(peer_id, 'Привет)')
                    elif action['type'] == 'chat_kick_user':
                        processed_flag = bot.send_message(peer_id, 'Хех')

    except Exception as exc_c:
        print(exc_c)
