#!/usr/bin/env python3

"""
Usage: malsub [-h] [-a <service>] [-H] [-p <num>] [-R] [-v ...]
              [-d | -f | -q | -r | -s | -t]
              [-i | -o | -l | -u]
              [<input> ...]

Interact with online malware, URL and intelligence analysis services for malware
samples, domain names, IP addresses or URLs.

Options:
  -h, --help  show this help message and exit

  -a, --analysis <service>  character-separated list of services (class or short names) [default: all]
  -H, --servhelp     show help messages about selected services and exit
  -p, --pause <num>  wait an interval in seconds between service requests (rate limit) [default: 0]
  -R, --recursive    recurse on input paths
  -v, --verbose      display verbose and debug messages

API functions:
  -d, --download  download files or malware samples
  -f, --find      search for arbitrary terms (input format irrelevant)
  -q, --quota     retrieve API user quota
  -r, --report    retrieve submission reports for domains, files, hash values, IP addresses or URLs
  -s, --submit    submit malware samples or URLs for analysis
  -t, --test      test API calls by calling each service function as defined with some default values

Input formats (hash values or files are given as default depending on options):
  -i, --ipaddr  input are IPv4 addresses (applies to '-r' only)
  -o, --domain  input are domain names (applies to '-r' only)
  -l, --appl    input are hash values for application lookups (applies to '-r' only)
  -u, --url     input are URLs (applies to '-r' and '-s' only)

Supported hash values: MD5, SHA1, SHA-256 and SHA-512.

Examples:
  - Retrieve user quota for Hybrid Analysis and be verbose:
$ python3 malsub.py -a ha -q -v

  - Submit an URL for analysis to VirusTotal and output verbose and debug
    messages:
$ python3 malsub.py -vva VirusTotal -su <url>

  - Submit two files to maltracker and VirusTotal and pause 60
    seconds between submissions:
$ python3 malsub.py -a mt,virustotal -p 60 -s <file1> <file2>

  - Retrieve reports for a file, for files under a recursive path and for a hash
    value:
$ python3 malsub.py -a VxStream,vt -rRv <file> <path> <hash>

  - Retrieve analysis reports of a domain from all supporting services:
$ python3 malsub.py -or <domain>

  - Retrieve analysis reports of a domain from all supporting services, but
    exclude ThreatCrowd and maltracker:
$ python3 malsub.py -a all,-ThreatCrowd,-mt -or <domain>

  - Retrieve an analysis report from PDF Examiner of a PDF file identified by
    its hash value:
$ python3 malsub.py -a pe -r <hash>

  - Download a malware sample from MalShare:
$ python3 malsub.py -a ms -d <hash>

Copyright (c) 2017 Diogo Fernandes
https://github.com/diogo-fern/malsub
"""

from docopt import docopt, printable_usage

from malsub.core import main

if __name__ == "__main__":
    exit(main.run(docopt(__doc__), printable_usage(__doc__)))


# https://malwareconfig.com/api/
# http://www.cryptam.com/
# https://github.com/mwtracker/cryptam_tools


# notes
# pyflakes, pylint, pychecker, and pep8
# CONTRIBUTING.md

# -b
# open URLs in the browser

# make groups
# -g mal
# -g intel
# -g url
# relative/full path for data/ and downl/

# password-protected samples
# compression

# read file or files from pipe? stdin
# find malware_samples/ -exec cat {} \; | malsub

# interactive console
# history of commands and output
# cache stuff
# submit a sample
# get report minutes later just by issuing "check"

# pip3.6 freeze > requirements.txt
