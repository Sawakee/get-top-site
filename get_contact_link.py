from bs4 import BeautifulSoup
import re
import sys
import requests

def extract_contact_link(url):
    try:
        res = requests.get(url, allow_redirects=True, timeout=5)
    except requests.RequestException:
        return []
    if res.status_code != 200:
        return []
    soup = BeautifulSoup(res.text, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        text = (a.get_text() or "").strip().lower()
        href = a["href"].lower()
        if re.search(r"(contact|inquiry|お問い合わせ|問い合わせ|問合)", text + href):
            links.append(a["href"])

    return links

def check_page_exists(url):
    try:
        res = requests.head(url, allow_redirects=True, timeout=5)
        return res.status_code == 200
    except requests.RequestException:
        return False

def check_sitemap(url):
    sitemap_urls = [url + "/sitemap.xml", url + "/sitemap_index.xml"]
    for sitemap_url in sitemap_urls:
        try:
            res = requests.get(sitemap_url, timeout=5)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "xml")
                urls = [loc.get_text() for loc in soup.find_all("loc")]
                contact_urls = [u for u in urls if re.search(r"(contact|inquiry|お問い合わせ|問い合わせ|問合)", u, re.I)]
                if contact_urls:
                    return contact_urls
        except requests.RequestException:
            continue
    return []

def get_contact_url(url):
    if url.endswith('/'):
        url = url[:-1]

    check_contact_page = check_page_exists(url + "/contact/")
    if check_contact_page:
        return url + "/contact/"

    check_contact_page = check_page_exists(url + "/inquiry/")
    if check_contact_page:
        return url + "/inquiry/"

    sitemap_links = check_sitemap(url)
    if sitemap_links:
        # print("Contact links found in sitemap:")
        # for link in sitemap_links:
        #     print(link)
        return sitemap_links[0]
    
    links = extract_contact_link(url)
    if links:
        # print("Possible contact links found:")
        # for link in links:
        #     print(link)
        return links[0] if links[0].startswith('http') else url + links[0]

def main():
    # load csv which path is passed as first argument
    if len(sys.argv) < 2:
        print("Usage: python script.py <csv_file>")
        sys.exit(1)
    csv_file = sys.argv[1]
    with open(csv_file, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split('|')
            company, url = parts[0], parts[1]

            contact_url = get_contact_url(url)
            print(f"{company}|{url}|{contact_url if contact_url else 'No contact page found'}")

if __name__ == "__main__":
    main()
