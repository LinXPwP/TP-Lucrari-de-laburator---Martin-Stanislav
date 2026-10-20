# Laboratorul 6 – Informații invizibile: forensics și steganografie

**Disciplina:** Tehnici de programare  
**Student:** [Nume Prenume]  
**Grupa:** [Grupa]

## Scopul lucrării

În acest laborator am utilizat Python pentru a decoda mesaje, a testa o cheie XOR, a compara hash-uri cu parole dintr-un dicționar și a analiza fișiere. De asemenea, am lucrat cu metadatele unei imagini, am extras o arhivă ZIP ascunsă și am ascuns și recuperat un mesaj prin metoda LSB.

## Lucrarea A – Decoder universal

### A1. Text și octeți

Am transformat textul `Salut` în bytes, apoi în format hexazecimal și înapoi în text.

- Text inițial: `Salut`
- Hexazecimal: `53616c7574`
- Text final: `Salut`

### A2. Recunoașterea tipului de codare

Am creat funcția `ghici_strat()`, care identifică după forma șirului codările URL, HEX și Base64.

Rezultatele testelor au fost: `url`, `hex`, `base64`, `necunoscut`.

### A3. Decodarea mesajelor

Am creat funcția `desfa()` pentru a decoda un singur strat:

- Base64 `U2FsdXQ=` → `Salut`
- HEX `48656c6c6f` → `Hello`
- URL `%53%61%6C%75%74` → `Salut`

### A4. Decodarea mai multor straturi

Am analizat fișierul `probe/mesaj.txt`. Am decodat pe rând două straturi Base64 și un strat HEX.

**Mesaj descoperit:** `FLAG{straturi_de_encoding}`

### A5. XOR cu o cheie de un octet

Am citit `probe/xor.bin` și am încercat toate cele 256 de chei posibile.

- **Cheia găsită:** `128` (adică `0x80`)
- **Mesajul recuperat:** `Un singur octet tine tot secretul... gaseste-l! FLAG{xor_un_octet}`

### A6. Căutarea parolei într-un dicționar

Am comparat primul hash din `probe/hashuri.txt` cu hash-urile MD5 calculate pentru cuvintele din `probe/wordlist.txt`.

- Algoritm: MD5 (hash de 32 de caractere hexazecimale)
- **Parola corespunzătoare primului hash:** `password`

### A7. Fișă JSON și test

Am adăugat argumente pentru rularea decoderului din terminal și salvarea rezultatului în `arsenal/forensics/fisa.json`. Am creat și `teste/test_decode.py`, care verifică decodarea Base64 pentru textul `Salut`.

**Test:** a fost raportat ca funcțional la rularea locală.

## Lucrarea B – Forensics pe fișiere și steganografie

### B1. Identificarea tipului real

Am citit primii octeți ai fișierelor pentru a identifica formatul după semnătura binară.

- `probe/foto.jpg` → JPEG
- `probe/ascuns.png` → PNG

### B2. Text citibil dintr-un fișier binar

Am folosit expresia regulată `rb"[ -~]{4,}"` pentru a identifica secvențe de minimum patru caractere imprimabile din `probe/ascuns.png`.

**Observație:** rezultatul exact afișat la B2 trebuie completat din terminal: [completează dacă este necesar].

### B3. Metadate EXIF și GPS

Am analizat metadatele imaginii `probe/foto.jpg`. Conform fișierului generator, acestea includ:

- Producător: `Apple`
- Model: `iPhone 13`
- Data: `2026:09:14 10:30:00`
- Latitudine: aproximativ `47.0167° N`
- Longitudine: `28.8575° E`
- Localitate indicată de coordonate: Chișinău

**Notă:** confirmă că aceste valori au fost efectiv afișate de programul B3; în funcție de versiunea Pillow, scrierea/citirea GPS poate necesita ajustări.

### B4. Extragerea arhivei ZIP ascunse

Am căutat semnătura `PK\x03\x04` în fișierul `probe/ascuns.png` și am salvat datele începând de la semnătură în `gasit.zip`.

Conform generatorului, arhiva conține `secret.txt`, cu mesajul:

**`FLAG{ascuns_prin_carving}`**

### B5. Ascunderea unui mesaj prin LSB

Am ascuns textul `FLAG{ascuns_in_pixeli}` în ultimii biți ai canalelor RGB ai imaginii. Am adăugat un octet zero pentru a marca sfârșitul mesajului și am salvat rezultatul în `stego.png`, în format PNG fără pierderi.

### B6. Recuperarea mesajului LSB

Am citit ultimii biți ai canalelor RGB din `stego.png`, i-am grupat câte opt și i-am transformat în caractere, oprindu-mă la octetul zero.

**Mesaj așteptat:** `FLAG{ascuns_in_pixeli}`  
**Rezultat efectiv în terminal:** [confirmă după rularea B6]

## Concluzie

În laborator am învățat să lucrăm cu bytes, codări Base64/HEX/URL, operația XOR, hash-uri, semnături de fișiere și metadate EXIF. Am observat și cum pot exista date ascunse într-un fișier și cum un mesaj poate fi ascuns în pixelii unei imagini prin LSB.

## Fișiere pentru predare

- `arsenal/forensics/decode.py`
- `arsenal/forensics/fisa.json`
- `teste/test_decode.py`
- `forensics.py`
- `stego.png`
- `raport.md`

Predarea se face prin **git commit** și **git push**, conform cerințelor laboratorului.
