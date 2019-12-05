#!/usr/bin/env python3
#web ui for the client

import datetime
import argoscuolanext as argo
import pickle
import pprint
pp = pprint.PrettyPrinter(indent=4)

from flask import Flask, redirect, url_for, render_template, request
app = Flask(__name__)

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


dati_oggi, dati_voti, dati_compiti = get_dati()

#BEGIN FLASK

@app.route('/voti/')
def page_voti():
	return render_template('voti.html', raw = dati_voti)


@app.route('/cosa-successo-oggi/')
def page_cosa_successo_oggi():
	return render_template('cosa-successo-oggi.html', raw = dati_oggi)


@app.route('/compiti-asse-sett/')
def page_compiti_asse_sett():
	oggi = datetime.date.today()
	settimana = []
	for i in range(7):
		settimana.append(str(oggi - datetime.timedelta(days=i)))

	return render_template('compiti-asse-sett.html', raw = dati_compiti, giorni = settimana)


@app.route('/compiti-asse-data/<data_assegnati>/')
def page_compiti_asse_data(data_assegnati):
	data_assegnati = '2019-' + data_assegnati
	return render_template('compiti-asse-data.html', raw = dati_compiti, data = data_assegnati)


#@app.route('/data-prompt/', methods = ['POST', 'GET'])
#def page_data_prompt():
#	if request.method == 'POST':
#		data_assegnati = (request.form).items()
#		print(data_assegnati)
#		return redirect(url_for(page_compiti_asse_data(data_assegnati)))
#	return render_template('data-prompt.html')


@app.route('/update/')
def page_update():
	update_dati()
	return render_template('update.html')


if __name__ == '__main__':
	app.run(debug = True)
