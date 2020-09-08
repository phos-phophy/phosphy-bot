import vk_api


class App:

    def __init__(self, client_id, client_secret, token):
        """initialization app"""

        self._client_id = client_id
        self._client_secret = client_secret
        self._token = token
        self.vk_session_app = vk_api.VkApi(token=token)
        self.vk_app = self.vk_session_app.get_api()

        print('PhosphyApp is ready')
