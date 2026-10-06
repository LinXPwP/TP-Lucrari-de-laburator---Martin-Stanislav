import requests
import time

BASE_URL = "https://cybercor.org"
TIMEOUT = 10

# Exercițiul 21. Prima funcție. Scrieți fetch(url), care returnează obiectul răspuns. Apelați-o pentru BASE_URL și afișați codul de stare.

def fetch_v1(url):
    return requests.get(url, timeout=TIMEOUT)

response_21 = fetch_v1(BASE_URL)
print("Exercițiul 21 Status:", response_21.status_code)

# Exercițiul 22. Returnarea unei singure valori. Scrieți get_status(url), care returnează doar codul de stare. Apelați-o pentru /, /robots.txt și /sitemap.xml, cu time.sleep(1) între apeluri.

def get_status_v1(url):
    """Returnează codul de stare HTTP pentru adresa url."""
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code

cai = ["/", "/robots.txt", "/sitemap.xml"]
for cale in cai:
    print(f"Exercițiul 22 Status pentru {cale}:", get_status_v1(BASE_URL + cale))
    time.sleep(1)

# Exercițiul 23. Parametri impliciți. Modificați funcția în fetch(url, timeout=10). Apelați-o o dată cu valoarea implicită și o dată cu timeout=3.

def fetch(url, timeout=10):
    return requests.get(url, timeout=timeout)

print("Exercițiul 23 cu timeout implicit:", fetch(BASE_URL).status_code)
print("Exercițiul 23 cu timeout=3:", fetch(BASE_URL, timeout=3).status_code)

# Exercițiul 24. O singură sarcină pe funcție. Scrieți get_title(html), care primește un șir HTML și returnează titlul paginii.

def get_title(html):
    start = html.find("<title>")
    if start == -1:
        return ""
    start += len("<title>")
    end = html.find("</title>")
    return html[start:end].strip()

html_test = fetch(BASE_URL).text
print("Exercițiul 24 Titlu:", get_title(html_test))

# Exercițiul 25. Docstring-uri. Adăugați un docstring funcției get_title și afișați-l cu help(get_title).

print("\n--- Exercițiul 25 ---")
help(get_title)

# Exercițiul 26. Adnotări de tip. Adăugați adnotări de tip (type hints) funcțiilor, de exemplu def get_status(url: str) -> int:. Apelați get_status(123) și observați ce se întâmplă. Vă opresc adnotările de tip?

def get_status(url: str) -> int:
    """Returnează codul de stare HTTP pentru adresa url, folosind adnotări de tip."""
    return requests.get(url, timeout=TIMEOUT).status_code

print("\n--- Exercițiul 26 ---")
try:
    get_status(123)
except Exception as e:
    print("Eroare generată:", type(e).__name__)

# Observație pentru ex. 26: Adnotările de tip (type hints) NU opresc programul la rulare.
# Ele sunt doar documentație și sunt folosite de lintere sau IDE-uri pentru a avertiza dezvoltatorul.
# Eroarea care apare (MissingSchema sau InvalidURL) este generată de biblioteca 'requests' pentru 
# că primește un număr în loc de un string valid, nu pentru că Python ar bloca execuția din cauza adnotării.

# Exercițiul 27. Fără opriri neașteptate. Scrieți page_exists(url), care returnează True sau False.

def page_exists(url: str) -> bool:
    try:
        requests.get(url, timeout=TIMEOUT)
        return True
    except requests.RequestException:
        return False

print("Exercițiul 27 (pagină falsă):", page_exists("https://this-domain-does-not-exist.invalid"))

# Exercițiul 28. Returnarea unui dicționar. Scrieți check_paths(base, paths), care primește o listă și returnează un dicționar {path: status_code}.

def check_paths(base, paths):
    rezultate = {}
    for p in paths:
        rezultate[p] = get_status(base + p)
        time.sleep(1) # Pauză politicoasă
    return rezultate

print("Exercițiul 28:", check_paths(BASE_URL, ["/", "/robots.txt", "/sitemap.xml"]))

# Exercițiul 29. Argumente cu nume. Scrieți get_header(url, name, default="lipsește"). Apelați-o cu argumente cu nume: get_header(BASE_URL, name="Server").

def get_header(url, name, default="lipsește"):
    response = fetch(url)
    return response.headers.get(name, default)

print("Exercițiul 29 Server:", get_header(BASE_URL, name="Server"))

# Exercițiul 30. Antete de securitate. Scrieți security_headers(url), care verifică prezența a cinci antete.

def security_headers(url):
    headers = fetch(url).headers
    return {
        "Strict-Transport-Security": "Strict-Transport-Security" in headers,
        "Content-Security-Policy": "Content-Security-Policy" in headers,
        "X-Frame-Options": "X-Frame-Options" in headers,
        "X-Content-Type-Options": "X-Content-Type-Options" in headers,
        "Referrer-Policy": "Referrer-Policy" in headers
    }

print("Exercițiul 30:", security_headers(BASE_URL))

# Exercițiul 31. Funcții care apelează funcții. Scrieți score_headers(results), care primește dicționarul din exercițiul 30 și returnează un șir precum "3/5".

def score_headers(results):
    prezente = sum(results.values()) # True este tratat ca 1, False ca 0
    total = len(results)
    return f"{prezente}/{total}"

print("Exercițiul 31 Scor securitate:", score_headers(security_headers(BASE_URL)))

# Exercițiul 32. Două funcții, o sarcină. Scrieți fetch_robots(base) și disallowed_paths(robots_text).

def fetch_robots(base):
    response = requests.get(base + "/robots.txt", timeout=TIMEOUT)
    if response.status_code == 200:
        return response.text
    return None

def disallowed_paths(robots_text):
    if robots_text is None:
        return []
    
    cai_interzise = []
    for linie in robots_text.splitlines():
        if linie.lower().startswith("disallow:"):
            cai_interzise.append(linie.split(":", 1)[1].strip())
    return cai_interzise

robots_txt = fetch_robots(BASE_URL)
print("Exercițiul 32 Căi interzise:", disallowed_paths(robots_txt))

# Exercițiul 33. Oricâte argumente. Scrieți response_times(*urls), care returnează un dicționar {url: secunde}. Apelați-o cu două URL-uri.

def response_times(*urls):
    rezultate = {}
    for url in urls:
        start_time = time.perf_counter()
        fetch(url)
        end_time = time.perf_counter()
        rezultate[url] = round(end_time - start_time, 4)
    return rezultate

print("Exercițiul 33 Timpi răspuns:", response_times(BASE_URL, "https://www.python.org"))

# Exercițiul 34. Argumente cu nume colectate. Scrieți log(message, **details), care afișează mesajul urmat de fiecare detaliu.

def log(message, **details):
    detalii_string = " | ".join([f"{cheie}={valoare}" for cheie, valoare in details.items()])
    print(f"{message} | {detalii_string}")

print("Exercițiul 34:")
log("verificat", url=BASE_URL, status=200)

# ==========================================
# VERIFICAȚI-VĂ:
# Care este diferența dintre a afișa o valoare cu print() în interiorul unei funcții și a o returna cu return?
# 
# print() doar AFIȘEAZĂ informația pe ecran (în terminal) pentru ca omul să o poată citi. 
# Rezultatul afișat se pierde imediat ce a fost afișat, iar funcția va returna valoarea implicită 'None'.
# 
# return EXPEDIAZĂ (returnează) datele înapoi către linia de cod care a apelat funcția. 
# Astfel, poți stoca rezultatul într-o variabilă, îl poți prelucra mai departe 
# sau îl poți trimite altei funcții (cum am făcut la Exercițiul 31, unde output-ul lui 
# security_headers a devenit input-ul lui score_headers).