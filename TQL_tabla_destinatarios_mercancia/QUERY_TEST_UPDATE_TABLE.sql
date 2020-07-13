START transaction;

SELECT a.strnombre_empresa, b.strdireccion, a.strcodigo_postal, a.strtelefono, a.strrif_empresa, a.strnombre_representante, b.nueva_tql, b.id_zona, c.zona, b.id_subzona, d.subzona
FROM ubiimarket_db.dt_empresa as a, ubiimarket_db.dt_direccion as b, ubiimarket_db.dt_zona as c, ubiimarket_db.dt_subzonas as d
WHERE a.id_empresa=b.id_empresa AND b.tipo='Dirección Fiscal' AND b.nueva_tql=1 AND b.id_zona=c.id AND b.id_subzona=d.id;

UPDATE ubiimarket_db.dt_empresa as a, ubiimarket_db.dt_direccion as b
SET b.nueva_tql=0
WHERE a.id_empresa=b.id_empresa AND b.tipo='Dirección Fiscal' AND b.nueva_tql=1;

SELECT a.strnombre_empresa, b.strdireccion, a.strcodigo_postal, a.strtelefono, a.strrif_empresa, a.strnombre_representante, b.nueva_tql, b.id_zona, c.zona, b.id_subzona, d.subzona
FROM ubiimarket_db.dt_empresa as a, ubiimarket_db.dt_direccion as b, ubiimarket_db.dt_zona as c, ubiimarket_db.dt_subzonas as d
WHERE a.id_empresa=b.id_empresa AND b.tipo='Dirección Fiscal' AND b.nueva_tql=1 AND b.id_zona=c.id AND b.id_subzona=d.id; 

ROLLBACK;