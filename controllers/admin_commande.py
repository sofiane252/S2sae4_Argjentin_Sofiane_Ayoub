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


@admin_commande.route('/admin/commande/show', methods=['get', 'post'])
def admin_commande_show():
    mycursor = get_db().cursor()
    commandes = None
    articles_commande = None
    id = request.form.get('idCommande')
    tuple_select = (id,)

    sql = '''SELECT user.username as username, SUM(ligne_commande.quantite) AS nbr_articles, SUM(ligne_commande.prix_unit * ligne_commande.quantite) 
          AS prix_total, commande.date_achat, commande.id_etat, commande.id_commande 
          FROM commande 
          INNER JOIN ligne_commande on commande.id_commande = ligne_commande.id_Commande 
          INNER JOIN user on commande.id_user = user.user_id 
          group by commande.date_achat, commande.id_etat, commande.id_commande order by date_achat DESC'''
    mycursor.execute(sql)
    commandes = mycursor.fetchall()

    sql = '''SELECT voiture.nom_voiture as nom, ligne_commande.quantite as quantite, ligne_commande.prix_unit as prix,
          SUM(ligne_commande.prix_unit * ligne_commande.quantite) as prix_ligne, commande.id_commande
          FROM ligne_commande 
          INNER JOIN commande on commande.id_commande = ligne_commande.id_Commande 
          INNER JOIN voiture on ligne_commande.id_voiture = voiture.id_voiture 
          WHERE commande.id_commande=%s GROUP BY voiture.nom_voiture, ligne_commande.quantite, ligne_commande.prix_unit, commande.id_commande '''
    mycursor.execute(sql, tuple_select)
    articles_commande = mycursor.fetchall()


    print(articles_commande)
    return render_template('admin/commandes/show.html', commandes=commandes, articles_commande=articles_commande)


@admin_commande.route('/admin/commande/valider', methods=['get', 'post'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    id_commande = request.form.get('idCommande')
    sql = " UPDATE commande SET id_etat=2 where id_commande=%s"
    mycursor.execute(sql, id_commande)
    get_db().commit()
    return redirect('/admin/commande/show') 
