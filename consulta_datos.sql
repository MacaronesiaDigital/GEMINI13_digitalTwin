/*
---------------------------------------------------------------------
 Cuestiones para la generalización de la visualización de los datos:
 - Añadir Ecomatik implica el uso de otras de otra tabla de diámetro
 --------------------------------------------------------------------
*/

-- Creamos la vista base de donde vamos a sacar los datos
CREATE VIEW base AS
SELECT sensor.id AS sensor_id, sensor.name AS type_name, sensor.type, station.name AS station_name, sensor.provider
	FROM farm, station, sensor, public.owner
	where farm.id = station.farm
	and sensor.station = station.id
	and public.owner.id = farm.owner
	and (public.owner.name = 'Domingo' or public.owner.name = 'Blas')
	and sensor.provider = 'Metos';

SELECT *
	FROM base
	
DROP VIEW ion_content, temperature, diameter, humidity, voltage
DROP VIEW base

/*
 Creamos la vista con el contenido iónico volumétrico
 Como todas las tablas que contienen esta medida tienen las mismas columnas,
 las unimos para obtener toda la información en una sola vista.
*/
CREATE VIEW ion_content AS
SELECT *
	FROM base, reg_sensor_15 as tipo
	WHERE tipo.sensor = base.sensor_id
UNION
SELECT *
	FROM base, reg_sensor_16 as tipo
	WHERE tipo.sensor = base.sensor_id
UNION
SELECT *
	FROM base, reg_sensor_17 as tipo
	WHERE tipo.sensor = base.sensor_id
UNION
SELECT *
	FROM base, reg_sensor_18 as tipo
	WHERE tipo.sensor = base.sensor_id
UNION
SELECT *
	FROM base, reg_sensor_19 as tipo
	WHERE tipo.sensor = base.sensor_id
UNION
SELECT *
	FROM base, reg_sensor_20 as tipo
	WHERE tipo.sensor = base.sensor_id
ORDER BY sensor_id, registered_date;

SELECT *
	FROM ion_content


-- Creamos la vista del diámetro obtenido por los dendrómetros
CREATE VIEW diameter AS 
SELECT *
	FROM base, reg_sensor_21 as tipo
	WHERE tipo.sensor = base.sensor_id
ORDER BY sensor_id, registered_date;

SELECT *
	FROM diameter


-- Creamos vista del panel solar y la bateria
CREATE VIEW voltage AS
SELECT *
	FROM base, reg_sensor_1 as tipo
	WHERE tipo.sensor = base.sensor_id
UNION
SELECT *
	FROM base, reg_sensor_2 as tipo
	WHERE tipo.sensor = base.sensor_id
ORDER BY sensor_id, registered_date;

SELECT *
	FROM voltage

/*
 Creamos la vista con el contenido de humedad en suelo
 tienen las mismas columnas, las unimos para obtener 
 toda la información en una sola vista.
*/
CREATE VIEW humidity AS
SELECT *
	FROM base, reg_sensor_9 as tipo
	WHERE tipo.sensor = base.sensor_id
UNION
SELECT *
	FROM base, reg_sensor_10 as tipo
	WHERE tipo.sensor = base.sensor_id
UNION
SELECT *
	FROM base, reg_sensor_11 as tipo
	WHERE tipo.sensor = base.sensor_id
UNION
SELECT *
	FROM base, reg_sensor_12 as tipo
	WHERE tipo.sensor = base.sensor_id
UNION
SELECT *
	FROM base, reg_sensor_13 as tipo
	WHERE tipo.sensor = base.sensor_id
UNION
SELECT *
	FROM base, reg_sensor_14 as tipo
	WHERE tipo.sensor = base.sensor_id
ORDER BY sensor_id, registered_date;

SELECT *
	FROM humidity
/*
 Creamos la vista con la temperatura del suelo
 tienen las mismas columnas, las unimos para obtener 
 toda la información en una sola vista.
*/
CREATE VIEW temperature AS
SELECT *
	FROM base, reg_sensor_3 as tipo
	WHERE tipo.sensor = base.sensor_id
UNION
SELECT *
	FROM base, reg_sensor_4 as tipo
	WHERE tipo.sensor = base.sensor_id
UNION
SELECT *
	FROM base, reg_sensor_5 as tipo
	WHERE tipo.sensor = base.sensor_id
UNION
SELECT *
	FROM base, reg_sensor_6 as tipo
	WHERE tipo.sensor = base.sensor_id
UNION
SELECT *
	FROM base, reg_sensor_7 as tipo
	WHERE tipo.sensor = base.sensor_id
UNION
SELECT *
	FROM base, reg_sensor_8 as tipo
	WHERE tipo.sensor = base.sensor_id
ORDER BY sensor_id, registered_date;
	
SELECT *
	FROM temperature