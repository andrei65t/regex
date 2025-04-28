# Conversia unei expresii regulate in automat finit determinist (DFA)
## Obiectiv: implementarea unui program care primeste expresii regulate si construieste un automat finit determinist echivalent.
### Structura proiectului:
  -`regex.json` in care se afla 20 de teste pentru a verifica functionalitatea progamului
  
  -`regex.py` program in Python care citeste regex.json, transforma in notatie postfixata si se construieste NFA ul folosind postfixul utilizand algoritmul lui Thompson. Ulterior se realizeaza converterste intr-un DFA echivalent, iar folosind functia de verificare a cuvintelor putem testa datele citite din fisierul json.

### Modul de rulare:
Programul a fost scris in python si se ruleaza cu `python3 regex.py` programul ocupandu-se de citirea din fisier si efectuarea sarcinilor

### Deciziile luate in implementare
  Pentru primul pas am avut nevoie sa marchez concatenarea cu un operator (pentru acesta am ales `.`) ulterior am transormat regexul in notatia sa postfixata in care am folosit o stiva pentru a retine operanzii pe aceasta.
  
Avand notatia postfixata am folsit algoritmul lui Thompson pentru a construi NFA-ul, la citirea unui caracter adaugam pe stiva nfa construit la acest pas, in momentul in care intalnim concatenare scoatem ultimele 2 NFA-uri din stiva si le unim printr-o tranztie epsilon. Pentru operatorul de alternare extragem ultimele doua NFA-uri din stiva, cream un nou start si un nou accept si adaugam tranzitii epsilon de la noul start catre starturile celor doua NFA-uri si de la accepturile lor catre noul accept. Pentru operatorul de repetare de zero sau mai multe ori adaugam tranzitii epsilon de la noul start catre startul vechi si noul accept si din acceptul vechi inapoi catre startul vechi si noul accept. Asemenea am realizat si operatorul repetare odata sau de mai multe ori, dar nu adaugam tranzitie directa de la noul start la noul accept. Pentru prezenta optionala cream start si accept si legam prin epsilon startul vechi si acceptul nou.

Dupa construirea NFA-ului l-am transformat in DFA folosind constructia prin multimi, iar tranzitiile se fac dupa mutarea pe un simbol si recalcularea epsilon-closure, in care calculeaza toate starile accesibile fara sa se consume litere

Dupa construirea DFA-ului, am verificat cuvintele de test parcurgand automatul litera cu litera si acceptand un cuvant doar daca dupa consumarea completa a ajuns intr-o stare finala.
