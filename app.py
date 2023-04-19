from flask import Flask, render_template, request
app = Flask(__name__)


import pandas as pd
import os
import matplotlib.pyplot as plt
df = pd.read_excel('https://github.com/wtitze/3E/blob/main/BikeStores.xls?raw=true', sheet_name="customers")

@app.route('/')
def home():
    l=list(set(df["city"]))
    l.sort()
    return render_template("home.html",lista=l)


@app.route('/esercizio1', methods=["GET"])
def esercizio1():
    nome = request.args.get('nome')
    cognome = request.args.get('cognome')
    df1=df[(df["first_name"]== nome) & (df["last_name"]== cognome)].to_html()
    return render_template("risultato.html", tabella=df1)
     
@app.route('/esercizio2/<cittadina>', methods=["GET"])
def esercizio2(cittadina):
    df2=df[df["city"]== cittadina].to_html()
    return render_template("risultato.html", tabella=df2)

@app.route('/esercizio3', methods=["GET"])
def esercizio3():
    df3=df.groupby('state').count()[["first_name"]].reset_index().to_html()
    return render_template("risultato.html", tabella=df3)

@app.route('/esercizio4', methods=["GET"])
def esercizio4():
    d=df.groupby('state').count()[["first_name"]].reset_index()
    df4=d[d["first_name"]==d["first_name"].max()].to_html()
    return render_template("risultato.html", tabella=df4)

@app.route('/esercizio5', methods=["GET"])
def esercizio5():
    d=df.groupby('state').count()[["first_name"]].reset_index()
    labels = d['state']
    dati = d['first_name']
    #primo grafico
    fig, ax = plt.subplots(figsize=(10,8))
    ax.bar(labels, dati, label='numero di clienti per ogni stato')
    ax.set_ylabel('stati')
    ax.set_title('clienti in tutti gli stati')
    ax.set_xticklabels(labels) 
    ax.legend()
    dir = "static/images"
    file_name = "graf.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    #secondo grafico
    fig, axax = plt.subplots(figsize=(15,8))
    axax.barh(labels, dati, label="totale casi in ogni regione")
    dir = "static/images"
    file_name = "graf2.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    #grafico tre
    plt.figure(figsize=(22, 10))
    plt.pie(dati, labels=labels, autopct='%1.1f%%')
    dir = "static/images"
    file_name = "graf3.png"
    save_path = os.path.join(dir, file_name)
    #serve per creare un immagine
    plt.savefig(save_path, dpi = 150)

    return render_template("grafici.html")

@app.route('/esercizio6', methods=["GET"])
def esercizio6():
    df6=df[df["email"].isnull()][["first_name", "last_name", "phone"]].to_html()
    return render_template("risultato.html", tabella=df6)

@app.route('/esercizio7', methods=["GET"])
def esercizio7():
    email= request.args.get('provider')
    df7=df[df["email"].str.endswith(f"@{email}",na=False)][["first_name", "last_name"]].to_html()
    return render_template("risultato.html", tabella=df7)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)