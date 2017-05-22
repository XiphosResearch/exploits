## FreeACS Pwn

This is the FreeACS exploit I disclosed during BSides Edinburgh.

Note, it is a horrible, disgusting, PoC. Not really "weaponized" or proper.

### Vulnerability Details  
FreeACS uses the "username" part of the HTTP Basic Authentication sent by a TR-069 client to the /tr069/ endpoint as part of the identifier for the CPE device that is connecting. It also completely fails to sanitize this user input. So by sending a CWMP NOTIFY message to the /tr069/ endpoint on the server, with an XSS payload in the username portion of the Basic Auth header, your XSS payload will end up inside the admin area, and fire when an admin logs in and looks at the registered devices.

We can then use a simple JS hook to add a new administrative user, granting us control over the ACS server.
