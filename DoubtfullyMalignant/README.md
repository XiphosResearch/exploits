# DoubtfullyMalignant - BenignCertain DoS PoC

This is a denial of service exploit that targets the NSA/TAO "BenignCertain" exploitation tool, the capabilities which are explained quite well over at [Mustafa Al-Bassam's blog post on the topic][musalbas].

I know, I know, "No More DoS PoC's", however, upon having a more skilled at reverse engineering colleague at Xiphos examine the binary in IDA, it was determined that this bug is probably not exploitable to gain RCE.
Either that or we just don't know how to do it ;)
Anyway, I drop this PoC here for you, so you, too, can crash silly NSA toys. 
And maybe one of you clever folks can figure out what we missed to gain RCE?

Anyhow, how this all works is. You set it up listening on a port.  
When bc-id is ran against it, it responds with the crashing data.

### For BenignCertain v1100:
BenignCertain v1100 has the parser built into the bc-id tool. If the -p, -c, -u or -P flag is set, which tells it to do parsing, it will crash on receiving the reply. It will also crash if told to read in such a file and analyse it.

### For BenignCertain v1110:
This will NOT crash bc-id, however, bc-id will write the data out to a file (serversipaddress.raw and serversipaddress.hex). This is due to the parsing code being split off to bc-parser.  
HOWEVER, when the parser (bc-parser) is ran on the created file, it will segfault because it is a hilariously badly coded piece of shit.

Hello to all fellow scientists of the glorious [Rum Research Institute ;)][rummery]

~ infodox // [@info_dox][twatter]

## Screenshot
### Exploiting v1100 (best screenshot)
![cheney](https://raw.githubusercontent.com/XiphosResearch/exploits/master/DoubtfullyMalignant/Malignant.png)

### Exploiting v1110
![blamblam](https://raw.githubusercontent.com/XiphosResearch/exploits/master/DoubtfullyMalignant/DoubtfullyMalignant.png)

## Licence
Licenced under the [WTFPL][wtfpl]

[musalbas]: https://musalbas.com/2016/08/18/equation-group-benigncertain.html
[wtfpl]: http://www.wtfpl.net/
[rummery]: https://rum.supply/
[twatter]: https://twitter.com/info_dox
