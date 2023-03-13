set client_encoding = 'UTF8';

CREATE SEQUENCE city_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."city" (
    "id" integer DEFAULT nextval('city_id_seq') NOT NULL,
    "name" character varying(100) NOT NULL,
    "longitude" real NOT NULL,
    "latitude" real NOT NULL,
    CONSTRAINT "city_id" PRIMARY KEY ("id"),
    CONSTRAINT "city_name" UNIQUE ("name")
) WITH (oids = false);

INSERT INTO "city" ("id", "name", "longitude", "latitude") VALUES
(1,	'Пермь',	56.2502,	58.0105);

CREATE SEQUENCE company_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."company" (
    "id" integer DEFAULT nextval('company_id_seq') NOT NULL,
    "city_id" integer NOT NULL,
    "name" character varying(100) NOT NULL,
    "description" character varying(255),
    "longitude" real NOT NULL,
    "latitude" real NOT NULL,
    "sanitary_zone_radius" real,
    CONSTRAINT "company_id" PRIMARY KEY ("id"),
    CONSTRAINT "company_name" UNIQUE ("name")
) WITH (oids = false);

INSERT INTO "company" ("id", "city_id", "name", "description", "longitude", "latitude", "sanitary_zone_radius") VALUES
(1,	1,	'ЛУКОЙЛ-Пермнефтеоргсинтез',	NULL,	57.922318,	56.134647,	NULL);

CREATE TABLE "public"."gas_analyzer" (
    "measurement" character varying(100) NOT NULL,
    "company_id" integer NOT NULL,
    "longitude" real NOT NULL,
    "latitude" real NOT NULL,
    CONSTRAINT "gas_analyzer_measurement_company_id" PRIMARY KEY ("measurement", "company_id")
) WITH (oids = false);

INSERT INTO "gas_analyzer" ("measurement", "company_id", "longitude", "latitude") VALUES
('gas_analyzer_1',	1,	57.952896,	56.13388),
('gas_analyzer_2',	1,	57.8943,	56.13321),
('gas_analyzer_3',	1,	57.89791,	56.090485),
('gas_analyzer_4',	1,	57.928215,	56.073975),
('gas_analyzer_5',	1,	57.944523,	56.08537),
('gas_analyzer_6',	1,	57.914364,	56.204987),
('gas_analyzer_7',	1,	57.88695,	56.176563),
('gas_analyzer_8',	1,	57.8839,	56.15102);

CREATE TABLE "public"."pipe" (
    "measurement" character varying(100) NOT NULL,
    "company_id" integer NOT NULL,
    "longitude" real NOT NULL,
    "latitude" real NOT NULL,
    CONSTRAINT "pipe_measurement_company_id" PRIMARY KEY ("measurement", "company_id")
) WITH (oids = false);

INSERT INTO "pipe" ("measurement", "company_id", "longitude", "latitude") VALUES
('pipe_1',	1,	57.920807,	56.14872),
('pipe_2',	1,	57.925385,	56.12424),
('pipe_3',	1,	57.90992,	56.132294),
('pipe_4',	1,	57.9092,	56.121628),
('pipe_5',	1,	57.916897,	56.11879);

ALTER TABLE ONLY "public"."company" ADD CONSTRAINT "company_city_id_fkey" FOREIGN KEY (city_id) REFERENCES city(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."gas_analyzer" ADD CONSTRAINT "gas_analyzer_company_id_fkey" FOREIGN KEY (company_id) REFERENCES company(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."pipe" ADD CONSTRAINT "pipe_company_id_fkey" FOREIGN KEY (company_id) REFERENCES company(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;