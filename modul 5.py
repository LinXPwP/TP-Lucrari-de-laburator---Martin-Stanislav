import requests
import time
import socket
import ssl
import json
import urllib.parse
from bs4 import BeautifulSoup

# Exercițiul 47: Constante de modul
DEFAULT_HEADERS = {"User-Agent": "WebLab-Stanislav"}
TIMEOUT = 10

def fetch(url):
    """Descărcați pagina și returnați obiectul răspuns, folosind timeout și antete."""
    return requests.get(url, headers=DEFAULT_HEADERS, timeout=TIMEOUT)

def get_status(url):
    """Returnează codul de stare HTTP pentru adresa URL."""
    return fetch(url).status_code

# BONUS: rescrierea cu BeautifulSoup
def get_title(html):
    """Extrage titlul paginii folosind biblioteca BeautifulSoup."""
    # Explicație BONUS: Folosind BeautifulSoup codul devine mai scurt și mult mai sigur.
    # Nu mai trebuie să facem feliere manuală de șiruri (slicing) cu .find(), 
    # iar biblioteca tratează perfect cazurile în care codul HTML este malformat 
    # sau tag-ul <title> are atribute suplimentare.
    soup = BeautifulSoup(html, 'html.parser')
    return soup.title.string.strip() if soup.title and soup.title.string else "Fără titlu"

# BONUS: rescrierea cu BeautifulSoup
def extract_links(html):
    """Extrage toate legăturile (href) unice dintr-o pagină folosind BeautifulSoup."""
    soup = BeautifulSoup(html, 'html.parser')
    # Căutăm toate tag-urile <a> care au un atribut href și le punem într-un Set (fără duplicate)
    return list(set(a['href'] for a in soup.find_all('a', href=True)))

def security_headers(url):
    """Verifică prezența a cinci antete de securitate HTTP."""
    headers = fetch(url).headers
    return {
        "Strict-Transport-Security": "Strict-Transport-Security" in headers,
        "Content-Security-Policy": "Content-Security-Policy" in headers,
        "X-Frame-Options": "X-Frame-Options" in headers,
        "X-Content-Type-Options": "X-Content-Type-Options" in headers,
        "Referrer-Policy": "Referrer-Policy" in headers
    }

def score_headers(results):
    """Returnează scorul antetelor de securitate (ex: '3/5')."""
    return f"{sum(results.values())}/{len(results)}"

def check_paths(base, paths):
    """Verifică lista de căi și returnează un dicționar cu codurile de stare HTTP."""
    rezultate = {}
    for p in paths:
        url_complet = urllib.parse.urljoin(base, p)
        rezultate[p] = get_status(url_complet)
        time.sleep(1) # Pauză între cererile repetate
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

# Exercițiul 50: Raportul site-ului
def site_report(url):
    """Generează raportul complet al site-ului, afișându-l și salvându-l în JSON."""
    print(f"=== Raport site: {url} ===")
    
    # 1. Cod de stare
    r = fetch(url)
    print(f"Cod de stare:      {r.status_code}")
    
    # 2. Titlu pagină
    titlu = get_title(r.text)
    print(f"Titlu:             {titlu}")
    
    # 3. Adresă IP
    domeniu = urllib.parse.urlparse(url).netloc
    try:
        ip = socket.gethostbyname(domeniu)
    except Exception:
        ip = "Necunoscut"
    print(f"Adresă IP:         {ip}")
    
    # 4. Lanțul de redirecționări
    r_http = requests.get(f"http://{domeniu}", headers=DEFAULT_HEADERS, timeout=TIMEOUT)
    if r_http.history:
        redir = " -> ".join([str(h.status_code) for h in r_http.history]) + f" -> {r_http.url}"
    else:
        redir = "Nicio redirecționare"
    print(f"Redirecționări:    {redir}")
    time.sleep(1)
    
    # 5. Scorul antetelor de securitate
    sec = security_headers(url)
    scor = score_headers(sec)
    print(f"Scor securitate:   {scor}")
    time.sleep(1)
    
    # 6. Zile rămase din certificat
    zile_cert = cert_days_left(domeniu)
    print(f"Certificat:        {zile_cert} de zile rămase")
    
    # 7. Numărul de legături
    toate_linkurile = extract_links(r.text)
    interne, externe = 0, 0
    for link in toate_linkurile:
        full_url = urllib.parse.urljoin(url, link)
        if urllib.parse.urlparse(full_url).netloc == domeniu:
            interne += 1
        else:
            externe += 1
    print(f"Legături:          {interne} interne, {externe} externe")
    
    # 8. Căi interzise (robots.txt)
    r_rob = fetch(urllib.parse.urljoin(url, "/robots.txt"))
    if r_rob.ok:
        cai_interzise = [linie.split(":", 1)[1].strip() for linie in r_rob.text.splitlines() if linie.lower().startswith("disallow:")]
    else:
        cai_interzise = []
    print(f"Căi interzise:     {', '.join(cai_interzise) if cai_interzise else 'Niciuna'}")
    
    # Salvare în report.json
    date_raport = {
        "url": url,
        "status_code": r.status_code,
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
    print("Salvat în report.json")

# Exercițiul 46: Blocul main
if __name__ == "__main__":
    print("Autotest:", get_status("https://cybercor.org"))
    
    # EXPLICAȚIE: De ce autotestul rulează doar aici?
    # În Python, variabila specială `__name__` are valoarea "__main__" doar atunci când 
    # fișierul este executat direct (ex: python webtools.py). 
    # Dacă fișierul este importat din alt script (cum facem în main.py), 
    # `__name__` devine "webtools", iar acest bloc `if` este complet ignorat.