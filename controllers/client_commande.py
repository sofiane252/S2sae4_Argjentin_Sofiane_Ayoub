#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()
    client_id = session['user_id']
    sql = "SELECT * FROM panier WHERE user_id=%s"
    mycursor.execute(sql, client_id)
    items_panier = mycursor.fetchall()
    if items_panier is None or len(items_panier) < 1:
        flash(u"Pas d'articles dans le panier")
        return redirect('/client/article/show')
    date_commande = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tuple_insert = (date_commande, client_id, '1')  # 1 : etat de commande
    sql = "INSERT INTO commande(date_achat,user_id,id_etat) VALUES (%s,%s,%s)"
    mycursor.execute(sql, tuple_insert)
    sql = "SELECT last_insert_id() as last_insert_id"
    mycursor.execute(sql)
    commande_id = mycursor.fetchone()
    print(commande_id, tuple_insert)
    for item in items_panier:
        tuple_insert = (client_id, item['id_voiture'])
        sql = "DELETE FROM panier WHERE user_id = %s AND id_voiture = %s"
        mycursor.execute(sql, tuple_insert)
        sql = "SELECT prix_unit_voiture FROM voiture WHERE id_voiture = %s"
        mycursor.execute(sql, item['id_voiture'])
        prix = mycursor.fetchone()
        sql = "INSERT INTO ligne_commande(id_commande, id_voiture, prix_unit, quantite) VALUES (%s,%s,%s, %s)"
        tuple_insert = (commande_id['last_insert_id'], item['id_voiture'], prix['prix_unit_voiture'], item['quantite'])
        print(tuple_insert)
        mycursor.execute(sql, tuple_insert)
    get_db().commit()
    flash(u'Commande ajoutée')
    return redirect('/client/article/show')
    # return redirect(url_for('client_index'))



@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    mycursor = get_db().cursor()
    commandes = None
    articles_commande = None
    sql = "SELECT * FROM commande"
    mycursor.execute(sql)
    commandes = mycursor.fetchall()
    return render_template('client/commandes/show.html', commandes=commandes, articles_commande=articles_commande)
