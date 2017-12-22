# bbsearch

## Overview

Simple script for fun after reading [Troy Hunt's article on bug hunting and vulnerability reporting](https://www.troyhunt.com/fixing-data-breaches-part-3-the-ease-of-disclosure/). The script checks for `security.txt` files present in root directories of websites as defined by [Ed Foudil's IETF draft spec](https://tools.ietf.org/html/draft-foudil-securitytxt-01). Many websites incorporate this file or a redirect at this address to a bug bounty or vulnerability reporting resource.

The script loads domain names from a local text file (default `domains.txt`), one site per line.

## Usage

`$ python bbsearch.py`
