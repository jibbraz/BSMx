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

    for device in devices:
        try:
            print(" Connecting to Device: " + device)
            net_connect = ConnectHandler(
                ip=device, device_type=device_type, username=username, password=password)

            prompter = net_connect.find_prompt()
            if '>' in prompter:
                net_connect.enable()

            outputShIntDes = net_connect.send_command('show interface description')
            if answerCatID in outputShIntDes:
                output = net_connect.send_command('show interfaces description | include ' + answerCatID) 
                interface = output.split()[0]
                output = net_connect.send_command('show running-config interface ' + interface + '| include address' )

                if 'ip' and 'address' in output:
                    ipAddr = output.split()[2]
                    ipAddr,subnet = ipAddr.split('/')
                    octet1,octet2,octet3,octet4 = ipAddr.split('.')
                    if int(octet4) % 2 == 0:octet4 = int(octet4)+1
                    ipNextHop = octet1+'.'+octet2+'.'+octet3+'.'+str(octet4)
                    print(ipNextHop)
            # ssh to ip nexthop
            net_connect.disconnect()
            print(" Connecting to Device: "+ipNextHop)
            net_connect = ConnectHandler(
                ip=ipNextHop, device_type=device_type, username=username, password=password)
            test = net_connect.send_command('show interface description')

        except:
            print(colored('Please connect to vpn before run script', "red"))
            continue

if __name__ == '__main__':
    main()
