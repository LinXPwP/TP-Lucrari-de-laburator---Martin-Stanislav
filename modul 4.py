import urllib.parse
import re
from html.parser import HTMLParser
import hashlib
import json
import socket
import ssl
import time
import requests

BASE_URL = "https://cybercor.org"
TIMEOUT = 10

# Exercițiul 35. Descompunerea unui URL. Folosiți urllib.parse.urlparse() pe https://cybercor.org/path?x=1#top. Afișați .scheme, .netloc, .path, .query și .fragment.
url_35 = "https://cybercor.org/path?x=1#top"
parsed = urllib.parse.urlparse(url_35)
print(parsed.scheme)
print(parsed.netloc)
print(parsed.path)
print(parsed.query)
print(parsed.fragment)
print()

# Exercițiul 36. Compunerea URL-urilor. Folosiți urllib.parse.urljoin() pentru a transforma legăturile relative /about, contact.html și ../index.html în URL-uri complete, pornind de la BASE_URL.
relative_links = ["/about", "contact.html", "../index.html"]
for link in relative_links:
    print(urllib.parse.urljoin(BASE_URL, link))
print()

# Exercițiul 37. Extragerea legăturilor. Folosiți re.findall(r'href="([^"]+)"', html) pentru a obține toate legăturile de pe pagina principală. Puneți codul într-o funcție extract_links(html), care returnează legăturile fără duplicate.
def extract_links(html):
    links = re.findall(r'href="([^"]+)"', html)
    return list(set(links))

# Exercițiul 38. Interne sau externe? Scrieți split_links(links, domain), care returnează două liste: legăturile de pe același domeniu și legăturile către alte site-uri. Folosiți mai întâi urljoin(), apoi urlparse().netloc.
def split_links(links, domain):
    interne = []
    externe = []
    for link in links:
        full_url = urllib.parse.urljoin(f"https://{domain}", link)
        netloc = urllib.parse.urlparse(full_url).netloc
        if netloc == domain:
            interne.append(full_url)
        else:
            externe.append(full_url)
    return interne, externe

html_page = requests.get(BASE_URL, timeout=TIMEOUT).text
all_links = extract_links(html_page)
interne, externe = split_links(all_links, "cybercor.org")
print(f"Găsite {len(all_links)} legături unice ({len(interne)} interne, {len(externe)} externe).\n")


# Exercițiul 39. Propriile metode. Creați o clasă care moștenește html.parser.HTMLParser și suprascrieți metoda handle_starttag(), pentru a colecta atributul src al fiecărui tag <img>.
class ImageFinder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "img":
            src = dict(attrs).get("src")
            if src:
                self.images.append(src)

test_html = """
<html><body>
  <img src="/logo.png" alt="Logo">
  <IMG SRC="poza.jpg">
  <img alt="imagine fără src">
  <img src="https://cdn.example.com/banner.webp" />
  <a href="/despre">Aceasta nu este o imagine</a>
</body></html>
"""
finder = ImageFinder()
finder.feed(test_html)
print(finder.images)

assert finder.images == [
    "/logo.png",                            
    "poza.jpg",                             
    "https://cdn.example.com/banner.webp",  
], "Parserul nu a găsit exact imaginile așteptate"
print("Testul a trecut!\n")

response_39 = requests.get(BASE_URL, timeout=TIMEOUT)
real_finder = ImageFinder()
real_finder.feed(response_39.text)
print(len(real_finder.images), "imagini găsite pe site:")
for src in real_finder.images:
    print(src)
print()

# Exercițiul 40. Amprenta paginii. Scrieți page_fingerprint(url), care returnează hashlib.sha256(response.content).hexdigest(). Rulați-o de două ori și comparați rezultatele. Când ar fi diferite?
def page_fingerprint(url):
    response = requests.get(url, timeout=TIMEOUT)
    return hashlib.sha256(response.content).hexdigest()

print("Amprenta 1:", page_fingerprint(BASE_URL))
print("Amprenta 2:", page_fingerprint(BASE_URL))

print()

# Exercițiul 41. Salvarea în JSON. Salvați antetele paginii principale în headers.json cu json.dump(dict(response.headers), file, indent=2). Apoi încărcați fișierul înapoi cu json.load() și afișați un antet din el.
response_41 = requests.get(BASE_URL, timeout=TIMEOUT)
with open("headers.json", "w", encoding="utf-8") as file:
    json.dump(dict(response_41.headers), file, indent=2)
    
with open("headers.json", "r", encoding="utf-8") as file:
    loaded_headers = json.load(file)
    
print("Antet Content-Type extras din JSON:", loaded_headers.get("Content-Type", "Nu a fost găsit"))
print()

# Exercițiul 42. Interogare DNS. Scrieți resolve(hostname), care returnează socket.gethostbyname(hostname). Afișați adresa IP a domeniului cybercor.org.
def resolve(hostname):
    return socket.gethostbyname(hostname)

print(f"IP pentru cybercor.org: {resolve('cybercor.org')}\n")

# Exercițiul 43. Expirarea certificatului. Scrieți cert_days_left(hostname), care se conectează la portul 443, citește certificatul și returnează câte zile mai sunt până la expirarea lui.
def cert_days_left(hostname):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            expire_timestamp = ssl.cert_time_to_seconds(cert["notAfter"])
            days_left = (expire_timestamp - time.time()) / (60 * 60 * 24)
            return int(days_left)

try:
    print(f"Zile rămase pentru certificatul cybercor.org: {cert_days_left('cybercor.org')}")
except Exception as e:
    print(f"Eroare la citirea certificatului: {e}")
print()

# Verificați-vă: în exercițiul 39, cine apelează handle_starttag()? Voi nu o apelați niciodată direct.
# R: Metoda handle_starttag() este apelată intern și automat de către clasa de bază HTMLParser 
# de fiecare dată când găsește un tag de deschidere în string-ul furnizat prin metoda `feed()`.