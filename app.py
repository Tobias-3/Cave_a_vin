from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

def init_db():
    with sqlite3.connect("cave_vin.db") as conn:
        cur = conn.cursor()
        cur.executescript(open("setup.sql").read())
        conn.commit()

@app.route('/')
def index():
    with sqlite3.connect("cave_vin.db") as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT vins.id, vins.nom, appellations.nom, vins.couleur, vins.nb_bouteilles 
            FROM vins 
            JOIN appellations ON vins.appellation_id = appellations.id
        """)
        vins = cur.fetchall()
        cur.execute("SELECT SUM(nb_bouteilles) FROM vins")
        total_bouteilles = cur.fetchone()[0] or 0
        cur.execute("SELECT couleur, SUM(nb_bouteilles) FROM vins GROUP BY couleur")
        bouteilles_par_couleur = cur.fetchall()
    return render_template("index.html", vins=vins, total_bouteilles=total_bouteilles, bouteilles_par_couleur=bouteilles_par_couleur)

@app.route('/ajouter_vin', methods=['GET', 'POST'])
def ajouter_vin():
    if request.method == 'POST':
        nom = request.form['nom']
        appellation_id = request.form['appellation_id']
        couleur = request.form['couleur']
        nb_bouteilles = request.form['nb_bouteilles']
        with sqlite3.connect("cave_vin.db") as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO vins (nom, appellation_id, couleur, nb_bouteilles) 
                VALUES (?, ?, ?, ?)
            """, (nom, appellation_id, couleur, nb_bouteilles))
            conn.commit()
        return redirect(url_for('index'))
    with sqlite3.connect("cave_vin.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM appellations")
        appellations = cur.fetchall()
    return render_template("ajouter_vin.html", appellations=appellations)

@app.route('/supprimer_vin/<int:vin_id>', methods=['POST'])
def supprimer_vin(vin_id):
    with sqlite3.connect("cave_vin.db") as conn:
        cur = conn.cursor()
        # Exécuter la requête de suppression
        cur.execute("DELETE FROM vins WHERE id = ?", (vin_id,))
        conn.commit()
    return redirect('/')

@app.route('/ajouter_appellation', methods=['GET', 'POST'])
def ajouter_appellation():
    if request.method == 'POST':
        nom = request.form['nom']
        region = request.form['region']
        pays = request.form['pays']
        # Les mets sont optionnels
        met1 = request.form.get('met1', None)
        met2 = request.form.get('met2', None)
        met3 = request.form.get('met3', None)
        met4 = request.form.get('met4', None)
        met5 = request.form.get('met5', None)
        with sqlite3.connect("cave_vin.db") as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO appellations (nom, region, pays, met1, met2, met3, met4, met5)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (nom, region, pays, met1, met2, met3, met4, met5))
            conn.commit()
        return redirect(url_for('index'))
    return render_template("ajouter_appellation.html")


@app.route('/filtrer_vins', methods=['GET', 'POST'])
def filtrer_vins():
    with sqlite3.connect("cave_vin.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT region FROM appellations")
        regions = cur.fetchall()
    
    if request.method == 'POST':
        selected_region = request.form.get('region')
        # Applique un filtrage basé sur la région sélectionnée, par exemple :
        cur.execute("""
            SELECT vins.nom, appellations.nom, vins.couleur, vins.nb_bouteilles
            FROM vins
            JOIN appellations ON vins.appellation_id = appellations.id
            WHERE appellations.region = ?
        """, (selected_region,))
        vins = cur.fetchall()
        return render_template("filtrer_vins.html", vins=vins, regions=regions)

    return render_template("filtrer_vins.html", regions=regions)

@app.route('/details_vin/<int:vin_id>')
def details_vin(vin_id):
    with sqlite3.connect("cave_vin.db") as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT vins.nom, appellations.nom, appellations.region, appellations.pays, appellations.met1, appellations.met2, appellations.met3, vins.couleur, appellations.met4, appellations.met5, vins.nb_bouteilles 
            FROM vins 
            JOIN appellations ON vins.appellation_id = appellations.id 
            WHERE vins.id = ?
        """, (vin_id,))
        vin = cur.fetchone()
    return render_template("details_vin.html", vin=vin)

if __name__ == '__main__':
    if not os.path.exists("cave_vin.db"):
        init_db()
    app.run(debug=True)
