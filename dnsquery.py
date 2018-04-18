#!/usr/bin/python3

import dns.resolver
import argparse
import ipaddress
from sys import exit

# Setup parser
parser = argparse.ArgumentParser(description='Bulk DNS Resolver (PTR, A, and AAAA)')
parser.add_argument('--input', '-i', required=True, help='newline delimited file containing IP addresses or hostnames to query')
parser.add_argument('--type', '-t', required=True, choices=['A', 'AAAA', 'PTR'], help='type of query: PTR, A, or AAAA')
parser.add_argument('--primary', default='9.9.9.9', help='primary DNS server')
parser.add_argument('--secondary', default='8.8.8.8', help='secondary DNS server')

# Parse arguments and store to variables for later use
arguments = parser.parse_args()

inputFile = arguments.input
queryType = arguments.type
dnsServers = [arguments.primary, arguments.secondary]

# Setup DNS resolver
resolver = dns.resolver.Resolver(configure=False)
resolver.nameservers = dnsServers

# Open file for reading
try:
    queries = open(inputFile, 'r')
except FileNotFoundError:
    print('ERROR: Input file not found!')
    exit()
except Exception as error:
    print('An unknown error has occurred:\n {}'.format(error))
    exit()

# Print header
print('DNS Query Results')

# Process queries and print to screen
for line in queries:
    # Strip whitespace (especially newline characters and spaces)
    query = line.strip()
    try:
        if 'PTR' in queryType:
            # Validate that the IP address is valid and retrieve its reverse pointer
            try:
                ipAddress = ipaddress.ip_address(query)
                query = ipAddress.reverse_pointer
            except ValueError as error:
                print('\n{}\n {} is not a valid IPv4 or IPv6 address.'.format(query, query))
                continue
        
        # Query DNS
        answer = resolver.query(query, queryType)
        
        # Print headers (for PTR, print IP address instead of reverse pointer)
        if 'PTR' in queryType:
            print('\n{}'.format(ipAddress))
        else:
            print('\n{}'.format(query))
        
        # Print responses from DNS query
        for response in answer:
            print('  {}'.format(response))
    
    # If the domain does not exist or if there is no PTR record
    except dns.resolver.NXDOMAIN as error:
        print(query)
        if 'PTR' in queryType:
            print('  \'PTR\' record not found for {}'.format(query))
        elif 'AAAA' in queryType:
            print('  \'AAAA\' record not found for {}'.format(query))
        # Default case is for query type A
        else:
            print('  \'A\' record not found for {}'.format(query))
    
    # This will catch weird errors, like incorrectly formatted PTR requests, etc.
    except dns.resolver.NoAnswer as error:
        print(query)
        print('  {}'.format(error))
    
    # Catches all other exceptions and exits
    except Exception as error:
        print(query)
        print('  Unknown error has occurred while querying DNS: {}'.format(error))
        exit()
