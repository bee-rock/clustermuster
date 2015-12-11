# clustermuster

## Description

A simple command line cluster manager which harnesses ssh to queue commands for a list of nodes.

## Installation

If you already have [Python](http://www.python.org/) and [pip](http://www.pip-installer.org/) 
on your system you can install the library simply by running:

     pip install ./downloads/clustermuster-0.1.tar.gz
     
## Quick start

clustermuster can be started via commandline which takes a configuration file detailing the 
addresses and ports of yournodes along with a port for which clustermuster will listen for
commands on:

	clustermuster -i example/nodes.yaml -p 9999
	
It is currently configured to print all debug information to the console, which you will see
as soon as it is started.
	
For each node in your list, you will need to use ssh keys to authenticate. You will need to
generate keys without passphrases in order to prevent clustermuster from stalling.

	ssh-keygen
	ssh-copy-id username@nodeaddress
	
See examples/nodes.yaml for a sample configuration. Now your client can send commands over port 9999
to the server in a json format which can specify a specific node or any node available. 
See example/client_example.py to see the schema.
     
## Development

You can also setup an environment for experimenting and development

1. Install virtualenv if you haven't already

	virtualenv venv
	source venv/bin/activate
	
2. Setup for development

	python setup.py develop

3. Run tests

	python setup.py test

## Reporting Issues/Feature requests

I created this package out of curiosity and to demonstrate a robust solution to an 
interesting problem using Python. It's a fairly basic package and I don't have much 
intention of adding a lot more functionality since there are other open source and 
commericial applications which have a large amount of development already. 

However, should you find this package useful, your poking turns something up
,or if you have suggestions, bugs or other issues specific to this library, file
them [here](https://github.com/bee-rock/clustermuster/issues) or contact me
at [brock@idevelopcode.com](mailto:brock@idevelopcode.com).
