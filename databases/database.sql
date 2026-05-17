--
-- PostgreSQL database dump
--

-- Dumped from database version 10.23
-- Dumped by pg_dump version 10.23

-- Started on 2026-05-17 20:32:54

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
-- TOC entry 3108 (class 0 OID 17634)
-- Dependencies: 209
-- Data for Name: absensi_log; Type: TABLE DATA; Schema: public; Owner: postgres
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


--
-- TOC entry 3138 (class 0 OID 18213)
-- Dependencies: 239
-- Data for Name: absensi_logbook; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.absensi_logbook (id_absen, id_siswa, waktu_masuk, waktu_keluar, durasi_menit, tanggal) VALUES (1, 3, '2026-05-17 13:03:10.434143', '2026-05-17 13:03:20.044833', 1, '2026-05-17');


--
-- TOC entry 3106 (class 0 OID 17612)
-- Dependencies: 207
-- Data for Name: enrollment; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.enrollment (id_enrollment, id_siswa, id_kelas, status_aktif, tanggal_daftar) VALUES (1, 3, 1, true, '2026-05-10 17:55:00.879093');
INSERT INTO public.enrollment (id_enrollment, id_siswa, id_kelas, status_aktif, tanggal_daftar) VALUES (2, 3, 2, true, '2026-05-10 17:59:34.486385');


--
-- TOC entry 3136 (class 0 OID 18171)
-- Dependencies: 237
-- Data for Name: forum_chat; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.forum_chat (id_chat, id_materi, id_user, pesan, created_at, parent_id) VALUES (3, 1, 2, 'jadi gimana?', '2026-05-17 12:06:46.496884', NULL);
INSERT INTO public.forum_chat (id_chat, id_materi, id_user, pesan, created_at, parent_id) VALUES (4, 1, 3, 'aman pak', '2026-05-17 12:07:05.679262', 3);
INSERT INTO public.forum_chat (id_chat, id_materi, id_user, pesan, created_at, parent_id) VALUES (9, 1, 3, 'tes', '2026-05-17 20:18:24.593718', NULL);


--
-- TOC entry 3132 (class 0 OID 18121)
-- Dependencies: 233
-- Data for Name: forum_diskusi; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.forum_diskusi (id_diskusi, id_kelas, id_penulis, judul, pesan, created_at) VALUES (1, 1, 2, 'Kosakata', 'bagaimana? apakah sudah bisa?', '2026-05-10 22:34:20.675238');


--
-- TOC entry 3110 (class 0 OID 17689)
-- Dependencies: 211
-- Data for Name: forum_kelas; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3130 (class 0 OID 18099)
-- Dependencies: 231
-- Data for Name: forum_komentar; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3128 (class 0 OID 18076)
-- Dependencies: 229
-- Data for Name: forum_topik; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3124 (class 0 OID 18017)
-- Dependencies: 225
-- Data for Name: jawaban_siswa; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3104 (class 0 OID 17594)
-- Dependencies: 205
-- Data for Name: kelas; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.kelas (id_kelas, nama_kelas, id_pengajar, level_bahasa, tipe_kelas, link_kelas, created_at) VALUES (1, 'Kelas A', 2, 'Level 1', 'offline', '', '2026-05-10 17:54:46.513398');
INSERT INTO public.kelas (id_kelas, nama_kelas, id_pengajar, level_bahasa, tipe_kelas, link_kelas, created_at) VALUES (2, 'Kelas B', 2, 'Level 2', 'online', 'https://meet.google.com/kfn-piqt-hxt', '2026-05-10 17:59:26.224281');


--
-- TOC entry 3142 (class 0 OID 18255)
-- Dependencies: 243
-- Data for Name: kelas_siswa; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3118 (class 0 OID 17964)
-- Dependencies: 219
-- Data for Name: kuis; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.kuis (id_kuis, id_kelas, judul_kuis, deskripsi, tingkat_kesulitan, created_at, is_published) VALUES (2, 1, 'Kosakata', '', 'Sedang', '2026-05-10 21:54:05.949272', true);
INSERT INTO public.kuis (id_kuis, id_kelas, judul_kuis, deskripsi, tingkat_kesulitan, created_at, is_published) VALUES (3, 1, 'Kosakata', '', 'Mudah', '2026-05-10 23:02:29.288801', true);
INSERT INTO public.kuis (id_kuis, id_kelas, judul_kuis, deskripsi, tingkat_kesulitan, created_at, is_published) VALUES (4, 2, 'batchim', '', 'Sulit', '2026-05-11 07:28:42.782657', false);


--
-- TOC entry 3096 (class 0 OID 17395)
-- Dependencies: 197
-- Data for Name: log_aktivitas_kuis; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3112 (class 0 OID 17740)
-- Dependencies: 213
-- Data for Name: materi; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.materi (id_materi, id_kelas, judul_materi, file_pdf, urutan, created_at) VALUES (1, 1, 'modul 1', 'Materi_K3LL.pdf', 1, '2026-05-10 18:26:33.204902');


--
-- TOC entry 3114 (class 0 OID 17755)
-- Dependencies: 215
-- Data for Name: materi_audio; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.materi_audio (id_audio, id_materi, file_audio) VALUES (1, 1, 'WhatsApp_Ptt_2026-03-04_at_08.51.00.ogg');
INSERT INTO public.materi_audio (id_audio, id_materi, file_audio) VALUES (2, 1, 'WhatsApp_Ptt_2026-03-04_at_06.56.04.ogg');
INSERT INTO public.materi_audio (id_audio, id_materi, file_audio) VALUES (3, 1, 'WhatsApp_Ptt_2026-02-19_at_15.58.26.ogg');


--
-- TOC entry 3098 (class 0 OID 17419)
-- Dependencies: 199
-- Data for Name: nilai_akhir_kuis; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3126 (class 0 OID 18042)
-- Dependencies: 227
-- Data for Name: nilai_kuis; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.nilai_kuis (id_nilai, id_kuis, id_siswa, total_nilai, catatan_analitik_ai, waktu_selesai, skor, status) VALUES (2, 2, 1, 0, NULL, '2026-05-10 22:39:06.601935', 85, 'Selesai');


--
-- TOC entry 3122 (class 0 OID 18000)
-- Dependencies: 223
-- Data for Name: opsi_pg; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.opsi_pg (id_opsi, id_soal, teks_opsi, is_benar) VALUES (9, 4, 'Guru', false);
INSERT INTO public.opsi_pg (id_opsi, id_soal, teks_opsi, is_benar) VALUES (10, 4, 'Siswa', true);
INSERT INTO public.opsi_pg (id_opsi, id_soal, teks_opsi, is_benar) VALUES (11, 4, 'Dokter', false);
INSERT INTO public.opsi_pg (id_opsi, id_soal, teks_opsi, is_benar) VALUES (12, 4, 'Polisi', false);


--
-- TOC entry 3116 (class 0 OID 17770)
-- Dependencies: 217
-- Data for Name: progres_materi; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3100 (class 0 OID 17438)
-- Dependencies: 201
-- Data for Name: rekomendasi_ai; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3140 (class 0 OID 18229)
-- Dependencies: 241
-- Data for Name: sertifikat; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.sertifikat (id_sertifikat, id_siswa, nama_sertifikat, file_pdf, tanggal_keluar, status_approve, id_kelas) VALUES (1, 3, 'lulus', 'uploads/sertifikat/Quotation_-_S00026.pdf', '2026-05-17 13:24:47.329278', false, NULL);


--
-- TOC entry 3134 (class 0 OID 18143)
-- Dependencies: 235
-- Data for Name: siswa_kelas; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3120 (class 0 OID 17982)
-- Dependencies: 221
-- Data for Name: soal_kuis; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.soal_kuis (id_soal, id_kuis, tipe_soal, teks_soal, file_media, kunci_jawaban, poin) VALUES (4, 2, 'Pilihan Ganda', 'Apa arti dari kosakata "학생" ?', NULL, NULL, 10);
INSERT INTO public.soal_kuis (id_soal, id_kuis, tipe_soal, teks_soal, file_media, kunci_jawaban, poin) VALUES (5, 2, 'Isian', 'Lengkapi kalimat berikut dengan partikel subjek yang tepat: "저___ Nicholas입니다."', NULL, '는', 20);
INSERT INTO public.soal_kuis (id_soal, id_kuis, tipe_soal, teks_soal, file_media, kunci_jawaban, poin) VALUES (6, 2, 'Suara', 'Bacalah kalimat salam berikut dengan intonasi yang jelas dan benar: "안녕하세요, 만나서 반갑습니다."', NULL, '안녕하세요 만나서 반갑습니다', 50);
INSERT INTO public.soal_kuis (id_soal, id_kuis, tipe_soal, teks_soal, file_media, kunci_jawaban, poin) VALUES (7, 3, 'Isian', 'ksckacs', NULL, '안녕하세요 만나서 반갑습니다', 10);


--
-- TOC entry 3102 (class 0 OID 17582)
-- Dependencies: 203
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.users (id, nama_lengkap, username, password, role, created_at) VALUES (1, 'Admin', 'admin_namsan', 'scrypt:32768:8:1$vt5SrFTSBpk7InfU$959a42c67ea086cd0308d4b99ba61c48dde6176bd49a68ee98cedbc144cd900bbca00d3ddb24c6b2d34a747bbbba414f622f54c9db3088ce26731d31fae1c7a0', 'admin', '2026-05-10 17:52:35.484161');
INSERT INTO public.users (id, nama_lengkap, username, password, role, created_at) VALUES (2, 'seonsaengnim_kim', 'seonsaengnim_kim', 'scrypt:32768:8:1$Eq6vftyI16HwpJ6U$efc06591b05a552755c3d73744b0d4bd4371a336a6a0ce3406113e5fbc1562d8639e66f86dc9059a43105d8b8ed6b7f4b91cb59504a21420e9175139fee3868b', 'pengajar', '2026-05-10 17:54:08.545219');
INSERT INTO public.users (id, nama_lengkap, username, password, role, created_at) VALUES (3, 'siswa_budi', 'siswa_budi', 'scrypt:32768:8:1$zwDpJDjmKnCJ0E03$3135fd90f293148fe561823f1e5e0e612748474bf3ca979949f661b543a2fa45b94d05173593988df805fabe0f24fd6a8eb3938ebf26f6351cf7263ce0a32ea3', 'siswa', '2026-05-10 17:54:34.589203');


--
-- TOC entry 3175 (class 0 OID 0)
-- Dependencies: 208
-- Name: absensi_log_id_absensi_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.absensi_log_id_absensi_seq', 12, true);


--
-- TOC entry 3176 (class 0 OID 0)
-- Dependencies: 238
-- Name: absensi_logbook_id_absen_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.absensi_logbook_id_absen_seq', 1, true);


--
-- TOC entry 3177 (class 0 OID 0)
-- Dependencies: 206
-- Name: enrollment_id_enrollment_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.enrollment_id_enrollment_seq', 2, true);


--
-- TOC entry 3178 (class 0 OID 0)
-- Dependencies: 236
-- Name: forum_chat_id_chat_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.forum_chat_id_chat_seq', 9, true);


--
-- TOC entry 3179 (class 0 OID 0)
-- Dependencies: 232
-- Name: forum_diskusi_id_diskusi_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.forum_diskusi_id_diskusi_seq', 1, true);


--
-- TOC entry 3180 (class 0 OID 0)
-- Dependencies: 210
-- Name: forum_kelas_id_pesan_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.forum_kelas_id_pesan_seq', 1, false);


--
-- TOC entry 3181 (class 0 OID 0)
-- Dependencies: 230
-- Name: forum_komentar_id_komentar_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.forum_komentar_id_komentar_seq', 1, false);


--
-- TOC entry 3182 (class 0 OID 0)
-- Dependencies: 228
-- Name: forum_topik_id_topik_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.forum_topik_id_topik_seq', 1, false);


--
-- TOC entry 3183 (class 0 OID 0)
-- Dependencies: 224
-- Name: jawaban_siswa_id_jawaban_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.jawaban_siswa_id_jawaban_seq', 1, false);


--
-- TOC entry 3184 (class 0 OID 0)
-- Dependencies: 204
-- Name: kelas_id_kelas_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.kelas_id_kelas_seq', 2, true);


--
-- TOC entry 3185 (class 0 OID 0)
-- Dependencies: 242
-- Name: kelas_siswa_id_kelas_siswa_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.kelas_siswa_id_kelas_siswa_seq', 1, false);


--
-- TOC entry 3186 (class 0 OID 0)
-- Dependencies: 218
-- Name: kuis_id_kuis_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.kuis_id_kuis_seq', 4, true);


--
-- TOC entry 3187 (class 0 OID 0)
-- Dependencies: 196
-- Name: log_aktivitas_kuis_id_log_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.log_aktivitas_kuis_id_log_seq', 1, false);


--
-- TOC entry 3188 (class 0 OID 0)
-- Dependencies: 214
-- Name: materi_audio_id_audio_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.materi_audio_id_audio_seq', 3, true);


--
-- TOC entry 3189 (class 0 OID 0)
-- Dependencies: 212
-- Name: materi_id_materi_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.materi_id_materi_seq', 1, true);


--
-- TOC entry 3190 (class 0 OID 0)
-- Dependencies: 198
-- Name: nilai_akhir_kuis_id_nilai_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.nilai_akhir_kuis_id_nilai_seq', 1, false);


--
-- TOC entry 3191 (class 0 OID 0)
-- Dependencies: 226
-- Name: nilai_kuis_id_nilai_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.nilai_kuis_id_nilai_seq', 2, true);


--
-- TOC entry 3192 (class 0 OID 0)
-- Dependencies: 222
-- Name: opsi_pg_id_opsi_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.opsi_pg_id_opsi_seq', 12, true);


--
-- TOC entry 3193 (class 0 OID 0)
-- Dependencies: 216
-- Name: progres_materi_id_progres_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.progres_materi_id_progres_seq', 1, false);


--
-- TOC entry 3194 (class 0 OID 0)
-- Dependencies: 200
-- Name: rekomendasi_ai_id_rekomendasi_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rekomendasi_ai_id_rekomendasi_seq', 1, false);


--
-- TOC entry 3195 (class 0 OID 0)
-- Dependencies: 240
-- Name: sertifikat_id_sertifikat_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sertifikat_id_sertifikat_seq', 1, true);


--
-- TOC entry 3196 (class 0 OID 0)
-- Dependencies: 234
-- Name: siswa_kelas_id_siswa_kelas_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.siswa_kelas_id_siswa_kelas_seq', 1, false);


--
-- TOC entry 3197 (class 0 OID 0)
-- Dependencies: 220
-- Name: soal_kuis_id_soal_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.soal_kuis_id_soal_seq', 7, true);


--
-- TOC entry 3198 (class 0 OID 0)
-- Dependencies: 202
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 3, true);


-- Completed on 2026-05-17 20:32:55

--
-- PostgreSQL database dump complete
--

