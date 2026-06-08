--
-- PostgreSQL database dump
--

-- Dumped from database version 10.23
-- Dumped by pg_dump version 10.23

-- Started on 2026-06-08 20:29:55

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

DROP DATABASE adapted;
--
-- TOC entry 3144 (class 1262 OID 17286)
-- Name: adapted; Type: DATABASE; Schema: -; Owner: -
--

CREATE DATABASE adapted WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'Indonesian_Indonesia.1252' LC_CTYPE = 'Indonesian_Indonesia.1252';


\connect adapted

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
-- TOC entry 1 (class 3079 OID 12924)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 3147 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 209 (class 1259 OID 17634)
-- Name: absensi_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.absensi_log (
    id_absensi integer NOT NULL,
    id_siswa integer,
    tanggal date DEFAULT CURRENT_DATE,
    waktu_login timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    waktu_logout timestamp without time zone,
    durasi_belajar_menit integer DEFAULT 0
);


--
-- TOC entry 208 (class 1259 OID 17632)
-- Name: absensi_log_id_absensi_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.absensi_log_id_absensi_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3148 (class 0 OID 0)
-- Dependencies: 208
-- Name: absensi_log_id_absensi_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.absensi_log_id_absensi_seq OWNED BY public.absensi_log.id_absensi;


--
-- TOC entry 235 (class 1259 OID 18213)
-- Name: absensi_logbook; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.absensi_logbook (
    id_absen integer NOT NULL,
    id_siswa integer,
    waktu_masuk timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    waktu_keluar timestamp without time zone,
    durasi_menit integer DEFAULT 0,
    tanggal date DEFAULT CURRENT_DATE
);


--
-- TOC entry 234 (class 1259 OID 18211)
-- Name: absensi_logbook_id_absen_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.absensi_logbook_id_absen_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3149 (class 0 OID 0)
-- Dependencies: 234
-- Name: absensi_logbook_id_absen_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.absensi_logbook_id_absen_seq OWNED BY public.absensi_logbook.id_absen;


--
-- TOC entry 207 (class 1259 OID 17612)
-- Name: enrollment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.enrollment (
    id_enrollment integer NOT NULL,
    id_siswa integer,
    id_kelas integer,
    status_aktif boolean DEFAULT true,
    tanggal_daftar timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- TOC entry 206 (class 1259 OID 17610)
-- Name: enrollment_id_enrollment_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.enrollment_id_enrollment_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3150 (class 0 OID 0)
-- Dependencies: 206
-- Name: enrollment_id_enrollment_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.enrollment_id_enrollment_seq OWNED BY public.enrollment.id_enrollment;


--
-- TOC entry 233 (class 1259 OID 18171)
-- Name: forum_chat; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.forum_chat (
    id_chat integer NOT NULL,
    id_materi integer,
    id_user integer,
    pesan text NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    parent_id integer
);


--
-- TOC entry 232 (class 1259 OID 18169)
-- Name: forum_chat_id_chat_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.forum_chat_id_chat_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3151 (class 0 OID 0)
-- Dependencies: 232
-- Name: forum_chat_id_chat_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.forum_chat_id_chat_seq OWNED BY public.forum_chat.id_chat;


--
-- TOC entry 229 (class 1259 OID 18121)
-- Name: forum_diskusi; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.forum_diskusi (
    id_diskusi integer NOT NULL,
    id_kelas integer,
    id_penulis integer,
    judul character varying(255) NOT NULL,
    pesan text NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- TOC entry 228 (class 1259 OID 18119)
-- Name: forum_diskusi_id_diskusi_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.forum_diskusi_id_diskusi_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3152 (class 0 OID 0)
-- Dependencies: 228
-- Name: forum_diskusi_id_diskusi_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.forum_diskusi_id_diskusi_seq OWNED BY public.forum_diskusi.id_diskusi;


--
-- TOC entry 211 (class 1259 OID 17689)
-- Name: forum_kelas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.forum_kelas (
    id_pesan integer NOT NULL,
    id_kelas integer,
    id_user integer,
    pesan text NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- TOC entry 210 (class 1259 OID 17687)
-- Name: forum_kelas_id_pesan_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.forum_kelas_id_pesan_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3153 (class 0 OID 0)
-- Dependencies: 210
-- Name: forum_kelas_id_pesan_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.forum_kelas_id_pesan_seq OWNED BY public.forum_kelas.id_pesan;


--
-- TOC entry 227 (class 1259 OID 18099)
-- Name: forum_komentar; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.forum_komentar (
    id_komentar integer NOT NULL,
    id_diskusi integer,
    id_penulis integer,
    isi_komentar text NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- TOC entry 226 (class 1259 OID 18097)
-- Name: forum_komentar_id_komentar_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.forum_komentar_id_komentar_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3154 (class 0 OID 0)
-- Dependencies: 226
-- Name: forum_komentar_id_komentar_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.forum_komentar_id_komentar_seq OWNED BY public.forum_komentar.id_komentar;


--
-- TOC entry 225 (class 1259 OID 18076)
-- Name: forum_topik; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.forum_topik (
    id_topik integer NOT NULL,
    id_kelas integer,
    id_penulis integer,
    judul_topik character varying(255) NOT NULL,
    isi_topik text NOT NULL,
    kategori character varying(50) DEFAULT 'Umum'::character varying,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- TOC entry 224 (class 1259 OID 18074)
-- Name: forum_topik_id_topik_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.forum_topik_id_topik_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3155 (class 0 OID 0)
-- Dependencies: 224
-- Name: forum_topik_id_topik_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.forum_topik_id_topik_seq OWNED BY public.forum_topik.id_topik;


--
-- TOC entry 221 (class 1259 OID 18017)
-- Name: jawaban_siswa; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.jawaban_siswa (
    id_jawaban integer NOT NULL,
    id_soal integer,
    id_siswa integer,
    jawaban_teks text,
    file_suara character varying(255),
    nilai_didapat integer DEFAULT 0,
    feedback_ai text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    file_rekaman character varying(255),
    durasi_detik integer DEFAULT 0,
    skor_ai integer
);


--
-- TOC entry 220 (class 1259 OID 18015)
-- Name: jawaban_siswa_id_jawaban_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.jawaban_siswa_id_jawaban_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3156 (class 0 OID 0)
-- Dependencies: 220
-- Name: jawaban_siswa_id_jawaban_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.jawaban_siswa_id_jawaban_seq OWNED BY public.jawaban_siswa.id_jawaban;


--
-- TOC entry 205 (class 1259 OID 17594)
-- Name: kelas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kelas (
    id_kelas integer NOT NULL,
    nama_kelas character varying(100) NOT NULL,
    id_pengajar integer,
    level_bahasa character varying(50) NOT NULL,
    tipe_kelas character varying(20) DEFAULT 'offline'::character varying,
    link_kelas text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- TOC entry 204 (class 1259 OID 17592)
-- Name: kelas_id_kelas_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kelas_id_kelas_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3157 (class 0 OID 0)
-- Dependencies: 204
-- Name: kelas_id_kelas_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kelas_id_kelas_seq OWNED BY public.kelas.id_kelas;


--
-- TOC entry 239 (class 1259 OID 18255)
-- Name: kelas_siswa; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kelas_siswa (
    id_kelas_siswa integer NOT NULL,
    id_kelas integer,
    id_siswa integer,
    tanggal_enroll timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- TOC entry 238 (class 1259 OID 18253)
-- Name: kelas_siswa_id_kelas_siswa_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kelas_siswa_id_kelas_siswa_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3158 (class 0 OID 0)
-- Dependencies: 238
-- Name: kelas_siswa_id_kelas_siswa_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kelas_siswa_id_kelas_siswa_seq OWNED BY public.kelas_siswa.id_kelas_siswa;


--
-- TOC entry 241 (class 1259 OID 18327)
-- Name: kuis; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kuis (
    id_kuis integer NOT NULL,
    id_kelas integer,
    judul_kuis character varying(255) NOT NULL,
    deskripsi text,
    waktu_menit integer DEFAULT 60,
    tanggal_dibuat timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    is_published boolean DEFAULT true
);


--
-- TOC entry 240 (class 1259 OID 18325)
-- Name: kuis_id_kuis_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kuis_id_kuis_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3159 (class 0 OID 0)
-- Dependencies: 240
-- Name: kuis_id_kuis_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kuis_id_kuis_seq OWNED BY public.kuis.id_kuis;


--
-- TOC entry 197 (class 1259 OID 17395)
-- Name: log_aktivitas_kuis; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.log_aktivitas_kuis (
    id_log integer NOT NULL,
    id_siswa integer,
    id_kuis integer,
    id_soal integer,
    jawaban_user character(1),
    is_correct boolean,
    waktu_pengerjaan_detik integer,
    tanggal_pengerjaan timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- TOC entry 196 (class 1259 OID 17393)
-- Name: log_aktivitas_kuis_id_log_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.log_aktivitas_kuis_id_log_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3160 (class 0 OID 0)
-- Dependencies: 196
-- Name: log_aktivitas_kuis_id_log_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.log_aktivitas_kuis_id_log_seq OWNED BY public.log_aktivitas_kuis.id_log;


--
-- TOC entry 213 (class 1259 OID 17740)
-- Name: materi; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.materi (
    id_materi integer NOT NULL,
    id_kelas integer,
    judul_materi character varying(200) NOT NULL,
    file_pdf character varying(255) NOT NULL,
    urutan integer DEFAULT 1,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- TOC entry 215 (class 1259 OID 17755)
-- Name: materi_audio; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.materi_audio (
    id_audio integer NOT NULL,
    id_materi integer,
    file_audio character varying(255) NOT NULL
);


--
-- TOC entry 214 (class 1259 OID 17753)
-- Name: materi_audio_id_audio_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.materi_audio_id_audio_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3161 (class 0 OID 0)
-- Dependencies: 214
-- Name: materi_audio_id_audio_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.materi_audio_id_audio_seq OWNED BY public.materi_audio.id_audio;


--
-- TOC entry 212 (class 1259 OID 17738)
-- Name: materi_id_materi_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.materi_id_materi_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3162 (class 0 OID 0)
-- Dependencies: 212
-- Name: materi_id_materi_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.materi_id_materi_seq OWNED BY public.materi.id_materi;


--
-- TOC entry 199 (class 1259 OID 17419)
-- Name: nilai_akhir_kuis; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.nilai_akhir_kuis (
    id_nilai integer NOT NULL,
    id_siswa integer,
    id_kuis integer,
    skor_total double precision NOT NULL,
    status_lulus boolean,
    waktu_selesai timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- TOC entry 198 (class 1259 OID 17417)
-- Name: nilai_akhir_kuis_id_nilai_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.nilai_akhir_kuis_id_nilai_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3163 (class 0 OID 0)
-- Dependencies: 198
-- Name: nilai_akhir_kuis_id_nilai_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.nilai_akhir_kuis_id_nilai_seq OWNED BY public.nilai_akhir_kuis.id_nilai;


--
-- TOC entry 223 (class 1259 OID 18042)
-- Name: nilai_kuis; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.nilai_kuis (
    id_nilai integer NOT NULL,
    id_kuis integer,
    id_siswa integer,
    total_nilai integer DEFAULT 0,
    catatan_analitik_ai text,
    waktu_selesai timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    skor double precision,
    status character varying(20) DEFAULT 'Selesai'::character varying
);


--
-- TOC entry 222 (class 1259 OID 18040)
-- Name: nilai_kuis_id_nilai_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.nilai_kuis_id_nilai_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3164 (class 0 OID 0)
-- Dependencies: 222
-- Name: nilai_kuis_id_nilai_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.nilai_kuis_id_nilai_seq OWNED BY public.nilai_kuis.id_nilai;


--
-- TOC entry 219 (class 1259 OID 18000)
-- Name: opsi_pg; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.opsi_pg (
    id_opsi integer NOT NULL,
    id_soal integer,
    teks_opsi text NOT NULL,
    is_benar boolean DEFAULT false
);


--
-- TOC entry 218 (class 1259 OID 17998)
-- Name: opsi_pg_id_opsi_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.opsi_pg_id_opsi_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3165 (class 0 OID 0)
-- Dependencies: 218
-- Name: opsi_pg_id_opsi_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.opsi_pg_id_opsi_seq OWNED BY public.opsi_pg.id_opsi;


--
-- TOC entry 217 (class 1259 OID 17770)
-- Name: progres_materi; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.progres_materi (
    id_progres integer NOT NULL,
    id_siswa integer,
    id_materi integer,
    status_selesai boolean DEFAULT false,
    waktu_selesai timestamp without time zone
);


--
-- TOC entry 216 (class 1259 OID 17768)
-- Name: progres_materi_id_progres_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.progres_materi_id_progres_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3166 (class 0 OID 0)
-- Dependencies: 216
-- Name: progres_materi_id_progres_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.progres_materi_id_progres_seq OWNED BY public.progres_materi.id_progres;


--
-- TOC entry 201 (class 1259 OID 17438)
-- Name: rekomendasi_ai; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.rekomendasi_ai (
    id_rekomendasi integer NOT NULL,
    id_siswa integer,
    kompetensi_lemah character varying(50),
    teks_rekomendasi text,
    id_materi_saran integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- TOC entry 200 (class 1259 OID 17436)
-- Name: rekomendasi_ai_id_rekomendasi_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.rekomendasi_ai_id_rekomendasi_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3167 (class 0 OID 0)
-- Dependencies: 200
-- Name: rekomendasi_ai_id_rekomendasi_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.rekomendasi_ai_id_rekomendasi_seq OWNED BY public.rekomendasi_ai.id_rekomendasi;


--
-- TOC entry 237 (class 1259 OID 18229)
-- Name: sertifikat; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sertifikat (
    id_sertifikat integer NOT NULL,
    id_siswa integer,
    nama_sertifikat character varying(255) NOT NULL,
    file_pdf character varying(255) NOT NULL,
    tanggal_keluar timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    status_approve boolean DEFAULT false,
    id_kelas integer
);


--
-- TOC entry 236 (class 1259 OID 18227)
-- Name: sertifikat_id_sertifikat_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.sertifikat_id_sertifikat_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3168 (class 0 OID 0)
-- Dependencies: 236
-- Name: sertifikat_id_sertifikat_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.sertifikat_id_sertifikat_seq OWNED BY public.sertifikat.id_sertifikat;


--
-- TOC entry 231 (class 1259 OID 18143)
-- Name: siswa_kelas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.siswa_kelas (
    id_siswa_kelas integer NOT NULL,
    id_siswa integer,
    id_kelas integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- TOC entry 230 (class 1259 OID 18141)
-- Name: siswa_kelas_id_siswa_kelas_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.siswa_kelas_id_siswa_kelas_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3169 (class 0 OID 0)
-- Dependencies: 230
-- Name: siswa_kelas_id_siswa_kelas_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.siswa_kelas_id_siswa_kelas_seq OWNED BY public.siswa_kelas.id_siswa_kelas;


--
-- TOC entry 243 (class 1259 OID 18340)
-- Name: soal_kuis; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.soal_kuis (
    id_soal integer NOT NULL,
    id_kuis integer,
    pertanyaan text NOT NULL,
    tipe_soal character varying(20) DEFAULT 'reading'::character varying,
    file_audio character varying(255),
    pilihan_a text,
    pilihan_b text,
    pilihan_c text,
    pilihan_d text,
    jawaban_benar text
);


--
-- TOC entry 242 (class 1259 OID 18338)
-- Name: soal_kuis_id_soal_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.soal_kuis_id_soal_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3170 (class 0 OID 0)
-- Dependencies: 242
-- Name: soal_kuis_id_soal_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.soal_kuis_id_soal_seq OWNED BY public.soal_kuis.id_soal;


--
-- TOC entry 203 (class 1259 OID 17582)
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id integer NOT NULL,
    nama_lengkap character varying(100) NOT NULL,
    username character varying(50) NOT NULL,
    password character varying(255) NOT NULL,
    role character varying(20) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT users_role_check CHECK (((role)::text = ANY ((ARRAY['siswa'::character varying, 'pengajar'::character varying, 'admin'::character varying])::text[])))
);


--
-- TOC entry 202 (class 1259 OID 17580)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3171 (class 0 OID 0)
-- Dependencies: 202
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 2836 (class 2604 OID 17637)
-- Name: absensi_log id_absensi; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.absensi_log ALTER COLUMN id_absensi SET DEFAULT nextval('public.absensi_log_id_absensi_seq'::regclass);


--
-- TOC entry 2869 (class 2604 OID 18216)
-- Name: absensi_logbook id_absen; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.absensi_logbook ALTER COLUMN id_absen SET DEFAULT nextval('public.absensi_logbook_id_absen_seq'::regclass);


--
-- TOC entry 2833 (class 2604 OID 17615)
-- Name: enrollment id_enrollment; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enrollment ALTER COLUMN id_enrollment SET DEFAULT nextval('public.enrollment_id_enrollment_seq'::regclass);


--
-- TOC entry 2867 (class 2604 OID 18174)
-- Name: forum_chat id_chat; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.forum_chat ALTER COLUMN id_chat SET DEFAULT nextval('public.forum_chat_id_chat_seq'::regclass);


--
-- TOC entry 2863 (class 2604 OID 18124)
-- Name: forum_diskusi id_diskusi; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.forum_diskusi ALTER COLUMN id_diskusi SET DEFAULT nextval('public.forum_diskusi_id_diskusi_seq'::regclass);


--
-- TOC entry 2840 (class 2604 OID 17692)
-- Name: forum_kelas id_pesan; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.forum_kelas ALTER COLUMN id_pesan SET DEFAULT nextval('public.forum_kelas_id_pesan_seq'::regclass);


--
-- TOC entry 2861 (class 2604 OID 18102)
-- Name: forum_komentar id_komentar; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.forum_komentar ALTER COLUMN id_komentar SET DEFAULT nextval('public.forum_komentar_id_komentar_seq'::regclass);


--
-- TOC entry 2858 (class 2604 OID 18079)
-- Name: forum_topik id_topik; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.forum_topik ALTER COLUMN id_topik SET DEFAULT nextval('public.forum_topik_id_topik_seq'::regclass);


--
-- TOC entry 2851 (class 2604 OID 18020)
-- Name: jawaban_siswa id_jawaban; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.jawaban_siswa ALTER COLUMN id_jawaban SET DEFAULT nextval('public.jawaban_siswa_id_jawaban_seq'::regclass);


--
-- TOC entry 2830 (class 2604 OID 17597)
-- Name: kelas id_kelas; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kelas ALTER COLUMN id_kelas SET DEFAULT nextval('public.kelas_id_kelas_seq'::regclass);


--
-- TOC entry 2876 (class 2604 OID 18258)
-- Name: kelas_siswa id_kelas_siswa; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kelas_siswa ALTER COLUMN id_kelas_siswa SET DEFAULT nextval('public.kelas_siswa_id_kelas_siswa_seq'::regclass);


--
-- TOC entry 2878 (class 2604 OID 18330)
-- Name: kuis id_kuis; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuis ALTER COLUMN id_kuis SET DEFAULT nextval('public.kuis_id_kuis_seq'::regclass);


--
-- TOC entry 2821 (class 2604 OID 17398)
-- Name: log_aktivitas_kuis id_log; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.log_aktivitas_kuis ALTER COLUMN id_log SET DEFAULT nextval('public.log_aktivitas_kuis_id_log_seq'::regclass);


--
-- TOC entry 2843 (class 2604 OID 17743)
-- Name: materi id_materi; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.materi ALTER COLUMN id_materi SET DEFAULT nextval('public.materi_id_materi_seq'::regclass);


--
-- TOC entry 2845 (class 2604 OID 17758)
-- Name: materi_audio id_audio; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.materi_audio ALTER COLUMN id_audio SET DEFAULT nextval('public.materi_audio_id_audio_seq'::regclass);


--
-- TOC entry 2823 (class 2604 OID 17422)
-- Name: nilai_akhir_kuis id_nilai; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.nilai_akhir_kuis ALTER COLUMN id_nilai SET DEFAULT nextval('public.nilai_akhir_kuis_id_nilai_seq'::regclass);


--
-- TOC entry 2854 (class 2604 OID 18045)
-- Name: nilai_kuis id_nilai; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.nilai_kuis ALTER COLUMN id_nilai SET DEFAULT nextval('public.nilai_kuis_id_nilai_seq'::regclass);


--
-- TOC entry 2848 (class 2604 OID 18003)
-- Name: opsi_pg id_opsi; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.opsi_pg ALTER COLUMN id_opsi SET DEFAULT nextval('public.opsi_pg_id_opsi_seq'::regclass);


--
-- TOC entry 2846 (class 2604 OID 17773)
-- Name: progres_materi id_progres; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.progres_materi ALTER COLUMN id_progres SET DEFAULT nextval('public.progres_materi_id_progres_seq'::regclass);


--
-- TOC entry 2825 (class 2604 OID 17441)
-- Name: rekomendasi_ai id_rekomendasi; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rekomendasi_ai ALTER COLUMN id_rekomendasi SET DEFAULT nextval('public.rekomendasi_ai_id_rekomendasi_seq'::regclass);


--
-- TOC entry 2873 (class 2604 OID 18232)
-- Name: sertifikat id_sertifikat; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sertifikat ALTER COLUMN id_sertifikat SET DEFAULT nextval('public.sertifikat_id_sertifikat_seq'::regclass);


--
-- TOC entry 2865 (class 2604 OID 18146)
-- Name: siswa_kelas id_siswa_kelas; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.siswa_kelas ALTER COLUMN id_siswa_kelas SET DEFAULT nextval('public.siswa_kelas_id_siswa_kelas_seq'::regclass);


--
-- TOC entry 2882 (class 2604 OID 18343)
-- Name: soal_kuis id_soal; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.soal_kuis ALTER COLUMN id_soal SET DEFAULT nextval('public.soal_kuis_id_soal_seq'::regclass);


--
-- TOC entry 2827 (class 2604 OID 17585)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 3104 (class 0 OID 17634)
-- Dependencies: 209
-- Data for Name: absensi_log; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.absensi_log (id_absensi, id_siswa, tanggal, waktu_login, waktu_logout, durasi_belajar_menit) VALUES (1, 3, '2026-05-11', '2026-05-11 07:33:03.158419', '2026-05-16 12:39:02.644048', 7506);
INSERT INTO public.absensi_log (id_absensi, id_siswa, tanggal, waktu_login, waktu_logout, durasi_belajar_menit) VALUES (2, 3, '2026-05-11', '2026-05-11 09:22:07.732101', '2026-05-16 12:39:02.644048', 7397);
INSERT INTO public.absensi_log (id_absensi, id_siswa, tanggal, waktu_login, waktu_logout, durasi_belajar_menit) VALUES (3, 3, '2026-05-16', '2026-05-16 12:01:51.130824', '2026-05-16 12:39:02.644048', 37);
INSERT INTO public.absensi_log (id_absensi, id_siswa, tanggal, waktu_login, waktu_logout, durasi_belajar_menit) VALUES (4, 3, '2026-05-16', '2026-05-16 12:03:55.597052', '2026-05-16 12:39:02.644048', 35);
INSERT INTO public.absensi_log (id_absensi, id_siswa, tanggal, waktu_login, waktu_logout, durasi_belajar_menit) VALUES (5, 3, '2026-05-16', '2026-05-16 12:13:35.996594', '2026-05-16 12:39:02.644048', 25);
INSERT INTO public.absensi_log (id_absensi, id_siswa, tanggal, waktu_login, waktu_logout, durasi_belajar_menit) VALUES (6, 3, '2026-05-16', '2026-05-16 12:43:09.893308', '2026-05-16 20:25:07.005544', 462);
INSERT INTO public.absensi_log (id_absensi, id_siswa, tanggal, waktu_login, waktu_logout, durasi_belajar_menit) VALUES (7, 3, '2026-05-16', '2026-05-16 20:26:51.298906', '2026-05-17 12:05:44.102359', 939);
INSERT INTO public.absensi_log (id_absensi, id_siswa, tanggal, waktu_login, waktu_logout, durasi_belajar_menit) VALUES (8, 3, '2026-05-17', '2026-05-17 12:06:57.598554', '2026-05-17 12:07:15.503586', 0);
INSERT INTO public.absensi_log (id_absensi, id_siswa, tanggal, waktu_login, waktu_logout, durasi_belajar_menit) VALUES (9, 3, '2026-05-17', '2026-05-17 12:17:12.060825', '2026-05-17 12:35:57.082261', 19);
INSERT INTO public.absensi_log (id_absensi, id_siswa, tanggal, waktu_login, waktu_logout, durasi_belajar_menit) VALUES (10, 3, '2026-05-17', '2026-05-17 12:40:57.372514', '2026-05-17 13:15:03.675151', 34);
INSERT INTO public.absensi_log (id_absensi, id_siswa, tanggal, waktu_login, waktu_logout, durasi_belajar_menit) VALUES (11, 3, '2026-05-17', '2026-05-17 13:16:23.067402', '2026-05-17 13:22:48.252281', 6);
INSERT INTO public.absensi_log (id_absensi, id_siswa, tanggal, waktu_login, waktu_logout, durasi_belajar_menit) VALUES (12, 3, '2026-05-17', '2026-05-17 19:28:24.596562', '2026-05-17 20:22:35.19129', 54);
INSERT INTO public.absensi_log (id_absensi, id_siswa, tanggal, waktu_login, waktu_logout, durasi_belajar_menit) VALUES (13, 3, '2026-05-17', '2026-05-17 20:39:44.442822', '2026-05-17 21:38:11.798311', 58);
INSERT INTO public.absensi_log (id_absensi, id_siswa, tanggal, waktu_login, waktu_logout, durasi_belajar_menit) VALUES (14, 3, '2026-05-17', '2026-05-17 21:35:49.132128', '2026-05-17 21:38:11.798311', 2);
INSERT INTO public.absensi_log (id_absensi, id_siswa, tanggal, waktu_login, waktu_logout, durasi_belajar_menit) VALUES (15, 3, '2026-05-18', '2026-05-18 07:43:33.284316', '2026-05-18 07:44:20.694143', 1);
INSERT INTO public.absensi_log (id_absensi, id_siswa, tanggal, waktu_login, waktu_logout, durasi_belajar_menit) VALUES (16, 3, '2026-05-18', '2026-05-18 08:09:55.360417', '2026-05-18 08:18:51.487913', 9);
INSERT INTO public.absensi_log (id_absensi, id_siswa, tanggal, waktu_login, waktu_logout, durasi_belajar_menit) VALUES (17, 3, '2026-05-18', '2026-05-18 08:19:38.016233', NULL, 0);
INSERT INTO public.absensi_log (id_absensi, id_siswa, tanggal, waktu_login, waktu_logout, durasi_belajar_menit) VALUES (18, 3, '2026-06-08', '2026-06-08 12:48:56.701685', NULL, 0);


--
-- TOC entry 3130 (class 0 OID 18213)
-- Dependencies: 235
-- Data for Name: absensi_logbook; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.absensi_logbook (id_absen, id_siswa, waktu_masuk, waktu_keluar, durasi_menit, tanggal) VALUES (1, 3, '2026-05-17 13:03:10.434143', '2026-05-17 13:03:20.044833', 1, '2026-05-17');


--
-- TOC entry 3102 (class 0 OID 17612)
-- Dependencies: 207
-- Data for Name: enrollment; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.enrollment (id_enrollment, id_siswa, id_kelas, status_aktif, tanggal_daftar) VALUES (1, 3, 1, true, '2026-05-10 17:55:00.879093');
INSERT INTO public.enrollment (id_enrollment, id_siswa, id_kelas, status_aktif, tanggal_daftar) VALUES (2, 3, 2, true, '2026-05-10 17:59:34.486385');


--
-- TOC entry 3128 (class 0 OID 18171)
-- Dependencies: 233
-- Data for Name: forum_chat; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.forum_chat (id_chat, id_materi, id_user, pesan, created_at, parent_id) VALUES (3, 1, 2, 'jadi gimana?', '2026-05-17 12:06:46.496884', NULL);
INSERT INTO public.forum_chat (id_chat, id_materi, id_user, pesan, created_at, parent_id) VALUES (4, 1, 3, 'aman pak', '2026-05-17 12:07:05.679262', 3);
INSERT INTO public.forum_chat (id_chat, id_materi, id_user, pesan, created_at, parent_id) VALUES (9, 1, 3, 'tes', '2026-05-17 20:18:24.593718', NULL);


--
-- TOC entry 3124 (class 0 OID 18121)
-- Dependencies: 229
-- Data for Name: forum_diskusi; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.forum_diskusi (id_diskusi, id_kelas, id_penulis, judul, pesan, created_at) VALUES (1, 1, 2, 'Kosakata', 'bagaimana? apakah sudah bisa?', '2026-05-10 22:34:20.675238');


--
-- TOC entry 3106 (class 0 OID 17689)
-- Dependencies: 211
-- Data for Name: forum_kelas; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- TOC entry 3122 (class 0 OID 18099)
-- Dependencies: 227
-- Data for Name: forum_komentar; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- TOC entry 3120 (class 0 OID 18076)
-- Dependencies: 225
-- Data for Name: forum_topik; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- TOC entry 3116 (class 0 OID 18017)
-- Dependencies: 221
-- Data for Name: jawaban_siswa; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- TOC entry 3100 (class 0 OID 17594)
-- Dependencies: 205
-- Data for Name: kelas; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.kelas (id_kelas, nama_kelas, id_pengajar, level_bahasa, tipe_kelas, link_kelas, created_at) VALUES (1, 'Kelas A', 2, 'Level 1', 'offline', '', '2026-05-10 17:54:46.513398');
INSERT INTO public.kelas (id_kelas, nama_kelas, id_pengajar, level_bahasa, tipe_kelas, link_kelas, created_at) VALUES (2, 'Kelas B', 2, 'Level 2', 'online', 'https://meet.google.com/kfn-piqt-hxt', '2026-05-10 17:59:26.224281');


--
-- TOC entry 3134 (class 0 OID 18255)
-- Dependencies: 239
-- Data for Name: kelas_siswa; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- TOC entry 3136 (class 0 OID 18327)
-- Dependencies: 241
-- Data for Name: kuis; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.kuis (id_kuis, id_kelas, judul_kuis, deskripsi, waktu_menit, tanggal_dibuat, is_published) VALUES (1, 1, 'Evaluasi Harian AI - Level Beginner', 'Uji coba AI AdaptEd untuk 4 kemampuan bahasa Korea', 60, '2026-05-18 08:54:01.422401', true);


--
-- TOC entry 3092 (class 0 OID 17395)
-- Dependencies: 197
-- Data for Name: log_aktivitas_kuis; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- TOC entry 3108 (class 0 OID 17740)
-- Dependencies: 213
-- Data for Name: materi; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.materi (id_materi, id_kelas, judul_materi, file_pdf, urutan, created_at) VALUES (1, 1, 'modul 1', 'Materi_K3LL.pdf', 1, '2026-05-10 18:26:33.204902');


--
-- TOC entry 3110 (class 0 OID 17755)
-- Dependencies: 215
-- Data for Name: materi_audio; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.materi_audio (id_audio, id_materi, file_audio) VALUES (1, 1, 'WhatsApp_Ptt_2026-03-04_at_08.51.00.ogg');
INSERT INTO public.materi_audio (id_audio, id_materi, file_audio) VALUES (2, 1, 'WhatsApp_Ptt_2026-03-04_at_06.56.04.ogg');
INSERT INTO public.materi_audio (id_audio, id_materi, file_audio) VALUES (3, 1, 'WhatsApp_Ptt_2026-02-19_at_15.58.26.ogg');


--
-- TOC entry 3094 (class 0 OID 17419)
-- Dependencies: 199
-- Data for Name: nilai_akhir_kuis; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- TOC entry 3118 (class 0 OID 18042)
-- Dependencies: 223
-- Data for Name: nilai_kuis; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.nilai_kuis (id_nilai, id_kuis, id_siswa, total_nilai, catatan_analitik_ai, waktu_selesai, skor, status) VALUES (2, 2, 1, 0, NULL, '2026-05-10 22:39:06.601935', 85, 'Selesai');


--
-- TOC entry 3114 (class 0 OID 18000)
-- Dependencies: 219
-- Data for Name: opsi_pg; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.opsi_pg (id_opsi, id_soal, teks_opsi, is_benar) VALUES (9, 4, 'Guru', false);
INSERT INTO public.opsi_pg (id_opsi, id_soal, teks_opsi, is_benar) VALUES (10, 4, 'Siswa', true);
INSERT INTO public.opsi_pg (id_opsi, id_soal, teks_opsi, is_benar) VALUES (11, 4, 'Dokter', false);
INSERT INTO public.opsi_pg (id_opsi, id_soal, teks_opsi, is_benar) VALUES (12, 4, 'Polisi', false);
INSERT INTO public.opsi_pg (id_opsi, id_soal, teks_opsi, is_benar) VALUES (13, 8, 'ijfia', true);
INSERT INTO public.opsi_pg (id_opsi, id_soal, teks_opsi, is_benar) VALUES (14, 8, 'sjci', false);
INSERT INTO public.opsi_pg (id_opsi, id_soal, teks_opsi, is_benar) VALUES (15, 8, 'scjsa', false);
INSERT INTO public.opsi_pg (id_opsi, id_soal, teks_opsi, is_benar) VALUES (16, 8, 'sjcpjsa', false);


--
-- TOC entry 3112 (class 0 OID 17770)
-- Dependencies: 217
-- Data for Name: progres_materi; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- TOC entry 3096 (class 0 OID 17438)
-- Dependencies: 201
-- Data for Name: rekomendasi_ai; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- TOC entry 3132 (class 0 OID 18229)
-- Dependencies: 237
-- Data for Name: sertifikat; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.sertifikat (id_sertifikat, id_siswa, nama_sertifikat, file_pdf, tanggal_keluar, status_approve, id_kelas) VALUES (1, 3, 'lulus', 'uploads/sertifikat/Quotation_-_S00026.pdf', '2026-05-17 13:24:47.329278', false, NULL);


--
-- TOC entry 3126 (class 0 OID 18143)
-- Dependencies: 231
-- Data for Name: siswa_kelas; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- TOC entry 3138 (class 0 OID 18340)
-- Dependencies: 243
-- Data for Name: soal_kuis; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.soal_kuis (id_soal, id_kuis, pertanyaan, tipe_soal, file_audio, pilihan_a, pilihan_b, pilihan_c, pilihan_d, jawaban_benar) VALUES (1, 1, 'Bacalah teks berikut dan tentukan artinya: "저는 Nicholas입니다."', 'reading', NULL, 'Saya adalah Nicholas', 'Nama saya adalah Budi', 'Saya pergi ke sekolah', 'Nicholas pergi ke pasar', 'A');
INSERT INTO public.soal_kuis (id_soal, id_kuis, pertanyaan, tipe_soal, file_audio, pilihan_a, pilihan_b, pilihan_c, pilihan_d, jawaban_benar) VALUES (2, 1, 'Dengarkan kalimat berikut dengan saksama dan ketikkan ulang teks Hangeul yang kamu dengar!', 'listening', 'audio/percakapan1.mp3', NULL, NULL, NULL, NULL, '안녕하세요');
INSERT INTO public.soal_kuis (id_soal, id_kuis, pertanyaan, tipe_soal, file_audio, pilihan_a, pilihan_b, pilihan_c, pilihan_d, jawaban_benar) VALUES (3, 1, 'Tekan tombol mikrofon di bawah, lalu ucapkan kalimat salam berikut dengan pelafalan yang jelas: "감사합니다"', 'speaking', NULL, NULL, NULL, NULL, NULL, '감사합니다');
INSERT INTO public.soal_kuis (id_soal, id_kuis, pertanyaan, tipe_soal, file_audio, pilihan_a, pilihan_b, pilihan_c, pilihan_d, jawaban_benar) VALUES (4, 1, 'Tuliskan sebuah esai pendek dalam bahasa Korea (Hangeul) mengenai aktivitas yang kamu lakukan pada akhir pekan ini!', 'writing', NULL, NULL, NULL, NULL, NULL, '주말');


--
-- TOC entry 3098 (class 0 OID 17582)
-- Dependencies: 203
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.users (id, nama_lengkap, username, password, role, created_at) VALUES (1, 'Admin', 'admin_namsan', 'scrypt:32768:8:1$vt5SrFTSBpk7InfU$959a42c67ea086cd0308d4b99ba61c48dde6176bd49a68ee98cedbc144cd900bbca00d3ddb24c6b2d34a747bbbba414f622f54c9db3088ce26731d31fae1c7a0', 'admin', '2026-05-10 17:52:35.484161');
INSERT INTO public.users (id, nama_lengkap, username, password, role, created_at) VALUES (2, 'seonsaengnim_kim', 'seonsaengnim_kim', 'scrypt:32768:8:1$Eq6vftyI16HwpJ6U$efc06591b05a552755c3d73744b0d4bd4371a336a6a0ce3406113e5fbc1562d8639e66f86dc9059a43105d8b8ed6b7f4b91cb59504a21420e9175139fee3868b', 'pengajar', '2026-05-10 17:54:08.545219');
INSERT INTO public.users (id, nama_lengkap, username, password, role, created_at) VALUES (3, 'siswa_budi', 'siswa_budi', 'scrypt:32768:8:1$zwDpJDjmKnCJ0E03$3135fd90f293148fe561823f1e5e0e612748474bf3ca979949f661b543a2fa45b94d05173593988df805fabe0f24fd6a8eb3938ebf26f6351cf7263ce0a32ea3', 'siswa', '2026-05-10 17:54:34.589203');


--
-- TOC entry 3172 (class 0 OID 0)
-- Dependencies: 208
-- Name: absensi_log_id_absensi_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.absensi_log_id_absensi_seq', 18, true);


--
-- TOC entry 3173 (class 0 OID 0)
-- Dependencies: 234
-- Name: absensi_logbook_id_absen_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.absensi_logbook_id_absen_seq', 1, true);


--
-- TOC entry 3174 (class 0 OID 0)
-- Dependencies: 206
-- Name: enrollment_id_enrollment_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.enrollment_id_enrollment_seq', 2, true);


--
-- TOC entry 3175 (class 0 OID 0)
-- Dependencies: 232
-- Name: forum_chat_id_chat_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.forum_chat_id_chat_seq', 9, true);


--
-- TOC entry 3176 (class 0 OID 0)
-- Dependencies: 228
-- Name: forum_diskusi_id_diskusi_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.forum_diskusi_id_diskusi_seq', 1, true);


--
-- TOC entry 3177 (class 0 OID 0)
-- Dependencies: 210
-- Name: forum_kelas_id_pesan_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.forum_kelas_id_pesan_seq', 1, false);


--
-- TOC entry 3178 (class 0 OID 0)
-- Dependencies: 226
-- Name: forum_komentar_id_komentar_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.forum_komentar_id_komentar_seq', 1, false);


--
-- TOC entry 3179 (class 0 OID 0)
-- Dependencies: 224
-- Name: forum_topik_id_topik_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.forum_topik_id_topik_seq', 1, false);


--
-- TOC entry 3180 (class 0 OID 0)
-- Dependencies: 220
-- Name: jawaban_siswa_id_jawaban_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.jawaban_siswa_id_jawaban_seq', 1, false);


--
-- TOC entry 3181 (class 0 OID 0)
-- Dependencies: 204
-- Name: kelas_id_kelas_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.kelas_id_kelas_seq', 2, true);


--
-- TOC entry 3182 (class 0 OID 0)
-- Dependencies: 238
-- Name: kelas_siswa_id_kelas_siswa_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.kelas_siswa_id_kelas_siswa_seq', 1, false);


--
-- TOC entry 3183 (class 0 OID 0)
-- Dependencies: 240
-- Name: kuis_id_kuis_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.kuis_id_kuis_seq', 1, false);


--
-- TOC entry 3184 (class 0 OID 0)
-- Dependencies: 196
-- Name: log_aktivitas_kuis_id_log_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.log_aktivitas_kuis_id_log_seq', 1, false);


--
-- TOC entry 3185 (class 0 OID 0)
-- Dependencies: 214
-- Name: materi_audio_id_audio_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.materi_audio_id_audio_seq', 3, true);


--
-- TOC entry 3186 (class 0 OID 0)
-- Dependencies: 212
-- Name: materi_id_materi_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.materi_id_materi_seq', 1, true);


--
-- TOC entry 3187 (class 0 OID 0)
-- Dependencies: 198
-- Name: nilai_akhir_kuis_id_nilai_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.nilai_akhir_kuis_id_nilai_seq', 1, false);


--
-- TOC entry 3188 (class 0 OID 0)
-- Dependencies: 222
-- Name: nilai_kuis_id_nilai_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.nilai_kuis_id_nilai_seq', 2, true);


--
-- TOC entry 3189 (class 0 OID 0)
-- Dependencies: 218
-- Name: opsi_pg_id_opsi_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.opsi_pg_id_opsi_seq', 16, true);


--
-- TOC entry 3190 (class 0 OID 0)
-- Dependencies: 216
-- Name: progres_materi_id_progres_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.progres_materi_id_progres_seq', 1, false);


--
-- TOC entry 3191 (class 0 OID 0)
-- Dependencies: 200
-- Name: rekomendasi_ai_id_rekomendasi_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.rekomendasi_ai_id_rekomendasi_seq', 1, false);


--
-- TOC entry 3192 (class 0 OID 0)
-- Dependencies: 236
-- Name: sertifikat_id_sertifikat_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.sertifikat_id_sertifikat_seq', 1, true);


--
-- TOC entry 3193 (class 0 OID 0)
-- Dependencies: 230
-- Name: siswa_kelas_id_siswa_kelas_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.siswa_kelas_id_siswa_kelas_seq', 1, false);


--
-- TOC entry 3194 (class 0 OID 0)
-- Dependencies: 242
-- Name: soal_kuis_id_soal_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.soal_kuis_id_soal_seq', 1, false);


--
-- TOC entry 3195 (class 0 OID 0)
-- Dependencies: 202
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_id_seq', 3, true);


--
-- TOC entry 2901 (class 2606 OID 17642)
-- Name: absensi_log absensi_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.absensi_log
    ADD CONSTRAINT absensi_log_pkey PRIMARY KEY (id_absensi);


--
-- TOC entry 2933 (class 2606 OID 18221)
-- Name: absensi_logbook absensi_logbook_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.absensi_logbook
    ADD CONSTRAINT absensi_logbook_pkey PRIMARY KEY (id_absen);


--
-- TOC entry 2897 (class 2606 OID 17621)
-- Name: enrollment enrollment_id_siswa_id_kelas_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enrollment
    ADD CONSTRAINT enrollment_id_siswa_id_kelas_key UNIQUE (id_siswa, id_kelas);


--
-- TOC entry 2899 (class 2606 OID 17619)
-- Name: enrollment enrollment_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enrollment
    ADD CONSTRAINT enrollment_pkey PRIMARY KEY (id_enrollment);


--
-- TOC entry 2931 (class 2606 OID 18180)
-- Name: forum_chat forum_chat_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.forum_chat
    ADD CONSTRAINT forum_chat_pkey PRIMARY KEY (id_chat);


--
-- TOC entry 2927 (class 2606 OID 18130)
-- Name: forum_diskusi forum_diskusi_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.forum_diskusi
    ADD CONSTRAINT forum_diskusi_pkey PRIMARY KEY (id_diskusi);


--
-- TOC entry 2903 (class 2606 OID 17698)
-- Name: forum_kelas forum_kelas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.forum_kelas
    ADD CONSTRAINT forum_kelas_pkey PRIMARY KEY (id_pesan);


--
-- TOC entry 2925 (class 2606 OID 18108)
-- Name: forum_komentar forum_komentar_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.forum_komentar
    ADD CONSTRAINT forum_komentar_pkey PRIMARY KEY (id_komentar);


--
-- TOC entry 2923 (class 2606 OID 18086)
-- Name: forum_topik forum_topik_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.forum_topik
    ADD CONSTRAINT forum_topik_pkey PRIMARY KEY (id_topik);


--
-- TOC entry 2915 (class 2606 OID 18029)
-- Name: jawaban_siswa jawaban_siswa_id_soal_id_siswa_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.jawaban_siswa
    ADD CONSTRAINT jawaban_siswa_id_soal_id_siswa_key UNIQUE (id_soal, id_siswa);


--
-- TOC entry 2917 (class 2606 OID 18027)
-- Name: jawaban_siswa jawaban_siswa_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.jawaban_siswa
    ADD CONSTRAINT jawaban_siswa_pkey PRIMARY KEY (id_jawaban);


--
-- TOC entry 2895 (class 2606 OID 17604)
-- Name: kelas kelas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kelas
    ADD CONSTRAINT kelas_pkey PRIMARY KEY (id_kelas);


--
-- TOC entry 2937 (class 2606 OID 18261)
-- Name: kelas_siswa kelas_siswa_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kelas_siswa
    ADD CONSTRAINT kelas_siswa_pkey PRIMARY KEY (id_kelas_siswa);


--
-- TOC entry 2939 (class 2606 OID 18337)
-- Name: kuis kuis_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuis
    ADD CONSTRAINT kuis_pkey PRIMARY KEY (id_kuis);


--
-- TOC entry 2885 (class 2606 OID 17401)
-- Name: log_aktivitas_kuis log_aktivitas_kuis_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.log_aktivitas_kuis
    ADD CONSTRAINT log_aktivitas_kuis_pkey PRIMARY KEY (id_log);


--
-- TOC entry 2907 (class 2606 OID 17760)
-- Name: materi_audio materi_audio_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.materi_audio
    ADD CONSTRAINT materi_audio_pkey PRIMARY KEY (id_audio);


--
-- TOC entry 2905 (class 2606 OID 17747)
-- Name: materi materi_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.materi
    ADD CONSTRAINT materi_pkey PRIMARY KEY (id_materi);


--
-- TOC entry 2887 (class 2606 OID 17425)
-- Name: nilai_akhir_kuis nilai_akhir_kuis_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.nilai_akhir_kuis
    ADD CONSTRAINT nilai_akhir_kuis_pkey PRIMARY KEY (id_nilai);


--
-- TOC entry 2919 (class 2606 OID 18054)
-- Name: nilai_kuis nilai_kuis_id_kuis_id_siswa_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.nilai_kuis
    ADD CONSTRAINT nilai_kuis_id_kuis_id_siswa_key UNIQUE (id_kuis, id_siswa);


--
-- TOC entry 2921 (class 2606 OID 18052)
-- Name: nilai_kuis nilai_kuis_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.nilai_kuis
    ADD CONSTRAINT nilai_kuis_pkey PRIMARY KEY (id_nilai);


--
-- TOC entry 2913 (class 2606 OID 18009)
-- Name: opsi_pg opsi_pg_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.opsi_pg
    ADD CONSTRAINT opsi_pg_pkey PRIMARY KEY (id_opsi);


--
-- TOC entry 2909 (class 2606 OID 17778)
-- Name: progres_materi progres_materi_id_siswa_id_materi_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.progres_materi
    ADD CONSTRAINT progres_materi_id_siswa_id_materi_key UNIQUE (id_siswa, id_materi);


--
-- TOC entry 2911 (class 2606 OID 17776)
-- Name: progres_materi progres_materi_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.progres_materi
    ADD CONSTRAINT progres_materi_pkey PRIMARY KEY (id_progres);


--
-- TOC entry 2889 (class 2606 OID 17447)
-- Name: rekomendasi_ai rekomendasi_ai_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rekomendasi_ai
    ADD CONSTRAINT rekomendasi_ai_pkey PRIMARY KEY (id_rekomendasi);


--
-- TOC entry 2935 (class 2606 OID 18238)
-- Name: sertifikat sertifikat_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sertifikat
    ADD CONSTRAINT sertifikat_pkey PRIMARY KEY (id_sertifikat);


--
-- TOC entry 2929 (class 2606 OID 18149)
-- Name: siswa_kelas siswa_kelas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.siswa_kelas
    ADD CONSTRAINT siswa_kelas_pkey PRIMARY KEY (id_siswa_kelas);


--
-- TOC entry 2941 (class 2606 OID 18349)
-- Name: soal_kuis soal_kuis_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.soal_kuis
    ADD CONSTRAINT soal_kuis_pkey PRIMARY KEY (id_soal);


--
-- TOC entry 2891 (class 2606 OID 17589)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 2893 (class 2606 OID 17591)
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- TOC entry 2945 (class 2606 OID 17643)
-- Name: absensi_log absensi_log_id_siswa_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.absensi_log
    ADD CONSTRAINT absensi_log_id_siswa_fkey FOREIGN KEY (id_siswa) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 2965 (class 2606 OID 18222)
-- Name: absensi_logbook absensi_logbook_id_siswa_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.absensi_logbook
    ADD CONSTRAINT absensi_logbook_id_siswa_fkey FOREIGN KEY (id_siswa) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 2944 (class 2606 OID 17627)
-- Name: enrollment enrollment_id_kelas_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enrollment
    ADD CONSTRAINT enrollment_id_kelas_fkey FOREIGN KEY (id_kelas) REFERENCES public.kelas(id_kelas) ON DELETE CASCADE;


--
-- TOC entry 2943 (class 2606 OID 17622)
-- Name: enrollment enrollment_id_siswa_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enrollment
    ADD CONSTRAINT enrollment_id_siswa_fkey FOREIGN KEY (id_siswa) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 2962 (class 2606 OID 18181)
-- Name: forum_chat forum_chat_id_materi_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.forum_chat
    ADD CONSTRAINT forum_chat_id_materi_fkey FOREIGN KEY (id_materi) REFERENCES public.materi(id_materi) ON DELETE CASCADE;


--
-- TOC entry 2963 (class 2606 OID 18186)
-- Name: forum_chat forum_chat_id_user_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.forum_chat
    ADD CONSTRAINT forum_chat_id_user_fkey FOREIGN KEY (id_user) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 2964 (class 2606 OID 18206)
-- Name: forum_chat forum_chat_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.forum_chat
    ADD CONSTRAINT forum_chat_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.forum_chat(id_chat) ON DELETE SET NULL;


--
-- TOC entry 2958 (class 2606 OID 18131)
-- Name: forum_diskusi forum_diskusi_id_kelas_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.forum_diskusi
    ADD CONSTRAINT forum_diskusi_id_kelas_fkey FOREIGN KEY (id_kelas) REFERENCES public.kelas(id_kelas) ON DELETE CASCADE;


--
-- TOC entry 2959 (class 2606 OID 18136)
-- Name: forum_diskusi forum_diskusi_id_penulis_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.forum_diskusi
    ADD CONSTRAINT forum_diskusi_id_penulis_fkey FOREIGN KEY (id_penulis) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 2946 (class 2606 OID 17699)
-- Name: forum_kelas forum_kelas_id_kelas_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.forum_kelas
    ADD CONSTRAINT forum_kelas_id_kelas_fkey FOREIGN KEY (id_kelas) REFERENCES public.kelas(id_kelas) ON DELETE CASCADE;


--
-- TOC entry 2947 (class 2606 OID 17704)
-- Name: forum_kelas forum_kelas_id_user_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.forum_kelas
    ADD CONSTRAINT forum_kelas_id_user_fkey FOREIGN KEY (id_user) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 2957 (class 2606 OID 18114)
-- Name: forum_komentar forum_komentar_id_penulis_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.forum_komentar
    ADD CONSTRAINT forum_komentar_id_penulis_fkey FOREIGN KEY (id_penulis) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 2956 (class 2606 OID 18109)
-- Name: forum_komentar forum_komentar_id_topik_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.forum_komentar
    ADD CONSTRAINT forum_komentar_id_topik_fkey FOREIGN KEY (id_diskusi) REFERENCES public.forum_topik(id_topik) ON DELETE CASCADE;


--
-- TOC entry 2954 (class 2606 OID 18087)
-- Name: forum_topik forum_topik_id_kelas_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.forum_topik
    ADD CONSTRAINT forum_topik_id_kelas_fkey FOREIGN KEY (id_kelas) REFERENCES public.kelas(id_kelas) ON DELETE CASCADE;


--
-- TOC entry 2955 (class 2606 OID 18092)
-- Name: forum_topik forum_topik_id_penulis_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.forum_topik
    ADD CONSTRAINT forum_topik_id_penulis_fkey FOREIGN KEY (id_penulis) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 2952 (class 2606 OID 18035)
-- Name: jawaban_siswa jawaban_siswa_id_siswa_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.jawaban_siswa
    ADD CONSTRAINT jawaban_siswa_id_siswa_fkey FOREIGN KEY (id_siswa) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 2942 (class 2606 OID 17605)
-- Name: kelas kelas_id_pengajar_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kelas
    ADD CONSTRAINT kelas_id_pengajar_fkey FOREIGN KEY (id_pengajar) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- TOC entry 2967 (class 2606 OID 18262)
-- Name: kelas_siswa kelas_siswa_id_kelas_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kelas_siswa
    ADD CONSTRAINT kelas_siswa_id_kelas_fkey FOREIGN KEY (id_kelas) REFERENCES public.kelas(id_kelas) ON DELETE CASCADE;


--
-- TOC entry 2968 (class 2606 OID 18267)
-- Name: kelas_siswa kelas_siswa_id_siswa_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kelas_siswa
    ADD CONSTRAINT kelas_siswa_id_siswa_fkey FOREIGN KEY (id_siswa) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 2949 (class 2606 OID 17761)
-- Name: materi_audio materi_audio_id_materi_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.materi_audio
    ADD CONSTRAINT materi_audio_id_materi_fkey FOREIGN KEY (id_materi) REFERENCES public.materi(id_materi) ON DELETE CASCADE;


--
-- TOC entry 2948 (class 2606 OID 17748)
-- Name: materi materi_id_kelas_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.materi
    ADD CONSTRAINT materi_id_kelas_fkey FOREIGN KEY (id_kelas) REFERENCES public.kelas(id_kelas) ON DELETE CASCADE;


--
-- TOC entry 2953 (class 2606 OID 18060)
-- Name: nilai_kuis nilai_kuis_id_siswa_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.nilai_kuis
    ADD CONSTRAINT nilai_kuis_id_siswa_fkey FOREIGN KEY (id_siswa) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 2951 (class 2606 OID 17784)
-- Name: progres_materi progres_materi_id_materi_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.progres_materi
    ADD CONSTRAINT progres_materi_id_materi_fkey FOREIGN KEY (id_materi) REFERENCES public.materi(id_materi) ON DELETE CASCADE;


--
-- TOC entry 2950 (class 2606 OID 17779)
-- Name: progres_materi progres_materi_id_siswa_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.progres_materi
    ADD CONSTRAINT progres_materi_id_siswa_fkey FOREIGN KEY (id_siswa) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 2966 (class 2606 OID 18239)
-- Name: sertifikat sertifikat_id_siswa_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sertifikat
    ADD CONSTRAINT sertifikat_id_siswa_fkey FOREIGN KEY (id_siswa) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 2961 (class 2606 OID 18155)
-- Name: siswa_kelas siswa_kelas_id_kelas_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.siswa_kelas
    ADD CONSTRAINT siswa_kelas_id_kelas_fkey FOREIGN KEY (id_kelas) REFERENCES public.kelas(id_kelas) ON DELETE CASCADE;


--
-- TOC entry 2960 (class 2606 OID 18150)
-- Name: siswa_kelas siswa_kelas_id_siswa_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.siswa_kelas
    ADD CONSTRAINT siswa_kelas_id_siswa_fkey FOREIGN KEY (id_siswa) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 2969 (class 2606 OID 18350)
-- Name: soal_kuis soal_kuis_id_kuis_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.soal_kuis
    ADD CONSTRAINT soal_kuis_id_kuis_fkey FOREIGN KEY (id_kuis) REFERENCES public.kuis(id_kuis) ON DELETE CASCADE;


--
-- TOC entry 3146 (class 0 OID 0)
-- Dependencies: 6
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: -
--

GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2026-06-08 20:29:56

--
-- PostgreSQL database dump complete
--

