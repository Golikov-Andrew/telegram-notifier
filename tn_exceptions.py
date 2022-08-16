class TelegramNotifierException(Exception):
    def __init__(self, telegram_notifier, msg):
        super().__init__(msg)

