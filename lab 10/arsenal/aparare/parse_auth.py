# A1

import re

TIPAR = re.compile(r"Failed password for (?:invalid user )?(\S+) from (\S+) port")

def exec(linie):
    m = TIPAR.search(linie)

    if m is None:
        return None

    return (m.group(1), m.group(2))


print(exec("Failed password for root from 203.0.113.9 port 51230 ssh2"))
print(exec("<linie stricata fara structura>"))

# A2

def citeste_esecuri(cale):
    esecuri = []

    try:
        f = open(cale, encoding="utf-8")
    except FileNotFoundError:
        print("nu gasesc", cale)
        return esecuri

    with f:
        for linie in f:
            r = exec(linie)

            if r is not None:
                esecuri.append({
                    "user": r[0],
                    "ip": r[1],
                })
    return esecuri

esecuri = citeste_esecuri("arsenal/aparare/start/auth.log")
print("esecuri:", len(esecuri))


# A3
from collections import Counter

fruct = ["mar", "para", "mar", "banana", "mar", "para"]
rezultat = Counter(fruct)
print(rezultat)

def pe_ip(esecuri):
    return Counter(e["ip"] for e in esecuri)

counts = pe_ip(esecuri)

for ip, n in counts.most_common(10):
    print(f"{ip}: {n}")


# A4

def main():
    esecuri = citeste_esecuri("arsenal/aparare/start/auth.log")
    counts = pe_ip(esecuri)

    print(f"Esecuri de autentificare: {len(esecuri)}")

    for ip, n in counts.most_common():
        print(f"{ip}: {n}")

if __name__ == "__main__":
    main()