#!/usr/bin/env python3

# applicazione per fare il login e recuperare i dati

import argoscuolanext as argo
import pickle
import os

paths = {
	"credenziali": "../dati/credenziali.pickle",
	"dati": "../dati/dati.pickle"
}


def get_credentials():
	try:
		with open(paths["credenziali"], 'rb') as handle:
			cred = pickle.load(handle)

	except FileNotFoundError:
		make_new_cred = input("file con credenziali non trovato, crearne di nuove? y/N ")
		cred = {}
		cred["CODICE_SCUOLA"] = input("codice scuola: ")
		cred["USERNAME"] = input("nome utente: ")
		cred["PASSWORD"] = input("password: ")

		if make_new_cred.lower() == 'y':
			print("--ATTENZIONE: dati salvati nel file credenziali.pickle, non dare a nessuno questo file e non cancellarlo, altrimenti dovrai reimpostare le credenziali")
			with open(paths["credenziali"], 'wb') as handle:
				pickle.dump(cred, handle)

	return cred


def get_dati():
	try:
		with open(paths["dati"], 'rb') as handle:
			all_dati = pickle.load(handle)
		return all_dati[0], all_dati[1], all_dati[2], all_dati[3]

	except FileNotFoundError:
		update_dati()
		return get_dati()


def update_dati():
	credenziali = get_credentials()
	session = argo.Session(credenziali["CODICE_SCUOLA"], credenziali["USERNAME"], credenziali["PASSWORD"])

	all_dati = [
		session.oggi(),
		session.votigiornalieri(),
		session.compiti(),
		session.promemoria()
	]

	try:
		os.remove(paths["dati"])
	except FileNotFoundError:
		pass
	with open(paths["dati"], 'wb') as handle:
		pickle.dump(all_dati, handle)
