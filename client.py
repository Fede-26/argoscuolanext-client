#!/usr/bin/env python3
import re
import argoscuolanext as argo
import pickle
import json
import pprint
pp = pprint.PrettyPrinter(indent=4)


def voti(dict):
	for x in dict["dati"]:

		if x["codVotoPratico"] == 'N':
			voto_pratico = "orale"
		elif x["codVotoPratico"] == 'S':
			voto_pratico = "scritto"
		elif x["codVotoPratico"] == 'P':
			voto_pratico = "pratico"

		print(x["datGiorno"], (x["desMateria"].lower()).capitalize(), ": ", x["codVoto"], " - ", voto_pratico, " (", x["desProva"], ")\n")


def cosa_successo_oggi(dict):
	for x in dict["dati"]:
		print(x["dati"]["desMateria"], ": ", x["dati"]["desArgomento"], "\n")        


def compiti_assegnati(dict):
	data = input("Data di assegnamento compiti (mm-gg): ")
	data = '2019-' + data
	print()
	for x in dict["dati"]:
		if x["datGiorno"] == data:
			if x["datCompitiPresente"]:
				data_consegna = "per il " + x["datCompiti"]
			else:
				data_consegna = ''
			print( x["datGiorno"], data_consegna, "-", (x["desMateria"].lower()).capitalize(), ": ", x["desCompiti"], "\n")


def main():

	try:

		with open('credenziali.pickle', 'rb') as handle:
			credenziali = pickle.load(handle)

	except FileNotFoundError:

		make_new_cred = input("file con credenziali non trovato, crearne di nuove? y/N ")

		credenziali = {}
		credenziali["CODICE_SCUOLA"] = input("codice scuola: ")
		credenziali["USERNAME"] = input("nome utente: ")
		credenziali["PASSWORD"] = input("password: ")

		if make_new_cred.lower() == 'y':
			print("--ATTENZIONE: dati salvati nel file credenziali.pickle, non dare a nessuno questo file e non cancellarlo, altrimenti dovrai reimpostare le credenziali")

			with open('credenziali.pickle', 'wb') as handle:
				pickle.dump(credenziali, handle)

	session = argo.Session(credenziali["CODICE_SCUOLA"], credenziali["USERNAME"], credenziali["PASSWORD"])

	while 1:

		what_view = input("\n\nCosa vuoi vedere? (V)oti, cosa hai fatto (o)ggi, (C)ompiti, (99)exit, [DEBUG: add R for raw output]... ").lower()
		print()

		if what_view == 'v':
			voti(session.votigiornalieri())

		elif what_view == 'vr':
			voti_raw = session.votigiornalieri()
			pp.pprint(voti_raw)

		elif what_view == 'o':
			oggi_raw = session.oggi()
			cosa_successo_oggi(oggi_raw)

		elif what_view == 'or':
			oggi_raw = session.oggi()
			pp.pprint(oggi_raw)

		elif what_view == 'c':
			compiti_raw = session.compiti()
			compiti_assegnati(compiti_raw)

		elif what_view == 'cr':
			compiti_raw = session.compiti()
			pp.pprint(compiti_raw)

		elif what_view == '99':
			exit()


if __name__ == '__main__':
    main()
