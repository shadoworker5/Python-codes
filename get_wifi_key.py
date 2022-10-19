"""
 * @author Kassoum TRAORE
 * @email shadoworker5.dev@gmail.com
 * @create date 2022-06-20 23:34:48
 * @modify date 2022-06-20 23:34:49
 * @desc [description]
"""
import subprocess
import re
from datetime import datetime
from art import tprint

# This function is use to get all profile
def get_profile():
    """ We use subprocess to send ping request to get all profile in this computer """
    return subprocess.check_output(["netsh", "wlan", "show", "profiles"], text=True)

# This function is use to convert all profile data in list
def convert_data(data):
    """ We use regex to parse data in list who contain only all profile name """
    convert_data = (re.findall("Profil Tous les utilisateurs    ÿ: .*", data))
    get_profile_list = [i.split(":")[1][1::] for i in convert_data if "Profil Tous les utilisateurs    ÿ" in i]
    return get_profile_list

def get_all_profile_key(profiles):
    """ We use this function to get all profile key and return that in list containt dict {ssid: name, passwor: key} """
    wifi_list = list()
    if len(profiles) != 0:
        for profile in profiles:
            wifi_profile = dict()
            
            try:
                result = subprocess.check_output(["netsh", "wlan", "show", "profiles", profile], text=True)
            except:
                continue

            if re.search("Cl‚ de s‚curit‚ÿÿÿÿÿÿÿÿ: Absent", result):
                continue
            else:
                wifi_profile["ssid"] = profile
                result_password = subprocess.check_output(["netsh", "wlan", "show", "profiles", profile, "key=clear"], text=True)
                password = re.search("Contenu de la cl‚            : .*", result_password)
                if password == None:
                    wifi_profile["password"] = None
                else:
                    wifi_profile["password"] = password[0].split(":")[1][1::]
                wifi_list.append(wifi_profile)

    return wifi_list

def print_result(data):
    if data:
        print('*'*70)
        print(f'# SSID {" "*30} || Password {"":<19}#')
        print('*'*70)
        for key in data:
            print(f'# {key["ssid"]:<35} || {key["password"]:<27} #')
            print('*'*70)
    else:
        print(f'Key not found')

def main():
    time_start = datetime.timestamp(datetime.today())
    convert_profile_list = convert_data(get_profile())
    profile_key = get_all_profile_key(convert_profile_list)
    print_result(profile_key)
    end_start = datetime.timestamp(datetime.today())
    print("Scan time: {} seconds".format(str(end_start - time_start).split(".")[0]))

if __name__ == '__main__':
    tprint('Shadoworker5')
    try:
        main()
    except:
        print("Keyboard interuption")
        exit()