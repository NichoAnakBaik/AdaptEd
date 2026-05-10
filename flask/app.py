import os
import psycopg2
import psycopg2.extras
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, g, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'namsan_fun_learning_123')

# Konfigurasi Upload
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ==============================================================================
# 1. DATABASE CONNECTION
# ==============================================================================
def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'adapted'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASS', 'postgres'),
            port=os.getenv('DB_PORT', '5432')
        )
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# ==============================================================================
# 2. AUTHENTICATION (Login, Signup, Logout, Absensi)
# ==============================================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['nama'] = user['nama_lengkap']
            session['role'] = user['role']
            
            # --- LOGIKA ABSENSI (Hanya untuk Siswa) ---
            if user['role'] == 'siswa':
                cur.execute("INSERT INTO absensi_log (id_siswa, waktu_login) VALUES (%s, %s)", 
                            (user['id'], datetime.now()))
                db.commit()

            flash(f"Selamat datang, {user['nama_lengkap']}!", "success")
            
            if user['role'] == 'admin': return redirect(url_for('dashboard_admin'))
            if user['role'] == 'pengajar': return redirect(url_for('dashboard_pengajar'))
            return redirect(url_for('dashboard_siswa'))
            
        flash("Username atau password salah.", "danger")
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        nama = request.form.get('nama_lengkap')
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role', 'siswa')
        
        db = get_db()
        cur = db.cursor()
        hashed_pw = generate_password_hash(password)
        
        try:
            cur.execute("INSERT INTO users (nama_lengkap, username, password, role) VALUES (%s, %s, %s, %s)",
                        (nama, username, hashed_pw, role))
            db.commit()
            flash("Pendaftaran berhasil! Silakan login.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            db.rollback()
            flash("Username sudah digunakan.", "danger")
            
    return render_template('signup.html')

@app.route('/logout', methods=['POST'])
def logout():
    # --- UPDATE LOG ABSENSI (Logout) ---
    if session.get('role') == 'siswa':
        db = get_db()
        cur = db.cursor()
        # Ambil log login terakhir siswa ini yang logout-nya masih kosong
        cur.execute("""
            UPDATE absensi_log 
            SET waktu_logout = %s, 
                durasi_belajar_menit = EXTRACT(EPOCH FROM (%s - waktu_login))/60
            WHERE id_siswa = %s AND waktu_logout IS NULL
        """, (datetime.now(), datetime.now(), session['user_id']))
        db.commit()

    session.clear()
    flash("Anda telah logout.", "info")
    return redirect(url_for('index'))

# ==============================================================================
# 3. DASHBOARD ROUTES
# ==============================================================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard_admin')
def dashboard_admin():
    if session.get('role') != 'admin': 
        return redirect(url_for('login'))
        
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    # 1. Hitung Statistik Ringkas
    cur.execute("SELECT COUNT(*) as total FROM users WHERE role='siswa'")
    total_siswa = cur.fetchone()['total']
    
    cur.execute("SELECT COUNT(*) as total FROM users WHERE role='pengajar'")
    total_pengajar = cur.fetchone()['total']
    
    cur.execute("SELECT COUNT(*) as total FROM kelas")
    total_kelas = cur.fetchone()['total']
    
    cur.execute("SELECT COUNT(*) as total FROM sertifikat WHERE status_approval='Pending'")
    pending_sertif = cur.fetchone()['total']

    # 2. Ambil 5 Pengguna yang Baru Mendaftar
    cur.execute("SELECT id, username, nama_lengkap, role, created_at FROM users ORDER BY created_at DESC LIMIT 5")
    users_terbaru = cur.fetchall()
    
    cur.close()
    
    return render_template('admin/dashboard_admin.html', 
                           total_siswa=total_siswa, 
                           total_pengajar=total_pengajar, 
                           total_kelas=total_kelas,
                           pending_sertif=pending_sertif,
                           users_terbaru=users_terbaru)

@app.route('/dashboard_siswa')
def dashboard_siswa():
    if session.get('role') != 'siswa': return redirect(url_for('login'))
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    # Ambil data progres modul untuk Dashboard Analytics
    cur.execute("SELECT COUNT(*) as t FROM progres_materi WHERE id_siswa = %s AND status_selesai = TRUE", (session['user_id'],))
    lulus_modul = cur.fetchone()['t']
    
    # Ambil info kelas (Online/Offline)
    cur.execute("""
        SELECT k.* FROM kelas k 
        JOIN enrollment e ON k.id_kelas = e.id_kelas 
        WHERE e.id_siswa = %s AND e.status_aktif = TRUE
    """, (session['user_id'],))
    kelas_info = cur.fetchone()
    
    return render_template('siswa/dashboard_siswa.html', lulus_modul=lulus_modul, kelas=kelas_info)

# Pastikan rute ini yang dipanggil di browser: /pengajar/dashboard
@app.route('/pengajar/dashboard')
def dashboard_pengajar(): # Nama fungsi ini harus sinkron dengan url_for nanti
    if session.get('role') != 'pengajar':
        return redirect(url_for('login'))
        
    db = get_db()
    cur = db.cursor()
    uid = session.get('user_id')

    # Query Kelas
    cur.execute("SELECT COUNT(*) FROM kelas WHERE id_pengajar = %s", (uid,))
    k = cur.fetchone()[0]

    # Query Kuis
    cur.execute("""
        SELECT COUNT(*) FROM kuis q 
        JOIN kelas k ON q.id_kelas = k.id_kelas 
        WHERE k.id_pengajar = %s
    """, (uid,))
    q = cur.fetchone()[0]
    
    cur.close()

    data_dashboard = {
        'total_kelas': int(k),
        'total_kuis': int(q),
        'nama_user': session.get('nama_lengkap', 'Seonsaengnim')
    }

    # Pastikan file fisiknya bernama: templates/pengajar/dashboard_pengajar.html
    return render_template('pengajar/dashboard_pengajar.html', data=data_dashboard)

# ==============================================================================
# PENGAJAR
# ==============================================================================

@app.route('/pengajar/kelas')
def pengajar_kelas():
    if session.get('role') != 'pengajar': 
        return redirect(url_for('login'))
        
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    id_pengajar = session.get('user_id')

    # 1. Ambil daftar kelas yang diampu
    cur.execute("SELECT * FROM kelas WHERE id_pengajar = %s", (id_pengajar,))
    kelas_list = cur.fetchall()

    # 2. Ambil siswa + Status Kelulusan (JOIN dengan tabel sertifikat)
    cur.execute("""
        SELECT e.id_kelas, u.id as id_siswa, u.nama_lengkap, e.tanggal_daftar,
               s.status_approval, s.file_sertifikat
        FROM enrollment e
        JOIN users u ON e.id_siswa = u.id
        JOIN kelas k ON e.id_kelas = k.id_kelas
        LEFT JOIN sertifikat s ON s.id_siswa = u.id AND s.id_kelas = k.id_kelas
        WHERE k.id_pengajar = %s AND e.status_aktif = TRUE
        ORDER BY u.nama_lengkap
    """, (id_pengajar,))
    siswa_list = cur.fetchall()

    for k in kelas_list:
        k['siswa'] = [s for s in siswa_list if s['id_kelas'] == k['id_kelas']]

    cur.close()
    return render_template('pengajar/kelas_siswa.html', kelas_list=kelas_list)

@app.route('/pengajar/progres/<int:id_kelas>/<int:id_siswa>')
def pengajar_progres(id_kelas, id_siswa):
    if session.get('role') != 'pengajar': return redirect(url_for('login'))
    
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    # 1. Ambil info siswa dan kelas
    cur.execute("""
        SELECT u.nama_lengkap, k.nama_kelas, k.level_bahasa 
        FROM users u, kelas k 
        WHERE u.id = %s AND k.id_kelas = %s
    """, (id_siswa, id_kelas))
    info = cur.fetchone()

    # 2. Ambil daftar materi dan status selesainya (JOIN dengan progres_materi)
    cur.execute("""
        SELECT m.judul_materi, m.urutan, 
               COALESCE(p.status_selesai, FALSE) as selesai,
               p.waktu_selesai
        FROM materi m
        LEFT JOIN progres_materi p ON m.id_materi = p.id_materi AND p.id_siswa = %s
        WHERE m.id_kelas = %s
        ORDER BY m.urutan ASC
    """, (id_siswa, id_kelas))
    progres_list = cur.fetchall()

    # 3. Hitung persentase
    total = len(progres_list)
    selesai = sum(1 for m in progres_list if m['selesai'])
    persen = (selesai / total * 100) if total > 0 else 0

    cur.close()
    return render_template('pengajar/progres_siswa.html', info=info, progres=progres_list, persen=persen)

@app.route('/pengajar/sertifikat', methods=['GET', 'POST'])
def pengajar_sertifikat():
    if session.get('role') != 'pengajar': 
        return redirect(url_for('login'))
        
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    id_pengajar = session.get('user_id')

    # KETIKA TOMBOL KIRIM DIKLIK (POST)
    if request.method == 'POST':
        id_kelas = request.form.get('id_kelas')
        id_siswa = request.form.get('id_siswa')
        file_pdf = request.files.get('file_sertifikat')

        # --- CCTV TERMINAL (Lihat hasilnya di terminal/CMD saat kamu klik kirim) ---
        print("\n=== DEBUG UPLOAD SERTIFIKAT ===")
        print(f"Kelas ID : {id_kelas}")
        print(f"Siswa ID : {id_siswa}")
        print(f"File PDF : {file_pdf.filename if file_pdf else 'TIDAK ADA FILE'}")
        
        # Gunakan .lower() agar .PDF atau .pdf sama-sama diterima
        if file_pdf and file_pdf.filename.lower().endswith('.pdf'):
            from werkzeug.utils import secure_filename
            import os
            from datetime import datetime
            
            pdf_name = secure_filename(file_pdf.filename)
            pdf_name = f"cert_{id_siswa}_{datetime.now().strftime('%H%M%S')}_{pdf_name}"
            
            # FITUR BARU: Otomatis buat folder jika foldernya belum ada
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
                print("Folder static/uploads/ baru saja dibuat otomatis.")

            # Simpan file secara fisik
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_name)
            file_pdf.save(file_path)
            print(f"File sukses disimpan di: {file_path}")

            try:
                cur.execute("""
                    INSERT INTO sertifikat (id_siswa, id_kelas, id_pengajar_pengaju, file_sertifikat, status_approval)
                    VALUES (%s, %s, %s, %s, 'Pending')
                """, (id_siswa, id_kelas, id_pengajar, pdf_name))
                db.commit()
                print("Database : BERHASIL DISIMPAN!")
                flash("PDF Sertifikat berhasil diunggah! Menunggu ACC Admin.", "success")
            except Exception as e:
                db.rollback()
                print(f"Database Error: {e}")
                flash("Gagal! Siswa ini mungkin sudah diajukan.", "danger")
        else:
            print("Error : Validasi file gagal (bukan PDF).")
            flash("File wajib berformat PDF!", "danger")
            
        print("===============================\n")
        return redirect(url_for('pengajar_sertifikat'))

    # TAMPILAN HALAMAN (GET)
    cur.execute("SELECT id_kelas, nama_kelas FROM kelas WHERE id_pengajar = %s", (id_pengajar,))
    kelas_list = cur.fetchall()

    cur.execute("""
        SELECT e.id_kelas, e.id_siswa, u.nama_lengkap 
        FROM enrollment e JOIN users u ON e.id_siswa = u.id
        WHERE e.status_aktif = TRUE
    """)
    siswa_list = cur.fetchall()

    cur.execute("""
        SELECT s.*, u.nama_lengkap as nama_siswa, k.nama_kelas
        FROM sertifikat s
        JOIN users u ON s.id_siswa = u.id
        JOIN kelas k ON s.id_kelas = k.id_kelas
        WHERE s.id_pengajar_pengaju = %s
        ORDER BY s.created_at DESC
    """, (id_pengajar,))
    riwayat = cur.fetchall()
    cur.close()

    return render_template('pengajar/upload_sertifikat.html', 
                           kelas_list=kelas_list, siswa_list=siswa_list, riwayat=riwayat)

@app.route('/pengajar/modul')
def pengajar_modul():
    if session.get('role') != 'pengajar': 
        return redirect(url_for('login'))
        
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    id_pengajar = session.get('user_id')

    # 1. Ambil kelas yang diampu pengajar
    cur.execute("SELECT id_kelas, nama_kelas, level_bahasa FROM kelas WHERE id_pengajar = %s", (id_pengajar,))
    kelas_list = cur.fetchall()

    # 2. Ambil semua modul (PDF) untuk kelas-kelas tersebut
    cur.execute("""
        SELECT m.*, k.nama_kelas 
        FROM materi m
        JOIN kelas k ON m.id_kelas = k.id_kelas
        WHERE k.id_pengajar = %s
        ORDER BY m.urutan ASC
    """, (id_pengajar,))
    materi_list = cur.fetchall()

    # 3. Ambil semua audio pendukung
    cur.execute("""
        SELECT ma.* FROM materi_audio ma
        JOIN materi m ON ma.id_materi = m.id_materi
        JOIN kelas k ON m.id_kelas = k.id_kelas
        WHERE k.id_pengajar = %s
    """, (id_pengajar,))
    audio_list = cur.fetchall()

    # 4. Kelompokkan data (Materi ke Kelas, Audio ke Materi)
    for m in materi_list:
        m['audios'] = [a for a in audio_list if a['id_materi'] == m['id_materi']]
    
    for k in kelas_list:
        k['modul'] = [m for m in materi_list if m['id_kelas'] == k['id_kelas']]

    cur.close()
    return render_template('pengajar/pantau_modul.html', kelas_list=kelas_list)

@app.route('/pengajar/kuis', methods=['GET', 'POST'])
def pengajar_kuis():
    if session.get('role') != 'pengajar': return redirect(url_for('login'))
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    user_id = session.get('user_id')

    if request.method == 'POST':
        # Logika simpan kuis baru
        id_kelas = request.form.get('id_kelas')
        judul = request.form.get('judul_kuis')
        desc = request.form.get('description')
        level = request.form.get('tingkat_kesulitan')
        cur.execute("INSERT INTO kuis (id_kelas, judul_kuis, deskripsi, tingkat_kesulitan, is_published) VALUES (%s, %s, %s, %s, FALSE)", (id_kelas, judul, desc, level))
        db.commit()
        return redirect(url_for('pengajar_kuis'))

    # AMBIL SEMUA KUIS (Tanpa filter pengajar dulu untuk ngetes apakah data muncul)
    cur.execute("""
        SELECT q.*, k.nama_kelas, 
        (SELECT COUNT(*) FROM soal_kuis s WHERE s.id_kuis = q.id_kuis) as total_soal 
        FROM kuis q 
        JOIN kelas k ON q.id_kelas = k.id_kelas
    """)
    kuis_list = cur.fetchall()

    cur.execute("SELECT id_kelas, nama_kelas FROM kelas")
    kelas_list = cur.fetchall()
    
    cur.close()
    return render_template('pengajar/kelola_kuis.html', kuis_list=kuis_list, kelas_list=kelas_list)

@app.route('/pengajar/kuis/publish/<int:id_kuis>')
def publish_kuis(id_kuis):
    # Keamanan: Pastikan hanya pengajar yang bisa akses
    if session.get('role') != 'pengajar': 
        return redirect(url_for('login'))
        
    db = get_db()
    cur = db.cursor()
    
    # Validasi: Cek apakah kuis sudah punya soal atau belum
    cur.execute("SELECT COUNT(*) FROM soal_kuis WHERE id_kuis = %s", (id_kuis,))
    jumlah_soal = cur.fetchone()[0]
    
    if jumlah_soal > 0:
        # Update status menjadi TRUE
        cur.execute("UPDATE kuis SET is_published = TRUE WHERE id_kuis = %s", (id_kuis,))
        db.commit()
        flash("Kuis berhasil di-publish! Sekarang siswa dapat melihat dan mengerjakan kuis ini.", "success")
    else:
        # Jika soal masih 0, jangan izinkan publish
        flash("Gagal! Kamu tidak bisa mempublikasikan kuis yang belum ada soalnya.", "danger")
        
    cur.close()
    # Lempar balik ke halaman daftar kuis
    return redirect(url_for('pengajar_kuis'))

@app.route('/pengajar/kuis/soal/<int:id_kuis>', methods=['GET', 'POST'])
def pengajar_soal(id_kuis):
    if session.get('role') != 'pengajar': return redirect(url_for('login'))
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # LOGIKA TAMBAH SOAL
    if request.method == 'POST':
        tipe = request.form.get('tipe_soal')
        teks = request.form.get('teks_soal')
        kunci = request.form.get('kunci_jawaban')
        poin = request.form.get('poin')

        cur.execute("""
            INSERT INTO soal_kuis (id_kuis, tipe_soal, teks_soal, kunci_jawaban, poin)
            VALUES (%s, %s, %s, %s, %s) RETURNING id_soal
        """, (id_kuis, tipe, teks, kunci, poin))
        id_soal = cur.fetchone()['id_soal']

        if tipe == 'Pilihan Ganda':
            opsis = request.form.getlist('opsi[]')
            jawaban_benar = request.form.get('jawaban_benar')
            for index, teks_opsi in enumerate(opsis):
                if teks_opsi.strip():
                    is_benar = (str(index) == jawaban_benar)
                    cur.execute("INSERT INTO opsi_pg (id_soal, teks_opsi, is_benar) VALUES (%s, %s, %s)", 
                                (id_soal, teks_opsi, is_benar))
        db.commit()
        flash("Soal berhasil ditambahkan!", "success")
        return redirect(url_for('pengajar_soal', id_kuis=id_kuis))

    # TAMPILAN HALAMAN
    cur.execute("SELECT * FROM kuis WHERE id_kuis = %s", (id_kuis,))
    kuis_info = cur.fetchone()

    cur.execute("""
        SELECT s.*, 
        (SELECT json_agg(o ORDER BY o.id_opsi) FROM opsi_pg o WHERE o.id_soal = s.id_soal) as opsi
        FROM soal_kuis s 
        WHERE s.id_kuis = %s 
        ORDER BY s.id_soal ASC
    """, (id_kuis,))
    soal_list = cur.fetchall()
    cur.close()
    return render_template('pengajar/kelola_soal.html', kuis=kuis_info, soal_list=soal_list)

@app.route('/pengajar/kuis/edit_soal/<int:id_soal>/<int:id_kuis>', methods=['POST'])
def edit_soal(id_soal, id_kuis):
    db = get_db()
    cur = db.cursor()
    teks = request.form.get('teks_soal')
    kunci = request.form.get('kunci_jawaban')
    poin = request.form.get('poin')
    tipe = request.form.get('tipe_soal')

    cur.execute("UPDATE soal_kuis SET teks_soal = %s, kunci_jawaban = %s, poin = %s WHERE id_soal = %s", 
                (teks, kunci, poin, id_soal))

    if tipe == 'Pilihan Ganda':
        cur.execute("DELETE FROM opsi_pg WHERE id_soal = %s", (id_soal,))
        opsis = request.form.getlist('opsi[]')
        jawaban_benar = request.form.get('jawaban_benar')
        for index, teks_opsi in enumerate(opsis):
            if teks_opsi.strip():
                is_benar = (str(index) == jawaban_benar)
                cur.execute("INSERT INTO opsi_pg (id_soal, teks_opsi, is_benar) VALUES (%s, %s, %s)", (id_soal, teks_opsi, is_benar))
    db.commit()
    cur.close()
    flash("Soal berhasil diperbarui!", "success")
    return redirect(url_for('pengajar_soal', id_kuis=id_kuis))

@app.route('/pengajar/kuis/hapus_soal/<int:id_soal>/<int:id_kuis>')
def hapus_soal(id_soal, id_kuis):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM soal_kuis WHERE id_soal = %s", (id_soal,))
    db.commit()
    cur.close()
    flash("Soal dihapus.", "warning")
    return redirect(url_for('pengajar_soal', id_kuis=id_kuis))

@app.route('/pengajar/forum')
def pengajar_forum():
    if session.get('role') != 'pengajar': return redirect(url_for('login'))
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    id_pengajar = session.get('user_id')

    # Pengajar hanya melihat forum dari kelas yang dia ajar
    cur.execute("SELECT id_kelas, nama_kelas FROM kelas WHERE id_pengajar = %s", (id_pengajar,))
    kelas_list = cur.fetchall()
    cur.close()
    return render_template('pengajar/forum_list.html', kelas_list=kelas_list)

@app.route('/pengajar/forum/kelas/<int:id_kelas>', methods=['GET', 'POST'])
def forum_detail(id_kelas):
    if session.get('role') != 'pengajar': return redirect(url_for('login'))
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    # 1. Ambil info kelas (untuk judul halaman)
    cur.execute("SELECT nama_kelas FROM kelas WHERE id_kelas = %s", (id_kelas,))
    kelas = cur.fetchone()

    # 2. Logika jika ada postingan baru (POST)
    if request.method == 'POST':
        judul = request.form.get('judul')
        pesan = request.form.get('pesan')
        cur.execute("""
            INSERT INTO forum_diskusi (id_kelas, id_penulis, judul, pesan) 
            VALUES (%s, %s, %s, %s)
        """, (id_kelas, session['user_id'], judul, pesan))
        db.commit()
        # Setelah posting, redirect ke halaman yang sama agar tidak double post saat refresh
        return redirect(url_for('forum_detail', id_kelas=id_kelas))

    # 3. AMBIL DAFTAR DISKUSI (Harus di luar blok IF agar diskusi_list terdefinisi)
    # Pastikan query ini benar dan id_diskusi sesuai dengan di DB
    cur.execute("""
        SELECT d.*, u.nama_lengkap as penulis,
        (SELECT COUNT(*) FROM forum_komentar k WHERE k.id_diskusi = d.id_diskusi) as jml_komentar
        FROM forum_diskusi d
        JOIN users u ON d.id_penulis = u.id
        WHERE d.id_kelas = %s 
        ORDER BY d.created_at DESC
    """, (id_kelas,))
    diskusi_list = cur.fetchall() # Di sini variabel didefinisikan
    
    cur.close()
    
    # Sekarang diskusi_list pasti sudah ada isinya (minimal list kosong [])
    return render_template('pengajar/forum_detail.html', 
                           diskusi_list=diskusi_list, 
                           kelas=kelas, 
                           id_kelas=id_kelas)

@app.route('/pengajar/forum/diskusi/<int:id_diskusi>', methods=['GET', 'POST'])
def diskusi_komentar(id_diskusi):
    if session.get('role') != 'pengajar': return redirect(url_for('login'))
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    if request.method == 'POST':
        isi = request.form.get('isi_komentar')
        cur.execute("INSERT INTO forum_komentar (id_diskusi, id_penulis, isi_komentar) VALUES (%s, %s, %s)",
                    (id_diskusi, session['user_id'], isi))
        db.commit()
        return redirect(url_for('diskusi_komentar', id_diskusi=id_diskusi))

    # Ambil postingan utama
    cur.execute("""
        SELECT d.*, u.nama_lengkap as penulis 
        FROM forum_diskusi d 
        JOIN users u ON d.id_penulis = u.id 
        WHERE d.id_diskusi = %s
    """, (id_diskusi,))
    diskusi = cur.fetchone()

    # Ambil semua komentar
    cur.execute("""
        SELECT k.*, u.nama_lengkap as penulis 
        FROM forum_komentar k 
        JOIN users u ON k.id_penulis = u.id 
        WHERE k.id_diskusi = %s ORDER BY k.created_at ASC
    """, (id_diskusi,))
    komentar_list = cur.fetchall()

    cur.close()
    return render_template('pengajar/forum_komentar.html', diskusi=diskusi, komentar_list=komentar_list)

@app.route('/pengajar/analitik')
def pengajar_analitik():
    if session.get('role') != 'pengajar':
        return redirect(url_for('login'))
        
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    id_pengajar = session.get('user_id')

    # 1. Statistik Ringkas: Total Kelas & Total Siswa Unik
    cur.execute("SELECT COUNT(*) as jml FROM kelas WHERE id_pengajar = %s", (id_pengajar,))
    total_kelas = cur.fetchone()['jml']

    cur.execute("""
        SELECT COUNT(DISTINCT sk.id_siswa) as jml 
        FROM siswa_kelas sk
        JOIN kelas k ON sk.id_kelas = k.id_kelas
        WHERE k.id_pengajar = %s
    """, (id_pengajar,))
    total_siswa = cur.fetchone()['jml']

    # 2. Query Data Grafik: Rata-rata Nilai per Kuis
    # Kita gunakan COALESCE agar kuis yang belum ada nilainya tetap muncul sebagai 0
    cur.execute("""
        SELECT q.judul_kuis, COALESCE(AVG(n.skor), 0) as rata_rata
        FROM kuis q
        LEFT JOIN nilai_kuis n ON q.id_kuis = n.id_kuis
        JOIN kelas k ON q.id_kelas = k.id_kelas
        WHERE k.id_pengajar = %s
        GROUP BY q.id_kuis, q.judul_kuis, q.created_at
        ORDER BY q.created_at ASC
    """, (id_pengajar,))
    
    chart_data_raw = cur.fetchall()
    
    # Parsing data untuk Chart.js (Sangat Penting!)
    chart_labels = [row['judul_kuis'] for row in chart_data_raw]
    chart_values = [float(row['rata_rata']) for row in chart_data_raw]

    # 3. Daftar Kuis dengan Partisipasi (Tabel Ringkasan)
    cur.execute("""
        SELECT q.judul_kuis, k.nama_kelas, 
               COUNT(n.id_nilai) as jumlah_mengerjakan,
               COALESCE(AVG(n.skor), 0) as rata_skor
        FROM kuis q
        JOIN kelas k ON q.id_kelas = k.id_kelas
        LEFT JOIN nilai_kuis n ON q.id_kuis = n.id_kuis
        WHERE k.id_pengajar = %s
        GROUP BY q.id_kuis, q.judul_kuis, k.nama_kelas
        ORDER BY jumlah_mengerjakan DESC
        LIMIT 5
    """, (id_pengajar,))
    top_kuis = cur.fetchall()

    cur.close()

    return render_template('pengajar/analitik.html', 
                           total_kelas=total_kelas, 
                           total_siswa=total_siswa,
                           chart_labels=chart_labels, 
                           chart_values=chart_values,
                           top_kuis=top_kuis)

# ==============================================================================
# 4. MODUL & MATERI (Admin Upload, Siswa View)
# ==============================================================================

@app.route('/admin/modul', methods=['GET', 'POST'])
def admin_modul():
    if session.get('role') != 'admin': return redirect(url_for('login'))
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    if request.method == 'POST':
        id_kelas = request.form.get('id_kelas')
        judul = request.form.get('judul_materi')
        urutan = request.form.get('urutan')
        
        file_pdf = request.files.get('file_pdf')
        files_audio = request.files.getlist('file_audio') # Ambil banyak file sekaligus
        
        # Validasi PDF
        if not file_pdf or not file_pdf.filename.endswith('.pdf'):
            flash("File utama wajib diisi dan harus berformat PDF!", "danger")
            return redirect(url_for('admin_modul'))
            
        try:
            # 1. Simpan PDF & Buat Modul
            pdf_name = secure_filename(file_pdf.filename)
            file_pdf.save(os.path.join(app.config['UPLOAD_FOLDER'], pdf_name))
            
            cur.execute("""
                INSERT INTO materi (id_kelas, judul_materi, file_pdf, urutan)
                VALUES (%s, %s, %s, %s) RETURNING id_materi
            """, (id_kelas, judul, pdf_name, urutan))
            
            id_materi_baru = cur.fetchone()['id_materi']
            
            # 2. Simpan Audio (Jika Ada)
            for audio in files_audio:
                if audio and audio.filename != '' and audio.filename.endswith(('.mp3', '.wav', '.ogg')):
                    audio_name = secure_filename(audio.filename)
                    audio.save(os.path.join(app.config['UPLOAD_FOLDER'], audio_name))
                    cur.execute("INSERT INTO materi_audio (id_materi, file_audio) VALUES (%s, %s)", (id_materi_baru, audio_name))
            
            db.commit()
            flash("Modul beserta audio berhasil diunggah!", "success")
        except Exception as e:
            db.rollback()
            print("Error Upload:", e)
            flash("Terjadi kesalahan sistem saat mengunggah.", "danger")
            
        return redirect(url_for('admin_modul'))

    # AMBIL DATA UNTUK DITAMPILKAN
    cur.execute("SELECT * FROM kelas ORDER BY level_bahasa, nama_kelas")
    kelas_list = cur.fetchall()
    
    cur.execute("""
        SELECT m.*, k.nama_kelas, 
               (SELECT COUNT(*) FROM materi_audio ma WHERE ma.id_materi = m.id_materi) as total_audio
        FROM materi m JOIN kelas k ON m.id_kelas = k.id_kelas
        ORDER BY k.nama_kelas, m.urutan
    """)
    materi_list = cur.fetchall()
    cur.close()
    
    return render_template('admin/manage_modul.html', kelas_list=kelas_list, materi_list=materi_list)

# ==============================================================================
# EDIT MODUL (PDF & MULTIPLE AUDIO)
# ==============================================================================

@app.route('/admin/modul/edit/<int:id_materi>', methods=['GET', 'POST'])
def edit_modul(id_materi):
    if session.get('role') != 'admin': return redirect(url_for('login'))
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    if request.method == 'POST':
        judul = request.form.get('judul_materi')
        urutan = request.form.get('urutan')
        id_kelas = request.form.get('id_kelas')
        file_pdf = request.files.get('file_pdf')
        files_audio_baru = request.files.getlist('file_audio_baru')
        
        try:
            # 1. Update Data Dasar
            cur.execute("""
                UPDATE materi SET judul_materi = %s, urutan = %s, id_kelas = %s 
                WHERE id_materi = %s
            """, (judul, urutan, id_kelas, id_materi))
            
            # 2. Update PDF jika ada file baru (Ganti PDF lama)
            if file_pdf and file_pdf.filename != '':
                # Ambil nama file lama untuk dihapus
                cur.execute("SELECT file_pdf FROM materi WHERE id_materi = %s", (id_materi,))
                old_pdf = cur.fetchone()['file_pdf']
                if old_pdf:
                    try: os.remove(os.path.join(app.config['UPLOAD_FOLDER'], old_pdf))
                    except: pass
                
                pdf_name = secure_filename(file_pdf.filename)
                pdf_name = f"rev_{datetime.now().strftime('%H%M%S')}_{pdf_name}"
                file_pdf.save(os.path.join(app.config['UPLOAD_FOLDER'], pdf_name))
                cur.execute("UPDATE materi SET file_pdf = %s WHERE id_materi = %s", (pdf_name, id_materi))

            # 3. Tambah Audio Baru (Jika ada)
            for audio in files_audio_baru:
                if audio and audio.filename != '':
                    audio_name = secure_filename(audio.filename)
                    audio_name = f"new_{datetime.now().strftime('%H%M%S')}_{audio_name}"
                    audio.save(os.path.join(app.config['UPLOAD_FOLDER'], audio_name))
                    cur.execute("INSERT INTO materi_audio (id_materi, file_audio) VALUES (%s, %s)", (id_materi, audio_name))
            
            db.commit()
            flash("Modul berhasil diperbarui!", "success")
            return redirect(url_for('admin_modul'))
        except Exception as e:
            db.rollback()
            print(e)
            flash("Gagal memperbarui modul.", "danger")

    # LOAD DATA UNTUK FORM
    cur.execute("SELECT m.*, k.nama_kelas FROM materi m JOIN kelas k ON m.id_kelas = k.id_kelas WHERE m.id_materi = %s", (id_materi,))
    materi = cur.fetchone()
    cur.execute("SELECT * FROM materi_audio WHERE id_materi = %s", (id_materi,))
    audio_list = cur.fetchall()
    cur.execute("SELECT id_kelas, nama_kelas FROM kelas")
    kelas_list = cur.fetchall()
    cur.close()
    
    return render_template('admin/edit_modul.html', m=materi, audios=audio_list, kelas_list=kelas_list)

@app.route('/admin/modul/delete_audio/<int:id_audio>', methods=['POST'])
def delete_audio(id_audio):
    """Menghapus satu file audio saja dari modul"""
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT file_audio, id_materi FROM materi_audio WHERE id_audio = %s", (id_audio,))
    audio = cur.fetchone()
    if audio:
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], audio['file_audio']))
            cur.execute("DELETE FROM materi_audio WHERE id_audio = %s", (id_audio,))
            db.commit()
            flash("File audio dihapus.", "info")
        except: pass
    cur.close()
    return redirect(url_for('edit_modul', id_materi=audio['id_materi']))

@app.route('/admin/modul/delete/<int:id_materi>', methods=['POST'])
def delete_modul(id_materi):
    # Logika hapus modul sama seperti sebelumnya
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM materi WHERE id_materi = %s", (id_materi,))
    db.commit()
    cur.close()
    flash("Modul berhasil dihapus.", "success")
    return redirect(url_for('admin_modul'))

# ==============================================================================
# 5. KUIS & FORUM (Draft Awal)
# ==============================================================================

@app.route('/forum')
def forum_global():
    # Logika forum per kelas/modul akan di-detailkan di tahap berikutnya
    return render_template('forum.html')

# ==============================================================================
# 6. RUTE KHUSUS ADMIN (KELOLA USER, KELAS, SERTIFIKAT, FORUM)
# ==============================================================================

@app.route('/admin/users', methods=['GET', 'POST'])
def manage_users():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
        
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    try:
        # --- LOGIKA KETIKA ADMIN KLIK "SIMPAN PENGGUNA" ---
        if request.method == 'POST':
            nama = request.form.get('nama_lengkap')
            username = request.form.get('username')
            password = request.form.get('password')
            role = request.form.get('role')
            
            # Enkripsi password
            hashed_pw = generate_password_hash(password)
            
            cur.execute("""
                INSERT INTO users (nama_lengkap, username, password, role) 
                VALUES (%s, %s, %s, %s)
            """, (nama, username, hashed_pw, role))
            
            db.commit() # Simpan permanen ke database
            flash(f"Pengguna {nama} ({role.capitalize()}) berhasil ditambahkan!", "success")
            
            return redirect(url_for('manage_users'))

        # --- LOGIKA MENAMPILKAN DAFTAR PENGGUNA (GET) ---
        cur.execute("SELECT id, username, nama_lengkap, role, created_at FROM users ORDER BY created_at DESC")
        users_list = cur.fetchall()
        
        return render_template('admin/manage_users.html', users_list=users_list)
        
    except Exception as e:
        db.rollback() # Batalkan jika ada error
        print("Error Kelola User:", e)
        flash("Gagal memproses data. Pastikan username belum digunakan.", "danger")
        return redirect(url_for('manage_users'))
        
    finally:
        # INI KUNCI AGAR TIDAK FREEZE: Cursor selalu ditutup apapun yang terjadi
        cur.close()

@app.route('/admin/users/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    """Rute untuk mengedit data pengguna yang sudah ada"""
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
        
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    # JIKA ADMIN MENYIMPAN PERUBAHAN (POST)
    if request.method == 'POST':
        nama = request.form.get('nama_lengkap')
        username = request.form.get('username')
        role = request.form.get('role')
        password = request.form.get('password') # Opsional
        
        try:
            # Jika password diisi, berarti admin ingin mereset passwordnya
            if password:
                hashed_pw = generate_password_hash(password)
                cur.execute("""
                    UPDATE users 
                    SET nama_lengkap = %s, username = %s, role = %s, password = %s
                    WHERE id = %s
                """, (nama, username, role, hashed_pw, user_id))
            else:
                # Jika password dikosongkan, update data lainnya saja
                cur.execute("""
                    UPDATE users 
                    SET nama_lengkap = %s, username = %s, role = %s
                    WHERE id = %s
                """, (nama, username, role, user_id))
                
            db.commit()
            flash(f"Data pengguna {nama} berhasil diperbarui!", "success")
            return redirect(url_for('manage_users'))
            
        except Exception as e:
            db.rollback()
            print("Error Edit User:", e)
            flash("Gagal memperbarui pengguna. Pastikan username tidak bentrok dengan yang lain.", "danger")
            
    # JIKA ADMIN BARU MEMBUKA HALAMAN (GET)
    cur.execute("SELECT id, username, nama_lengkap, role FROM users WHERE id = %s", (user_id,))
    user_data = cur.fetchone()
    cur.close()
    
    if not user_data:
        flash("Pengguna tidak ditemukan.", "danger")
        return redirect(url_for('manage_users'))
        
    return render_template('admin/edit_user.html', user=user_data)

@app.route('/admin/users/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    """Rute untuk menghapus pengguna"""
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
        
    # Mencegah admin menghapus akunnya sendiri yang sedang dipakai login
    if user_id == session.get('user_id'):
        flash("Tindakan dicegah! Anda tidak dapat menghapus akun Anda sendiri.", "danger")
        return redirect(url_for('manage_users'))

    db = get_db()
    cur = db.cursor()
    
    try:
        # Menghapus user berdasarkan ID
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        db.commit()
        flash("Pengguna berhasil dihapus dari sistem.", "success")
    except Exception as e:
        db.rollback()
        print("Error Hapus User:", e)
        flash("Gagal menghapus pengguna. Data ini mungkin sedang terikat dengan kelas atau nilai aktif.", "danger")
    finally:
        cur.close()
        
    return redirect(url_for('manage_users'))

# ==============================================================================
# MANAJEMEN KELAS (ADMIN)
# ==============================================================================

@app.route('/admin/kelas', methods=['GET', 'POST'])
def admin_kelas():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    if request.method == 'POST':
        nama_kelas = request.form.get('nama_kelas')
        id_pengajar = request.form.get('id_pengajar')
        level_bahasa = request.form.get('level_bahasa')
        tipe_kelas = request.form.get('tipe_kelas')
        link_kelas = request.form.get('link_kelas')
        
        try:
            # Jika pengajar tidak dipilih, simpan sebagai NULL
            id_pengajar = id_pengajar if id_pengajar else None
            
            cur.execute("""
                INSERT INTO kelas (nama_kelas, id_pengajar, level_bahasa, tipe_kelas, link_kelas)
                VALUES (%s, %s, %s, %s, %s)
            """, (nama_kelas, id_pengajar, level_bahasa, tipe_kelas, link_kelas))
            db.commit()
            flash(f"Kelas '{nama_kelas}' berhasil dibuat!", "success")
        except Exception as e:
            db.rollback()
            print(f"Error Create Kelas: {e}")
            flash("Gagal membuat kelas baru.", "danger")
        return redirect(url_for('admin_kelas'))

    # Ambil daftar kelas beserta nama lengkap pengajarnya
    cur.execute("""
        SELECT k.*, u.nama_lengkap as nama_pengajar 
        FROM kelas k 
        LEFT JOIN users u ON k.id_pengajar = u.id
        ORDER BY k.created_at DESC
    """)
    kelas_list = cur.fetchall()
    
    # Ambil daftar pengajar untuk dropdown di Modal
    cur.execute("SELECT id, nama_lengkap FROM users WHERE role = 'pengajar' ORDER BY nama_lengkap")
    pengajar_list = cur.fetchall()
    cur.close()
    
    return render_template('admin/manage_kelas.html', kelas_list=kelas_list, pengajar_list=pengajar_list)

@app.route('/admin/kelas/edit/<int:id_kelas>', methods=['GET', 'POST'])
def edit_kelas(id_kelas):
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    if request.method == 'POST':
        nama = request.form.get('nama_kelas')
        pengajar = request.form.get('id_pengajar')
        level = request.form.get('level_bahasa')
        tipe = request.form.get('tipe_kelas')
        link = request.form.get('link_kelas')
        
        try:
            cur.execute("""
                UPDATE kelas 
                SET nama_kelas = %s, id_pengajar = %s, level_bahasa = %s, tipe_kelas = %s, link_kelas = %s
                WHERE id_kelas = %s
            """, (nama, pengajar if pengajar else None, level, tipe, link, id_kelas))
            db.commit()
            flash("Perubahan kelas berhasil disimpan!", "success")
            return redirect(url_for('admin_kelas'))
        except Exception as e:
            db.rollback()
            flash("Gagal memperbarui data kelas.", "danger")

    # Load data awal
    cur.execute("SELECT * FROM kelas WHERE id_kelas = %s", (id_kelas,))
    kelas = cur.fetchone()
    cur.execute("SELECT id, nama_lengkap FROM users WHERE role = 'pengajar'")
    pengajar_list = cur.fetchall()
    cur.close()
    
    return render_template('admin/edit_kelas.html', kelas=kelas, pengajar_list=pengajar_list)

@app.route('/admin/kelas/delete/<int:id_kelas>', methods=['POST'])
def delete_kelas(id_kelas):
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute("DELETE FROM kelas WHERE id_kelas = %s", (id_kelas,))
        db.commit()
        flash("Kelas telah dihapus secara permanen.", "success")
    except Exception as e:
        db.rollback()
        flash("Gagal menghapus kelas. Pastikan tidak ada data siswa atau materi yang terikat.", "danger")
    finally:
        cur.close()
    return redirect(url_for('admin_kelas'))

# ==============================================================================
# MANAJEMEN SERTIFIKAT (ADMIN APPROVAL)
# ==============================================================================

@app.route('/admin/sertifikat', methods=['GET', 'POST'])
def admin_sertifikat():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
        
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    # JIKA ADMIN KLIK TOMBOL ACC ATAU TOLAK (POST)
    if request.method == 'POST':
        id_sertifikat = request.form.get('id_sertifikat')
        aksi = request.form.get('aksi') # Isinya 'Approved' atau 'Rejected'
        catatan = request.form.get('keterangan_admin', '')
        
        try:
            cur.execute("""
                UPDATE sertifikat 
                SET status_approval = %s, keterangan_admin = %s, tanggal_terbit = CURRENT_DATE 
                WHERE id_sertifikat = %s
            """, (aksi, catatan, id_sertifikat))
            db.commit()
            
            if aksi == 'Approved':
                flash('Sertifikat berhasil disetujui (ACC)!', 'success')
            else:
                flash('Pengajuan sertifikat ditolak.', 'warning')
                
        except Exception as e:
            db.rollback()
            print("Error Approval Sertifikat:", e)
            flash('Gagal memproses sertifikat.', 'danger')
            
        return redirect(url_for('admin_sertifikat'))
            
    # AMBIL DATA UNTUK DITAMPILKAN (GET)
    cur.execute("""
        SELECT s.*, u.nama_lengkap as nama_siswa, k.nama_kelas, k.level_bahasa, p.nama_lengkap as nama_pengajar
        FROM sertifikat s
        JOIN users u ON s.id_siswa = u.id
        JOIN kelas k ON s.id_kelas = k.id_kelas
        LEFT JOIN users p ON s.id_pengajar_pengaju = p.id
        ORDER BY k.level_bahasa, k.nama_kelas, s.created_at DESC
    """)
    semua_data = cur.fetchall()
    
    pending_list = [s for s in semua_data if s['status_approval'] == 'Pending']
    riwayat_list = [s for s in semua_data if s['status_approval'] != 'Pending']
    
    cur.close()
    return render_template('admin/manage_sertifikat.html', pending=pending_list, riwayat=riwayat_list)
    
    # Pisahkan data menggunakan Python List Comprehension agar mudah di HTML
    pending_list = [s for s in semua_data if s['status_approval'] == 'Pending']
    riwayat_list = [s for s in semua_data if s['status_approval'] != 'Pending']
    
    cur.close()
    return render_template('admin/manage_sertifikat.html', pending=pending_list, riwayat=riwayat_list)

@app.route('/admin/forum')
def admin_forum():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
        
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT k.id_kelas, k.nama_kelas, COUNT(f.id_pesan) as total_pesan
        FROM kelas k
        LEFT JOIN forum_kelas f ON k.id_kelas = f.id_kelas
        GROUP BY k.id_kelas, k.nama_kelas
    """)
    forum_summary = cur.fetchall()
    cur.close()
    
    return render_template('admin/pantau_forum.html', forum_summary=forum_summary)

@app.route('/admin/forum/<int:id_kelas>')
def admin_forum_detail(id_kelas):
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
        
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    try:
        cur.execute("SELECT nama_kelas FROM kelas WHERE id_kelas = %s", (id_kelas,))
        kelas_info = cur.fetchone()
        
        if not kelas_info:
            flash("Kelas tidak ditemukan.", "danger")
            return redirect(url_for('admin_forum'))

        cur.execute("""
            SELECT f.*, u.nama_lengkap, u.role 
            FROM forum_kelas f
            JOIN users u ON f.id_user = u.id
            WHERE f.id_kelas = %s
            ORDER BY f.created_at ASC
        """, (id_kelas,))
        pesan_list = cur.fetchall()
        
        return render_template('admin/pantau_forum_detail.html', kelas=kelas_info, pesan_list=pesan_list)
        
    except Exception as e:
        print("Error Detail Forum Admin:", e)
        flash("Terjadi kesalahan saat mengambil data forum.", "danger")
        return redirect(url_for('admin_forum'))
    finally:
        cur.close()


# ==============================================================================
# ENROLLMENT: MASUKKAN SISWA KE KELAS (ADMIN)
# ==============================================================================

@app.route('/admin/enrollment', methods=['GET', 'POST'])
def admin_enrollment():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
        
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    # PROSES INPUT SISWA KE KELAS
    if request.method == 'POST':
        id_siswa = request.form.get('id_siswa')
        id_kelas = request.form.get('id_kelas')
        
        try:
            cur.execute("""
                INSERT INTO enrollment (id_siswa, id_kelas, status_aktif)
                VALUES (%s, %s, TRUE)
            """, (id_siswa, id_kelas))
            db.commit()
            flash("Siswa berhasil ditambahkan!", "success")
        except Exception as e:
            db.rollback()
            flash("Siswa sudah terdaftar di kelas ini.", "warning")
        return redirect(url_for('admin_enrollment'))

    # 1. Ambil Semua Kelas
    cur.execute("SELECT * FROM kelas ORDER BY level_bahasa, nama_kelas")
    kelas_list = cur.fetchall()
    
    # 2. Ambil Semua Siswa yang sudah terdaftar di kelas manapun
    cur.execute("""
        SELECT e.id_enrollment, e.id_kelas, u.nama_lengkap as nama_siswa 
        FROM enrollment e
        JOIN users u ON e.id_siswa = u.id
        ORDER BY u.nama_lengkap
    """)
    semua_enrollment = cur.fetchall()
    
    # 3. Ambil Daftar Semua Siswa (untuk pilihan di dropdown)
    cur.execute("SELECT id, nama_lengkap FROM users WHERE role = 'siswa' ORDER BY nama_lengkap")
    daftar_siswa = cur.fetchall()
    
    # 4. Kelompokkan siswa ke dalam variabel kelas masing-masing
    for k in kelas_list:
        k['siswa_terdaftar'] = [s for s in semua_enrollment if s['id_kelas'] == k['id_kelas']]
        
    cur.close()
    return render_template('admin/manage_enrollment.html', kelas_list=kelas_list, daftar_siswa=daftar_siswa)

@app.route('/admin/enrollment/delete/<int:id_enrollment>', methods=['POST'])
def delete_enrollment(id_enrollment):
    """Rute untuk mengeluarkan siswa dari kelas"""
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
        
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute("DELETE FROM enrollment WHERE id_enrollment = %s", (id_enrollment,))
        db.commit()
        flash("Siswa berhasil dikeluarkan dari kelas.", "success")
    except Exception as e:
        db.rollback()
        flash("Gagal mengeluarkan siswa.", "danger")
    finally:
        cur.close()
        
    return redirect(url_for('admin_enrollment'))


# ==============================================================================
# GLOBAL CONTEXT PROCESSOR (Agar variabel tersedia di semua file HTML)
# ==============================================================================
@app.context_processor
def inject_user_level():
    user_level = None
    # Hanya jalankan query ini jika yang login adalah siswa
    if session.get('role') == 'siswa' and session.get('user_id'):
        try:
            db = get_db()
            cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # Cek siswa ini sedang aktif di kelas apa
            cur.execute("""
                SELECT k.nama_kelas, k.level_bahasa 
                FROM enrollment e
                JOIN kelas k ON e.id_kelas = k.id_kelas
                WHERE e.id_siswa = %s AND e.status_aktif = TRUE
                LIMIT 1
            """, (session.get('user_id'),))
            
            kelas_aktif = cur.fetchone()
            
            if kelas_aktif:
                # Formatnya akan menjadi "Level 1 - Beginner A"
                user_level = f"{kelas_aktif['level_bahasa']} - {kelas_aktif['nama_kelas']}"
            else:
                user_level = "Belum Terdaftar Kelas"
                
            cur.close()
        except Exception as e:
            print("Error Context Processor:", e)
            user_level = "Data tidak ditemukan"
            
    return dict(user_level=user_level)

# ==============================================================================
# RUN APP
# ==============================================================================
if __name__ == '__main__':
    app.run(debug=True)