
# B1

def tip_real(cale):

    with open(cale, "rb") as f:
        cap = f.read(8)

    if cap.startswith(b"%PDF"):
        return "pdf"

    if cap.startswith(b"\x89PNG"):
        return "png"

    if cap.startswith(b"\xff\xd8"):
        return "jpeg"

    if cap.startswith(b"PK\x03\x04"):
        return "zip/docx"

    return cap.hex()


print("--- B1 ---")
print("foto.jpg:", tip_real("probe/foto.jpg"))
print("ascuns.png:", tip_real("probe/ascuns.png"))


# B2

import re

print("\n--- B2 ---")

with open("probe/ascuns.png", "rb") as f:
    date = f.read()

texte = re.findall(rb"[ -~]{4,}", date)

for text in texte:
    print(text.decode())



# B3

from PIL import Image
from PIL.ExifTags import TAGS

print("\n--- B3 ---")

img = Image.open("probe/foto.jpg")

exif = img.getexif()

for id, val in exif.items():
    print(TAGS.get(id, id), "=", val)

gps = exif.get_ifd(34853)

if gps:
    lat = gps[2]
    lon = gps[4]

    latitudine = float(lat[0]) + float(lat[1])/60 + float(lat[2])/3600
    longitudine = float(lon[0]) + float(lon[1])/60 + float(lon[2])/3600

    if gps[1] == "S":
        latitudine = -latitudine

    if gps[3] == "W":
        longitudine = -longitudine

    print("Latitudine:", latitudine)
    print("Longitudine:", longitudine)

else:
    print("Nu exista date GPS.")


# B4

print("\n--- B4 ---")

with open("probe/ascuns.png", "rb") as f:
    date = f.read()


i = date.find(b"PK\x03\x04")

if i != -1:

    with open("gasit.zip", "wb") as f:
        f.write(date[i:])

    print("Arhiva extrasa de la octetul:", i)
    print("Fisierul gasit.zip a fost creat!")

else:
    print("Nu am gasit arhiva ZIP.")



# B5

from PIL import Image

print("\n--- B5 ---")

img = Image.open("probe/foto.jpg").convert("RGB")

px = list(img.getdata())

mesaj = b"FLAG{ascuns_in_pixeli}"

mesaj = mesaj + b"\x00"

biti = "".join(f"{x:08b}" for x in mesaj)

px_nou = []

i = 0

for r, g, b in px:

    if i < len(biti):
        r = (r & ~1) | int(biti[i])
        i += 1

    if i < len(biti):
        g = (g & ~1) | int(biti[i])
        i += 1

    if i < len(biti):
        b = (b & ~1) | int(biti[i])
        i += 1
    px_nou.append((r, g, b))

img.putdata(px_nou)

img.save("stego.png")

print("Mesaj ascuns cu succes!")
print("Imagine creata: stego.png")



# B6

print("\n--- B6 ---")

img = Image.open("stego.png").convert("RGB")

px = list(img.getdata())

biti = ""

for r, g, b in px:
    biti += str(r & 1)
    biti += str(g & 1)
    biti += str(b & 1)

mesaj = ""

for i in range(0, len(biti), 8):

    octet = biti[i:i+8]

    if len(octet) < 8:
        break

    numar = int(octet, 2)

    if numar == 0:
        break
    mesaj += chr(numar)

print("Mesaj descoperit:", mesaj)
