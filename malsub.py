#!/usr/bin/env python3

"""Usage: malsub [-h] (-s | -c) <services> (bin|url) <INPUT>

Query a malware analysis service for an analysis or a report.

Options and commands:
  -h, --help  Show this help message and exit.
  -s, --submit  Submit a malware sample or URL.
  -c, --check  Check an analysis of a specific service.
  <services>  Service(s) delimited by a comma. [default: all]

Required: services.txt in JSON
"""

from sys import exit
from docopt import docopt, printable_usage
from urllib.parse import quote_plus
from requests import post, get
from json import load as json_load
from itertools import chain
from collections import OrderedDict

AVCAESAR = "avcaesar"
MALTRACKER = "maltracker"
MALWR = "malwr"
METASCAN = "metascan"
VT = "vt"
ALL = "all"

SERV = []
SERVf = [ALL, AVCAESAR, MALTRACKER, MALWR, METASCAN, VT]
SERVi = []

SUBMIT, CHECK = "submit", "check"
OPT = None
BIN, URL = "bin", "url"
MODE = None
POST, GET = "POST", "GET"

ARG = None

def raise_sysExit (*args):
	if len(args) == 1:
		raise SystemExit ('[!] %s' % args[0])
	elif len(args) == 2:
		raise SystemExit ('[!] %s: %s: %s' % args[0], type(args[1]), args[1])
	else:
		raise SystemExit ('[!] %s' % str(args))

class Service (object):
	def __init__ (self, d):
		self.name = d['name']
		self.url = dict()
		self.url[BIN] = d['urlb']
		self.url[URL] = d['urlu']
		self.key = d['key']
		self.id = d['id']
		self.api = dict()
		self.api[BIN] = dict()
		self.api[URL] = dict()
		self.method = dict()
		self.method[BIN] = dict()
		self.method[URL] = dict()

		self.api[BIN][SUBMIT] = d['apib'][0].split()[1]		
		self.api[BIN][CHECK] = d['apib'][1].split()[1]		
		self.method[BIN][SUBMIT] = d['apib'][0].split()[0]
		self.method[BIN][CHECK] = d['apib'][1].split()[0]

		if d['apiu'] is not None:
			self.api[URL][SUBMIT] = d['apiu'][0].split()[1]
			self.api[URL][CHECK] = d['apiu'][1].split()[1]
			self.method[URL][SUBMIT] = d['apiu'][0].split()[0]
			self.method[URL][CHECK] = d['apiu'][1].split()[0]
		else:
			self.api[URL][SUBMIT] = self.api[URL][CHECK] = None
			self.method[URL][SUBMIT] = self.method[URL][CHECK] = None

	def __repr__ (self):
		return ("<Service %s: %s %s, %s %s, %s %s>" % 
				(self.name, self.url[BIN], self.url[URL],
				self.method[BIN], self.api[BIN], 
				self.method[URL], self.api[URL]))
	def __str__ (self):
		return ('Service %s:\n urlb:\t%s\n urlu:\t%s\n' + 
				' apib:\t%s %s\n apiu:\t%s %s\n' % 
				(self.name, self.url[BIN], self.url[URL], 
				self.method[BIN], self.api[BIN], 
				self.method[URL], self.api[URL]))

def read ():
	try: 
		d = json_load (open ('services.txt'))
	except IOError as e:
		raise_sysExit ('I/O ERROR: services.txt', e)
	vec = []
	fields = ['name', 'urlb', 'urlu', 'apib', 'apiu', 'key', 'id']
	for k, v in d.items():
		if (ALL in SERVi or v['name'] in SERVi) and v['name'] in SERVf:
			if sorted(list(v.keys())) == sorted(fields):
				vec.append(Service (v))
			else:
				print (k, list(v.keys()), fields)
				raise_sysExit ('JSON ERROR: %s with incorrect fields' % k)
		else:
			print ('[!] WARNING: not using %s' % v["name"])
	if len(vec) == 0:
		raise_sysExit ('no services defined or selected')
	return vec

def api_data (s):
	data = {s.key[0]: s.key[1]}
	api = s.url[MODE] + s.api[MODE][OPT]

	if OPT == CHECK:
		if s.name == METASCAN:
			if MODE == BIN:
				api += ARG
			else: # encode URL
				api += quote_plus(ARG, '')
		else:
			if s.name == AVCAESAR or s.name == MALTRACKER:
				api += ARG
			else: # s.name == MALWR or s.name == VT:
				data[s.id] = ARG
	else: # submit
		if s.name == METASCAN and MODE == URL: # encode URL
			api += quote_plus(ARG, '')
		if MODE == URL and (s.name == MALTRACKER or s.name == VT):
			data['url'] = ARG
	return api, data

def request (s, api, files, data):
	r = None
	method = s.method[MODE][OPT]
	headers = {'Accept': '*/*', 'User-Agent': ''}
	if s.name == METASCAN:
		headers = dict(chain(headers.items(), data.items()))
	print ('(%s): HTTP %s:' % (api, method), end="")
	try:
		if method == POST:
			r = post (api, files=files, data=data, headers=headers)
		elif method == GET:
			r = get (api, data=data, headers=headers)
		else:
			print ('[!] WARNING: invalid HTTP request: %s' % method)
			raise Exception
	except Exception as e:
		print (' %s ERROR: failed for %s: %s: %s' % method, s.name, type(e), e)
		return None, None
	print (' %d\n' % r.status_code)
	return r, method

def print_response (s, r):
	if r == None:
		return
	d = r.text
	try:
		d = r.json()
		msg = ''

		if s.name == MALWR:
			msg += '\tstatus:\t%s\n' % d['status']
			if OPT == SUBMIT:
				msg += '\t  uuid:\t%s\n\tsha256:\t%s\n' % d['uuid'], d['sha256']
		elif s.name == VT:
			msg += ('\t   msg:\t%s\n\t plink:\t%s\n' %
				(d['verbose_msg'], d['permalink']))
			if MODE == BIN:
				msg += ('\t   md5:\t%s\n\t  sha1:\t%s\n\tsha256:\t%s\n' % 
					(d['md5'], d['sha1'], d['sha256']))
			else:
				msg += '\t   url:\t%s\n' % d['url']
			if OPT == CHECK:
				msg += ('\t sdate:\t%s\n\t ratio:\t%d/%d\n' % 
					(d['scan_date'], d['positives'], d['total']))
				if d['positives'] > 0:
					od = OrderedDict (sorted(d['scans'].items()))
					msg += '\t scans:\n'
					for k, v in od.items():
						if v['detected']:
							msg += ('\t\t{:>20}: {:<45} {} v{}\n'.format(
								k, v['result'], v['update'], v['version']))
		elif s.name == METASCAN:
			if MODE == BIN:
				msg += '\t  uuid:\t%s\n' % d['data_id']
				if OPT == CHECK:
					msg += '\t  name:\t%s\n' % d['file_info']['display_name']
					msg += '\t   md5:\t%s\n' % d['file_info']['md5'].lower()
					msg += '\t  sha1:\t%s\n' % d['file_info']['sha1'].lower()
					msg += '\tsha256:\t%s\n' % d['file_info']['sha256'].lower()
					msg += '\tresult:\t%s\n' % d['scan_results']['scan_all_result_a']
					od = dict()
					for k, v in d['scan_results']['scan_details'].items():
						if v['threat_found'] != '':
							od[k] = v
					if len(od) > 0:
						msg += '\t scans:\n'
						od = OrderedDict(sorted(od.items()))
						for k, v in od.items():
							msg += ('\t\t{:>20}: {:<45} {}\n'.format(
								k, v['threat_found'], v['def_time']))
			else:
				msg += '\t    ip:\t%s\n\t   geo:\n' % d['address']
				for k, v in d['geo_info'].items():
					msg += '\t\t{:>20}: {:<45}\n'.format(k, v)
				msg += ('\t sdate:\t%s\n\t ratio:\t%d\n\t scans:\n' % 
					(d['start_time'], d['detected_by']))
				od = dict()
				for i in d['scan_results']:
					od[i['source']] = dict(i['results'][0])
				od = OrderedDict (sorted(od.items()))
				for k, v in od.items():
					msg += ('\t\t{:>30}: {:<10} {} {} {}\n'.format(
						k, v['assessment'], v['result'], 
						v['detecttime'], v['alternativeid']))
		print (msg)
	except ValueError:
		print ('\t   msg:\t%s' % d)

def main ():
	args = docopt (__doc__)

	global SERV, SERVi
	global OPT, MODE, ARG

	SERVi = args['<services>'].split(',')
	ARG = args['<INPUT>']

	if len(SERVi) == 0 or (args['--check'] and len(SERVi) > 1):
		raise SystemExit (printable_usage(__doc__).strip())

	# opt
	if args['--submit']:
		OPT = SUBMIT
	else:
		OPT = CHECK
	# mode
	if args[BIN]:
		MODE = BIN
	else:
		MODE = URL

	# read services.txt
	SERV = read ()
	SERV = [s for s in SERV if s.api[MODE][OPT] is not None]

	files = data = {}

	if OPT == SUBMIT and MODE == BIN:
		try: 
			ARG = open (args['<INPUT>'], "rb")
		except Exception as e:
			raise_sysExit ('I/O ERROR: %s' % args['<INPUT>'], e)
		files = {'file': (ARG.name, ARG)}

	for s in SERV:
		print ('\n %s ' % s.name, end='')
		# api and data
		api, data = api_data (s)
		# request
		r, method = request (s, api, files, data)
		# pretty print
		print_response (s, r)
		print ('\n done!')


if __name__ == "__main__":
	exit(main ())
else:
	print ("malsub.py should not be imported to other module(s)")
