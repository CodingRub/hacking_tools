import subprocess, optparse, re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option('-i', '--interface', dest="interface", help="Interface to change its MAC address")
    parser.add_option('-m', '--mac', dest="new_mac", help="New MAC address")
    (options, args) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
    elif not options.new_mac:
        parser.error("[-] Please specify a new mac, use --help for more info")
    return options

def change_mac(interface, new_mac):
    print(f"[+] Changing MAC address for {interface} to {new_mac}")
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    res = ""
    ifconfig_res = subprocess.check_output(["ifconfig", interface])
    mac_search_res = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_res))
    if mac_search_res:
        res = mac_search_res.group(0)
    else:
        print("[-] Could not read MAC address.")
    return res

options = get_arguments()
current_mac = get_current_mac(options.interface)
print(f"Current MAC = {current_mac}")
change_mac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print(f"[+] MAC address was successfully changed to {current_mac}")
else:
    print(f"[-] MAC address didn't changed.")