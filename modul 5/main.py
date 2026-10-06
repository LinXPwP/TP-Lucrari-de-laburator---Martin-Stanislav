import argparse

# Exercițiul 44 și 45: Importarea anumitor nume
from webtools import site_report, check_paths, save_paths_to_csv, get_title, security_headers

def main():
    # Exercițiul 48: Argumente din linia de comandă (modificat pentru a rula și fără argumente)
    parser = argparse.ArgumentParser(description="Proiect Final WebLab")
    
    # Am adăugat nargs="?" și default="https://cybercor.org"
    parser.add_argument(
        "url", 
        nargs="?", 
        default="https://cybercor.org", 
        help="Adresa URL țintă (ex: https://cybercor.org)"
    )
    args = parser.parse_args()

    # Rulăm Exercițiul 50: Generează raportul în consolă și crează report.json
    site_report(args.url)

    # Rulăm Exercițiul 49: Creăm report.csv
    cai_de_test = ["/admin", "/private", "/robots.txt"]
    rezultate = check_paths(args.url, cai_de_test)
    save_paths_to_csv(rezultate)

if __name__ == "__main__":
    main()