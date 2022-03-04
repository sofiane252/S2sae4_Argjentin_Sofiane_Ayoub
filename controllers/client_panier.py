#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    user_id = session['user_id']
    id_voiture = request.form.get('idArticle')
    quantite = request.form.get('quantite')
    stock = request.form.get('stock')

    tuple_select = (id_voiture, user_id)
    print(tuple_select, quantite)
    sql = "SELECT * FROM panier WHERE id_voiture=%s AND user_id=%s"
    mycursor.execute(sql, tuple_select)
    article_panier = mycursor.fetchone()

    tuple_select2 = (id_voiture)
    sql2 = "SELECT * FROM voiture WHERE id_voiture=%s"
    mycursor.execute(sql2, tuple_select2)
    article = mycursor.fetchone()

    if not (article_panier is None) and article_panier['quantite'] >= 1:
        tuple_update = (quantite, user_id, id_voiture)
        sql = "UPDATE panier SET quantite = quantite+%s WHERE user_id = %s AND id_voiture=%s"
        mycursor.execute(sql, tuple_update)
    else:
        tuple_insert = (user_id, id_voiture, quantite)
        sql = "INSERT INTO panier(user_id,id_voiture,quantite) VALUES (%s,%s,%s)"
        mycursor.execute(sql, tuple_insert)

    get_db().commit()
    return redirect('/client/article/show')
    #return redirect(url_for('client_index'))

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    user_id = session['user_id']
    id_voiture = request.form.get('idArticle')
    tuple_delete = (id_voiture, user_id)

    sql = "UPDATE panier SET quantite = quantite-1 WHERE id_voiture = %s AND user_id=%s"
    mycursor.execute(sql, tuple_delete)
    get_db().commit()

    sql = "Select quantite from panier where id_voiture=%s and user_id=%s"
    mycursor.execute(sql, tuple_delete)
    var = mycursor.fetchall()
    if var == [{'quantite': 0}]:
        sql = "DELETE from panier where id_voiture=%s and user_id=%s"
        mycursor.execute(sql, tuple_delete)
        get_db().commit()
    return redirect('/client/article/show')
    #return redirect(url_for('client_index'))


@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    user_id = session['user_id']

    sql = "DELETE FROM panier WHERE user_id=%s"
    mycursor.execute(sql, user_id)
    get_db().commit()

    return redirect('/client/article/show')
    #return redirect(url_for('client_index'))


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    user_id = session['user_id']
    id_voiture = request.form.get('idArticle')
    tuple_delete = (id_voiture, user_id)

    sql = "DELETE FROM panier WHERE id_voiture=%s AND user_id=%s"
    mycursor.execute(sql, tuple_delete)
    get_db().commit()

    return redirect('/client/article/show')
    #return redirect(url_for('client_index'))


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)
    print("word:" + filter_word + str(len(filter_word)))
    if filter_word or filter_word == "":
        if len(filter_word) > 1:
            if filter_word.isalpha():
                session['filter_word'] = filter_word
            else:
                flash(u' votre Mot de recherché doit être composé uniquement de lettres')
        else:
            if len(filter_word) == 1:
                flash(u'votre Mot recherché doit être composé de au moins 2 lettres')
            else:
                session.pop('filter_word', None)
    if filter_prix_min or filter_prix_max:
        if filter_prix_min.isdecimal() and filter_prix_max.isdecimal():
            if int(filter_prix_min) < int(filter_prix_max):
                session['filter_prix_min'] = filter_prix_min
                session['filter_prix_max'] = filter_prix_max
            else:
                flash(u'min < max')
        else:
            flash(u'min et max doivent être des numériques')
    if filter_types and filter_types != []:
        print("filter_types:", filter_types)
        if isinstance(filter_types, list):
            check_filter_type = True
            for number_type in filter_types:
                print("test", number_type)
                if not number_type.isdecimal():
                    check_filter_type = False
        if check_filter_type:
            session['filter_types'] = filter_types
    else:
        session.pop('filter_types', None)

    return redirect('/client/article/show')
    #return redirect(url_for('client_index'))


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    session.pop('filter_word', None)
    session.pop('filter_prix_min', None)
    session.pop('filter_prix_max', None)
    session.pop('filter_types', None)
    print("suppr filtre")
    return redirect('/client/article/show')
    #return redirect(url_for('client_index'))
