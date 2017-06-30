# Remote Root Exploit for WePresent WiPG 1000, 1500, 2000 Devices.
This is a trivial remote root exploit that targets the WePresent WiPG 1000, 1500, and 2000 devices. It implements the command injection vulnerability (preauth) mentioned in [this advisory](https://www.redguard.ch/advisories/wepresent-wipg1000.txt) to get a root shell on the device using the built in netcat executable present.

## Usage
Just run the exploit with the URL of the device, your connectback host, and your connectback port.

You can get a TTY by doing the following:

First, run `stty -echo raw; nc -l -v -p 6666 ; stty sane` to start a listener.  
Next, when you get a shell, it won't work properly. So type in "script /dev/null" and hit CTRL+J.  
Next, type "reset" and you SHOULD have a TTY.  
If all else fails just use the shitty netcat shell to stage a better payload that does deliver a TTY.

## Screenshots of Use/Example Use
Here we have a screenshot of it working.  
![lol](https://raw.githubusercontent.com/XiphosResearch/exploits/master/wipgpwn/sanitizedexploit.png)

## Licence
Licenced under the [WTFPL][wtfpl]

[wtfpl]: http://www.wtfpl.net/
