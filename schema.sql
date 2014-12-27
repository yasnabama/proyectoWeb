BEGIN TRANSACTION;
CREATE TABLE 'usuario' ( 'id_usuario' integer not null primary key autoincrement, 'nombre' text not null, 'cargo' text not null);
CREATE TABLE `trago` (
	`tipo`	TEXT NOT NULL,
	`trago`	TEXT NOT NULL UNIQUE,
	`id_trago`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
);
CREATE TABLE `pedido_trago` (
	`id_pedido`	INTEGER NOT NULL,
	`id_trago`	INTEGER NOT NULL,
	`cantidad`	INTEGER NOT NULL,
	`estado`	TEXT NOT NULL,
	PRIMARY KEY(id_pedido, id_trago)
	foreign key (id_pedido) references pedido(id_pedido), 
	foreign key (id_trago) references trago(id_trago)
);
CREATE TABLE `pedido` (
	`id_pedido`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`id_garzon`	INTEGER NOT NULL,
	`n_mesa`	INTEGER NOT NULL,
	`fecha`	TEXT NOT NULL,
	foreign key (id_garzon) references usuario(id_usuario)
);
CREATE TABLE 'conexion'( 'ip' text not null, 'id_usuario' integer not null, 'date' real not null, primary key(ip, id_usuario), foreign key (id_usuario) references usuario(id_usuario));
;
;
;
COMMIT;
