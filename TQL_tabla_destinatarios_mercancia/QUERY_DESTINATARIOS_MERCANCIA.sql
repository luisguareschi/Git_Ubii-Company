SELECT a.strnombre_empresa, b.strdireccion, a.strcodigo_postal, a.strtelefono, a.strrif_empresa, a.strnombre_representante, b.nueva_tql
FROM ubiimarket_db.dt_empresa as a, ubiimarket_db.dt_direccion as b 
WHERE a.id_empresa=b.id_empresa AND b.tipo='Dirección Fiscal' AND b.nueva_tql=1