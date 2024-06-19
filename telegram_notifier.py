import traceback
from datetime import datetime

import requests




class TelegramNotifier:
    """
    Посылает сообщения пользователям телеграма
    """

    def __init__(self, is_activated: bool, bot_token: str, log_file_path: str):
        self._is_activated = is_activated
        self._base_url = f'https://api.telegram.org/bot{bot_token}/'
        self._log_file_path = log_file_path
        self._chat_id_dict = dict()

    def load_clients(self, client_dict: dict):
        if self._is_activated is not True:
            return
        for k, v in client_dict.items():
            self._chat_id_dict[k] = v

    def log(self, *args, **kwargs):
        if self._is_activated is not True:
            return
        text = '\t'.join(list(args))
        with open(self._log_file_path, 'a') as f:
            f.write(f'{datetime.now()}\t{text}')

    def send_message_to(self, client: str, message: str) -> dict:
        if self._is_activated is not True:
            return {}
        result = {}
        try:
            resp = requests.get(f'{self._base_url}sendMessage', params={
                'chat_id': self._chat_id_dict[client],
                'text': message
            })
            resp.raise_for_status()
            result = resp.json()
        except:
            self.log(traceback.format_exc() + "\n")
        finally:
            return result

    def _send_photo(self, client, files) -> dict:
        if self._is_activated is not True:
            return {}
        result = {}
        try:
            resp = requests.post(f'{self._base_url}sendPhoto', params={
                'chat_id': self._chat_id_dict[client]
            }, files=files)
            resp.raise_for_status()
            result = resp.json()
        except:
            self.log(traceback.format_exc() + "\n")
        finally:
            return result

    def send_image_to(self, client: str, image_path: str) -> dict:
        if self._is_activated is not True:
            return {}
        return {client: self._send_photo(client, {'photo': open(image_path, 'rb')})}

    def send_message_to_all(self, message: str):
        if self._is_activated is not True:
            return
        for client in self._chat_id_dict:
            self.send_message_to(client, message)

    def send_image_to_all(self, image_path: str) -> dict:
        if self._is_activated is not True:
            return {}
        image_binary = open(image_path, 'rb')
        result = dict()
        for client in self._chat_id_dict:
            result[client] = (self.send_image_binary_to(client, image_binary))
        return result

    def send_image_binary_to_all(self, binary_data):
        if self._is_activated is not True:
            return
        for client in self._chat_id_dict:
            self.send_image_binary_to(client, binary_data)

    def send_image_binary_to(self, client, binary_data) -> dict:
        if self._is_activated is not True:
            return {}
        return self._send_photo(client, {'photo': binary_data})


if __name__ == '__main__':
    from tnconf import bot_token, telegram_clients, is_activated
    telegram_notifier = TelegramNotifier(is_activated, bot_token, 'telegram_notifier_log.txt')
    telegram_notifier.load_clients(telegram_clients)
    ans = telegram_notifier.send_message_to('GAV', 'content 1')
    # telegram_notifier.send_message_to_all('content 2')
    # telegram_notifier.send_image_to_all('test_img.png')
    # telegram_notifier.send_image_binary_to_all(open('test_img.png', 'rb'))
    # ans = telegram_notifier.send_image_to_all('test_imgf.png')
    # ans = telegram_notifier.send_image_to('GAV','test_img.png')
    # ans = telegram_notifier.send_image_to_all('test_img.png')
    print(ans)

