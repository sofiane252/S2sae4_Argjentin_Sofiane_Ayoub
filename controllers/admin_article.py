#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

admin_article = Blueprint('admin_article', __name__,
                        template_folder='templates')

@admin_article.route('/admin/article/show')
def show_article():
    mycursor = get_db().cursor()
    sql = "SELECT * FROM voiture INNER JOIN type_voiture ON type_voiture.id_type_voiture = voiture.id_type_voiture " \
          "INNER JOIN carburant ON carburant.id_carburant = voiture.id_carburant " \
          "INNER JOIN nbr_places ON nbr_places.id_nbr_places = voiture.id_nbr_places " \
          "INNER JOIN nbr_portes ON nbr_portes.id_nbr_portes = voiture.id_nbr_portes " \
          "INNER JOIN modele ON modele.id_modele = voiture.id_modele " \
          "INNER JOIN couleur ON couleur.id_couleur = voiture.id_couleur " \
          "INNER JOIN marque ON marque.id_marque = voiture.id_marque ORDER BY id_voiture"
    mycursor.execute(sql)
    articles = mycursor.fetchall()
    # print(articles)
    return render_template('admin/article/show_article.html', articles=articles)

@admin_article.route('/admin/article/add', methods=['GET'])
def add_article():
    mycursor = get_db().cursor()
    sql = "SELECT * FROM voiture"
    mycursor.execute(sql)
    articles = mycursor.fetchall()
    sql2 = "SELECT * FROM type_voiture"
    mycursor.execute(sql2)
    types_articles = mycursor.fetchall()
    sql3 = "SELECT * FROM carburant"
    mycursor.execute(sql3)
    carburants = mycursor.fetchall()
    sqlpa = "SELECT * FROM nbr_places"
    mycursor.execute(sqlpa)
    nbr_places = mycursor.fetchall()
    sqlpo = "SELECT * FROM nbr_portes"
    mycursor.execute(sqlpo)
    nbr_portes = mycursor.fetchall()
    sql4 = "SELECT * FROM modele"
    mycursor.execute(sql4)
    modeles = mycursor.fetchall()
    sql5 = "SELECT * FROM couleur"
    mycursor.execute(sql5)
    couleurs = mycursor.fetchall()
    sql6 = "SELECT * FROM marque"
    mycursor.execute(sql6)
    marques = mycursor.fetchall()
    return render_template('admin/article/add_article.html', articles=articles, types_articles=types_articles, nbr_places=nbr_places, nbr_portes=nbr_portes, modeles=modeles, carburants=carburants, couleurs=couleurs, marques=marques)

@admin_article.route('/admin/article/add', methods=['POST'])
def valid_add_article():
    mycursor = get_db().cursor()
    prix_unit_voiture = request.form.get('prix_unit_voiture', '')
    description = request.form.get('description', '')
    image_voiture = request.form.get('image_voiture', '')
    id_type_voiture = request.form.get('id_type_voiture', '')
    # type_article_id = int(type_article_id)
    id_carburant = request.form.get('id_carburant', '')
    id_nbr_places = request.form.get('id_nbr_places', '')
    id_nbr_portes = request.form.get('id_nbr_portes', '')
    id_modele = request.form.get('id_modele', '')
    id_couleur = request.form.get('id_couleur', '')
    id_marque = request.form.get('id_marque', '')
    stock_voiture = request.form.get('stock_voiture', '')
    tuple_insert = (prix_unit_voiture, description, image_voiture, id_type_voiture, id_carburant,id_nbr_places, id_nbr_portes, id_modele, id_couleur, id_marque, stock_voiture)
    sql = "INSERT INTO voiture(prix_unit_voiture, description, image_voiture, id_type_voiture, id_carburant, id_nbr_places, id_nbr_portes, id_modele, id_couleur, id_marque, stock_voiture) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    print(u'voiture ajouté , id du modele :', id_modele)
    message = u'voiture ajouté , id du modele : ' + id_modele + ', stock : ' + stock_voiture
    flash(message)
    return redirect(url_for('admin_article.show_article'))

@admin_article.route('/admin/article/delete', methods=['GET'])
def delete_article():
    mycursor = get_db().cursor()
    id_voiture = request.args.get('id_voiture', '')
    # id_voiture = request.form.get('id_voiture', '')
    tuple_delete = (id_voiture)

    sql = "SELECT * FROM panier WHERE id_voiture=%s"
    mycursor.execute(sql, id_voiture)
    result = mycursor.fetchall()
    if result:
        sql = "DELETE FROM panier WHERE id_voiture=%s"
        mycursor.execute(sql, id_voiture)
        flash(u'Une voiture supprimé y compris dans les paniers, id de la voiture : ' + id_voiture)
    sql = "DELETE FROM voiture WHERE id_voiture=%s"
    mycursor.execute(sql, tuple_delete)
    get_db().commit()

    print("une voiture supprimé, id de la voiture : ", id_voiture)
    flash(u'une voiture supprimé, id de la voiture : ' + id_voiture)
    return redirect(url_for('admin_article.show_article'))

@admin_article.route('/admin/article/edit/<int:id_voiture>', methods=['GET'])
def edit_article(id_voiture):
    mycursor = get_db().cursor()
    sql = "SELECT * FROM voiture WHERE id_voiture=%s"
    mycursor.execute(sql, id_voiture)
    articles = mycursor.fetchone()
    sql2 = "SELECT * FROM type_voiture"
    mycursor.execute(sql2)
    types_articles = mycursor.fetchall()
    sql3 = "SELECT * FROM carburant"
    mycursor.execute(sql3)
    carburants = mycursor.fetchall()
    sqlpa = "SELECT * FROM nbr_places"
    mycursor.execute(sqlpa)
    nbr_places = mycursor.fetchall()
    sqlpo = "SELECT * FROM nbr_portes"
    mycursor.execute(sqlpo)
    nbr_portes = mycursor.fetchall()
    sql4 = "SELECT * FROM modele"
    mycursor.execute(sql4)
    modeles = mycursor.fetchall()
    sql5 = "SELECT * FROM couleur"
    mycursor.execute(sql5)
    couleurs = mycursor.fetchall()
    sql6 = "SELECT * FROM marque"
    mycursor.execute(sql6)
    marques = mycursor.fetchall()
    return render_template('admin/article/edit_article.html', articles=articles, types_articles=types_articles, carburants=carburants, nbr_places=nbr_places, nbr_portes=nbr_portes, modeles=modeles, couleurs=couleurs, marques=marques)

@admin_article.route('/admin/article/edit', methods=['POST'])
def valid_edit_article():
    mycursor = get_db().cursor()
    id_voiture = request.form.get('id_voiture', '')
    prix_unit_voiture = request.form.get('prix_unit_voiture', '')
    description = request.form.get('description', '')
    image_voiture = request.form.get('image_voiture', '')
    id_type_voiture = request.form.get('id_type_voiture', '')
    # type_article_id = int(type_article_id)
    id_carburant = request.form.get('id_carburant', '')
    id_nbr_places = request.form.get('id_nbr_places', '')
    id_nbr_portes = request.form.get('id_nbr_portes', '')
    id_modele = request.form.get('id_modele', '')
    id_couleur = request.form.get('id_couleur', '')
    id_marque = request.form.get('id_marque', '')
    stock_voiture = request.form.get('stock_voiture', '')
    tuple_edit = (prix_unit_voiture, description, image_voiture, id_type_voiture, id_carburant, id_nbr_places, id_nbr_portes, id_modele, id_couleur, id_marque, stock_voiture, id_voiture)
    sql = "UPDATE voiture SET prix_unit_voiture=%s, description=%s, image_voiture=%s, id_type_voiture=%s, id_carburant=%s, id_nbr_places=%s, id_nbr_portes=%s, id_modele=%s, id_couleur=%s, id_marque=%s, stock_voiture=%s WHERE id_voiture=%s"
    mycursor.execute(sql, tuple_edit)
    get_db().commit()

    print(u' Une voiture modifié, id de la voiture : ', id_voiture, ", id du modele : ", id_modele)
    flash(u' une voiture modifié, id de la voiture : '+id_voiture+", id du modele : "+ id_modele)
    return redirect(url_for('admin_article.show_article'))