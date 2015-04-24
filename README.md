# `malsub`

`malsub.py` is a Python 3.4.x script that submits a malware sample or a URL to multiple online services simultaneously via their RESTful APIs. It also allows to check the status of a specific analysis and pretty prints the results.

`malsub` was written while having in mind the needs of security analysts who submit many samples on a regular basis.

# Supported Services

Currently the following services are supported:
* [AVCaesar](https://avcaesar.malware.lu/);
* [maltracker](https://maltracker.net/);
* [Malwr](https://malwr.com/);
* [Metascan Online](https://www.metascan-online.com/); and
* [VirusTotal](https://www.virustotal.com/).

# Dependencies

malsub.py requires the following Python modules to be installed:
*  [`docopt`](https://github.com/docopt/docopt); and
*  [`requests`](http://docs.python-requests.org/)

Both can be be installed via `pip`. Check the documentation of each module for more information.

# Notes

`malsub` requires a `services.json` file in the same path of the script. The file contains metadata and API information of each service. It must be in JSON. For security reasons the provided file is only populated with [VirusTotal](https://www.virustotal.com/).

Each service requires a valid API key in order to make authenticated requests. A registered account is required by each company in order to get one and to get a view of their API.

Finally, it should be noted that `malsub` does not make use of every single API call that the services provide. Instead, it uses the basic calls to create a new analysis and to check upon an existing one.
