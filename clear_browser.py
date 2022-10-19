"""
 * @author Shadoworker5 Dev
 * @email shadoworker5.dev@gmail.com
 * @create date 2022-05-15 23:37:46
 * @modify date 2022-10-19 23:38:15
 * @desc [description]
"""
# from art import tprint
import os
import json
import base64
import win32crypt
from Crypto.Cipher import AES
from datetime import datetime, timedelta
import sqlite3

VERSION = '1.0.0'
menu_list = [
    'Brave history', 'Password save in Brave',
    'Chrome history','Password save in Chrome',
    'Microsoft Edge history', 'Password save in Microsoft Edge',
    'Clean history', 'Clean password',
    'Exit'
]

browser_list = ['Brave', 'Google Chrome', 'Microsoft Edge']

database_path = {
    'brave_history'     : f'{os.environ["USERPROFILE"]}/AppData/Local/BraveSoftware/Brave-Browser/User Data/Default/History',
    'brave_login'       : f'{os.environ["USERPROFILE"]}/AppData/Local/BraveSoftware/Brave-Browser/User Data/Default/Login Data',
    'chrome_history'    : f'{os.environ["USERPROFILE"]}/AppData/Local/Google/Chrome/User Data/Default/History',
    'chrome_login'      : f'{os.environ["USERPROFILE"]}/AppData/Local/Google/Chrome/User Data/Default/Login Data',
    'edge_history'      : f'{os.environ["USERPROFILE"]}/AppData/Local/Microsoft/Edge/User Data/Default/History',
    'edge_login'        : f'{os.environ["USERPROFILE"]}/AppData/Local/Microsoft/Edge/User Data/Default/Login Data'
}

local_state_path = {
    'brave'     : f'{os.environ["USERPROFILE"]}/AppData/Local/BraveSoftware/Brave-Browser/User Data/Local State',
    'chrome'    : f'{os.environ["USERPROFILE"]}/AppData/Local/Google/Chrome/User Data/Local State',
    'edge'      : f'{os.environ["USERPROFILE"]}/AppData/Local/Microsoft/Edge/User Data/Local State'
}

def choose_yes_no(msg):
    while True:
        try:
            choose = str(input(f"{msg} [y/n] default[n]: "))
            if choose.upper() == 'Y' or choose.upper() == 'N':
                break
            if len(choose) == 0:
                choose = 'n'
                break
        except ValueError:
            print("Please choose between Y or N")
            continue
    return choose.upper()

def save_in_file(message):
    response = choose_yes_no('\nDo you want to save your message?')

    if response == 'Y':
        file_name = str(datetime.timestamp(datetime.today())).split('.')[0]+'.txt'
        
        with open(file_name, 'w') as file:
            file.write(message)
        print('Message successfully\n')
    main()

def db_connection(database):
    return sqlite3.connect(database)

def kill_browser(browser):
    try:
        os.system(f"taskkill /im {browser}.exe /f")
    except Exception as e:
        return
        
def chrome_date_and_time(chrome_data):
    if chrome_data:
        return datetime(1601, 1, 1) + timedelta(microseconds=chrome_data)
    else:
        return 0

def get_encryption_key(browser):
    local_computer_directory_path = local_state_path[browser]
    with open(local_computer_directory_path, "r", encoding="utf-8") as f:
        local_state_data = f.read()
        local_state_data = json.loads(local_state_data)

    encryption_key = base64.b64decode(local_state_data["os_crypt"]["encrypted_key"])[5:]
    
    return win32crypt.CryptUnprotectData(encryption_key, None, None, None, 0)[1]

def decode_password(password, encryption_key):
    try:
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(encryption_key, AES.MODE_GCM, iv)
        uncipher_password = cipher.decrypt(password)[:-16].decode()
        if uncipher_password:
            return uncipher_password
        else:
            return "Undefined"
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            return "No Passwords"

def browser_history(browser):
    kill_browser(browser=browser)
    db_query    = db_connection(database_path[browser+'_history'])
    db_cursor   = db_query.cursor()
    history     = db_cursor.execute('SELECT id, title, url, visit_count, last_visit_time FROM urls').fetchall()
    print(f'+{"-"*100}+')
    print(f'{" ":<36} List of history ({len(history)})')
    print(f'+{"-"*100}+')

    for item in history:
        print(f' ID url             : {item[0]}')
        print(f' Title              : {item[1]}')
        print(f' Url                : {item[2]}')
        print(f' Visit count        : {item[3]}')
        print(f' Last time visit    : {chrome_date_and_time(item[4])}')
        print(f'+{"-"*100}+')
    print(f'{" ":<36} List of history ({len(history)})')
    print(f'+{"-"*100}+\n')
    main()

def browser_password(browser):
    db_query = db_connection(database_path[browser+'_login'])
    user_password = db_query.execute('SELECT id, origin_url, action_url, username_value, password_value, federation_url, date_created, times_used, date_last_used, date_password_modified FROM logins').fetchall()
    print(f'+{"-"*100}+')
    print(f' {" ":<35} List of user_password ({len(user_password)}) {" ":<35}')
    print(f'+{"-"*100}+')
    encryption_key = get_encryption_key(browser)
    
    for item in user_password:
        print(f'| ID url                    : {item[0]}')
        print(f'| Origin url                : {item[1]}')
        print(f'| Action url                : {item[2] if item[2] else "Undefined"}')
        print(f'| Username value            : {item[3] if item[3] else "Undefined"}')
        print(f'| Password value            : {decode_password(item[4], encryption_key)}')
        print(f'| Federation url            : {item[5] if item[5] else "Undefined"}')
        print(f'| Created at                : {chrome_date_and_time(item[6])}')
        print(f'| Time used                 : {item[7]}')
        print(f'| Date last time use        : {chrome_date_and_time(item[8])}')
        print(f'| Date password modified    : {chrome_date_and_time(item[9])}')
        print(f'|{"-"*100}|')
    print(f' {" ":<35} List of user_password ({len(user_password)}) {" ":<35}')
    print(f'+{"-"*100}+\n')
    main()

def clear_browser(browser, table):
    db_query = db_connection(database_path[browser+'_'+table])
    db_cursor = db_query.cursor()
    if table == 'login':
        table = 'logins'
    else:
        table = 'urls'
    query = f'DELETE FROM {table}'
    db_cursor.execute(query)
    db_query.commit()
    db_query.close()
    print(f"Data has been deleted successfully from table {table}")
    main()
    
def get_input(msg, format):
    while True:
        try:
            response = format(input(msg))
            if isinstance(response, format):
                break
            else:
                print('Error. Please try again')
        except ValueError:
            print(f'Ooops!!! you must enter data of {format} type')
    return response

def choose_browser(table_name):
    print('\nChoose your browser')
    for i, value in enumerate(browser_list):
        print(f'[{str(i+1)}] {value}')
    while True:
        item = get_input('#> ', int)
        if item in range(1, len(browser_list) + 1):
            break
        else:
            print(f'Vous devez choisir entre 1 et {len(browser_list)}')
            
    if item == 1:
        clear_browser('brave', table_name)
    elif item == 2:
        clear_browser('chrome', table_name)
    elif item == 3:
        clear_browser('edge', table_name)

def choose_menu(list_menu):
    while True:
        item = get_input('#> ', int)
        if item in range(1, len(list_menu) + 1):
            break
        else:
            print(f'Vous devez choisir entre 1 et {len(list_menu)}')
    
    os.system('cls')
    if item == 1:
        browser_history('brave')
    elif item == 2:
        browser_password('brave')
    elif item == 3:
        browser_history('chrome')
    elif item == 4:
        browser_password('chrome')
    elif item == 5:
        browser_history('edge')
    elif item == 6:
        browser_password('edge')
    elif item == 7:
        choose_browser('history')
    elif item == 8:
        choose_browser('login')
    else:
        print('Bye... See you later')
        exit(0)

def main():
    for i, value in enumerate(menu_list):
        print(f'[{str(i+1)}] {value}')
    choose_menu(menu_list)

if __name__ == '__main__':
    banner = r"""
      ____  _      _____     _     _   _ 
     / ___|| |    | ____|   / \   | \ | |
    | |    | |    |  _|    / _ \  |  \| |
    | |___ | |___ | |___  / ___ \ | |\  |
     \____||_____||_____|/_/   \_\|_| \_|
    """
    if os.name == 'nt':
        try:
            print(banner)
            main()
        except Exception as e:
            print(f'Error: {e}')
            exit(0)
        except KeyboardInterrupt as e:
            print(f'User interruption............')
            exit(0)
    else:
        print(f'This version ({VERSION}) is only available for Windows platform')
        exit(0)