#!/usr/bin/env python3
import requests
import sys
import re

# Disable insecure request warnings
requests.packages.urllib3.disable_warnings()

def extract_url(line):
    # Use regex to find a valid URL
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
    ]

    results = []

    for x in x_headers:
        header = {
             'Accept'           : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
             'Cache-Control'    : 'no-cache',
             'User-Agent'       : 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/1337.0',
             'Connection'       : 'close',
             x : url
        }

        try:
            res = requests.get('{}://{}'.format(method, url), headers=header, timeout=3, verify=False)
            results.append({'header': x, 'status_code': res.status_code, 'response_size': len(res.text)})
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

        # Determine if the URL uses http or https
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
