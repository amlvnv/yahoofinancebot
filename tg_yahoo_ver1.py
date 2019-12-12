import telebot
import yahoofinance as yf
import pandas as pd
import csv
import xlsxwriter
import datetime
from telebot import types
import config
import dbworker

bot = telebot.TeleBot("912369144:AAGFubh8zUNljIpZzF4hTcnKW1ZUo-SHiew") # импорт токена

markup = types.ReplyKeyboardRemove()



today = datetime.datetime.today().strftime("%d-%m-%Y-%H-%M")  # текущая дата и время для названия отчета отчета


def data_download():  # функция создания DataFrame с нужными акциями
    stocks = yf.HistoricalPrices(ticker, start_date, end_date)
    csv_exported = stocks.to_csv('data.csv')
    global df_imported
    df_imported = pd.read_csv('data.csv')
    return df_imported


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,'Бот выгружает с Yahoo Finance цены акций нужных вам компаний. На данный момент в один xlsx-файл можно выгрузить только один тикер. Обращаем внимание, что тикеры ММВБ необходимо писать с  ".ME"  на конце.  /download', reply_markup=markup)


@bot.message_handler(commands=['download'])
def one_more_time(message):
    bot.send_message(message.chat.id,"Введи необходимый тикер (должен соотвествовать тикерам Yahoo Finance, напр. YNDX.ME)")
    dbworker.set_state(message.chat.id, config.States.S_ENTER_TICKER.value)

@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_TICKER.value)
def user_entetring_ticker(message):
    global ticker
    ticker = message.text
    bot.send_message(message.chat.id, "Введи начальную дату в формате YYYY-MM-DD")
    dbworker.set_state(message.chat.id, config.States.S_ENTER_STARTDATE.value)


@bot.message_handler(
    func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_STARTDATE.value)
def user_entering_startdate(message):
    global start_date
    start_date = message.text
    bot.send_message(message.chat.id, "Введи конечную дату в формате YYYY-MM-DD")
    dbworker.set_state(message.chat.id, config.States.S_ENTER_ENDDATE.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_ENDDATE.value)
def user_entering_enddate(message):
    global end_date
    end_date = message.text
    writer = pd.ExcelWriter(ticker+ '-' + today + '.xlsx', engine='xlsxwriter')  # создание Excel файла
    data_download()
    df_imported.to_excel(writer, sheet_name=ticker)  # создание вкладки с котировками
    writer.save()
    report = open(ticker+ '-' + today + '.xlsx', 'rb')
    bot.send_document(message.chat.id, report)
    bot.send_message(message.chat.id, 'Скачать еще - /download')
    dbworker.set_state(message.chat.id, config.States.S_FINISH.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_FINISH.value)
def finish(message):
    bot.send_message(message.chat.id, 'Скачать еще - /download')



bot.polling(none_stop=True)


