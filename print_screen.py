import pyautogui
import os


def take_print_screen():
    try:
        full_path = os.path.abspath(os.path.join('.', 'ExportData'))
        pic_path = os.path.abspath(os.path.join('.', 'ExportData', 'screenshot.bmp'))
        if not os.path.exists(full_path) or not os.path.isdir(full_path):
            os.mkdir(full_path)
        pic = pyautogui.screenshot()
        pic.save(pic_path)
        return 1
    except Exception as ex:
        return "Unknown error occurred. Details: {}".format(ex)
