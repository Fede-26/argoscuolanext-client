#!/usr/bin/env python3
import datetime
import argoscuolanext as argo
import pickle
import pprint
pp = pprint.PrettyPrinter(indent=4)

paths = {
	"credenziali": "credenziali.pickle",
	"dati": "dati.pickle"
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
		return all_dati[0], all_dati[1], all_dati[2]

	except FileNotFoundError:
		update_dati()
		return get_dati()


def update_dati():

	credenziali = get_credentials()

	session = argo.Session(credenziali["CODICE_SCUOLA"], credenziali["USERNAME"], credenziali["PASSWORD"])

	all_dati = [
		session.oggi(),
		session.votigiornalieri(),
		session.compiti()
	]

	with open(paths["dati"], 'wb') as handle:
		pickle.dump(all_dati, handle)


def voti(raw):		#tutti i voti assegnati
	for x in reversed(raw["dati"]):
		if x["codVotoPratico"] == 'N':
			voto_pratico = "orale"
		elif x["codVotoPratico"] == 'S':
			voto_pratico = "scritto"
		elif x["codVotoPratico"] == 'P':
			voto_pratico = "pratico"

		print(x["datGiorno"], (x["desMateria"].lower()).capitalize(), ": ", x["codVoto"], " - ", voto_pratico, " (", x["desProva"], ")\n")


def cosa_successo_oggi(raw):
	for x in raw["dati"]:
		try:
			print(x["dati"]["desMateria"], ": ", x["dati"]["desArgomento"], "\n")
		except KeyError:
			pass


def compiti_asse_data(raw):		#compiti assegnati una determinata data
	data = input("Data di assegnamento compiti (mm-gg): ")
	data = '2019-' + data
	print()

	for x in raw["dati"]:
		if x["datGiorno"] == data:
			if x["datCompitiPresente"]:
				data_consegna = "per il " + x["datCompiti"]
			else:
				data_consegna = ''
			print(x["datGiorno"], data_consegna, "-", (x["desMateria"].lower()).capitalize(), ": ", x["desCompiti"], "\n")


def compiti_asse_sett(raw):		#compiti assegnati fino a 7 giorni prima
	oggi = datetime.date.today()
	settimana = []
	for i in range(7):
		settimana.append(oggi - datetime.timedelta(days=i))

	for data in reversed(settimana):
		for x in raw["dati"]:
			# print(data)
			# print(x["datGiorno"])
			if x["datGiorno"] == str(data):
				print(x["datGiorno"], "-", (x["desMateria"].lower()).capitalize(), ": ", x["desCompiti"], "\n")


def main():
	dati_oggi, dati_voti, dati_compiti = get_dati()
	looping = False

	while 1:
		what_view = input("\n\nCosa vuoi vedere? (V)oti, cosa hai fatto (O)ggi, (C)ompiti, (CS)compiti sett. scorsa, (UP)date, (99)exit, [DEBUG: add R for raw output]... ").lower()
		print()

		if what_view == 'v':
			voti(dati_voti)

		elif what_view == 'vr':
			voti_raw = dati_voti
			pp.pprint(voti_raw)

		elif what_view == 'o':
			oggi_raw = dati_oggi
			cosa_successo_oggi(oggi_raw)

		elif what_view == 'or':
			oggi_raw = dati_oggi
			pp.pprint(oggi_raw)

		elif what_view == 'c':
			compiti_raw = dati_compiti
			compiti_asse_dati(compiti_raw)

		elif what_view == 'cr':
			compiti_raw = dati_compiti
			pp.pprint(compiti_raw)

		elif what_view == 'cs':
			compiti_raw = dati_compiti
			compiti_asse_sett(compiti_raw)

		elif what_view == 'up':
			update_dati()
			get_dati()

		elif what_view == '99':
			exit()


if __name__ == '__main__':
	main()
