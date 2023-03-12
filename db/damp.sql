set client_encoding = 'UTF8';

CREATE SEQUENCE "city_id_seq" INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."city" (
    "id" integer DEFAULT nextval('"city_id_seq"') NOT NULL,
    "name" character varying(100) NOT NULL,
    "longitude" real NOT NULL,
    "latitude" real NOT NULL,
    CONSTRAINT "city_id" PRIMARY KEY ("id"),
    CONSTRAINT "city_name" UNIQUE ("name")
) WITH (oids = false);

INSERT INTO "city" ("name", "longitude", "latitude") VALUES
('Perm',	56.2502,	58.0105);

CREATE SEQUENCE "company_id_seq" INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."company" (
    "id" integer DEFAULT nextval('"company_id_seq"') NOT NULL,
    "city_id" integer NOT NULL,
    "name" character varying(100) NOT NULL,
    "description" character varying(255) NOT NULL,
    "longitude" real NOT NULL,
    "latitude" real NOT NULL,
    "sanitary_zone_radius" real NOT NULL,
    CONSTRAINT "company_id" PRIMARY KEY ("id"),
    CONSTRAINT "company_name" UNIQUE ("name")
) WITH (oids = false);


CREATE TABLE "public"."gas_analyzer" (
    "measurement" character varying(100) NOT NULL,
    "company_id" integer NOT NULL,
    "longitude" real NOT NULL,
    "latitude" real NOT NULL,
    CONSTRAINT "gas_analyzer_measurement" PRIMARY KEY ("measurement")
) WITH (oids = false);


CREATE TABLE "public"."pipe" (
    "measurement" character varying(100) NOT NULL,
    "company_id" integer NOT NULL,
    "longitude" real NOT NULL,
    "latitude" real NOT NULL,
    CONSTRAINT "pipe_measurement" PRIMARY KEY ("measurement")
) WITH (oids = false);


ALTER TABLE ONLY "public"."company" ADD CONSTRAINT "company_city_id_fkey" FOREIGN KEY (city_id) REFERENCES city(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."gas_analyzer" ADD CONSTRAINT "gas_analyzer_company_id_fkey" FOREIGN KEY (company_id) REFERENCES company(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."pipe" ADD CONSTRAINT "pipe_company_id_fkey" FOREIGN KEY (company_id) REFERENCES company(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;