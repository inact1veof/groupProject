--
-- PostgreSQL database dump
--

-- Dumped from database version 14.5 (Ubuntu 14.5-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 15.1 (Ubuntu 15.1-1.pgdg22.04+1)

-- Started on 2023-02-16 21:58:50 +05

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 4 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 210 (class 1259 OID 24582)
-- Name: City; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."City" (
    id integer NOT NULL,
    name character varying NOT NULL,
    longitude real NOT NULL,
    latitude real NOT NULL
);


ALTER TABLE public."City" OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 24581)
-- Name: City_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."City" ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."City_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 212 (class 1259 OID 24594)
-- Name: Company; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Company" (
    id integer NOT NULL,
    name character varying NOT NULL,
    longitude real NOT NULL,
    latitude real NOT NULL,
    city_id integer NOT NULL,
    radius_zone real NOT NULL
);


ALTER TABLE public."Company" OWNER TO postgres;

--
-- TOC entry 211 (class 1259 OID 24593)
-- Name: Company_id_seq1; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."Company" ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."Company_id_seq1"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 213 (class 1259 OID 32772)
-- Name: Gas_analyzer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Gas_analyzer" (
    id character varying NOT NULL,
    longitude real NOT NULL,
    latitude real NOT NULL,
    description text,
    city_id integer NOT NULL
);


ALTER TABLE public."Gas_analyzer" OWNER TO postgres;

--
-- TOC entry 214 (class 1259 OID 32789)
-- Name: Pipe; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Pipe" (
    id character varying NOT NULL,
    company_id integer NOT NULL,
    longitude real NOT NULL,
    latitude real NOT NULL
);


ALTER TABLE public."Pipe" OWNER TO postgres;

--
-- TOC entry 3369 (class 0 OID 24582)
-- Dependencies: 210
-- Data for Name: City; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3371 (class 0 OID 24594)
-- Dependencies: 212
-- Data for Name: Company; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3372 (class 0 OID 32772)
-- Dependencies: 213
-- Data for Name: Gas_analyzer; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3373 (class 0 OID 32789)
-- Dependencies: 214
-- Data for Name: Pipe; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3380 (class 0 OID 0)
-- Dependencies: 209
-- Name: City_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."City_id_seq"', 1, false);


--
-- TOC entry 3381 (class 0 OID 0)
-- Dependencies: 211
-- Name: Company_id_seq1; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Company_id_seq1"', 1, false);


--
-- TOC entry 3223 (class 2606 OID 24586)
-- Name: City City_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."City"
    ADD CONSTRAINT "City_pkey" PRIMARY KEY (id);


--
-- TOC entry 3225 (class 2606 OID 24622)
-- Name: Company Company_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Company"
    ADD CONSTRAINT "Company_pkey" PRIMARY KEY (id);


--
-- TOC entry 3227 (class 2606 OID 32794)
-- Name: Gas_analyzer city_gas; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Gas_analyzer"
    ADD CONSTRAINT city_gas FOREIGN KEY (city_id) REFERENCES public."City"(id) NOT VALID;


--
-- TOC entry 3226 (class 2606 OID 24611)
-- Name: Company company_city; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Company"
    ADD CONSTRAINT company_city FOREIGN KEY (city_id) REFERENCES public."City"(id) NOT VALID;


--
-- TOC entry 3228 (class 2606 OID 32799)
-- Name: Pipe pipe_company; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Pipe"
    ADD CONSTRAINT pipe_company FOREIGN KEY (company_id) REFERENCES public."Company"(id) NOT VALID;


--
-- TOC entry 3379 (class 0 OID 0)
-- Dependencies: 4
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2023-02-16 21:58:51 +05

--
-- PostgreSQL database dump complete
--

