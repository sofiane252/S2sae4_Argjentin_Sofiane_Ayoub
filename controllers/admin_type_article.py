#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

admin_type_article = Blueprint('admin_type_article', __name__,
                        template_folder='templates')

@admin_type_article.route('/admin/type-article/show')
def show_type_article():
    mycursor = get_db().cursor()
    types_articles = []
    return render_template('admin/type_article/show_type_article.html', types_articles=types_articles)

@admin_type_article.route('/admin/type-article/add', methods=['GET'])
def add_type_article():
    return render_template('admin/type_article/add_type_article.html')

@admin_type_article.route('/admin/type-article/add', methods=['POST'])
def valid_add_type_article():
    libelle = request.form.get('libelle', '')
    tuple_insert = (libelle,)
    message = u'type ajouté , libellé :'+libelle
    flash(message)
    return redirect('/admin/type-article/show') #url_for('show_type_article')

@admin_type_article.route('/admin/type-article/delete', methods=['GET'])
def delete_type_article():
    id_type_article = request.args.get('id', '')
    flash(u'suppression type article , id : ' + id_type_article)
    return redirect('/admin/type-article/show') #url_for('show_type_article')

@admin_type_article.route('/admin/type-article/edit/<int:id>', methods=['GET'])
def edit_type_article(id):
    mycursor = get_db().cursor()
    type_article = []
    return render_template('admin/type_article/edit_type_article.html', type_article=type_article)

@admin_type_article.route('/admin/type-article/edit', methods=['POST'])
def valid_edit_type_article():
    libelle = request.form['libelle']
    id_type_article = request.form.get('id', '')
    flash(u'type article modifié, id: ' + id_type_article + " libelle : " + libelle)
    return redirect('/admin/type-article/show') #url_for('show_type_article')







