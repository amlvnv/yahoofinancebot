# -*- coding: utf-8 -*-

from enum import Enum

token = "912369144:AAGFubh8zUNljIpZzF4hTcnKW1ZUo-SHiew"
db_file = "database.vdb"


class States(Enum):
    """
    Мы используем БД Vedis, в которой хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)
    """
    S_START = "0"  # Начало нового диалога
    S_ENTER_TICKER = "1"
    S_ENTER_STARTDATE = "2"
    S_ENTER_ENDDATE = "3"
    S_FINISH = "4"
    S_ONE_MORE_TICKER = "5"