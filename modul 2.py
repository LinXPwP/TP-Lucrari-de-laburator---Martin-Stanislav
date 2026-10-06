# Exercițiul 9. Elementele de bază ale răspunsului. Descărcați pagina principală și afișați response.status_code, response.ok, response.url și response.encoding. Lângă fiecare linie, scrieți un comentariu care spune dacă este un atribut sau o metodă.

import requests

BASE_URL = 'https://cybercor.org'
response = requests.get(BASE_URL)

print(response.status_code) # atribut
print(response.ok)          # atribut
print(response.url)         # atribut
print(response.encoding)    # atribut

# Exercițiul 10. Tratarea erorilor cu o metodă. Apelați response.raise_for_status() pe pagina principală. Apoi trimiteți o cerere către BASE_URL + "/this-page-does-not-exist" și prindeți excepția requests.HTTPError. Afișați un mesaj prietenos în loc să lăsați programul să se oprească cu eroare.

response.raise_for_status()

try:
    bad_response = requests.get(BASE_URL + "/this-page-does-not-exist")
    bad_response.raise_for_status()
except requests.HTTPError:
    print("Pagina nu a putut fi găsită (Eroare 404). Vă rugăm să verificați adresa.")

# Exercițiul 11. Toate antetele. Parcurgeți response.headers.items() și afișați fiecare antet în forma Nume: valoare.

for name, value in response.headers.items():
    print(f"{name}: {value}")

# Exercițiul 12. Metode de dicționar. Folosiți response.headers.get() pentru a afișa antetele Server și Content-Type, cu "lipsește" ca valoare implicită. Apoi încercați response.headers.get("content-type"), cu litere mici. Ce observați?

print(response.headers.get("Server", "lipsește"))
print(response.headers.get("Content-Type", "lipsește"))
print(response.headers.get("content-type", "lipsește"))

# Observație: Dicționarele de antete din requests nu țin cont de majuscule/minuscule (sunt case-insensitive).
# De aceea, "Content-Type" și "content-type" returnează exact aceeași valoare.

# Exercițiul 13. Înlănțuirea metodelor de șir. Numărați de câte ori apare cuvântul cyber pe pagina principală, cu response.text.lower().count("cyber"). Într-un comentariu, explicați de ce puteți înlănțui .lower() și .count().

print(response.text.lower().count("cyber"))

# Puteți înlănțui aceste metode deoarece .lower() returnează un nou șir de caractere (string), 
# care deține la rândul său propria metodă .count().

# Exercițiul 14. Găsirea titlului. Folosiți .find() și felierea (slicing) pe response.text pentru a extrage textul dintre <title> și </title>. Curățați-l cu .strip() și afișați-l.

html = response.text
start = html.find("<title>") + len("<title>")
end = html.find("</title>")

titlu = html[start:end].strip()
print(titlu)

# Exercițiul 15. Numărarea liniilor. Împărțiți codul HTML în linii cu .splitlines(). Afișați câte linii sunt și lungimea celei mai lungi linii, folosind max(lines, key=len).

lines = response.text.splitlines()
print("Număr total de linii:", len(lines))
if lines:
    print("Lungimea celei mai lungi linii:", len(max(lines, key=len)))

# Exercițiul 16. Verificarea HTTPS. Folosiți .startswith() pentru a verifica dacă response.url începe cu https://. Afișați Conexiune securizată sau Conexiune nesecurizată.

if response.url.startswith("https://"):
    print("Conexiune securizată")
else:
    print("Conexiune nesecurizată")

# Exercițiul 17. Urmărirea redirecționărilor. Trimiteți o cerere către http://cybercor.org (HTTP simplu, fără S). Parcurgeți response.history și afișați codul de stare și URL-ul fiecărei redirecționări, apoi URL-ul final.

r_http = requests.get("http://cybercor.org")

for resp in r_http.history:
    print(resp.status_code, resp.url)

print("URL final:", r_http.url)

# Exercițiul 18. HEAD versus GET. Trimiteți o cerere către pagina principală cu requests.head() și una cu requests.get(). Comparați len(response.content) pentru ambele și explicați diferența într-un comentariu.

r_head = requests.head(BASE_URL)
r_get = requests.get(BASE_URL)

print("Lungime conținut HEAD:", len(r_head.content))
print("Lungime conținut GET:", len(r_get.content))

# Diferența constă în faptul că metoda HEAD solicită serverului doar antetele (headers) răspunsului, 
# fără a descărca corpul propriu-zis al paginii (HTML-ul). Din acest motiv, len(r_head.content) este 0, 
# fiind util pentru a verifica starea paginii economisind lățime de bandă.

# Exercițiul 19. Cookie-uri. Parcurgeți response.cookies și afișați, pentru fiecare cookie, atributele .name și .secure. Dacă nu există cookie-uri, afișați Niciun cookie setat.

if response.cookies:
    for cookie in response.cookies:
        print(cookie.name, cookie.secure)
else:
    print("Niciun cookie setat.")

# Exercițiul 20. Sesiuni. Creați un obiect requests.Session() și setați un User-Agent personalizat cu session.headers.update({"User-Agent": "WebLab-<numele vostru>"}). Trimiteți o cerere către ECHO_URL + "/headers" și confirmați în rezultat că antetul a fost trimis.
# Verificați-vă: atât response.text, cât și response.json() vă dau corpul răspunsului. De ce unul are paranteze, iar celălalt nu?

ECHO_URL = "https://httpbin.org"

session = requests.Session()
session.headers.update({"User-Agent": "WebLab-Student"})

r_session = session.get(ECHO_URL + "/headers")
date_returnate = r_session.json()

print("User-Agent-ul confirmat de server este:", date_returnate["headers"].get("User-Agent"))

# VERIFICAȚI-VĂ:
# response.text NU are paranteze pentru că este un ATRIBUT. Reprezintă o proprietate/valoare
# care a fost deja descărcată și stocată în memorie în prealabil, deci doar o accesați.
# 
# response.json() ARE paranteze pentru că este o METODĂ (o funcție). Când este apelată, execută 
# o acțiune: procesează și parșează în mod dinamic textul brut pentru a-l transforma într-un dicționar.