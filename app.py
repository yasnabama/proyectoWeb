# -*- coding: utf-8 -*-
import os
import hashlib
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
	if activo(request.remote_addr)==False:
		return render_template('log.html')
	else:
		db=connect_db()
		cur=db.execute('SELECT id_trago, trago, tipo from trago ')
		entries=cur.fetchall()
		db.close()
		return render_template('entries.html',entries=entries)

#si estas con sesion activa no entras a logiarte
@app.route('/log')
def log_():
	if activo(request.remote_addr)==False:
		return render_template('log.html')
	else:	
		return show_entries()

def activo(a):
	ip=a
	db=connect_db()
	
	cur=db.execute('SELECT julianday(datetime(\'now\'))-fecha FROM conexion WHERE conexion.ip=\''+ip+'\'')
	ultimac=[row[0] for row in cur.fetchall()]

	#si ha pasado más de 4 horas el usuario es sacado
	if (len(ultimac)!=0 and ultimac[0]>0.0003) or (len(ultimac)==0):
		cur=db.execute('DELETE FROM conexion WHERE conexion.ip=\''+ip+'\'')
		db.commit();
		return False
	else:
		return True

@app.route('/', methods=['GET', 'POST'])
def login():
	if request.method=='GET':
		return render_template('form.html')
	elif request.method=='POST':
		usuario=request.form['inputUser']
		clave=request.form['inputPassword']
		ip=request.remote_addr
		
		db=connect_db()
		
		

		cur=db.execute('SELECT id_usuario FROM usuario WHERE usuario.nombre=\''+usuario+'\'')
		us=[row[0] for row in cur.fetchall()]
		if len(us) == 0:
			return render_template('errorUC.html')
		else:
			hc=hashlib.md5()
			hc.update(clave.encode('utf-8'))
			claveh=hc.digest()
			cur=db.execute('SELECT pass FROM usuario WHERE usuario.nombre=\''+usuario+'\'')
			entries=[row[0] for row in cur.fetchall()]
			if (str(claveh)==entries[0]):
				cur=db.execute('INSERT into conexion (ip, id_usuario, fecha) values (\''+ip+'\','+str(us[0])+', julianday(datetime(\'now\')))')
				db.commit()
				return show_entries()
			else:
				return render_template('errorUC.html')
		db.close()
		
	else:
		return "Acceso Denegado"

@app.route('/form', methods=['GET', 'POST'])
def new_orden():
	if activo(request.remote_addr)==False:
		return render_template('log.html')
	else:
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