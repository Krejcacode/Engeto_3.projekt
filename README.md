# Engeto_3.projekt
Třetí Projekt k Python Academii. Webscrapovaní výsledků voleb
## Popis projektu 
Tento projekt slouží k extrahování výsledků parlamentních voleb z roku 2021 ze stránky [volby.cz]([https://www.volby.cz/pls/ps2021/ps3?xjazyk=CZ)
## Instalace knihoven
Knihovny, které jsou použity v kódu jsou uložené v souboru `requirements.txt`. Pro instalaci je vhodné použít nové virtuální prostředí.
```bash
python -m venv moje_virt_prostredi       #Vytvoření virtuálního prostředí
moje-virt-prostredi\Scripts\activate     #Aktivace virtuálního prostředí
pip install requests                     #Instalování knihoven
```
## Spuštění projektu
Spuštění souboru `main.py` v příkazovém řádku je třeba spustit s dvoumi povinnými argumenty.
```bash
python main.py <odkaz-uzemniho-celku> <vysledny-soubor>
```
Výsledný soubor potřebuje obsahovat příponu `csv`. Do souboru se potom stáhnou výsledky.
## Ukázka projektu
Například si zvolím, že chci vyscrapovat výsledky z okresu Beroun.
Soubor si pojmenuju vysledky_beroun pro jednoduchost.
1.argument `https://www.volby.cz/pls/ps2021/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2102`
2.argument `vysledky_beroun.csv`
Spuštění programu:
```bash
python main.py 'https://www.volby.cz/pls/ps2021/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2102' 'vysledky_beroun.csv'
```
Průběh programu:
```bash
Stahuji odkazy na obce z https://www.volby.cz/pls/ps2021/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2102
Nalezeno 85 obcí. Začínám stahovat data...
Hotovo! Data byla uložena do vysledky_beroun.csv
```
Částečný výstup:
```bash
kód obce;název obce;registrovaní;obálky;platné;ALIANCE NÁRODNÍCH SIL;ANO 2011...
534421;Bavoryně;282;173;173;0;41;0;0;5;1;0;29;18;0;46;1;17;8;1;2;4;0
531057;Beroun;14753;9780;9739;3;2 190;13;14;343;16;33;1 865;487;19;3 170;80;688;278;8;99;391;42
531081;Broumy;765;560;560;4;159;4;2;25;1;5;126;26;2;114;8;26;12;2;1;36;7
.....
```
  

