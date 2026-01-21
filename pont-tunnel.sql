-- Fusion des ponts et tunnel

--import des CSV en brute 

-- fusion  : attention field 5 = field 4 

-- renommage colonne 

ALTER TABLE "planIGN_route_sou_n25_temp"  RENAME COLUMN field_1 TO geom__c;
ALTER TABLE "planIGN_route_sou_n25_temp"  RENAME COLUMN field_2 TO glp;
ALTER TABLE "planIGN_route_sou_n25_temp"  RENAME COLUMN field_3 TO local;
ALTER TABLE "planIGN_route_sou_n25_temp"  RENAME COLUMN field_4 TO n25;

ALTER TABLE "planIGN_route_sup_n25_temp"  RENAME COLUMN field_1 TO geom__c;
ALTER TABLE "planIGN_route_sup_n25_temp"  RENAME COLUMN field_2 TO glp;
ALTER TABLE "planIGN_route_sup_n25_temp"  RENAME COLUMN field_3 TO local;
ALTER TABLE "planIGN_route_sup_n25_temp"  RENAME COLUMN field_4 TO n25;

ALTER TABLE "planIGN_route_n25_ini_temp"  RENAME COLUMN field_1 TO geom__c;
ALTER TABLE "planIGN_route_n25_ini_temp"  RENAME COLUMN field_2 TO glp;
ALTER TABLE "planIGN_route_n25_ini_temp"  RENAME COLUMN field_3 TO local;
ALTER TABLE "planIGN_route_n25_ini_temp"  RENAME COLUMN field_5 TO n25;

----- Fusion des tables en une
INSERT INTO "planIGN_route_n25_ini_temp"(geom__c,glp,local,n25)
SELECT geom__c,glp,local,n25 FROM public."planIGN_route_sup_n25_temp";

INSERT INTO "planIGN_route_n25_ini_temp"(geom__c,glp,local,n25)
SELECT geom__c,glp,local,n25 FROM public."planIGN_route_sou_n25_temp";

------- ajout colonne geom et creation de la geom
ALTER TABLE public."planIGN_route_n25_ini_temp"
ADD COLUMN geom geometry(MULTILINESTRING, 2154);

UPDATE public."planIGN_route_n25_ini_temp"
SET geom = ST_Transform(
              ST_Force2D(
                  ST_GeomFromEWKB(decode(geom__c, 'hex'))
              ),
              2154
          );

DELETE FROM public."planIGN_route_n25_ini_temp" a
WHERE NOT EXISTS (
    SELECT geom
    FROM limite_tempo m
    WHERE ST_Within(
        a.geom, 
        ST_Transform(m.geom, 2154)  
    )
);

ALTER TABLE public."planIGN_route_n25_ini_temp"
ADD COLUMN selection Integer;

ALTER TABLE public."planIGN_route_n25_ini_temp"
DROP COLUMN field_4;


UPDATE public."planIGN_route_n25_ini_temp"
SET selection = 1
WHERE local ILIKE 'AUT%' OR local ILIKE 'PRIN%';

UPDATE public."planIGN_route_n25_ini_temp"
SET selection = 2
WHERE local ILIKE 'REG%';

UPDATE public."planIGN_route_n25_ini_temp"
SET selection = 3
WHERE local ILIKE 'BRET%' OR local ILIKE 'LOC%';

UPDATE public."planIGN_route_n25_ini_temp"
SET selection = 4
WHERE local ILIKE 'NON%';
-- Aut  1
-- BRET 3
-- LOC 3
-- NON 4
-- PRIN 1
-- REG 2

CREATE INDEX IF NOT EXISTS planign_n10_geom_geom_idx
    ON public."PlanIGN_n10" USING gist
    (geom)
    TABLESPACE pg_default;
	
	
	
	
	
	
	
	
	
ALTER TABLE "planIGN_route_sou_n50_temp"  RENAME COLUMN field_1 TO geom__c;
ALTER TABLE "planIGN_route_sou_n50_temp"  RENAME COLUMN field_2 TO glp;
ALTER TABLE "planIGN_route_sou_n50_temp"  RENAME COLUMN field_3 TO local;
ALTER TABLE "planIGN_route_sou_n50_temp"  RENAME COLUMN field_4 TO n50;

ALTER TABLE "planIGN_route_sup_n50_temp"  RENAME COLUMN field_1 TO geom__c;
ALTER TABLE "planIGN_route_sup_n50_temp"  RENAME COLUMN field_2 TO glp;
ALTER TABLE "planIGN_route_sup_n50_temp"  RENAME COLUMN field_3 TO local;
ALTER TABLE "planIGN_route_sup_n50_temp"  RENAME COLUMN field_4 TO n50;

ALTER TABLE "planIGN_route_n50_ini_temp"  RENAME COLUMN field_1 TO geom__c;
ALTER TABLE "planIGN_route_n50_ini_temp"  RENAME COLUMN field_2 TO glp;
ALTER TABLE "planIGN_route_n50_ini_temp"  RENAME COLUMN field_3 TO local;
ALTER TABLE "planIGN_route_n50_ini_temp"  RENAME COLUMN field_5 TO n50;

----- Fusion des tables en une
INSERT INTO "planIGN_route_n50_ini_temp"(geom__c,glp,local,n50)
SELECT geom__c,glp,local,n50 FROM public."planIGN_route_n50_ini_temp";

INSERT INTO "planIGN_route_n50_ini_temp"(geom__c,glp,local,n50)
SELECT geom__c,glp,local,n50 FROM public."planIGN_route_sou_n50_temp";

------- ajout colonne geom et creation de la geom
ALTER TABLE public."planIGN_route_n50_ini_temp"
ADD COLUMN geom geometry(MULTILINESTRING, 2154);

UPDATE public."planIGN_route_n50_ini_temp"
SET geom = ST_Transform(
              ST_Force2D(
                  ST_GeomFromEWKB(decode(geom__c, 'hex'))
              ),
              2154
          );

DELETE FROM public."planIGN_route_n50_ini_temp" a
WHERE NOT EXISTS (
    SELECT geom
    FROM limite_tempo m
    WHERE ST_Within(
        a.geom, 
        ST_Transform(m.geom, 2154)  
    )
);

ALTER TABLE public."planIGN_n50"
ADD COLUMN selection Integer;

ALTER TABLE public."planIGN_n50"
DROP COLUMN field_4;


UPDATE public."planIGN_n50"
SET selection = 1
WHERE local ILIKE 'AUT%';

UPDATE public."planIGN_n50"
SET selection = 2
WHERE local ILIKE 'REG%' Or local ILIKE 'LOC%' Or  local ILIKE 'PRIN%'  ;



CREATE INDEX IF NOT EXISTS planign_n50_geom_geom_idx
    ON public."planIGN_route_n50_ini_temp" USING gist
    (geom)
    TABLESPACE pg_default;	
	
	
	
	
	
	
	


