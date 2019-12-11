#!/usr/bin/env python3

# applicazione principale (avviare questa)


import datetime
import os
import sys
import pprint
pp = pprint.PrettyPrinter(indent=4)
sys.path.append("../modules")
import gestdati as gsd


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


def promemoria(raw):
	oggi = datetime.date.today()
	for x in raw["dati"]:
		if x["datGiorno"] >= str(oggi):
			print(x["datGiorno"] + " :  " + x["desAnnotazioni"])


def main():
	dati_oggi, dati_voti, dati_compiti, dati_promemoria = gsd.get_dati()

	while 1:
		what_view = input(
"""\n\nCosa vuoi vedere?
(V)oti,
cosa hai fatto (O)ggi,
(C)ompiti, (CS)compiti sett. scorsa,
(P)romemoria
(UP)date,
(del-all)
(99)exit,
[DEBUG: add R for raw output]... """).lower()
		print()

		if what_view == 'v':
			voti(dati_voti)

		elif what_view == 'vr':
			pp.pprint(dati_voti)

		elif what_view == 'o':
			cosa_successo_oggi(dati_oggi)

		elif what_view == 'or':
			pp.pprint(dati_oggi)

		elif what_view == 'c':
			compiti_asse_data(dati_compiti)

		elif what_view == 'cr':
			pp.pprint(dati_compiti)

		elif what_view == 'cs':
			compiti_asse_sett(dati_compiti)

		elif what_view == 'p':
			promemoria(dati_promemoria)

		elif what_view == 'pr':
			pp.pprint(dati_promemoria)

		elif what_view == 'up':
			gsd.update_dati()
			gsd.get_dati()

		elif what_view == 'del-all':
			try:
				os.remove(gsd.paths["dati"])
				os.remove(gsd.paths["credenziali"])
				exit()
			except FileNotFoundError:
				print("1 or more file not found")
				exit()

		elif what_view == '99':
			exit()

		else:
			print()

if __name__ == '__main__':
	main()
