# dnsquery
**Bulk DNS Resolver**

## Overview 
This program processes a line-delimited file of IP addresses or domain names and will query 9.9.9.9 for the provided IP addresses and domain names. The program supports querying for A, AAAA, and PTR records.
* Note that 8.8.8.8 is used as a secondary DNS server, in case 9.9.9.9 is inaccessible.

## Dependencies
This program relies upon 1 outside library: *dnspython*. This can be installed by running ```pip3 install dnspython```. All other libraries are included as part of Python 3.

## Notes and Warnings

* This program requires Python 3 and does not work in Python 2.7.
* To output to file, pipe the output to file using the proper commands for your system.
* If conducting reverse DNS lookups (PTR records), do not provide the IP addresses in reverse pointer notation.
  * For example, to query for the domain name associated with 8.8.8.8, put ```8.8.8.8``` in the file. 
  * Do **not** put ```8.8.8.8.in-addr.arpa``` in the file! The program automatically converts IP addresses into reverse pointer notation.
