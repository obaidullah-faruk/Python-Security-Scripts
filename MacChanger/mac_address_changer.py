#!/usr/bin/env python3

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()

    parser.add_option("-i", "--interface", dest="interface", help="Interface to change it's mac address")
    parser.add_option("-m", "--mac", dest="mac_address", help="New mac address")

    (options, arguments) = parser.parse_args()
    
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
    elif not options.mac_address:
         parser.error("[-] Please specify an mac address, use --help for more info")
    return options

def change_mac_address(interface, mac_address):

    print(f"[+] Changing MAC address for Interface {interface} to {mac_address}") 

    # subprocess.call("sudo ifconfig " + interface + " down", shell=True) 
    # subprocess.call("sudo ifconfig " + interface +  " hw ether " + mac_address, shell=True)
    # subprocess.call("sudo ifconfig " + interface + " up", shell=True ) 

    subprocess.call(['sudo', 'ifconfig', interface, "down"])
    subprocess.call(['sudo', 'ifconfig', interface, "hw", "ether", mac_address])
    subprocess.call(['sudo', 'ifconfig', interface, "up"])

def get_interface_result(interface):
    modified_interface = subprocess.check_output(['sudo', 'ifconfig', interface]) 
    # print(f"{modified_interface}")
    return modified_interface

def get_current_mac_address(ifconfig_result):
    # print(type(ifconfig_result)) # Bytes Class
    mac_address_search_result = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', str(ifconfig_result))
    return mac_address_search_result

def check_mac_change(current_mac, input_mac):
    if current_mac == input_mac:
        print(f"Mac Address Change Successful. Current Mac address is:  {current_mac}")
    else:
        print(f"Mac Address Change Unsuccessful. Current Mac address is:  {current_mac}")
    
def read_mac_address(mac_address_search_result):
    if mac_address_search_result:
        current_mac = mac_address_search_result.group(0)
        check_mac_change(current_mac, options.mac_address)
    else:
        print(f"Could not read mac address")
     
options = get_arguments()
change_mac_address(options.interface, options.mac_address)
ifconfig_result = get_interface_result(options.interface)
mac_address_search_result = get_current_mac_address(ifconfig_result)
read_mac_address(mac_address_search_result)

# Run by : ./mac_address_changer.py -i wlp2s0 -m 10:22:44:55:66:77
# Run by : ./mac_address_changer.py --interface wlp2s0 --mac 10:22:44:55:66:77
