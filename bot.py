import vk_api
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.upload import VkUpload
from vk_api.utils import get_random_id


class Bot:

    def __init__(self, token, group_id):
        """initialization bot"""

        self._token = token
        self.group_id = group_id
        self.vk_session_bot = vk_api.VkApi(token=token)
        self.long_poll = VkBotLongPoll(vk=self.vk_session_bot, group_id=group_id)
        self.vk_bot = self.vk_session_bot.get_api()
        self.upload = VkUpload(self.vk_bot)

        print('PhosphyBot is ready')

    def send_message(self, to_id, message='', attachment=None):
        """send a message to the specified id (to_id) and return the success of the operation"""

        try:
            self.vk_bot.messages.send(peer_id=to_id,
                                      message=message,
                                      attachment=attachment,
                                      random_id=get_random_id())
            return True
        except Exception as exc_m:
            print(exc_m)
            return False  # need to improve try-except

    def send_sticker(self, to_id, sticker_id):
        try:
            self.vk_bot.messages.send(peer_id=to_id,
                                      sticker_id=sticker_id,
                                      random_id=get_random_id())
            return True
        except Exception as exc_m:
            print(exc_m)
            return False  # need to improve try-except

    def get_members(self, peer_id):
        """return the list of information about all members of conversation"""

        try:
            return self.vk_bot.messages.getConversationMembers(peer_id=peer_id, group_id=self.group_id)['items']
        except Exception as exc_m:
            print(exc_m)  # need to improve try-except

        return list()

    def get_user_info(self, user_id):
        """return the list of usual information about user"""

        try:
            return self.vk_bot.users.get(user_ids=user_id)
        except Exception as exc_m:
            print(exc_m)  # need to improve try-except

        return list()

    def user_is_admin(self, user_id, peer_id, members=None):
        """check whether person is admin"""
        
        if peer_id == user_id:
            return True

        try:
            if members is None:
                members = self.get_members(peer_id)

            for member in members:
                if member['member_id'] == user_id:
                    if 'is_admin' in member:
                        return member['is_admin']
                    return False
        except Exception as exc_m:
            print(exc_m)  # need to improve try-except

        return False

    def user_is_owner(self, user_id, peer_id, members=None):
        """check whether person is admin"""
        
        if peer_id == user_id:
            return True

        try:
            if members is None:
                members = self.get_members(peer_id)

            for member in members:
                if member['member_id'] == user_id:
                    if 'is_owner' in member:
                        return member['is_owner']
                    return False
        except Exception as exc_m:
            print(exc_m)  # need to improve try-except

        return False

    def user_is_chat_member(self, user_id, peer_id, members=None):
        """check whether person is chat member"""

        try:
            if members is None:
                members = self.get_members(peer_id)

            for member in members:
                if member['member_id'] == user_id:
                    return True
        except Exception as exc_m:
            print(exc_m)  # need to improve try-except

        return False

    def remove_user(self, chat_id, user_id):
        """try to remove user from chat and return the success of the operation"""

        try:
            self.vk_bot.messages.removeChatUser(chat_id=chat_id,
                                                user_id=user_id)
            return True
        except Exception as exc_m:
            print(exc_m)  # need to improve try-except

        return False
