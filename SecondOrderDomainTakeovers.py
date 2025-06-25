# coding=utf-8
# python3

import requests
import urllib3
import dns.resolver
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# SSL uyarılarını kapat
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

GLOBAL_HTTP_TIMEOUT = 7
UA = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
}

# Subdomain takeover imzaları (daha da genişletilmiş)
PROVIDERS = {
    "github.io": ["There isn’t a GitHub Pages site here"],
    "herokuapp.com": ["no such app"],
    "s3.amazonaws.com": ["NoSuchBucket"],
    "azurewebsites.net": ["404 Web Site not found"],
    "fastly.net": ["Fastly error: unknown domain"],
    "bitbucket.io": ["Repository not found"],
    "pantheonsite.io": ["The gods are wise, but do not know of the site which you seek"],
    "cloudfront.net": ["Bad request", "ERROR: The request could not be satisfied"],
    "surge.sh": ["project not found"],
    "intercom.io": ["Uh oh. That page doesn't exist."],
    "wordpress.com": ["Do you want to register this domain?"],
    "zendesk.com": ["Help Center Closed"],
    "readthedocs.io": ["404 Not Found", "Unknown page"],
    "unbouncepages.com": ["The requested URL was not found on this server."],
    "webflow.io": ["The page you are looking for doesn’t exist or has been moved"],
    "statuspage.io": ["page doesn’t exist"],
    "cargo.site": ["404 Not Found"],
    "shopify.com": ["Sorry, this shop is currently unavailable"],
    "ghost.io": ["The thing you were looking for is no longer here, or never was"],
    "helpscoutdocs.com": ["We could not find what you're looking for."],
    "desk.com": ["Please check the URL or go back a page."],
    "teamwork.com": ["Oops - looks like the page is gone."],
    "tilda.ws": ["Domain isn’t connected to a website yet."],
    "uservoice.com": ["This UserVoice subdomain is currently available!"],
    "kayako.com": ["Help Desk not found"],
    "getsatisfaction.com": ["This community does not exist"],
    "wishpond.com": ["The webpage cannot be found"],
    "aftership.com": ["Oops. The page you were looking for doesn't exist"],
    "simplebooklet.com": ["We couldn't find this page"],
    "acquia-sites.com": ["Website not found"],
    "instapage.com": ["Looks like you have taken a wrong turn"],
    "clickfunnels.com": ["This page is no longer available"]
}

def normalize_url(domain, src):
    src = src.strip().rstrip('/')
    if src.startswith('//'): return 'http:' + src
    if src.startswith('/'): return f'http://{domain}{src}'
    if src.startswith('http'): return src
    return f'http://{domain}/{src}'

def extract_resources(domain, html, headers):
    tree = BeautifulSoup(html, 'html.parser')
    urls = []
    urls += [normalize_url(domain, s['src']) for s in tree.find_all('script', src=True)]
    urls += [normalize_url(domain, s['href']) for s in tree.find_all('a', href=True)]
    urls += [normalize_url(domain, s['href']) for s in tree.find_all('link', href=True)]
    if 'Access-Control-Allow-Origin' in headers:
        cors = headers['Access-Control-Allow-Origin'].split(',')
        urls += [c.strip() for c in cors if c.strip() != '*']
    return set(urls)

def extract_domain(url):
    return urlparse(url).netloc

def check_takeover(subd):
    try:
        answers = dns.resolver.resolve(subd, 'CNAME')
        target = str(answers[0].target).rstrip('.')
    except:
        return False, None

    try:
        r = requests.get(f'http://{subd}', timeout=GLOBAL_HTTP_TIMEOUT, headers=UA, verify=False)
        body = r.text
    except:
        body = ''

    for provider, sigs in PROVIDERS.items():
        if provider in target:
            for sig in sigs:
                if sig in body:
                    return True, (target, sig)
    return False, None

def main(target_domain):
    try:
        r = requests.get(f'https://{target_domain}', timeout=GLOBAL_HTTP_TIMEOUT, headers=UA, verify=False)
    except Exception as e:
        print(f"[!] {target_domain} sayfasina erisilemedi: {e}")
        return

    urls = extract_resources(target_domain, r.text, r.headers)
    subdomains = set(extract_domain(url) for url in urls if extract_domain(url))
    print(f"[+] {len(subdomains)} adet harici kaynak bulundu.")

    for subd in sorted(subdomains):
        print(f"[*] Kontrol ediliyor: {subd}")
        vulnerable, info = check_takeover(subd)
        if vulnerable:
            print(f"\033[91m[!] TAKEOVER MUMKUN: {subd} -> CNAME {info[0]} (imza: '{info[1]}')\033[0m")
        else:
            print(f"[-] Guvenli: {subd}")

if __name__ == '__main__':
    domains = ['ads.realizeperformance.com','yahoso.com','sqislls.com','sqilsls.team'] #Domain yazılacak yer
    for domain in domains:
        print(f"\n=========== {domain} ===========")
        main(domain)



