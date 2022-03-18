#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

client_article = Blueprint('client_article', __name__,
                        template_folder='templates')

@client_article.route('/client/index')
@client_article.route('/client/article/show')      # remplace /client
def client_article_show():                                 # remplace client_index
    mycursor = get_db().cursor()
    articles = []
    types_articles = []
    articles_panier = []
    prix_total = None

    sql = "select *, voiture.id_voiture as id ,voiture.image_voiture as image,voiture.prix_unit_voiture as prix, modele.libelle_modele as nom,voiture.stock_voiture as stock from voiture inner join modele on modele.id_modele = voiture.id_modele inner join marque on voiture.id_marque = marque.id_marque "

    list_param = []
    condition_and = ""
    if "filter_word" in session or "filter_prix_min" in session or "filter_prix_max" in session or "filter_types" in session:
        sql = sql + " WHERE "
    if "filter_word" in session:
        sql = sql + " modele.libelle_modele LIKE %s "
        recherche = "%" + session["filter_word"] + "%"
        list_param.append(recherche)
        condition_and = " AND "
    if "filter_prix_min" in session or "filter_prix_max" in session:
        sql = sql + condition_and + " voiture.prix_unit_voiture BETWEEN %s AND %s "
        list_param.append(session['filter_prix_min'])
        list_param.append(session['filter_prix_max'])
        condition_and = " AND "
    if "filter_types" in session:
        sql = sql + condition_and
        last_item = session['filter_types'][-1]
        for item in session['filter_types']:
            sql = sql + "voiture.id_marque=%s"
            if item != last_item:
                sql = sql + " or "
            list_param.append(item)
        sql = sql
    sql += ';'
    tuple_sql = tuple(list_param)
    print(tuple_sql)
    print(sql)
    if "filter_word" in session or "filter_prix_min" in session or "filter_prix_max" in session or "filter_types" in session:
        mycursor.execute(sql, tuple_sql)
    else:
        mycursor.execute(sql)

    voitures = mycursor.fetchall()
    print(voitures)
    articles = voitures
    sql = "select * from marque"
    mycursor.execute(sql)
    type_voiture = mycursor.fetchall()
    types_articles = type_voiture
    #prix = request.form.get('prix')
    sql = "select * ,modele.libelle_modele as nom,voiture.prix_unit_voiture as prix, panier.quantite from panier inner join voiture on panier.id_voiture = voiture.id_voiture inner join modele on modele.id_modele = voiture.id_modele where user_id=%s"
    mycursor.execute(sql, session['user_id'])
    articles_panier = mycursor.fetchall()
    sql = "SELECT SUM(voiture.prix_unit_voiture * panier.quantite) AS prix_total FROM panier INNER JOIN voiture ON panier.id_voiture = voiture.id_voiture WHERE panier.user_id = %s"
    mycursor.execute(sql, session['user_id'])
    prix_total = mycursor.fetchone()['prix_total']
    # print(articles_panier)
    #sql = "select SUM(prix_unit_voiture) as total from voiture "
    #mycursor.execute(sql)
    #prix_total = mycursor.fetchall()  # requete à faire
    return render_template('client/boutique/panier_article.html', articles=articles, articlesPanier=articles_panier, prix_total=prix_total, itemsFiltre=types_articles)

@client_article.route('/client/article/details/<int:id>', methods=['GET'])
def client_article_details(id):
    mycursor = get_db().cursor()
    article=None
    commentaires=None
    commandes_articles=None
    return render_template('client/boutique/article_details.html', article=article, commentaires=commentaires, commandes_articles=commandes_articles)