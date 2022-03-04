#!/usr/bin/python
from netmiko import ConnectHandler
from termcolor import colored

def read_txt(path='devices.txt'):
    with open(path) as file:
        txt_content = file.read()
    return txt_content

def main():
    devices = read_txt().strip().splitlines()
    device_type = 'cisco_ios'
    username = 'admin'
    password = 'P@ssw0rd'

    #find CATID
    answerCatID = input('What is CATID would you like to find : ')
    
    try:
        for device in devices:
            print(" Connecting to Device: " + device)
            net_connect = ConnectHandler(
                ip=device, device_type=device_type, username=username, password=password)

            prompter = net_connect.find_prompt()
            if '>' in prompter:
                net_connect.enable()

            outputShIntDes = net_connect.send_command('show interface description')

            if answerCatID in outputShIntDes:
                output = net_connect.send_command('show interfaces description | include ' + answerCatID) 
                int = output.split()[0]
                output = net_connect.send_command('show running-config interface ' + int)
                print(output)

                if 'ip' and 'address' in output:
                    print('yes')

    except:
        print(colored('Please connect to vpn before run script', "red"))
        pass

if __name__ == '__main__':
    main()
