#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                        template_folder='templates')

@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['get','post'])
def admin_commande_show():
    mycursor = get_db().cursor()
    commandes = None
    articles_commande = None
    id = request.form.get('idCommande')
    tuple_select = (id)

    sql = '''SELECT user.username as username, SUM(ligne_commande.quantite) AS nbr_articles, SUM(ligne_commande.prix_unit * ligne_commande.quantite) 
          AS prix_total, commande.date_achat, commande.id_etat, commande.id_commande 
          FROM commande 
          INNER JOIN ligne_commande on commande.id_commande = ligne_commande.id_commande 
          INNER JOIN user on commande.user_id = user.user_id 
          group by commande.date_achat, commande.id_etat, commande.id_commande order by date_achat DESC'''
    mycursor.execute(sql)
    commandes = mycursor.fetchall()
    articles_commande = None

    if id is not None:
        sql = '''SELECT modele.libelle_modele as nom, ligne_commande.quantite as quantite, ligne_commande.prix_unit as prix,
            SUM(ligne_commande.prix_unit * ligne_commande.quantite) as prix_ligne, commande.id_commande
            FROM ligne_commande 
            INNER JOIN commande on commande.id_commande = ligne_commande.id_commande 
            INNER JOIN voiture on ligne_commande.id_voiture = voiture.id_voiture 
            INNER JOIN modele ON voiture.id_modele = modele.id_modele
            WHERE commande.id_commande=%s 
            GROUP BY modele.libelle_modele, ligne_commande.quantite, ligne_commande.prix_unit, commande.id_commande'''
        print(tuple_select, sql)
        mycursor.execute(sql, tuple_select)
        articles_commande = mycursor.fetchall()
        print(articles_commande)

    return render_template('admin/commandes/show.html', commandes=commandes, articles_commande=articles_commande)

@admin_commande.route('/admin/commande/valider', methods=['get','post'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    id_commande = request.form.get('idCommande')

    sql0 = '''SELECT id_etat FROM commande WHERE id_commande=%s'''
    mycursor.execute(sql0, id_commande)
    result = mycursor.fetchall()
    # print(result[0]['id_etat'])

    if result[0]['id_etat'] == 1:
        sql2 = '''SELECT voiture.id_voiture, ligne_commande.quantite, voiture.stock_voiture from ligne_commande 
                  INNER JOIN voiture on ligne_commande.id_voiture = voiture.id_voiture where ligne_commande.id_Commande=%s'''
        mycursor.execute(sql2, id_commande)
        result = mycursor.fetchall()
        # print(result)

        for i in range(len(result)):
            id_voiture = result[i]['id_voiture']
            quantite = result[i]['quantite']
            stock_voiture = result[i]['stock_voiture']
            if quantite <= stock_voiture:
                tuple_update = (quantite, id_voiture)
                # print(tuple_update)
                sql2 = "UPDATE voiture SET stock_voiture = stock_voiture-%s WHERE id_voiture=%s"
                mycursor.execute(sql2, tuple_update)
                print(sql2)
            else:
                flash("Il n'y a pas assez de stock. Renouvelez-le puis réessayer.")
                break

        if quantite <= stock_voiture:
            sql = " UPDATE commande SET id_etat=2 where id_commande=%s"
            mycursor.execute(sql, id_commande)
        get_db().commit()

        return redirect('/admin/commande/show')

    if result[0]['id_etat'] == 2:
        sql1 = "UPDATE commande SET id_etat=3 where id_commande=%s"
        mycursor.execute(sql1, id_commande)
        get_db().commit()

        return redirect('/admin/commande/show')

    return redirect('/admin/commande/show')
