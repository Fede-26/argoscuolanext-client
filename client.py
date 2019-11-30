#!/usr/bin/env python3
import re
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

        if new_cred.lower() == 'y':
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

    what_view = input("cosa vuoi vedere? (V)oti, cosa hai fatto (O)ggi, [DEBUG: (VR) voti_raw]... ").lower()
    print()
    if what_view == 'v':
        voti_raw = session.votigiornalieri()
        # print(voti_raw["dati"][1]["desMateria"])
        for x in voti_raw["dati"]:
            print(x["datGiorno"], x["desMateria"].lower(), ": ", x["codVoto"])
    elif what_view == 'vr':
        voti_raw = session.votigiornalieri()
        pp.pprint(voti_raw)

    # pp.pprint(session.votigiornalieri())

    elif what_view == 'o':
        cosa_successo = session.oggi()
        pp.pprint(cosa_successo)


if __name__ == '__main__':
    main()


"""
codVotoPratico: -N orale
                -S scritto
                -P pratico
"""
