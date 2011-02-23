# sshort - a simple ssh connection helper

A little helper script which comes handy when you're dealing with lots
of ssh connections to many different servers on daily basis. 

So instead of typing:
    ssh firstname.lastname@somehost.someserver.someisp.com
    
You can type (for example):
    sshort.py panda

Basically, sshort is a wrapper around ssh binary which makes executing 
ssh connections a bit easier and faster.

## Basic usage

Creating a new sshort connection:
    ./sshort.py -s name -t user@host.com
    
Executing a connection:
    ./sshort.py name
    
Creating a connection with optional ssh arguments:
    ./sshort.py -s name -t user@host.com -p "-p 1234"

Which is an equivalent of:
    ssh -p 1234 user@host.com
    
Removing sshort connection:
    ./sshort.py -r name
    
Listing all stored connections:
    ./sshort -l
    
## Storage engine

Connections are stored in $HOME/.sshort file by default in following,
pipe-separated format:
    name|user@host.com|optional_ssh_args
    
## Disclaimer

This script seems dead simple but is really my very first, usable Python
program which I wrote having >5 years of PHP experience. In fact, I wrote
sshort with PHP first and have been using on my local machine for ages,
so I thought porting it to Python would be nice learning excercise. :)

Lots of PHP influence in first code commits is more than expected. 
Comments and improvement suggestions are more than welcome. Thanks!

Dawid Lorenz, dawid-at-lorenz-dot-co 