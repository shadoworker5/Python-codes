"""
 * @author Kassoum TRAORE
 * @email shadoworker5.dev@gmail.com
 * @create date 2021-10-05 16:24:01
 * @modify date 2022-05-17 00:46:18
 * @desc [description]
"""

""" You must use this script by example 127.0.0.1 10000 1 """
from datetime import datetime
import socket
import threading
import sys
from csv import reader

result = list()

def load_port_list(port, i):
    with open('port_name_list.csv', 'r') as file:
        csv_reader = reader(file)
        for row in csv_reader:
            if row[1] == port:
                if row[row[1].index(port) + i] == '':
                    return 'Unknow service'
                return row[row[1].index(port) + i]

def scan(ip, port, port_dict, delay):
    sp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(delay)
    
    try:
        sp.connect((ip, port))
        port_dict[port] = "open"
        sp.close()
    except:
        port_dict[port] = "close"
    
    result.append(port_dict)

def async_call(address_ip, ports, delay):
    port_dict = dict()
    count_open_port = 0
    time_start = datetime.timestamp(datetime.today())

    for port in range(ports):
        t = threading.Thread(target=scan, args=(address_ip, port, port_dict, delay))
        result.append(t)

    print("Loading............\n")

    for port in range(ports):
        result[port].start()

    for port in range(ports):
        result[port].join()
    print(f"+{'-'*105}+")
    print(f'| Port {" "*5} | Type of protocol {" "*10}| Service {" "*42} | Status {" ":<2}|')
    print(f"+{'-'*105}+")
    for i in range(ports):
        if port_dict[i] == "open":
            print(f'| {str(i):<10} | {load_port_list(str(i), 2):<26} | {load_port_list(str(i), 3):<50} | {port_dict[i]:<8} |')
            count_open_port += 1
            print(f"+{'-'*105}+")
    end_start = datetime.timestamp(datetime.today())
    print("\nScan time: {} seconds".format(str(end_start - time_start)[:5]))
    print("Scan result: {} are open and {} are close or filter".format(str(count_open_port), str(len(port_dict) - count_open_port)))
        
def main(address_ip, port, delay):
    """ This is main function we launch at begining of all """
    async_call(address_ip, port, delay)
    
if __name__ == '__main__':
    if len(sys.argv) == 4:
        try:
            main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
        except KeyboardInterrupt:
            print("Keyboard Interruption.\nBye")
            exit()
    else:
        print("Syntax error. Use for example 127.0.0.1 10000 1\n127.0.0.1: target IP\n10000: 10000 first port number\n1: delay of send request")
        exit()