
----Creation d'une table unique-----------


CREATE TABLE IF NOT EXISTS public.hydro_bis (
    id INTEGER GENERATED ALWAYS AS IDENTITY,
    id_hydro INTEGER,
    "order" INTEGER,
    geom geometry(MultiLineString,2154),
    min_zoom INTEGER,
    max_zoom INTEGER
);

CREATE TABLE hydro_all AS
SELECT  id as id_hydro, "order", geom, 10 AS zoom FROM hydro_10
UNION ALL
SELECT id as id_hydro, "order", geom, 11 AS zoom FROM hydro_11
UNION ALL
SELECT id as id_hydro, "order", geom, 12 AS zoom FROM hydro_12
UNION ALL
SELECT id as id_hydro, "order", geom, 13 AS zoom FROM hydro_13
UNION ALL
SELECT id as id_hydro, "order", geom, 14 AS zoom FROM hydro_14
UNION ALL
SELECT id as id_hydro, "order", geom, 15 AS zoom FROM hydro_15
UNION ALL
SELECT id as id_hydro, "order", geom, 16 AS zoom FROM lbc.hydro_16;


INSERT INTO public.hydro_bis (id_hydro, geom, "order", min_zoom, max_zoom)
SELECT
    id_hydro,
    geom,
	"order",
    MIN(zoom) AS min_zoom,
    MAX(zoom) +1 AS max_zoom
FROM hydro_all
GROUP BY id_hydro, geom, "order";

UPDATE hydro_bis 
SET min_zoom = 7
WHERE min_zoom = 10;

UPDATE hydro_bis 
SET max_zoom = 24
WHERE max_zoom = 17;
--------------------------CODE TOPONYME ---------------------------------


CREATE TABLE IF NOT EXISTS public.points
(
    id INTEGER GENERATED ALWAYS AS IDENTITY,
	ogc_fid integer,
    toponyme character varying COLLATE pg_catalog."default",
    niveau integer,
    geom geometry(Point,2154),
    min_zoom integer,
    max_zoom integer
)



CREATE TABLE points_all AS
SELECT  ogc_fid,toponyme, niveau , geom, 10 AS zoom FROM public.points_zoom10
UNION ALL
SELECT ogc_fid,toponyme, niveau , geom, 11 AS zoom FROM public.points_zoom11
UNION ALL
SELECT ogc_fid,toponyme, niveau , geom, 12 AS zoom FROM public.points_zoom12
UNION ALL
SELECT ogc_fid,toponyme, niveau , geom, 13 AS zoom FROM public.points_zoom14
UNION ALL
SELECT ogc_fid,toponyme, niveau , geom, 14 AS zoom FROM public.points_zoom15
UNION ALL
SELECT ogc_fid,toponyme, niveau , geom, 15 AS zoom FROM public.points_zoom16
UNION ALL
SELECT ogc_fid,toponyme, niveau, geom, 16 AS zoom FROM points_zoom17;


INSERT INTO public.points (ogc_fid,toponyme, niveau, geom, min_zoom, max_zoom)
SELECT
    ogc_fid,
	toponyme, 
	niveau, 
    geom,
    MIN(zoom) AS min_zoom,
    MAX(zoom) +1 AS max_zoom
FROM points_all
GROUP BY ogc_fid, geom, toponyme, niveau;

UPDATE points 
SET min_zoom = 7
WHERE min_zoom = 10;

UPDATE points 
SET max_zoom = 24
WHERE max_zoom = 17;




-------------------------- AJOUT INDEX



CREATE INDEX IF NOT EXISTS hydro_geom_geom_idx
    ON public."hydro" USING gist
    (geom)
    TABLESPACE pg_default;
	
	
CREATE INDEX IF NOT EXISTS points_geom_geom_idx
    ON public."points" USING gist
    (geom)
    TABLESPACE pg_default;
	
	