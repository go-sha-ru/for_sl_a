import logging
import re
from logging import config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'default_formatter': {
            'format': '[%(levelname)s:%(asctime)s] %(message)s'
        },
    },

    'handlers': {
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter',
        },
        'file_handler': {
            'class': 'logging.FileHandler',
            'formatter': 'default_formatter',
            'level': 'INFO',
            'mode': 'w',
            'filename': 'sport_log.log',
        }
    },

    'loggers': {
        'sport_log': {
            'handlers': ['file_handler'],
            'propagate': False,
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['file_handler']
    },
}

logging.config.dictConfig(LOGGING_CONFIG)


class Message:
    EXAMPLE_MESSAGE = "0003 C1 01:13:02.877 00[CR]"
    MESSAGE_FORMAT = "BBBBxNNxHH:MM:SS.zhqxGGCR"
    MESSAGE_FORMAT_RE = "(\d{4})\s(..)\s(\d{2}:\d{2}:\d{2})\.(\d{3})\s(\d{2})(\[CR])"
    raw_message = ''
    MESSAGE = "спортсмен, нагрудный номер {number} прошёл отсечку {cutoff} в «{time}»"

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Message, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self._logger = logging.getLogger('file_handler')

    def __call__(self, message, *args, **kwargs):
        self.raw_message = message.decode("utf-8")
        if self.raw_message != "Hello" or self.raw_message != b'\r\n':
            check = self._check_message()
            if check is None or False:
                return 'Error message'
            return check

    def __str__(self):
        return "Сборщик сообщений"

    def _check_message(self):
        check = re.match(Message.MESSAGE_FORMAT_RE, self.raw_message)
        if check is not None:
            time = check.group(3) + '.' + check.group(4)[:-1]
            message = self.MESSAGE.format(number=check.group(1), cutoff=check.group(2), time=time)
            self.log(check.group(), message)
            if check.group(5) == '00':
                return message
            return 'All Ok'

    def log(self, raw_message, full_message):
        self._logger.info(raw_message)
        self._logger.info(full_message)
