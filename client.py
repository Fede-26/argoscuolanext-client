#!/usr/bin/env python3
import datetime
import argoscuolanext as argo
import pickle
import pprint
pp = pprint.PrettyPrinter(indent=4)

paths = {
	"credenziali": "credenziali.pickle",
	"data": "data.pickle"
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


def get_data():
	try:
		with open(paths["data"], 'rb') as handle:
			all_data = pickle.load(handle)
		return all_data[0], all_data[1], all_data[2]

	except FileNotFoundError:
		update_data()
		return get_data()


def update_data():

	credenziali = get_credentials()

	session = argo.Session(credenziali["CODICE_SCUOLA"], credenziali["USERNAME"], credenziali["PASSWORD"])

	all_data = [
		session.oggi(),
		session.votigiornalieri(),
		session.compiti()
	]

	with open(paths["data"], 'wb') as handle:
		pickle.dump(all_data, handle)


def voti(raw):
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


def compiti_asse_data(raw):
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


def compiti_asse_sett(raw):
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
	data_oggi, data_voti, data_compiti = get_data()
	looping = False

	while 1:
		what_view = input("\n\nCosa vuoi vedere? (V)oti, cosa hai fatto (O)ggi, (C)ompiti, (CS)compiti sett. scorsa, (UP)date, (99)exit, [DEBUG: add R for raw output]... ").lower()
		print()

		if what_view == 'v':
			voti(data_voti)

		elif what_view == 'vr':
			voti_raw = data_voti
			pp.pprint(voti_raw)

		elif what_view == 'o':
			oggi_raw = data_oggi
			cosa_successo_oggi(oggi_raw)

		elif what_view == 'or':
			oggi_raw = data_oggi
			pp.pprint(oggi_raw)

		elif what_view == 'c':
			compiti_raw = data_compiti
			compiti_asse_data(compiti_raw)

		elif what_view == 'cr':
			compiti_raw = data_compiti
			pp.pprint(compiti_raw)

		elif what_view == 'cs':
			compiti_raw = data_compiti
			compiti_asse_sett(compiti_raw)

		elif what_view == 'up':
			update_data()
			get_data()

		elif what_view == '99':
			exit()


if __name__ == '__main__':
	main()
