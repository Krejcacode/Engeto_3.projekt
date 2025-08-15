"""
main.py: třetí projekt do Engeto Online Python Akademie

author: Martin Krejčiřík
email: krejcirikmartin9@gmail.com
"""
# Instalace potřebných knihoven:
import sys
import re
import csv
import requests
from bs4 import BeautifulSoup


def zkontroluj_argumenty():
    """Ověří, že byly zadány správné argumenty:
    1. Odkaz na územní celek (URL z volby.cz)
    2. Název výstupního CSV souboru."""
    if len(sys.argv) != 3 or not sys.argv[1].startswith("https://www.volby.cz/pls/ps2021/") or not sys.argv[2].endswith(".csv"):
        print("Chyba: Zadejte 2 argumenty: [odkaz_na_územní_celek] [vystupni_soubor.csv]")
        print("Příklad: python main.py 'https://www.volby.cz/pls/ps2021/ps32?...' 'vysledky.csv'")
        sys.exit(1)
    return sys.argv[1], sys.argv[2]


def stahni_stranku(url):
    """Stáhne HTML stránku a vrátí ji jako objekt BeautifulSoup."""
    stranka = requests.get(url)
    if stranka.status_code != 200:
        print(f"Chyba: nepodařilo se stáhnout stránku (status code {stranka.status_code})")
        sys.exit(1)
    return BeautifulSoup(stranka.text, "html.parser")


def ziskej_odkazy_na_obce(soup, base_url):
    """Najde unikátní odkazy na stránky jednotlivých obcí."""
    odkazy = set()
    for a in soup.find_all("a", href=True): # Projde všechny odkazy na stránce
        if "xobec" in a["href"] and "xvyber" in a["href"]: # Odkaz musí obsahovat parametry xobec a xvyber
            odkazy.add(base_url + a["href"]) # Přidá základní URL k odkazu
    return list(odkazy)


def najdi_text(soup, selector):
    """Vrátí text elementu podle CSS selektoru, nebo prázdný řetězec, pokud neexistuje."""
    element = soup.select_one(selector) # Použije CSS selektor pro vyhledání elementu
    return element.text.strip().replace("\xa0", "") if element else "" 


def ziskej_data_obce(soup, url_obce):
    """Získá kód obce, název, počty voličů, obálek, platných hlasů
    a hlasy pro jednotlivé strany z detailní stránky obce."""
    data = {}

    # Kód obce z URL (parametr xobec)
    match = re.search(r"xobec=(\d+)", url_obce)
    data["kód obce"] = match.group(1) if match else ""

    # Název obce
    for h3 in soup.find_all("h3"):
        if h3.get_text(strip=True).startswith("Obec:"): # Hledá H3 s textem začínajícím na "Obec:"
            data["název obce"] = h3.get_text(strip=True).replace("Obec: ", "") # Vyčistí text od "Obec: "
            break

    # Základní údaje
    data["registrovaní"] = najdi_text(soup, "td.cislo[headers='sa2']")
    data["obálky"] = najdi_text(soup, "td.cislo[headers='sa5']")
    data["platné"] = najdi_text(soup, "td.cislo[headers='sa6']")

    # Hlasy pro strany
    data.update(ziskej_strany_a_hlasy(soup)) # Přidá hlasy pro strany do slovníku
    return data


def ziskej_strany_a_hlasy(soup):
    """Vrátí slovník {název strany: počet hlasů} ze všech částí tabulek na stránce."""
    strany = {}
    for h3 in soup.find_all("h3"): # Projde všechny H3 elementy
        if "část" in h3.get_text(): # Hledá H3, které obsahují slovo "část"
            tab = h3.find_next("table")
            if not tab:
                continue
            for tr in tab.find_all("tr"): # Projde všechny řádky tabulky
                bunky = tr.find_all("td") 
                if len(bunky) >= 3: # Ověří, že řádek má alespoň 3 buňky
                    nazev = bunky[1].get_text(strip=True) # Název strany je ve druhé buňce
                    hlasy = bunky[2].get_text(strip=True) # Hlasy jsou ve třetí buňce
                    strany[nazev] = hlasy
    return strany


def uloz_csv(seznam_obci, vystupni_soubor):
    """Uloží seznam slovníků s daty obcí do CSV souboru.
    Sloupce pro strany se vytvoří dynamicky podle všech záznamů."""
    if not seznam_obci:
        print("Žádná data k uložení.")
        return

    hlavicka = ["kód obce", "název obce", "registrovaní", "obálky", "platné"]

    # Přidání všech unikátních názvů stran
    vsechny_strany = sorted({klic for obec in seznam_obci for klic in obec if klic not in hlavicka})   # Seřadí názvy stran
    hlavicka.extend(vsechny_strany) 

    with open(vystupni_soubor, "w", newline="", encoding="utf-8-sig") as f: # Otevře soubor pro zápis
        writer = csv.writer(f, delimiter=';') # Použije středník jako oddělovač
        writer.writerow(hlavicka) # Zapíše hlavičku do CSV
        for obec in seznam_obci:
            radek = [obec.get(sloupec, "0") for sloupec in hlavicka] # Vytvoří řádek s daty obce podle hlavičky
            writer.writerow(radek) 

# Hlavní část programu

if __name__ == "__main__": 
    odkaz, vystupni_soubor = zkontroluj_argumenty() 
    base_url = "https://www.volby.cz/pls/ps2021/" # Základní URL pro odkazy na obce

    print(f"Stahuji odkazy na obce z {odkaz}") 
    soup = stahni_stranku(odkaz) 
    odkazy_na_obce = ziskej_odkazy_na_obce(soup, base_url)

    if not odkazy_na_obce: 
        print("Chyba: Nepodařilo se najít žádné odkazy na obce.")
        sys.exit(1)

    print(f"Nalezeno {len(odkazy_na_obce)} obcí. Začínám stahovat data...")
    vsechna_data = [] 
    for odkaz_obec in odkazy_na_obce:
        soup_obec = stahni_stranku(odkaz_obec)
        vsechna_data.append(ziskej_data_obce(soup_obec, odkaz_obec))

    uloz_csv(vsechna_data, vystupni_soubor)
    print(f"Hotovo! Data byla uložena do {vystupni_soubor}")