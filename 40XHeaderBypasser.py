#!/usr/bin/env python3
import requests
import sys
import re
import random
import time

requests.packages.urllib3.disable_warnings()

def extract_url(line):
    url_regex = r'(https?://\S+)'
    match = re.search(url_regex, line)
    if match:
        return match.group(1)
    else:
        return None

def test_url(url, method):
    x_headers = [
        'X-Originating-IP',
        'X-Forwarded-For',
        'X-Remote-IP',
        'X-Remote-Addr',
        'X-Client-IP',
        'X-Host',
        'X-Forwared-Host',
        'X-Original-URL',
        'X-Rewrite-URL'    
    ]

    results = []

    
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    accept_header = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'

    for x in x_headers:
        header = {
             'Accept'           : accept_header,
             'Cache-Control'    : 'no-cache',
             'User-Agent'       : user_agent,
             'Connection'       : 'close',
             x : url
        }

        try:
            res = requests.get('{}://{}'.format(method, url), headers=header, timeout=3, verify=False)
            results.append({'header': x, 'status_code': res.status_code, 'response_size': len(res.text)})
           
            time.sleep(random.uniform(1, 3))
        except requests.exceptions.RequestException as e:
            results.append({'header': x, 'status_code': 'Error', 'response_size': 0})

    return results

def main():
    if len(sys.argv) != 2:
        print('[!] Usage: python3 check.py <file_with_urls>')
        sys.exit(1)

    urls_file = sys.argv[1]

    with open(urls_file, 'r') as f:
        lines = f.read().splitlines()

    for line in lines:
        url = extract_url(line)
        if not url:
            print(f'[!] Invalid URL format: {line}')
            continue

        if url.startswith('http://'):
            method = 'http'
            url = url[len('http://'):]
        elif url.startswith('https://'):
            method = 'https'
            url = url[len('https://'):]
        else:
            print(f'[!] Invalid URL format: {url}')
            continue

        results = test_url(url, method)

        print(f'URL: {method}://{url}')
        for result in results:
            print(f'[-] {result["status_code"]} | {result["header"]}\t| response-size: {result["response_size"]}')
        print()

if __name__ == "__main__":
    main()
