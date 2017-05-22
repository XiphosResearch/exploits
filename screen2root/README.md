# screen2root

## TL;DR
On systems where screen is version 4.5.0 (Screen version 4.05.00 (GNU) 10-Dec-16), and setuid root, you can use it to create arbritary files with root permissions containing arbritary content.

This PoC creates an /etc/ld.so.preload file pointing to a library that creates a setuid root shell and then calls screen again to trigger it.

TL;DR you get root.

Original bug report is [here](https://lists.gnu.org/archive/html/screen-devel/2017-01/msg00025.html)

## Screenshot
[![lol](https://raw.githubusercontent.com/XiphosResearch/exploits/master/screen2root/screen2root.png)]

## Reproducing:
Install [this version](https://ftp.gnu.org/gnu/screen/screen-4.5.0.tar.gz) of screen.

Howto:
```
wget https://ftp.gnu.org/gnu/screen/screen-4.5.0.tar.gz
tar -xf screen-4.5.0.tar.gz
cd screen-4.5.0
./configure
make
sudo make install
```
Now you have an exploitable version.

## Notes
According to [this poster on reddit](https://www.reddit.com/r/netsec/comments/5pz0bs/gnu_screen_root_exploit/dcw86ur/) you can even use this on boxes with [grsec](https://grsecurity.net) with trivial modifications. I have yet to experiment with evading Samhain, but I suspect it is not going to be hard.
