import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
import argparse
import time

def print_banner():
    blue = "\033[94m"
    reset = "\033[0m"
    banner = r"""
 _    _      _     _____
| |  | |    | |   /  ___|
| |  | | ___| |__ \ `--.  ___ _ __ __ _ _ __   ___ _ __
| |/\| |/ _ \ '_ \ `--. \/ __| '__/ _` | '_ \ / _ \ '__|
\  /\  /  __/ |_) /\__/ / (__| | | (_| | |_) |  __/ |
 \/  \/ \___|_.__/\____/ \___|_|  \__,_| .__/ \___|_|
                                       | |
                                       |_|

                    WebScraper - Dustin (DustinWorlds) - 2025
"""
    print(f"{blue}{banner}{reset}")

def normalize_domain_url(url, main_domain, excluded_domains):
    parsed = urlparse(url)
    netloc = parsed.netloc.lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]

    if any(netloc.endswith(excl) for excl in excluded_domains):
        return None

    if netloc.endswith(main_domain):
        parsed = parsed._replace(netloc=netloc)
        scheme = 'https'
        parsed = parsed._replace(scheme=scheme)
        url = urlunparse(parsed._replace(fragment=''))
        if url.endswith('/'):
            url = url[:-1]
        return url
    else:
        return None

def crawl_single_url(url, main_domain, excluded_domains, visited, depth=0, max_depth=3):
    if depth > max_depth:
        return
    try:
        r = requests.get(url, timeout=20)
        soup = BeautifulSoup(r.text, 'html.parser')

        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(url, href)
            normalized_url = normalize_domain_url(full_url, main_domain, excluded_domains)

            if normalized_url and normalized_url not in visited:
                visited.add(normalized_url)
                print(f"[+] Founded Path: {normalized_url}")
                time.sleep(1.5)
                crawl_single_url(normalized_url, main_domain, excluded_domains, visited, depth + 1, max_depth)

    except Exception as e:
        print(f"[!] Crawl Error {url}: {e}")

def crawl_paths(start_url, main_domain, excluded_domains):
    visited = set()
    normalized_start = normalize_domain_url(start_url, main_domain, excluded_domains)
    if not normalized_start:
        print(f"[!] Start URL {start_url} does not match the domain {main_domain} or is excluded")
        return visited

    visited.add(normalized_start)
    crawl_single_url(normalized_start, main_domain, excluded_domains, visited)
    return visited

def get_subdomains_crtsh(domain):
    print(f"[=] Search Subdomains for {domain} ...")
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        r = requests.get(url, timeout=10)
        json_data = r.json()
        subdomains = set()
        for entry in json_data:
            name_value = entry['name_value']
            for sub in name_value.split("\n"):
                if sub.endswith(domain):
                    subdomains.add(sub.strip())
        return list(subdomains)
    except Exception as e:
        print(f"[!] Subdomain Search Error: {e}")
        return []

def recursive_subdomain_search(domain, excluded_domains, all_found=None, depth=1, max_depth=2):
    if all_found is None:
        all_found = set()

    if domain in all_found or domain in excluded_domains:
        return all_found

    all_found.add(domain)
    subdomains = get_subdomains_crtsh(domain)

    for sub in subdomains:
        if sub not in all_found and sub not in excluded_domains and depth < max_depth:
            recursive_subdomain_search(sub, excluded_domains, all_found, depth + 1, max_depth)

    return all_found

if __name__ == "__main__":
    print_banner()

    parser = argparse.ArgumentParser(description="Web Scraper")
    parser.add_argument("-u", "--url", required=True, help="Target Domain (z.B. example.com oder mehrere mit Komma getrennt)")
    parser.add_argument("-f", "--filter", help="Comma-separated list of domains to exclude (z.B. test.com,test.org)")
    parser.add_argument("--subdomain", action="store_true", help="Subdomain Search activation")
    parser.add_argument("--path", action="store_true", help="Path Crawling activation")
    args = parser.parse_args()

    target_domains = [d.strip().lower() for d in args.url.split(",")]
    excluded_domains = set()

    if args.filter:
        excluded_domains.update([f.strip().lower() for f in args.filter.split(",")])

    all_paths = []
    all_subdomains_all = set()

    for main_domain in target_domains:
        all_subdomains = set()

        if args.subdomain:
            all_subdomains = recursive_subdomain_search(main_domain, excluded_domains)
            all_subdomains_all.update(all_subdomains)
            print(f"\n[=] Founded Subdomains for {main_domain} ({len(all_subdomains)}):")
            for sub in sorted(all_subdomains):
                print(f" - {sub}")

        if args.path:
            domains_to_crawl = all_subdomains if args.subdomain else {main_domain}
            for domain_to_crawl in domains_to_crawl:
                if any(domain_to_crawl.endswith(excl) for excl in excluded_domains):
                    print(f"[!] Skipping excluded domain: {domain_to_crawl}")
                    continue

                start_url = f"https://{domain_to_crawl}"
                print(f"\n[=] Crawl {start_url}")
                paths = crawl_paths(start_url, main_domain, excluded_domains)
                all_paths.extend(paths)

    if args.path or args.subdomain:
        save = input("\nDo you want to save the results in a txt? (y/n): ").strip().lower()
        if save == "y":
            if all_paths:
                filename_paths = "WebScraper_Paths.txt"
                with open(filename_paths, "w", encoding="utf-8") as f:
                    f.write("Founded Paths:\n")
                    for p in all_paths:
                        f.write(p + "\n")
                print(f"[+] Paths stored in {filename_paths}")

            if all_subdomains_all:
                filename_subs = "WebScraper_Subdomains.txt"
                with open(filename_subs, "w", encoding="utf-8") as f:
                    f.write("Founded Subdomains:\n")
                    for s in sorted(all_subdomains_all):
                        f.write(s + "\n")
                print(f"[+] Subdomains stored in {filename_subs}")
        else:
            print("No saving performed.")
