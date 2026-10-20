# A1
print("\n--- A1 ---")

s = "Salut"
print("Text original:", s)

b = s.encode()
print("Bytes:", b)

hex_text = b.hex()
print("Hexadecimal:", hex_text)

b_refacut = bytes.fromhex(hex_text)
print("Bytes refacuti:", b_refacut)

print("Text final:", b_refacut.decode())


# A2 

import re

def ghici_strat(s):

    if re.search(r"%[0-9A-Fa-f]{2}", s):
        return "url"

    if re.fullmatch(r"[0-9A-Fa-f]+", s) and len(s) % 2 == 0:
        return "hex"

    if re.fullmatch(r"[A-Za-z0-9+/]+={0,2}", s) and len(s) % 4 == 0:
        return "base64"

    return "necunoscut"


print("\n--- A2 ---")
print(ghici_strat("%2Fetc"))
print(ghici_strat("48656c6c6f"))
print(ghici_strat("U2FsdXQ="))
print(ghici_strat("Salut lume!"))


# A3

import base64
from urllib.parse import unquote

def desfa(s):
    strat = ghici_strat(s)

    if strat == "base64":
        rezultat = base64.b64decode(s)

    elif strat == "hex":
        rezultat = bytes.fromhex(s)

    elif strat == "url":
        rezultat = unquote(s).encode()

    else:
        rezultat = s.encode()

    return strat, rezultat


# Testam functia
print("\n--- A3 ---")

print(desfa("U2FsdXQ="))
print(desfa("48656c6c6f"))
print(desfa("%53%61%6C%75%74"))


# A4

def citibil(b):
    return all(32 <= c < 127 for c in b)


print("\n--- A4 ---")

with open("probe/mesaj.txt", "r") as f:
    val = f.read().strip()

for i in range(8):
    strat, b = desfa(val)

    print("Strat:", strat)
    print("Rezultat:", b)

    if strat == "necunoscut":
        break

    val = b.decode()

    if val.startswith("FLAG{"):
        print("Mesaj final:", val)
        break


# A5 

print("\n--- A5 ---")

with open("probe/xor.bin", "rb") as f:
    date = f.read()

for k in range(256):

    clar = bytes(b ^ k for b in date)

    if citibil(clar):
        print("Cheie gasita:", k)
        print("Mesaj:", clar.decode())
        break


# A6

import hashlib

print("\n--- A6 ---")

with open("probe/hashuri.txt", "r") as f:
    tinta = f.readline().strip()

print("Lungime hash:", len(tinta))

with open("probe/wordlist.txt", "r") as f:

    for cuv in f:
        cuv = cuv.strip()

        hash_cuv = hashlib.md5(cuv.encode()).hexdigest()

        if hash_cuv == tinta:
            print("Parola gasita:", cuv)
            break


# A7

import argparse
import json
import os

def a7():
    p = argparse.ArgumentParser()

    p.add_argument("intrare")
    p.add_argument("--fisier", action="store_true")

    a = p.parse_args()

    if a.fisier:
        with open(a.intrare, "rb") as f:
            mesaj = f.read().decode()
    else:
        mesaj = a.intrare

    strat, rezultat = desfa(mesaj)

    fisa = {
        "strat": strat,
        "rezultat": rezultat.decode()
    }

    os.makedirs("arsenal/forensics", exist_ok=True)

    with open("arsenal/forensics/fisa.json", "w",
              encoding="utf-8") as f:
        json.dump(fisa, f, indent=4)

    print("Strat:", strat)
    print("Rezultat:", rezultat.decode())
    print("Fisierul fisa.json a fost creat!")

def main():
    a7()
