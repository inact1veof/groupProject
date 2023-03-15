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
(1,	1,	'ЛУКОЙЛ-Пермнефтеоргсинтез',	NULL,	56.1346460146535,	57.92231916465072,	NULL);

CREATE TABLE "public"."gas_analyzer" (
    "measurement" character varying(100) NOT NULL,
    "company_id" integer NOT NULL,
    "longitude" real NOT NULL,
    "latitude" real NOT NULL,
    CONSTRAINT "gas_analyzer_measurement_company_id" PRIMARY KEY ("measurement", "company_id")
) WITH (oids = false);

INSERT INTO "gas_analyzer" ("measurement", "company_id", "longitude", "latitude") VALUES
('gas_analyzer_1',	1,	56.1338811120596,	57.95289533980933),
('gas_analyzer_2',	1,	56.1867691771204,	57.94070228983883),
('gas_analyzer_3',	1,	56.20498713933395,	57.91436234775402),
('gas_analyzer_4',	1,	56.18411612461943,	57.89042563976504),
('gas_analyzer_5',	1,	56.13866055102109,	57.88499722322343),
('gas_analyzer_6',	1,	56.086364168788265,	57.90284450835055),
('gas_analyzer_7',	1,	56.07534925656922,	57.92437878990272),
('gas_analyzer_8',	1,	56.09395113649093,	57.945436405625635);

CREATE TABLE "public"."pipe" (
    "measurement" character varying(100) NOT NULL,
    "company_id" integer NOT NULL,
    "longitude" real NOT NULL,
    "latitude" real NOT NULL,
    CONSTRAINT "pipe_measurement_company_id" PRIMARY KEY ("measurement", "company_id")
) WITH (oids = false);

INSERT INTO "pipe" ("measurement", "company_id", "longitude", "latitude") VALUES
('pipe_1',	1,	56.1487195730304,	57.92080497904481),
('pipe_2',	1,	56.12424034685258,	57.92538636947342),
('pipe_3',	1,	56.13229364907698,	57.909919616174015),
('pipe_4',	1,	56.121629186534754,	57.909197899621944),
('pipe_5',	1,	56.11878956521833,	57.91689793503993);

CREATE SEQUENCE guide_record_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."guide" (
    "id" integer DEFAULT nextval('guide_record_id_seq') NOT NULL,
    "substance_name" character varying(100) NOT NULL,
    "pdk_mr" real NOT NULL,
    "pdk_ss" real NOT NULL
) WITH (oids = false);

INSERT INTO "guide" ("id", "substance_name", "pdk_mr", "pdk_ss") VALUES
(1, 'PM_10', 0.3, 0,3);


ALTER TABLE ONLY "public"."company" ADD CONSTRAINT "company_city_id_fkey" FOREIGN KEY (city_id) REFERENCES city(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."gas_analyzer" ADD CONSTRAINT "gas_analyzer_company_id_fkey" FOREIGN KEY (company_id) REFERENCES company(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."pipe" ADD CONSTRAINT "pipe_company_id_fkey" FOREIGN KEY (company_id) REFERENCES company(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;