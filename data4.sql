-- Supabase Migration Schema for EduTech/AdaptEd
-- Generated cleanly to replace the previous pg_dump format

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. users
CREATE TABLE public.users (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    nama_lengkap VARCHAR(255) NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    role VARCHAR(50) DEFAULT 'siswa',
    created_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

-- 2. kelas
CREATE TABLE public.kelas (
    id_kelas UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nama_kelas VARCHAR(255) NOT NULL,
    id_pengajar UUID REFERENCES public.users(id) ON DELETE SET NULL,
    level_bahasa VARCHAR(50),
    tipe_kelas VARCHAR(50),
    link_kelas TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE public.kelas ENABLE ROW LEVEL SECURITY;

-- [NEW] 3. jadwal_kelas
CREATE TABLE public.jadwal_kelas (
    id_jadwal UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_kelas UUID REFERENCES public.kelas(id_kelas) ON DELETE CASCADE,
    hari VARCHAR(50),
    jam_mulai TIME,
    jam_selesai TIME,
    link_pertemuan TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE public.jadwal_kelas ENABLE ROW LEVEL SECURITY;

-- 4. enrollment
CREATE TABLE public.enrollment (
    id_enrollment UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_siswa UUID REFERENCES public.users(id) ON DELETE CASCADE,
    id_kelas UUID REFERENCES public.kelas(id_kelas) ON DELETE CASCADE,
    status_aktif BOOLEAN DEFAULT true,
    tanggal_daftar TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE public.enrollment ENABLE ROW LEVEL SECURITY;

-- 5. kelas_siswa
CREATE TABLE public.kelas_siswa (
    id_kelas_siswa UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_siswa UUID REFERENCES public.users(id) ON DELETE CASCADE,
    id_kelas UUID REFERENCES public.kelas(id_kelas) ON DELETE CASCADE
);
ALTER TABLE public.kelas_siswa ENABLE ROW LEVEL SECURITY;

-- 6. siswa_kelas
CREATE TABLE public.siswa_kelas (
    id_siswa_kelas UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_siswa UUID REFERENCES public.users(id) ON DELETE CASCADE,
    id_kelas UUID REFERENCES public.kelas(id_kelas) ON DELETE CASCADE
);
ALTER TABLE public.siswa_kelas ENABLE ROW LEVEL SECURITY;

-- 7. absensi_log
CREATE TABLE public.absensi_log (
    id_absensi UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_siswa UUID REFERENCES public.users(id) ON DELETE CASCADE,
    id_jadwal UUID REFERENCES public.jadwal_kelas(id_jadwal) ON DELETE CASCADE, -- [MODIFIED] Link to jadwal_kelas
    tanggal DATE,
    waktu_login TIMESTAMPTZ,
    waktu_logout TIMESTAMPTZ,
    durasi_belajar_menit INTEGER
);
ALTER TABLE public.absensi_log ENABLE ROW LEVEL SECURITY;

-- 8. absensi_logbook
CREATE TABLE public.absensi_logbook (
    id_absen UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_siswa UUID REFERENCES public.users(id) ON DELETE CASCADE,
    id_jadwal UUID REFERENCES public.jadwal_kelas(id_jadwal) ON DELETE CASCADE, -- [MODIFIED] Link to jadwal_kelas
    waktu_masuk TIMESTAMPTZ,
    waktu_keluar TIMESTAMPTZ,
    durasi_menit INTEGER,
    tanggal DATE
);
ALTER TABLE public.absensi_logbook ENABLE ROW LEVEL SECURITY;

-- 9. materi
CREATE TABLE public.materi (
    id_materi UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_kelas UUID REFERENCES public.kelas(id_kelas) ON DELETE CASCADE,
    judul_materi VARCHAR(255),
    file_pdf VARCHAR(255),
    urutan INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE public.materi ENABLE ROW LEVEL SECURITY;

-- 10. materi_audio
CREATE TABLE public.materi_audio (
    id_audio UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_materi UUID REFERENCES public.materi(id_materi) ON DELETE CASCADE,
    file_audio VARCHAR(255)
);
ALTER TABLE public.materi_audio ENABLE ROW LEVEL SECURITY;

-- 11. progres_materi
CREATE TABLE public.progres_materi (
    id_progres UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_siswa UUID REFERENCES public.users(id) ON DELETE CASCADE,
    id_materi UUID REFERENCES public.materi(id_materi) ON DELETE CASCADE,
    status BOOLEAN
);
ALTER TABLE public.progres_materi ENABLE ROW LEVEL SECURITY;

-- 12. forum_topik
CREATE TABLE public.forum_topik (
    id_topik UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_kelas UUID REFERENCES public.kelas(id_kelas) ON DELETE CASCADE,
    judul VARCHAR(255)
);
ALTER TABLE public.forum_topik ENABLE ROW LEVEL SECURITY;

-- 13. forum_diskusi
CREATE TABLE public.forum_diskusi (
    id_diskusi UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_kelas UUID REFERENCES public.kelas(id_kelas) ON DELETE CASCADE,
    id_penulis UUID REFERENCES public.users(id) ON DELETE CASCADE,
    judul VARCHAR(255),
    pesan TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE public.forum_diskusi ENABLE ROW LEVEL SECURITY;

-- 14. forum_komentar
CREATE TABLE public.forum_komentar (
    id_komentar UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_diskusi UUID REFERENCES public.forum_diskusi(id_diskusi) ON DELETE CASCADE,
    komentar TEXT
);
ALTER TABLE public.forum_komentar ENABLE ROW LEVEL SECURITY;

-- 15. forum_kelas
CREATE TABLE public.forum_kelas (
    id_pesan UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_kelas UUID REFERENCES public.kelas(id_kelas) ON DELETE CASCADE,
    pesan TEXT
);
ALTER TABLE public.forum_kelas ENABLE ROW LEVEL SECURITY;

-- 16. forum_chat
CREATE TABLE public.forum_chat (
    id_chat UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_materi UUID REFERENCES public.materi(id_materi) ON DELETE CASCADE,
    id_user UUID REFERENCES public.users(id) ON DELETE CASCADE,
    pesan TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    parent_id UUID REFERENCES public.forum_chat(id_chat) ON DELETE CASCADE
);
ALTER TABLE public.forum_chat ENABLE ROW LEVEL SECURITY;

-- 17. kuis
CREATE TABLE public.kuis (
    id_kuis UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_kelas UUID REFERENCES public.kelas(id_kelas) ON DELETE CASCADE,
    judul_kuis VARCHAR(255),
    deskripsi TEXT,
    waktu_menit INTEGER,
    tanggal_dibuat TIMESTAMPTZ DEFAULT NOW(),
    is_published BOOLEAN DEFAULT true
);
ALTER TABLE public.kuis ENABLE ROW LEVEL SECURITY;

-- 18. log_aktivitas_kuis
CREATE TABLE public.log_aktivitas_kuis (
    id_log UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_siswa UUID REFERENCES public.users(id) ON DELETE CASCADE,
    id_kuis UUID REFERENCES public.kuis(id_kuis) ON DELETE CASCADE
);
ALTER TABLE public.log_aktivitas_kuis ENABLE ROW LEVEL SECURITY;

-- 19. soal_kuis
CREATE TABLE public.soal_kuis (
    id_soal UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_kuis UUID REFERENCES public.kuis(id_kuis) ON DELETE CASCADE,
    pertanyaan TEXT,
    tipe_soal VARCHAR(50),
    file_audio VARCHAR(255),
    pilihan_a TEXT,
    pilihan_b TEXT,
    pilihan_c TEXT,
    pilihan_d TEXT,
    jawaban_benar VARCHAR(255)
);
ALTER TABLE public.soal_kuis ENABLE ROW LEVEL SECURITY;

-- 20. opsi_pg
CREATE TABLE public.opsi_pg (
    id_opsi UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_soal UUID REFERENCES public.soal_kuis(id_soal) ON DELETE CASCADE,
    teks_opsi TEXT,
    is_benar BOOLEAN
);
ALTER TABLE public.opsi_pg ENABLE ROW LEVEL SECURITY;

-- 21. jawaban_siswa
CREATE TABLE public.jawaban_siswa (
    id_jawaban UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_siswa UUID REFERENCES public.users(id) ON DELETE CASCADE,
    id_soal UUID REFERENCES public.soal_kuis(id_soal) ON DELETE CASCADE,
    jawaban TEXT,
    file_audio_jawaban VARCHAR(255), -- [NEW] For Voice answers
    durasi_detik INTEGER DEFAULT 0,
    skor_ai INTEGER DEFAULT 0,
    feedback_ai TEXT,
    waktu_submit TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE public.jawaban_siswa ENABLE ROW LEVEL SECURITY;

-- 22. nilai_kuis
CREATE TABLE public.nilai_kuis (
    id_nilai UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_kuis UUID REFERENCES public.kuis(id_kuis) ON DELETE CASCADE,
    id_siswa UUID REFERENCES public.users(id) ON DELETE CASCADE,
    total_nilai INTEGER,
    catatan_analitik_ai TEXT,
    waktu_selesai TIMESTAMPTZ,
    skor INTEGER,
    status VARCHAR(50)
);
ALTER TABLE public.nilai_kuis ENABLE ROW LEVEL SECURITY;

-- 23. nilai_akhir_kuis
CREATE TABLE public.nilai_akhir_kuis (
    id_nilai UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_siswa UUID REFERENCES public.users(id) ON DELETE CASCADE
);
ALTER TABLE public.nilai_akhir_kuis ENABLE ROW LEVEL SECURITY;

-- 24. rekomendasi_ai
CREATE TABLE public.rekomendasi_ai (
    id_rekomendasi UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_siswa UUID REFERENCES public.users(id) ON DELETE CASCADE
);
ALTER TABLE public.rekomendasi_ai ENABLE ROW LEVEL SECURITY;

-- 25. sertifikat
CREATE TABLE public.sertifikat (
    id_sertifikat UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_siswa UUID REFERENCES public.users(id) ON DELETE CASCADE,
    nama_sertifikat VARCHAR(255),
    file_pdf VARCHAR(255),
    tanggal_keluar TIMESTAMPTZ,
    generated_at TIMESTAMPTZ DEFAULT NOW(), -- [NEW] Auto-generate tracking
    status_approve BOOLEAN DEFAULT false,
    id_kelas UUID REFERENCES public.kelas(id_kelas) ON DELETE SET NULL
);
ALTER TABLE public.sertifikat ENABLE ROW LEVEL SECURITY;

-- Basic RLS Policies Example (Can be customized later)
-- CREATE POLICY "Users can view their own data" ON public.users FOR SELECT USING (auth.uid() = id);
