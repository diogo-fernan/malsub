#!/usr/bin/env python3

"""Usage: malsub [-h] [-a <service>] (-d | -f | -q | -r | -s | -t) [-i | -o | -l | -u] [-p <seconds>] [-v ...] [<input> ...]

Interact with online malware and phishing analysis services for malware samples, domain names, IP addresses or URLs.

Options:
  -h, --help  show this help message and exit

  -a, --analysis <service>  character-separated list of services (class or short names) [default: all]
  -p, --pause <seconds>     wait an interval between service requests (rate limit) [default: 0]
  -v, --verbose             display verbose and debug messages

API functions:
  -d, --download  download files or malware samples
  -f, --find      search for arbitrary terms (input format irrelevant)
  -q, --quota     retrieve API user quota
  -r, --report    retrieve submission reports for domains, hash values, IP addresses or URLs
  -s, --submit    submit malware samples or URLs for analysis
  -t, --test      test API calls by calling each service function as defined with some default values

Input formats (hash values or files are given as default depending on options):
  -i, --ipaddr  input are IPv4 addresses (applies to '-r' only)
  -o, --domain  input are domain names (applies to '-r' only)
  -l, --appl    input are hash values for application lookups (applies to '-r' only)
  -u, --url     input are URLs (applies to '-r' and '-s' only)

Supported hash values: MD5, SHA1, SHA-256 and SHA-512.

Copyright (c) 2017 Diogo Fernandes
https://github.com/diogo-fern/malsub
"""

from docopt import docopt

from malsub.core import main

exit(main.run(docopt(__doc__)))


# notes
# pyflakes, pylint, pychecker, and pep8
# CONTRIBUTING.md

# read file or files from pipe? stdin
# find malware_samples/ -exec cat {} \; | malsub

# -r, --recurse  recurse a directory

# interactive console
# history of commands and output
# cache stuff
# submit a sample
# get report minutes later just by issuing "check"

# pip3.6 freeze > requirements.txt
