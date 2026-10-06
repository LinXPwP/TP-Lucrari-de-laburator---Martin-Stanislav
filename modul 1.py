# Exercițiul 1. Primul import. Scrieți import requests și afișați requests.__version__. Apoi scrieți import urllib.request. Într-un comentariu, explicați de ce requests a avut nevoie de pip install, iar urllib nu.
import requests
print(requests.__version__)

import urllib.request

# requests trebuie de instalat deoarece sste un bibioteca externa, 
# nu o biblioteca standard, dar urllib este o bibioteca standard.

# Exercițiul 2. Două stiluri de import. Descărcați pagina BASE_URL cu requests.get() și afișați codul de stare. Apoi rescrieți același script folosind from requests import get. Într-un comentariu, scrieți câte un avantaj al fiecărui stil.

import requests
from requests import get

BASE_URL = 'https://www.python.org'

response = requests.get(BASE_URL)
print(response.status_code)

response = get(BASE_URL)
print(response.status_code)

# Avantaj 1: Puteți folosi funcția get() pentru a rescrie codul de stare.
# Avantaj 2: Puteți folosi funcția requests.get() pentru a rescrie codul de stare.

# Exercițiul 3. Alias-uri. Importați requests cu un alias: import requests as rq. Descărcați pagina principală cu rq.get(). Într-un comentariu, spuneți când un alias face codul mai ușor de citit și când îl face mai greu de citit.

import requests as rq

BASE_URL = 'https://www.python.org'
response = rq.get(BASE_URL)

# Un alias face codul mai ușor de citit atunci când numele original al bibliotecii 
# este lung și repetitiv, iar comunitatea a adoptat o convenție standard. Astfel se evită 
# aglomerarea vizuală a codului.

# Exercițiul 4. Doar biblioteca standard. Descărcați pagina principală folosind doar urllib.request.urlopen(). Afișați atributul .status al răspunsului și primele 200 de caractere din corp.
# Indiciu: .read() returnează octeți (bytes). Folosiți .decode("utf-8") ca să îi transformați într-un șir de caractere.

import urllib.request

BASE_URL = 'https://www.python.org'

response = urllib.request.urlopen(BASE_URL)
print(response.status)
print(response.read().decode("utf-8")[:200])

# Exercițiul 5. Priviți în interiorul unui modul. Rulați print(dir(requests)). Alegeți trei nume din rezultat și scrieți, într-un comentariu, dacă fiecare este o funcție, o clasă sau un modul.

import requests

print(dir(requests))

# 1. get        -> Este o FUNCȚIE).
# 2. Session    -> Este o CLASĂ.
# 3. exceptions -> Este un MODUL.

# Exercițiul 6. Citiți documentația. Rulați help(requests.get). Găsiți parametrul care setează timpul maxim de așteptare și folosiți-l într-o cerere.

import requests

BASE_URL = 'https://www.python.org'

response = requests.get(BASE_URL, timeout=5)
print(response.status_code)

# Exercițiul 7. Cronometrarea unei cereri. Importați time și măsurați cât durează o cerere către pagina principală, apelând time.perf_counter() înainte și după. Comparați rezultatul cu response.elapsed.

import requests
import time

BASE_URL = 'https://www.python.org'

start = time.perf_counter()
response = requests.get(BASE_URL)
end = time.perf_counter()

print(end - start)
print(response.elapsed) # elapsed - timpul de așteptare în milisecunde 

# Exercițiul 8. Când un import eșuează. Scrieți un script care încearcă import bs4 într-un bloc try / except ImportError. Dacă modulul lipsește, afișați: Instalați modulul cu: pip install beautifulsoup4.
# Verificați-vă: care este diferența dintre un modul, un pachet și o bibliotecă?

try:
    import bs4
    
    html_text = '<html><head><title>Salut!</title></head><body><h1>Hello, world!</h1></body></html>'
    soup = bs4.BeautifulSoup(html_text, 'html.parser')
    
    print(soup.title.string)
    print(soup.body.h1.string)

except ImportError: 
    print('Instalați modulul cu: pip install beautifulsoup4')