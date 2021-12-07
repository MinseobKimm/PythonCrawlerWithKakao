#http://lalo.esran.com/
import os
import pyautogui
import pyperclip
import platform
import subprocess
import pandas as pd
import numpy as np
import requests
import json
url = 'http://ip-api.com/json'
data = requests.get(url)
res = data.json()

url = 'https://dapi.kakao.com/v2/local/search/keyword.json'

#params = {'query' : '편의점', 'x' : res['lon'], 'y' :  res['lat'], 'radius' : 1000, 'category_group_code' : 'CS2'}
params = {'query' : '편의점', 'x' : 127.03751, 'y' :  36.01376, 'radius' : 10000, 'category_group_code' : 'CS2'}

headers = {"Authorization": "KakaoAK f8a9a5215692348e6ad7a6ae987234c2"}
total = requests.get(url, params=params, headers=headers).json()['documents']



def initialize():
    print(pyautogui.size())
    pyautogui.PAUSE = 0.1
    python_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(python_path)


# XXX: KakaoTalk path is set only to default install path
def get_kakao_cmd():
    user_os = platform.system()
    kakao_path = ['C:\Program Files (x86)\Kakao\KakaoTalk\KakaoTalk.exe']
    if user_os == 'Darwin':
        kakao_path = ['open', '-a', 'KakaoTalk']
    return kakao_path


def run_kakao():
    kakao_path = get_kakao_cmd()
    print(f'Run KakaoTalk : {kakao_path}')
    try:
        subprocess.run(kakao_path)
    except Exception:
        print('[ERROR] Execute Kakaotalk')
        raise


def enter_chatroom(chat_idx):
    chat_imgs = ['chat.png', 'chat_with_msg.png']
    for chat_png in chat_imgs:
        try:
            click_img(chat_png)
        except TypeError:
            print(f'Not match with image: {chat_png}')
            pass
        except Exception:
            print(f'[ERROR] Click image: {chat_png}')

    # Focus on 1st chatroom
    pyautogui.hotkey(*home_key)
    print(*home_key)
    print(f"Enter the {chat_idx}th chatroom")
    for _ in range(1, chat_idx):
        pyautogui.press('down')
    pyautogui.press('enter')


# TODO: Return response to sending msg (Need Cursor check)
def send_msg(msg):
    pyperclip.copy(msg)
    pyautogui.hotkey(cmd_key, 'v')
    pyautogui.press('enter')


def click_img(png_name):
    img_path = os.path.join('img', png_name)
    location = pyautogui.locateCenterOnScreen(img_path, confidence=0.7)
    x, y = location
    if is_retina:
        x = x / 2
        y = y / 2
    pyautogui.moveTo(x, y)
    pyautogui.click()

def bubble_sort(total):
    for i in range(len(total)):
        for j in range(i,len(total)-1):
            if total[j]['distance'] > total[j+1]['distance']:
                total[j], total[j+1] = total[j+1], total[j]
    return total

def talk_check():
    initialize()
    """Set chatroom index and message below
        Example like this
        chatroom_idx = 1
        my_msg = 'test'
    """
    chatroom_idx = 1
    my_msg=''
    bubble_sort(total)

    for i in range(0,len(total)-1):
        my_msg+=total[i]['place_name']+'\n'
        my_msg +='거리 :'+total[i]['distance'] +'m\n'
        n='주소 : ' + 'https://map.kakao.com/link/map/'+total[i]['id']+'\n\n'
        my_msg +=n


    try:
        run_kakao()
        enter_chatroom(chatroom_idx)
        send_msg(my_msg)
        return True
    except Exception as e:
        print(f'Error: {e}')
        return False


# Config changed by OS
cmd_key = 'ctrl'
home_key = ('home', '')
is_retina = False

if platform.system() == "Darwin":
    is_retina = subprocess.call("system_profiler SPDisplaysDataType | grep 'retina'", shell=True)
    cmd_key = 'command'
    home_key = ('option', 'up')

if __name__ == "__main__":

    talk_result = talk_check()
    if talk_result:
        exit(0)
    else:
        exit(1)
