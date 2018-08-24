#!/usr/bin/env python3.6.5
import getpass
import os

import telebot
from telebot import types

import bot_configuration
import email_sender
import print_screen

bot = telebot.TeleBot(bot_configuration.TOKEN)


# Initial message
@bot.message_handler(commands=['start', 'action-menu'])
def bot_menu(message):
    markup = types.ReplyKeyboardMarkup()
    btn_action_menu = types.KeyboardButton('/action-menu')
    btn_help = types.KeyboardButton('/help')
    btn_screen_shot_funcs = types.KeyboardButton('/screen-shot-funcs')
    markup.row(btn_action_menu, btn_help)
    markup.row(btn_screen_shot_funcs)
    bot.send_message(message.chat.id, "Select action ", reply_markup=markup)


# Screen-shot related messages
@bot.message_handler(commands=['screen-shot-funcs'])
def screen_shot_functions(message):
    markup = types.ReplyKeyboardMarkup()
    btn_action_menu = types.KeyboardButton('/action-menu')
    btn_help = types.KeyboardButton('/help')
    btn_take_screen_shot = types.KeyboardButton('/take-screen-shot')
    btn_send_screen_shot = types.KeyboardButton('/send-screen-shot')
    markup.row(btn_action_menu, btn_help)
    markup.row(btn_take_screen_shot, btn_send_screen_shot)
    bot.send_message(message.chat.id, "Select action ", reply_markup=markup)


# Help
@bot.message_handler(commands=['help'])
def command_helper(message):
    commands = "/help   : Show's this message\n" \
               "/action-menu   : Show's original menu, where you can choose essential topics\n" \
               "/take-screen-shot   : Takes screen-shot of user's desktop\n" \
               "/send-screen-shot   : Gives option of sending screen-shot to email or as telegram message\n" \
               "/email-screen-shot   : Email screen-shot\n" \
               "/message-screen-shot   : Message screen-shot\n"
    bot.send_message(message.chat.id, commands)


# Take a screen-shot
@bot.message_handler(commands=['take-screen-shot'])
def take_screen_shot(message):
    screen = print_screen.take_print_screen()
    if screen == 1:
        bot.send_message(message.chat.id, "Screen-shot was taken")
    else:
        bot.send_message(message.chat.id, screen)


# Message or Email screen-shot
@bot.message_handler(commands=['send-screen-shot'])
def send_screen_shot(message):
    markup = types.ReplyKeyboardMarkup()
    btn_action_menu = types.KeyboardButton('/action-menu')
    btn_help = types.KeyboardButton('/help')
    btn_email_screen_shot = types.KeyboardButton('/email-screen-shot')
    btn_screen_shot_funcs = types.KeyboardButton('/message-screen-shot')
    markup.row(btn_action_menu, btn_help)
    markup.row(btn_email_screen_shot, btn_screen_shot_funcs)
    bot.send_message(message.chat.id, "(WARNING!) Messages sent through Telegram may be a bit distorted (WARNING!)")
    bot.send_message(message.chat.id, "Select action ", reply_markup=markup)


# Email screen-shot
@bot.message_handler(commands=['email-screen-shot'])
def email_screen_shot(message):
    email = email_sender.sending_screen_shot()
    if email == 1:
        bot.send_message(message.chat.id, "Email has been sent")
    else:
        bot.send_message(message.chat.id, email)


# Message screen-shot
@bot.message_handler(commands=['message-screen-shot'])
def message_screen_shot(message):
    filename = os.path.abspath(os.path.join('.', 'ExportData', 'screenshot.bmp'))
    user_name = getpass.getuser()
    caption = "Screen-shot from {}'s computer".format(user_name)
    photo = open(filename, 'rb')
    bot.send_photo(message.chat.id, photo, caption=caption)


bot.polling()
