# PissPoorPool, or p2pool for short

We routinely audit PHP applications which deal with finance, money and digital currencies because nobody likes having their money stolen because of some poorly written web application exposed them to the internet nasties.

Todays winner is [p2pool-node-status](https://github.com/johndoe75/p2pool-node-status), a GUI for the `p2pool` Bitcoin mining pool software.

This also highlights the futility of trying to make PHP applications secure, in many cases trying to fix bugs with software written in PHP will come back to bite you in the arse even if you think you're done it right.

See the following commit: https://github.com/johndoe75/p2pool-node-status/commit/5f9ea51e1647d63c77c691ce8bdd2c6ccc873c28

```
There are two major security holes in the default jsonp.php file.  An attacker
could easily fetch any file off the local server by simply passing in a filename
into $_GET['report'] variable.  Second, an attacker could essentially send out
and receive web requests on behalf of your server, since theres no validating
of the hostname.  I've added the ability to whitelist a hostname in case anyone
wants to lock their script down.
```

As usual the culprit is a JSONP proxy handler (before the 'fix'):

```php
$report = $_GET['report']; $host= $_GET['host'];
$json = file_get_contents($host . $report);
echo sprintf('%s(%s);', $_GET['callback'], $json);
```

After the fix the script still allows you to control the full URL, with a validation check disabled by default which would've prevented this whole escapade. The validation after the fix is as follows:

 * `$web_url = $_GET['host'] . $_GET['report']`
 * `if (file_exists($web_url)) ... die()`
 * `if (!filter_var($web_url, FILTER_VALIDATE_URL)) ... die`
 * `file_get_contents($web_url)`

Now, let me see... what magic can PHP do that passes these two checks, oh yea:

 * `?host=php://filter/resource=file:///etc/passwd&report=`

Pwned....

## Recommendations

 1. Change `$force_host = false;` to `$force_host = true;`

