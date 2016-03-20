## unsanitary - ASAN/Setuid Root Local Root Exploit

Exploits unsanitized env var passing in ASAN which leads to file clobbering as root when executing setuid root binaries compiled with ASAN.

Uses an overwrite of /etc/ld.so.preload to get root on a vulnerable system. Supply your own target binary to use for exploitation.

Implements the bug found here: http://seclists.org/oss-sec/2016/q1/363

## Video of Exploitation   

[![Demo](http://img.youtube.com/vi/jhSIm3auQMk/0.jpg)](http://www.youtube.com/watch?v=jhSIm3auQMk "unsanitary")
