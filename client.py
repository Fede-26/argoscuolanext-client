#!/usr/bin/env python3
import argoscuolanext  # to install it run "pip3 install --user argoscuolanext"
import pickle
import json
import pprint
pp = pprint.PrettyPrinter(indent=4)


def main():

    try:

        with open('credenziali.pickle', 'rb') as handle:
            credenziali = pickle.load(handle)

    except FileNotFoundError:

        new_cred = input("file con credenziali non trovato, crearne di nuove? y/N ")

        if new_cred.lower() == "y":
            credenziali = {}
            credenziali["CODICE_SCUOLA"] = input("codice scuola: ")
            credenziali["USERNAME"] = input("nome utente: ")
            credenziali["PASSWORD"] = input("password: ")
            print("--ATTENZIONE: dati salvati nel file credenziali.pickle, non dare a nessuno questo file e non cancellarlo, altrimenti dovrai reimpostare le credenziali")

            with open('credenziali.pickle', 'wb') as handle:
                pickle.dump(credenziali, handle)

        else:
            print("USCITA DAL PROGRAMMA")
            quit()

    session = argoscuolanext.Session(
        credenziali["CODICE_SCUOLA"], credenziali["USERNAME"], credenziali["PASSWORD"])

    pp.pprint(session.votigiornalieri())
    #voti_json = json.loads(str(session.votigiornalieri()))
    # print(voti_json)
    #print(json.dumps(voti_json, indent=4, sort_keys=True))


if __name__ == '__main__':
    main()
