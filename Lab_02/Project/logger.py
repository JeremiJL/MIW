import os
from enum import Enum
from logging import DEBUG, INFO

debugEnabled = os.getenv("DEBUG", "false").lower() == "true"

class LogLevel(Enum):
    INFO = 0
    DEBUG = 1

def log(message: str, level: LogLevel = DEBUG):
    if level == LogLevel.INFO or debugEnabled:
        print(message)
