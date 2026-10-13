import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    return f"https://{host.rstrip('/')}/{path.lstrip('/')}"


def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    if url.startswith("https://"):
        return True
    else:
        return False
    
print(build_url("example.com", "login"))
print(build_url("example.com", "/login"))
print(is_https("https://example.com/login"))


def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    response = requests.get(url)
    print(f"Status: {response.status_code}\nContent-Type: {response.headers.get('Content-Type')}")

show_response("https://httpbin.org/html")

def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    try:
        response = requests.get(url, timeout=5)
        return {
            "status": response.status_code,
            "content_type": response.headers.get("Content-Type"),
            "length": len(response.content),
            "server": response.headers.get("Server", "unknown"),
        }

    except requests.exceptions.Timeout:
        return {"status": None, "error": "timeout"}
    except Exception:
        return {"status": None, "error": "request failed"}

print(check_site("https://httpbin.org/json"))

def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    results = []
    for site in SITES:
        result = check_site(site)
        results.append(result)
        if result["status"] == 200:
            print(f"Site: {site}, Status: {result['status']}, Length: {result['length']} octeti")
    # afisam reusitele si nereusitele
    print(f"Reusite: {sum(1 for r in results if r['status'] == 200)} | Esuate: {sum(1 for r in results if r['status'] != 200)}")



def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    try:
        response = requests.get(url, timeout=5)
        response_header_names = {name.lower() for name in response.headers}
    except requests.exceptions.Timeout:
        return {"status": None, "error": "timeout"}
    except requests.exceptions.RequestException:
        return {"status": None, "error": "request failed"}

    present = [header for header in SECURITY_HEADERS if header.lower() in response_header_names]
    missing = [header for header in SECURITY_HEADERS if header.lower() not in response_header_names]
    score = int(len(present) / len(SECURITY_HEADERS) * 100) if SECURITY_HEADERS else 0
    return {"present": present, "missing": missing, "score": score}

def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    pass
