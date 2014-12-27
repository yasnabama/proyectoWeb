BEGIN TRANSACTION;
CREATE TABLE "usuario" (
	`id_usuario`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`nombre`	text NOT NULL,
	`cargo`	text NOT NULL,
	`pass`	TEXT
);
INSERT INTO `usuario` VALUES ('1','Yasna Barrientos','Mesera','b''\xe6zqD\xf9\xa5\x14\x13\xe6\xb6\xfd\x01Vk\xe7\xc7''');
INSERT INTO `usuario` VALUES ('2','Pablo Riquelme','Mesero','b''E;\xce^IWF}h\xab1Y\xfe\x1ac\xa0''');
INSERT INTO `usuario` VALUES ('3','Ivo Cuq','Barman','b''\xb7\xcbQ<\xf2L&p\xfd\xa9\xa1\x8ee\x1b\xd6\xe6''');
CREATE TABLE `trago` (
	`tipo`	TEXT NOT NULL,
	`trago`	TEXT NOT NULL UNIQUE,
	`id_trago`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
);
INSERT INTO `trago` VALUES ('cerveza','Kunstmann Torobayo','1');
INSERT INTO `trago` VALUES ('cerveza','Cuello Negro Rubia','2');
INSERT INTO `trago` VALUES ('Vino','Tocornal Tinto','3');
INSERT INTO `trago` VALUES ('Vino','Santa Elena Blanco','4');
INSERT INTO `trago` VALUES ('Pisco','Piscola','5');
INSERT INTO `trago` VALUES ('Pisco','Kriptonita','6');
INSERT INTO `trago` VALUES ('Vodka','Ruso Negro','7');
INSERT INTO `trago` VALUES ('Vodka','Caipiroska','8');
INSERT INTO `trago` VALUES ('Ron','Roncola','9');
INSERT INTO `trago` VALUES ('Ron','Mojito','10');
INSERT INTO `trago` VALUES ('Bebida','Coca-Cola','11');
INSERT INTO `trago` VALUES ('Bebida','Fanta','12');
CREATE TABLE `pedido_trago` (
	`id_pedido`	INTEGER NOT NULL,
	`id_trago`	INTEGER NOT NULL,
	`cantidad`	INTEGER NOT NULL,
	`estado`	TEXT NOT NULL,
	PRIMARY KEY(id_pedido, id_trago)
	foreign key (id_pedido) references pedido(id_pedido), 
	foreign key (id_trago) references trago(id_trago)
);
INSERT INTO `pedido_trago` VALUES ('1','1','2','pendiente');
INSERT INTO `pedido_trago` VALUES ('1','3','1','pendiente');
INSERT INTO `pedido_trago` VALUES ('2','6','1','en barra');
INSERT INTO `pedido_trago` VALUES ('3','10','2','servido');
INSERT INTO `pedido_trago` VALUES ('3','9','2','servido');
CREATE TABLE `pedido` (
	`id_pedido`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`id_garzon`	INTEGER NOT NULL,
	`n_mesa`	INTEGER NOT NULL,
	`fecha`	TEXT NOT NULL,
	foreign key (id_garzon) references usuario(id_usuario)
);
INSERT INTO `pedido` VALUES ('1','1','1','2014-12-27 14:17:03');
INSERT INTO `pedido` VALUES ('2','1','2','2014-12-27 14:17:22');
INSERT INTO `pedido` VALUES ('3','2','3','2014-12-27 14:17:40');
CREATE TABLE 'conexion'( 'ip' text not null, 'id_usuario' integer not null, 'date' real not null, primary key(ip, id_usuario), foreign key (id_usuario) references usuario(id_usuario));
;
;
;
COMMIT;
