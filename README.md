                       _           _
                      | |         | |
       _ __ ___   __ _| |___ _   _| |__     +--+
      | '_ ` _ \ / _` | / __| | | | '_ \   +--+|
      | | | | | | (_| | \__ \ |_| | |_) |  |  |+
      |_| |_| |_|\__,_|_|___/\__,_|_.__/   +--+

*malsub* is a Python 3.6.x framework that wraps several web services of **online malware and URL analysis sites** through their **RESTful Application Programming Interfaces (APIs)**. It supports submitting files or URLs for analysis, retrieving reports by hash values, domains, IPv4 addresses or URLs, downloading samples and other files, making generic searches and getting API quota values. The framework is designed in a modular way so that new services can be added with ease by following the provided **template module** and functions to make HTTP `GET` and `POST` requests and to pretty print results. This approach avoids having to write individual and specialized wrappers for each and every API by leveraging what they have in common in their calls and responses. The framework is also multi-threaded and dispatches service API functions across a thread pool for each input argument, meaning that it spawns a pool of threads per each file provided for submission or per each hash value provided for report retrieval, for example.

The following publicly available services are currently included in *malsub*:

* [AVCaesar](https://avcaesar.malware.lu/);
* [Have I been pwned?](https://haveibeenpwned.com/);
* [Hybrid Analysis](https://www.hybrid-analysis.com/);
* [MalShare](https://malshare.com/);
* [maltracker](https://maltracker.net/);
* [malwr](https://malwr.com/);
* [Metadefender](https://www.metadefender.com/);
* [OpenPhish](https://openphish.com/);
* [PDF Examiner](https://www.pdfexaminer.com/);
* [PhishTank](http://www.phishtank.com/);
* [QuickSand](https://www.quicksand.io/);
* [Safe Browsing](https://developers.google.com/safe-browsing/);
* [Threat Crowd](https://www.threatcrowd.org/);
* [ThreatStream](https://www.anomali.com/platform/threatstream);
* [URLVoid](http://www.urlvoid.com/);
* [VirusTotal](https://www.virustotal.com/);
* [VxStream](https://www.vxstream-sandbox.com/).

Most of these services require API keys that are generated after registering an account in their respective websites, which need to be specified in the `apikey.yaml` file according to the given structure. Note that some of the already bundled services are limited in supported operations due to the fact that they were developed with free API keys. API keys associated with paid subscriptions are allowed to make additional calls not open to the public and may not be restricted by a given quota. Yet, *malsub* can process multiple input arguments and pause between requests as a workaround for cooldown periods.

The main goal of *malsub* is to serve as a one-stop-shop for querying multiple online services of malware analysis and for aiding investigators. It is thus suitable for incident response, forensic and malware analysts, as well as for security practitioners alike.

# Dependencies and Usage

*malsub* requires a few modules that are specified in `requirements.txt`. The framework is structured into a package and sub packages. Its folder structure and some key files to be taken into consideration when using it or developing additional service modules are described as follows:

* `malsub/malsub.py`: application entry point;
* `malsub/data/`: miscellaneous data folder;
    * `apikey.yaml`: YAML data file of the API key and username pairs;
* `malsub/downl/`: downloads folder of files and samples;
* `malsub/malsub/`: *malsub* package;
* `malsub/malsub/common/`: modules that have a common use all throughout;
    * `out.py`: module with output displaying functions according to specific formats and log level (debug, verbose, informational or error);
    * `frmt.py`: module with pretty display functions like dictionary to JSON and tabular formats;
    * `rw.py`: module with read and write functions;
* `malsub/malsub/core/`: core modules of the application;
    * `web.py`: module responsible for handling HTTP requests;
* `malsub/malsub/service/`: services developed as modules parsed during runtime;
    * `base.py`: base template module for service construction.

The supported options are the following:

```
Usage: malsub [-h] [-a <service>] [-H] [-p <num>] [-R] [-v ...]
              [-d | -f | -q | -r | -s | -t]
              [-i | -o | -l | -u]
              [<input> ...]

Interact with online malware and phishing analysis services for malware samples, domain names, IP addresses or URLs.

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
```

# Examples

* Retrieve user quota for AVCaesar and Hybrid Analysis and be verbose:
```
$ python3 malsub.py -a avc,ha -q -v
```

* Submit an URL for analysis to VirusTotal and output verbose and debug messages:
```
$ python3 malsub.py -vva VirusTotal -su <url>
```

* Submit two files to maltracker, QuickSand and VirusTotal and pause 60 seconds between submissions:
```
$ python3 malsub.py -a mt,qs,virustotal -p 60 -s <file1> <file2>
```

* Retrieve reports for a file, for files under a recursive path and for a hash value:
```
$ python3 malsub.py -a VxStream,vt -rRv <file> <path> <hash>
```

* Retrieve analysis reports of a domain from all supporting services:
```
$ python3 malsub.py -or <domain>
```

* Retrieve analysis reports of a domain from all supporting services, but exclude ThreatCrowd and maltracker:
```
$ python3 malsub.py -a all,-ThreatCrowd,-mt -or <domain>
```

* Retrieve an analysis report from PDF Examiner of a PDF file identified by its hash value:
```
$ python3 malsub.py -a pe -r <hash>
```

* Download a malware sample from MalShare:
```
$ python3 malsub.py -a ms -d <hash>
```

# Service Modules

Modules of services are developed as subclasses of the `Service` class  in `malsub/service/base.py`. `Service` is an abstract class that lays out the attributes and functions that must be implemented by subclasses to ensure that service modules have all that is necessary for the main application. The full list of supported API functions is the following:

* `download_file`: download a file or a sample matching a given hash value;
* `report_file`: retrieve an analysis report for a file submission identified by its hash value;
* `submit_file`: submit a file for analysis;
* `report_app`: retrieve a report for a known application given a hash value;
* `report_dom`: retrieve a report for a domain name;
* `report_ip`: retrieve a report for an IPv4 address;
* `report_url`: retrieve a report for a URL;
* `submit_url`: submit a URL for analysis;
* `search`: perform searches of arbitrary terms;
* `quota`: query user quota data.

All the above listed API functions have specific signatures in respect to arguments that must be respected. The framework works with simple custom `File` and `Hash` classes to respectively represent files and hash values by defining a few file attributes like name and size and hash type. Some of the API functions receive such `File` and `Hash` objects as arguments, which must be accessed by their attributes in order to build request parameters.

For instance, the `report_file` function of the `VirusTotal` service module example below, here included for illustration, accesses the hash value through `hash.hash`. Moreover, the framework reads API key and username pairs from `apikey.yaml` and sets them to their respective services during initialization. These can be retrieved in the form of a dictionary with `self.get_apikey()`. Note that making HTTP requests requires only passing a well-defined `APISpec` object to the `request` function. APIs vary from service to service, particularly in the fields in which data is transmitted across, with some using HTTP query parameters, others the body of `POST` requests or even cookies. The `APISpec` class is prepared to handle all these variations that are diligently passed onto `requests` for HTTP communications.

```
from malsub.service.base import APISpec, Service
from malsub.core.crypto import Hash
from malsub.core.file import File
from malsub.core.web import request, openurl
from malsub.common import out, frmt

class VirusTotal(Service):
    # full name of the service
    name = "VirusTotal"
    # short name of the service
    sname = "vt"
    # length of the API key
    api_keyl = 64

    # API specification to download a file or a sample
    api_dowf = APISpec()
    # API specification to retrieve a file report
    api_repf = APISpec("POST", "https://www.virustotal.com", "/vtapi/v2/file/report")
    # ... (other API functions specifications)

    # '@Service.unsupported' marks a function as unsupported by a particular
    # service, being ignored by the main application
    @Service.unsupported
    def download_file(self, hash: Hash):
        # all base functions need to be explicitly declared even if not used by
        # a service
        pass

    def report_file(self, hash: Hash):
        # 'hash' is an object of 'Hash' with a hash value and its type (MD5,
        # SHA1, SHA-256 or SHA-512)
        # fill in the request fields
        # in this case, the 'data' corresponds to the HTTP POST body data
        # 'self.get_apikey()' returns the corresponding API key pair
        self.api_repf.data = {**self.get_apikey(), "resource": hash.hash}
        # make the request
        data, _ = request(self.api_repf)
        # format results as a JSON dictionary and "prune" the tree at depth one
        data = frmt.jsontree(data, depth=1)
        # data = frmt.jsonvert(data["scans"]) # tabular format
        # open a URL in the browser
        openurl(data["permalink"])
        # return the pretty-print formatted data ready for display
        return out.pformat(data)

    # ... (other API functions)
```

# Future Work

* Documentation;
* Refine error handling and data display of API responses, namely the summarization of multiple requests;
* Extend supported API functions;
* Implement additional API services as modules;
* Develop an interactive command-line interface;
* Integrate with other frameworks like [Cuckoo](http://www.cuckoosandbox.org/) and [Viper](https://github.com/viper-framework/viper).

# Change History

* *malsub* **20170607**: added Have I been pwned? and Anomali ThreatStream as intelligence services, and added service exclusion in `-a` with a dash precedence (*e.g.*, `-a all,-ha` excludes Hybrid Analysis).
* *malsub* **20170329**: added `-H` to output help information about services, fixed AVCaesar, modified URLVoid and made other improvements.
* *malsub* **20170319**: made generic improvements, added files as input for report retrieval, added a recurse option and added VxStream (private version of Hybrid Analysis) as a service module.
* *malsub* **20170305**: first major release.

# Acknowledgments

Thanks to Payload Security for kindly providing access to VxStream.
