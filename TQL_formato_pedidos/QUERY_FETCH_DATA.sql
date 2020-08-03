SELECT a.id as id_pedido, a.tb_status_id, b.id_producto, c.id_unidad_presentacion, d.strsiglas as unidad, b.intcantidad as cantidad, b.id_lote, e.id_almacen_ubii, f.nombre_almacen, a.CreatedOn, g.cod_sap, h.moneda
FROM ubiimarket_db.dt_pedido as a, ubiimarket_db.dt_detalle_pedido as b, ubiimarket_db.dt_productos as c, ubiimarket_db.tm_unidad_presentacion as d, ubiimarket_db.dt_lote as e, ubiimarket_db.dt_almacen_ubii as f, ubiimarket_db.dt_producto_tql as g, ubiimarket_db.tb_metodo_pago as h
WHERE a.tb_status_id=24 AND a.id=b.dt_pedido_id AND b.id_producto=c.id_producto AND b.id_producto=g.id_producto AND c.id_unidad_presentacion=d.id_presentacion AND b.id_lote=e.id_lote AND  e.id_almacen_ubii=f.id_almacen AND f.rif='J-075525973' AND a.id_metodo_pago=h.id_metodo



