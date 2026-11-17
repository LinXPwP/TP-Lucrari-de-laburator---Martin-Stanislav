
# A1 + A2

from dataclasses import dataclass, asdict
import json

CAI_SUSPECTE = ("\\Temp\\", "\\Roaming\\")


@dataclass
class Proces:
    pid: int
    nume: str
    user: str
    cale: str

    # A2 - Verificarea procesului
    def e_suspect(self):
        return any(c in self.cale for c in CAI_SUSPECTE)


# Testare A1 + A2

p = Proces(
    3120,
    "update.exe",
    "ana",
    r"C:\Users\ana\AppData\Local\Temp\update.exe"
)

print(p.pid, p.nume)
print(p)
print(p.e_suspect())

# python -m arsenal.windows.inventar


# A3 - 
# python -m arsenal.windows.inventar

SUSPECTE_ID = {4625, 1102, 7045}

@dataclass
class Eveniment:
    id: int
    nivel: str
    sursa: str
    cont: str
    mesaj: str

    def e_suspect(self):
        return self.id in SUSPECTE_ID or self.nivel == "critical"



# Testare A3

e1 = Eveniment(
    4625,
    "warning",
    "Security",
    "administrator",
    "An account failed to log on"
)

e2 = Eveniment(
    1000,
    "information",
    "Application",
    "ana",
    "Application started"
)

e3 = Eveniment(
    1000,
    "critical",
    "System",
    "SYSTEM",
    "Critical system event"
)

print("Eveniment 1:", e1.e_suspect())
print("Eveniment 2:", e2.e_suspect())
print("Eveniment 3:", e3.e_suspect())

# A4
# python -m arsenal.windows.inventar

def procese_din_json(cale):
    with open(cale, encoding="utf-8") as f:
        return [Proces(**d) for d in json.load(f)]


# Testare A4

procese = procese_din_json(
    "arsenal/windows/start/procese.json"
)

print("procese:", len(procese))

print(
    "suspecte:",
    sum(1 for p in procese if p.e_suspect())
)




# B1 + B2
# python -m arsenal.windows.inventar

@dataclass
class Inventar:
    procese: list

    # B1 - Incarcarea proceselor din JSON
    @classmethod
    def din_json(cls, cale):
        with open(cale, encoding="utf-8") as f:
            return cls([Proces(**d) for d in json.load(f)])

    def __len__(self):
        return len(self.procese)

    # B2 - Selectarea proceselor suspecte
    def suspecte(self):
        rezultat = []

        for p in self.procese:
            if p.e_suspect():
                rezultat.append(p)

        return rezultat

    # B2 - Gruparea proceselor dupa utilizator
    def pe_user(self):
        rezultat = {}

        for p in self.procese:
            rezultat.setdefault(p.user, []).append(p.nume)

        return rezultat




# Testare B1

if __name__ == "__main__":
    inv = Inventar.din_json(
        "arsenal/windows/start/procese.json"
    )

    print("procese:", len(inv))


# B3 

# Rulare normala:
# python -m arsenal.windows.inventar arsenal/windows/start

# Rulare JSON:
# python -m arsenal.windows.inventar arsenal/windows/start --json


def evenimente_din_json(cale):
    with open(cale, encoding="utf-8") as f:
        return [Eveniment(**d) for d in json.load(f)]


def main():
    import argparse

    p = argparse.ArgumentParser()

    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")

    a = p.parse_args()

    inv = Inventar.din_json(a.capturi + "/procese.json")
    ev = evenimente_din_json(a.capturi + "/evenimente.json")

    alarma = [e for e in ev if e.e_suspect()]

    if a.json:
        raport = {
            "procese_suspecte": [
                asdict(p) for p in inv.suspecte()
            ],
            "evenimente_alarma": [
                asdict(e) for e in alarma
            ]
        }

        print(json.dumps(raport, indent=4, ensure_ascii=False))

    else:
        print(f"Procese: {len(inv)} | suspecte: {len(inv.suspecte())}")

        for p in inv.suspecte():
            print(f" [{p.pid}] {p.nume} ({p.user}) {p.cale}")

        print(f"Evenimente: {len(ev)} | alarma: {len(alarma)}")

        for e in alarma:
            print(f" {e.id} [{e.nivel}] {e.cont}: {e.mesaj}")


if __name__ == "__main__":
    main()
