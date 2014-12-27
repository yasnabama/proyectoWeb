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


@app.route('/')
def show_entries():
	db=connect_db()
	cur=db.execute('SELECT id_trago, trago, tipo from trago ')
	entries=cur.fetchall()
	db.close()
	return render_template('entries.html',entries=entries)

@app.route('/form', methods=['GET', 'POST'])
def new_post():
	if request.method=='GET':
		return render_template('form.html')
	elif request.method=='POST':
		title=request.form['title']
		description=request.form['description']
		db=connect_db()
		db.execute(
			'insert into entry (title,description) values (?,?	)[title,description]')
		db.commit()
		db.close()
		return u"Operacion exitosa"
	else:
		return "Acceso Denegado"

if __name__ == "__main__":
	app.run(debug=True)