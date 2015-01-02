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
	redirect,
	json)
from werkzeug import secure_filename


app=Flask(__name__)

def connect_db():
	"""Retorna una conexion a la BD"""
	path_to_db='bar.db'
	rv=sqlite3.connect(path_to_db)
	rv.row_factory=sqlite3.Row
	return rv

@app.route('/confirmarP/<string:data>',methods=['POST'])
def confirmarP(data):
	consu=data.split("-")
	mesa=consu[0] #Numero de mesa
	trago=consu[1] #trago
	trago=trago.replace("_"," ")
	cantidad=int(consu[2])
	i=int(consu[3]);
	ip=request.remote_addr # Usuario conectado para saber su id
	if (i==1):
		#hace insert en tabla pedido
		db=connect_db()
		us=db.execute('SELECT id_usuario FROM conexion WHERE conexion.ip=\''+ip+'\'') #Obtiene el usuario (garzon)conectado para añadirlo a la tabla pedido.
		us=[row[0] for row in us.fetchall()]
		cur=db.execute('INSERT into pedido (id_garzon, n_mesa, fecha) values ('+str(us[0])+','+str(mesa)+', datetime(\'now\')) ')
		db.commit()
		#Select para saber el id_pedido generado con el insert actual.
		us1=db.execute('SELECT id_pedido FROM pedido ORDER BY id_pedido DESC LIMIT 1')
		us1=[row[0] for row in us1.fetchall()]
		print(us1[0])
		#Select para saber el id_trago 
		us2=db.execute('SELECT id_trago FROM trago where trago.trago=\''+trago+'\'')
		us2=[row[0] for row in us2.fetchall()]
		print(us2[0])
		#insert a tabla pedido_trago de la prierma fila que encuentra en la tabla resumen. 
		cur=db.execute('INSERT into pedido_trago (id_pedido, id_trago, cantidad, estado) values ('+str(us1[0])+','+str(us2[0])+','+str(cantidad)+', "pendiente") ')
		db.commit()
		db.close()
		return new_orden()
	else:
		db=connect_db()
		#Select para saber el id_pedido generado con el insert actual.
		us1=db.execute('SELECT id_pedido FROM pedido ORDER BY id_pedido DESC LIMIT 1')
		us1=[row[0] for row in us1.fetchall()]
		print(us1[0])
		#Select para saber el id_trago 
		us2=db.execute('SELECT id_trago FROM trago where trago.trago=\''+trago+'\'')
		us2=[row[0] for row in us2.fetchall()]
		# insert con las demas filas de la tabla. 
		print(us2[0])
		cur=db.execute('INSERT into pedido_trago (id_pedido, id_trago, cantidad, estado) values ('+str(us1[0])+','+str(us2[0])+','+str(cantidad)+', "pendiente") ')
		db.commit()
		db.close()
		return new_orden()


@app.route('/tipo_Trago',methods=['POST'])
def tipo_Trago():
	tipoT=str(request.form['seleccionTipoTrago'])
	return eleccionTrago(tipoT)

#actualiza el estado del pedido... informando que se encuentra en barra para ser servid
@app.route('/pendientes',methods=['POST'])
def servido():
	if activo(request.remote_addr)==False:
		return render_template('log.html')
	else:

		id_p=str(request.form['idp'])
		trago=str(request.form['trago'])
		db=connect_db()
		cur=db.execute('update pedido_trago set estado=\'en barra\' WHERE id_pedido=\''+id_p+'\' and id_trago=(SELECT id_trago from trago where trago=\''+trago+'\');')
		db.commit();
		db.close();
		return pedido_barra()


@app.route('/entries',methods=['POST'])
def entregado():
	if activo(request.remote_addr)==False:
		return render_template('log.html')
	else:
		id_p=str(request.form['idp'])
		trago=str(request.form['trago'])
		db=connect_db()
		cur=db.execute('update pedido_trago set estado=\'servido\' WHERE id_pedido=\''+id_p+'\' and id_trago=(SELECT id_trago from trago where trago=\''+trago+'\');')
		db.commit();
		db.close();
		return show_entries()

def eleccionTrago(tipoT):
	db=connect_db()
	cur=db.execute('SELECT trago from trago where trago.tipo=\''+tipoT+'\'')
	ent=[row[0] for row in cur.fetchall()]
	pal=''
	for i in range (len(ent)):
		pal=pal+str(ent[i])+'-'
	db.close()
	print(pal)
	return pal


@app.route('/enbarra')
def show_entries():
	if activo(request.remote_addr)==False:
		return render_template('log.html')
	else:	
		if(cargo_usuario()=='m'):
			db=connect_db()
			cur=db.execute('select pedido.id_pedido, n_mesa, trago, cantidad from pedido, pedido_trago, trago where pedido.id_pedido=pedido_trago.id_pedido and estado=\'en barra\' and pedido_trago.id_trago=trago.id_trago;')
			entries=cur.fetchall()
			db.close()
			return render_template('entries.html', pedido=entries)
		else:
			return render_template('invalidoM.html')
#si estas con sesion activa no entras a logiarte FALTA VER Q CARGO
@app.route('/')
def log_():
	if activo(request.remote_addr)==False:
		return render_template('log.html')
	else:
		if(cargo_usuario()=='m'):
			return show_entries()
		else:
			return pedido_barra()

def cargo_usuario():
	db=connect_db()
	cur=db.execute('select cargo from usuario, conexion where conexion.id_usuario=usuario.id_usuario and ip=\''+request.remote_addr+'\';')
	co=[row[0] for row in cur.fetchall()]
	if(co[0]=='Barman'):
		return 'b'
	else:
		return 'm'
	db.close

def activo(a):
	ip=a
	db=connect_db()
	
	cur=db.execute('SELECT julianday(datetime(\'now\'))-fecha FROM conexion WHERE conexion.ip=\''+ip+'\'')
	ultimac=[row[0] for row in cur.fetchall()]

	#si ha pasado más de 4 horas el usuario es sacado
	if (len(ultimac)!=0 and ultimac[0]>0.0070) or (len(ultimac)==0):
		cur=db.execute('DELETE FROM conexion WHERE conexion.ip=\''+ip+'\'')
		db.commit();
		return False
	else:
		return True
def cargo(usuario):
	db=connect_db()
	cur=db.execute('SELECT cargo FROM usuario WHERE usuario.nombre=\''+usuario+'\'')
	cargo=[row[0] for row in cur.fetchall()]
	db.close()
	if (str(cargo[0])=='Mesero' or str(cargo[0])=='Mesera'):
		return 'm'
	else:
		return 'b'

#logea a los usuarios
@app.route('/log', methods=['GET', 'POST'])
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
				if (cargo(usuario)=='m'):
					return show_entries()
				else:
					return pedido_barra()
			else:
				return render_template('errorUC.html')
		db.close()
		
	else:
		return "Acceso Denegado"

@app.route('/out')
def logout():
	
	ipc=request.remote_addr
	db=connect_db()
	cur=db.execute('delete FROM conexion WHERE ip=\''+ipc+'\'')
	db.commit()
	db.close()
	return log_()
	

#carga los pedidos pendientes para que el barman los pueda tener en lista
@app.route('/pendientes')
def pedido_barra():
	if activo(request.remote_addr)==False:
		return render_template('log.html')
	else:
		if (cargo_usuario()=='b'):
			db=connect_db()
			cur=db.execute('select pedido.id_pedido, n_mesa, trago, cantidad from pedido, pedido_trago, trago where pedido.id_pedido=pedido_trago.id_pedido and estado=\'pendiente\' and pedido_trago.id_trago=trago.id_trago;')
			entries=cur.fetchall()
			db.close()
			return render_template('tragospendientes.html', pedido=entries)
		else:
			return render_template('invalidoB.html')

@app.route('/form', methods=['GET', 'POST'])
def new_orden():
	if activo(request.remote_addr)==False:
		return render_template('log.html')
	else:
		if (cargo_usuario()=='m'):
			if request.method=='GET':
				db=connect_db()
				cur=db.execute('SELECT distinct tipo from trago ')
				entries=cur.fetchall()
				db.close()
				return render_template('form.html',entries=entries)
			else:
				return "Acceso Denegado"
		else:
			return render_template('invalidoM.html')


if __name__ == "__main__":
	app.run(debug=True)