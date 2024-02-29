# Třetí krok

import re

def spojit_srt_soubory(soubor1, soubor2, soubor3, soubor4, vystupni_soubor):
    with open(soubor1, 'r', encoding='utf-8') as f1, open(soubor2, 'r', encoding='utf-8') as f2, open(soubor3, 'r', encoding='utf-8') as f3, open(soubor4, 'r', encoding='utf-8') as f4, open(vystupni_soubor, 'w', encoding='utf-8') as vystup:
        posun_casu = 0  # Inicializace proměnné pro posun času
        
        # Pro každý řádek v prvním souboru
        for line in f1:
            vystup.write(line)
        
        # Posun času pro druhý soubor
        posun_casu += ziskat_delku_posledniho_souboru(soubor1)
        
        # Pro každý řádek v druhém souboru
        for line in f2:
            if "-->" in line:  # Pokud je řádek s časovým označením
                casova_oznaceni = line.strip().split(" --> ")
                print(casova_oznaceni)
                nove_casy = posunout_casova_oznaceni(casova_oznaceni, posun_casu)
                vystup.write(f"{nove_casy[0]} --> {nove_casy[1]}\n")
            else:
                vystup.write(line)
        
        # Posun času pro třetí soubor
        posun_casu += ziskat_delku_posledniho_souboru(soubor2)
        
        # Pro každý řádek v třetím souboru
        for line in f3:
            if "-->" in line:  # Pokud je řádek s časovým označením
                casova_oznaceni = line.strip().split(" --> ")
                nove_casy = posunout_casova_oznaceni(casova_oznaceni, posun_casu)
                vystup.write(f"{nove_casy[0]} --> {nove_casy[1]}\n")
            else:
                vystup.write(line)
                
        # Pro každý řádek ve čtvrtém souboru
        for line in f4:
            if "-->" in line:  # Pokud je řádek s časovým označením
                casova_oznaceni = line.strip().split(" --> ")
                nove_casy = posunout_casova_oznaceni(casova_oznaceni, posun_casu)
                vystup.write(f"{nove_casy[0]} --> {nove_casy[1]}\n")
            else:
                vystup.write(line)

def ziskat_delku_posledniho_souboru(soubor):
    # Získat délku posledního času v souboru
    with open(soubor, 'r', encoding='utf-8') as f:
        radky = f.readlines()
        posledni_radka = radky[-2]
        casova_oznaceni = posledni_radka.strip().split(" --> ")
        konecny_cas = casova_oznaceni[1].split(":")
        hodiny, minuty, sekundy_a_milisekundy = konecny_cas
        hodiny = int(hodiny)
        minuty = int(minuty)
        sekundy, _ = sekundy_a_milisekundy.split(",")
        sekundy = int(sekundy)
        delka_casu = (hodiny * 3600 + minuty * 60 + sekundy) * 1000
        print(delka_casu)
        return delka_casu #v milisekundách

def posunout_casova_oznaceni(casova_oznaceni, posun_casu):
    nove_casy = []
    for cas in casova_oznaceni:
        # Odstranění čárky na poslední pozici a posledních tří nul z každého prvku
        cas_bez_carky = re.sub(r',0+$', '', cas)
        # print(f"o kolik se má čas posunout v milisekundách: {posun_casu}")
        
        hodiny, minuty, vteriny = map(int, cas_bez_carky.split(":"))
        celkovy_cas = (hodiny * 3600 + minuty * 60 + vteriny) * 1000
        novy_cas = celkovy_cas + posun_casu
        
        nove_hodiny, zbytek = divmod(novy_cas // 1000, 3600)
        nove_minuty, nove_vteriny = divmod(zbytek, 60)
        nove_milisekundy = novy_cas % 1000
        
        nove_casy.append(f"{nove_hodiny:02d}:{nove_minuty:02d}:{nove_vteriny:02d},{nove_milisekundy:03d}")
    
    return nove_casy

# Příklad použití
soubor1 = "transcript 1.srt"
soubor2 = "transcript 2.srt"
soubor3 = "transcript 3.srt"
soubor4 = "transcript_last.srt"
vystupni_soubor = "vystupni_soubor.srt"

spojit_srt_soubory(soubor1, soubor2, soubor3, soubor4, vystupni_soubor)
