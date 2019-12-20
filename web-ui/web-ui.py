#!/usr/bin/env python3
# web ui for the client

import datetime
import pprint
import os
import sys
from flask import Flask, redirect, url_for, render_template, request

pp = pprint.PrettyPrinter(indent=4)

sys.path.append("../modules")
import gestdati as gsd

app = Flask(__name__)
app.debug = True  # uncomment to develop using debug


dati_oggi, dati_voti, dati_compiti, dati_promemoria = gsd.get_dati()


# BEGIN FLASK


@app.route("/")
def page_default():
    return redirect("/cosa-successo-oggi/")


@app.route("/voti/")
def page_voti():
    return render_template("voti.html", raw=dati_voti)


@app.route("/cosa-successo-oggi/")
def page_cosa_successo_oggi():
    return render_template("cosa-successo-oggi.html", raw=dati_oggi)


@app.route("/compiti-asse-sett/")
def page_compiti_asse_sett():
    oggi = datetime.date.today()
    settimana = []
    for i in range(7):
        settimana.append(str(oggi - datetime.timedelta(days=i)))

    return render_template("compiti-asse-sett.html", raw=dati_compiti, giorni=settimana)


@app.route("/compiti-asse-data/<data_assegnati>/")
def page_compiti_asse_data(data_assegnati):
    return render_template(
        "compiti-asse-data.html", raw=dati_compiti, data=data_assegnati
    )


@app.route("/data-prompt/", methods=["POST", "GET"])
def page_data_prompt():
    if request.method == "POST":
        data_assegnati = request.form["data_assegnati"]
        return redirect("../compiti-asse-data/" + data_assegnati)
    return render_template("data-prompt.html")


@app.route("/promemoria/")
def promemoria():
    oggi = str(datetime.date.today())
    return render_template("promemoria.html", raw=dati_promemoria, oggi=oggi)


@app.route("/update/")
def page_update():
    gsd.update_dati()
    dati_oggi, dati_voti, dati_compiti, dati_promemoria = gsd.get_dati()
    return render_template("update.html")


if __name__ == "__main__":
    app.run()
