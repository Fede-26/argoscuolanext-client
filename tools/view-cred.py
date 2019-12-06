#!/usr/bin/env python3
import pickle
import pprint
pp = pprint.PrettyPrinter(indent=4)

paths = {
	"credenziali": "../credenziali.pickle",
	"dati": "../dati.pickle"
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

pp.pprint(get_credentials())
