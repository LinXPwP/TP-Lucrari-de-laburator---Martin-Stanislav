import requests
import time
import socket
import ssl
import json
import urllib.parse
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# Exercițiul 47: Constante de modul
DEFAULT_HEADERS = {"User-Agent": "WebLab-Stanislav"}
TIMEOUT = 10

def fetch(url):
    """Descărcați pagina și returnați obiectul răspuns, folosind timeout și antete."""
    return requests.get(url, headers=DEFAULT_HEADERS, timeout=TIMEOUT)

def get_status(url):
    """Returnează codul de stare HTTP pentru adresa URL."""
    try:
        return fetch(url).status_code
    except requests.RequestException:
        return "Eroare"

def get_title(html):
    """Extrage titlul paginii folosind biblioteca BeautifulSoup."""
    soup = BeautifulSoup(html, 'html.parser')
    return soup.title.string.strip() if soup.title and soup.title.string else "Fără titlu"

def extract_links(html):
    """Extrage toate legăturile (href) unice dintr-o pagină folosind BeautifulSoup."""
    soup = BeautifulSoup(html, 'html.parser')
    return list(set(a['href'] for a in soup.find_all('a', href=True)))

def security_headers(url):
    """Verifică prezența a cinci antete de securitate HTTP."""
    try:
        headers = fetch(url).headers
    except requests.RequestException:
        headers = {}
    return {
        "Strict-Transport-Security": "Strict-Transport-Security" in headers,
        "Content-Security-Policy": "Content-Security-Policy" in headers,
        "X-Frame-Options": "X-Frame-Options" in headers,
        "X-Content-Type-Options": "X-Content-Type-Options" in headers,
        "Referrer-Policy": "Referrer-Policy" in headers
    }

def score_headers(results):
    """Returnează scorul antetelor de securitate (ex: '3/5')."""
    if not results:
        return "0/0"
    return f"{sum(results.values())}/{len(results)}"

def check_paths(base, paths):
    """Verifică lista de căi și returnează un dicționar cu codurile de stare HTTP."""
    rezultate = {}
    for p in paths:
        url_complet = urllib.parse.urljoin(base, p)
        rezultate[p] = get_status(url_complet)
        time.sleep(1)
    return rezultate

def cert_days_left(hostname):
    """Returnează numărul de zile rămase până la expirarea certificatului SSL."""
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                expire_timestamp = ssl.cert_time_to_seconds(cert["notAfter"])
                return int((expire_timestamp - time.time()) / 86400)
    except Exception:
        return 0

# Exercițiul 49: Un raport CSV
def save_paths_to_csv(rezultate, filename="report.csv"):
    """Salvează rezultatul funcției check_paths() într-un fișier CSV."""
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["path", "status", "checked_at"])
        timp_curent = datetime.now().isoformat()
        for path, status in rezultate.items():
            writer.writerow([path, status, timp_curent])

# Exercițiul 50: Proiect final - Raportul site-ului
def site_report(url):
    """Generează raportul complet al site-ului."""
    print(f"=== Raport site: {url} ===")
    
    # 1. Cod de stare
    try:
        r = fetch(url)
        status_code = r.status_code
        html_text = r.text
    except Exception:
        status_code = "Eroare"
        html_text = ""

    # 2. Titlu pagină
    titlu = get_title(html_text)
    
    # 3. Adresă IP
    domeniu = urllib.parse.urlparse(url).netloc
    try:
        ip = socket.gethostbyname(domeniu)
    except Exception:
        ip = "Necunoscut"
    
    # 4. Lanțul de redirecționări
    try:
        r_http = requests.get(f"http://{domeniu}", headers=DEFAULT_HEADERS, timeout=TIMEOUT)
        if r_http.history:
            redir = " -> ".join([str(h.status_code) for h in r_http.history]) + f" -> {r_http.url}"
        else:
            redir = "Nicio redirecționare"
    except Exception:
        redir = "Eroare"
    
    # 5. Scorul antetelor de securitate
    sec = security_headers(url)
    scor = score_headers(sec)
    
    # 6. Zile rămase din certificat
    zile_cert = cert_days_left(domeniu)
    
    # 7. Numărul de legături
    toate_linkurile = extract_links(html_text)
    interne, externe = 0, 0
    for link in toate_linkurile:
        full_url = urllib.parse.urljoin(url, link)
        if urllib.parse.urlparse(full_url).netloc == domeniu:
            interne += 1
        else:
            externe += 1
            
    # 8. Căi interzise (robots.txt)
    try:
        r_rob = fetch(urllib.parse.urljoin(url, "/robots.txt"))
        if r_rob.ok:
            cai_interzise = [linie.split(":", 1)[1].strip() for linie in r_rob.text.splitlines() if linie.lower().startswith("disallow:")]
        else:
            cai_interzise = []
    except Exception:
         cai_interzise = []
    
    cai_afisare = ", ".join(cai_interzise) if cai_interzise else "Niciuna"
    
    # Afișare cu formatare strictă (<18 caractere) conform imaginii de referință
    print(f"{'Cod de stare:':<18}{status_code}")
    print(f"{'Titlu:':<18}{titlu}")
    print(f"{'Adresă IP:':<18}{ip}")
    print(f"{'Redirecționări:':<18}{redir}")
    print(f"{'Scor securitate:':<18}{scor}")
    print(f"{'Certificat:':<18}{zile_cert} de zile rămase")
    print(f"{'Legături:':<18}{interne} interne, {externe} externe")
    print(f"{'Căi interzise:':<18}{cai_afisare}")
    print("Salvat în report.json")
    
    # Salvare în report.json
    date_raport = {
        "url": url,
        "status_code": status_code,
        "title": titlu,
        "ip": ip,
        "redirects": redir,
        "security_score": scor,
        "cert_days_left": zile_cert,
        "links": {"internal": interne, "external": externe},
        "disallowed_paths": cai_interzise
    }
    with open("report.json", "w", encoding="utf-8") as file:
        json.dump(date_raport, file, indent=4)

# Exercițiul 46: Blocul main (Autotest)
if __name__ == "__main__":
    print("Autotest:", get_status("https://cybercor.org"))
    # Explicație: Autotestul rulează doar când webtools.py este executat direct.
    # Când este importat în main.py, variabila __name__ va fi "webtools", deci blocul if nu se execută.