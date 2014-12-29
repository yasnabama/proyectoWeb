# -*- coding: utf-8 -*-
import os
from sqlite3 import dbapi2 as sqlite3
from flask import(
	Flask, 
	render_template,
	request,
	url_for,
	flash,
	redirect)
from werkzeug import secure_filename


app=Flask(__name__)

def connect_db():
	"""Retorna una conexion a la BD"""
	path_to_db='bar.db'
	rv=sqlite3.connect(path_to_db)
	rv.row_factory=sqlite3.Row
	return rv

@app.route('/tipo_Trago', methods=['POST'])
def signUpUser():
    tipo =  request.form['username'];
    password = request.form['password'];
    return json.dumps({'status':'OK','user':user,'pass':password});


@app.route('/')
def show_entries():
	db=connect_db()
	cur=db.execute('SELECT id_trago, trago, tipo from trago ')
	entries=cur.fetchall()
	db.close()
	return render_template('entries.html',entries=entries)

@app.route('/form', methods=['GET', 'POST'])
def new_orden():
	if request.method=='GET':
		db=connect_db()
		cur=db.execute('SELECT distinct tipo from trago ')
		entries=cur.fetchall()
		db.close()
		return render_template('form.html',entries=entries)
	else:
		return "Acceso Denegado"

def tipo_trago():

	return render_template('form.html',entries=entries)


if __name__ == "__main__":
	app.run(debug=True)