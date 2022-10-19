"""
 * @author Kassoum TRAORE
 * @email shadoworker5.dev@gmail.com
 * @create date 2022-06-20 23:33:52
 * @modify date 2022-07-26 00:14:42
 * @version: 1.0.0
 * @desc This version is for window device
"""
import subprocess
import re as regex
import socket
import sys
from datetime import datetime
import threading

hosts = []
result = list()
response_name = list()

def get_user_name(ip, dict_name):
    try:
        name, other, host_ip = socket.gethostbyaddr(ip)
        dict_name[ip] = name
        response_name.append(dict_name)
    except:
        dict_name[ip] = "Not found"
        response_name.append(dict_name)

def async_get_name() ->dict:
    dict_name = dict()
    
    for ip in hosts:
        thread_ip = threading.Thread(target=get_user_name, args=(ip, dict_name))
        response_name.append(thread_ip)
    
    for ip in range(len(hosts)):
        response_name[ip].start()
    
    for ip in range(len(hosts)):
        response_name[ip].join()
    
    return dict_name

def ping_request(host, dict_ip):
    command = subprocess.Popen("ping "+ host +" -n 2", shell=True, stdout=subprocess.PIPE, text=True)
    response, erreur = command.communicate()
    if regex.search(" Impossible de joindre l'h“te de destination.", response) == None:
        dict_ip[host] = "open"
        result.append(dict_ip)

def async_ping(host, start_ip, end_ip):
    dict_ip = dict()
    split_host = host.split('.')
    host = split_host[0]+'.'+split_host[1]+'.'+split_host[2]+'.'

    for ip in range(start_ip, end_ip + 1):
        target = host+str(ip)
        t = threading.Thread(target=ping_request, args=(target, dict_ip))
        result.append(t)

    print(f"Loading{'.'*20}\n")
    
    for ip in range(len(result)):
        result[ip].start()

    for ip in dict_ip:
        hosts.append(ip)

def main(address_ip, start_ip, end_ip):
    """ This is main function we launch at begining of all """
    time_start = datetime.timestamp(datetime.today())
    async_ping(address_ip, start_ip, end_ip)
    ip_user_name = async_get_name()

    print(f"+{'-'*60}+")
    print(f'| IP {" "*15} | Host name {" ":<28}|')
    print(f"+{'-'*60}+")
    
    for i in ip_user_name:
        print(f'| {i:<18} | {ip_user_name[i]:<37} |')
        print(f"+{'-'*60}+")
    
    end_start = datetime.timestamp(datetime.today())
    print("\nScan time: {} seconds".format(str(end_start - time_start)[:5]))
    print(f"Host found: {str(len(ip_user_name))}")

if __name__ == '__main__':
    if len(sys.argv) == 4:
        try:
            main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
        except KeyboardInterrupt:
            print("Keyboard Interruption.\nBye")
            exit()
    else:
        print("Error. You must use this script by example 127.0.0.1 1 255")
        exit()