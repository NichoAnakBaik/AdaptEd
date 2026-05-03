# ==============================================================================
# 1. IMPORTS
# ==============================================================================
import os
import time
import traceback
from collections import OrderedDict
from datetime import datetime, timedelta
from functools import wraps
import random

# Tambahan untuk PostgreSQL dan .env
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

from flask import (Flask, flash, g, jsonify, redirect, render_template, request,
                   session, url_for)
from werkzeug.utils import secure_filename

# Load variabel dari file .env
load_dotenv()

# ==============================================================================
# 2. INISIALISASI DAN KONFIGURASI APLIKASI
# ==============================================================================
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret_namsan_123')

# Konfigurasi Upload yang Robust
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'ppt', 'pptx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Batas 16MB

# Buat folder upload jika belum ada
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ==============================================================================
# 3. KONEKSI DATABASE & FUNGSI BANTUAN
# ==============================================================================

def get_db():
    """Membuka koneksi database PostgreSQL baru jika belum ada."""
    if 'db' not in g:
        if 'db' not in g:
            g.db = psycopg2.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                database=os.getenv('DB_NAME', 'adapted'),
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASS', '065002300019')
            )
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    """Menutup koneksi database pada akhir request."""
    db = g.pop('db', None)
    if db is not None and not db.closed:
        db.close()

def allowed_file(filename):
    """Memeriksa apakah ekstensi file diizinkan."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.template_filter('format_datetime')
def format_datetime_filter(value):
    """Custom filter Jinja2 untuk memformat datetime."""
    if value is None:
        return ''
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        except (ValueError, TypeError):
            return value
    if isinstance(value, datetime):
        return value.strftime('%d %B %Y, %H:%M')
    return value

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin':
            flash('Anda tidak memiliki izin untuk mengakses halaman ini.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# GANTI TOTAL FUNGSI generate_unique_id ANDA DENGAN VERSI BARU INI

def generate_unique_id(role, cursor):
    """
    Membuat ID unik (NIM/NIP) 8-digit yang HANYA BERISI ANGKA dan aman
    untuk kolom INT biasa.
    """
    # [PERBAIKAN] Gunakan 1 untuk mahasiswa, 2 untuk dosen
    role_digit = "1" if role == 'mahasiswa' else "2"

    if role == 'mahasiswa':
        table_name = "mahasiswa"
        column_name = "NIM"
    else: # Dosen
        table_name = "dosen"
        column_name = "nip"

    while True:
        # [PERBAIKAN] Membuat ID dengan format baru yang lebih pendek
        # 2 digit tahun (misal: "25" untuk 2025)
        year_str = time.strftime("%y")
        # 5 digit angka acak (00000 sampai 99999)
        random_digits = f"{random.randint(0, 99999):05d}"

        # Gabungkan menjadi ID 8-digit: 1 + 2 + 5 = 8 digit
        new_id = f"{role_digit}{year_str}{random_digits}"

        # Periksa ke database apakah ID ini sudah ada
        query = f"SELECT {column_name} FROM {table_name} WHERE {column_name} = %s"
        cursor.execute(query, (new_id,))

        if not cursor.fetchone():
            # Jika ID unik, kembalikan sebagai string angka
            # Database akan otomatis mengubahnya ke INT saat disimpan
            return new_id
        
def query_db(query, args=(), one=False):
    cur = get_db().cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# ==============================================================================
# 4. RUTE UTAMA & AUTENTIKASI
# (Tidak ada perubahan di bagian ini, disertakan untuk kelengkapan)
# ==============================================================================

@app.route('/')
def index():
    # Jika user sudah login, arahkan ke dashboard masing-masing
    if 'user_id' in session:
        if session.get('role') == 'pengajar':
            return redirect(url_for('dashboard_pengajar'))
        elif session.get('role') == 'siswa':
            return redirect(url_for('dashboard_siswa'))
    
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'] # Catatan: Sebaiknya gunakan check_password_hash
        
        db = get_db()
        cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user and user['password'] == password: # Ganti dengan hash check nanti
            session['user_id'] = user['id']
            session['role'] = user['role']
            session['nama'] = user['nama_lengkap']

            # Routing berdasarkan role baru
            if user['role'] == 'admin':
                return redirect(url_for('dashboard_admin'))
            elif user['role'] == 'pengajar':
                return redirect(url_for('dashboard_pengajar'))
            elif user['role'] == 'siswa':
                return redirect(url_for('dashboard_siswa'))
        
        flash('Username atau Password salah!', 'danger')
    return render_template('login.html')

# Ganti seluruh fungsi signup() Anda dengan kode ini di flask_app.py

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        nama = request.form['nama_lengkap']
        role = request.form['role'] # 'siswa' atau 'pengajar'

        try:
            db = get_db()
            cur = db.cursor()
            cur.execute("""
                INSERT INTO users (username, password, role, nama_lengkap) 
                VALUES (%s, %s, %s, %s) RETURNING id
            """, (username, password, role, nama))
            db.commit()
            cur.close()
            flash('Pendaftaran berhasil! Silakan login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
            
    return render_template('signup.html')


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash("Anda telah berhasil logout.", "success")
    return redirect(url_for('index'))


# ==============================================================================
# 5. DASHBOARD & PROFIL PENGGUNA
# (Tidak ada perubahan di bagian ini, disertakan untuk kelengkapan)
# ==============================================================================

@app.route('/dashboard_pengajar')
def dashboard_pengajar():
    if session.get('role') != 'pengajar':
        return redirect(url_for('login'))
    
    # Mengambil kelas yang diajar oleh pengajar ini
    kelas_saya = query_db("SELECT * FROM kelas WHERE id_pengajar = %s", (session['user_id'],))
    
    # Kita tetap arahkan ke folder 'dosen' agar kamu tidak perlu ubah nama folder template dulu
    return render_template('pengajar/dashboard_pengajar.html', kelas=kelas_saya)

@app.route('/dashboard_siswa')
def dashboard_siswa():
    if session.get('role') != 'siswa':
        return redirect(url_for('login'))
    
    # Mengambil kelas yang diikuti siswa
    kelas_enrolled = query_db("""
        SELECT k.* FROM kelas k 
        JOIN enrollment e ON k.id_kelas = e.id_kelas 
        WHERE e.id_siswa = %s
    """, (session['user_id'],))
    
    return render_template('siswa/dashboard_siswa.html', kelas=kelas_enrolled)

@app.route('/dashboard_admin')
def dashboard_admin():
    if session.get('role') != 'admin':
        flash('Akses ditolak. Halaman ini khusus Admin.', 'danger')
        return redirect(url_for('login'))

    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        # Mengambil statistik dasar untuk ditampilkan di Widget
        cur.execute("SELECT COUNT(*) as total FROM users WHERE role = 'siswa'")
        total_siswa = cur.fetchone()['total']

        cur.execute("SELECT COUNT(*) as total FROM users WHERE role = 'pengajar'")
        total_pengajar = cur.fetchone()['total']

        cur.execute("SELECT COUNT(*) as total FROM kelas")
        total_kelas = cur.fetchone()['total']

        cur.execute("SELECT COUNT(*) as total FROM kuis")
        total_kuis = cur.fetchone()['total']

        # Mengambil 5 pengguna terbaru yang baru mendaftar
        cur.execute("""
            SELECT username, nama_lengkap, role, created_at 
            FROM users 
            ORDER BY created_at DESC LIMIT 5
        """)
        users_terbaru = cur.fetchall()

        return render_template('admin/dashboard_admin.html',
                               total_siswa=total_siswa,
                               total_pengajar=total_pengajar,
                               total_kelas=total_kelas,
                               total_kuis=total_kuis,
                               users_terbaru=users_terbaru)
    except Exception as e:
        print("Error Dashboard Admin:", e)
        flash("Terjadi kesalahan saat memuat data admin.", "danger")
        return redirect(url_for('index'))
    finally:
        cur.close()


# GANTI FUNGSI LAMA ANDA DENGAN YANG INI DI flask_app.py

@app.route('/update_mahasiswa_profile', methods=['POST'])
def update_mahasiswa_profile():
    if session.get('role') != 'mahasiswa':
        return redirect(url_for('login'))

    user_id = session['user_id']
    # Ambil SEMUA data dari form, termasuk NIM
    nama = request.form.get('nama')
    nim = request.form.get('nim')
    email = request.form.get('email')
    jurusan = request.form.get('jurusan')
    angkatan = request.form.get('angkatan')
    no_hp = request.form.get('no_hp')
    alamat = request.form.get('alamat')

    # Validasi sekarang menyertakan NIM
    if not all([nama, nim, email, jurusan]):
        flash('Data wajib (Nama, NIM, Email, Jurusan) harus diisi.', 'danger')
        return redirect(url_for('dashboard'))

    con = get_db()
    cur = con.cursor(dictionary=True)
    try:
        # Cek apakah NIM yang dimasukkan sudah dipakai oleh user LAIN.
        cur.execute("SELECT user_id FROM mahasiswa WHERE NIM = %s AND user_id != %s", (nim, user_id))
        if cur.fetchone():
            flash('NIM sudah digunakan oleh mahasiswa lain.', 'danger')
            return redirect(url_for('dashboard'))

        # Cek apakah profil untuk user ini sudah ada atau belum.
        cur.execute("SELECT user_id FROM mahasiswa WHERE user_id = %s", (user_id,))
        profil_exists = cur.fetchone()

        if profil_exists:
            # Jika profil sudah ada, UPDATE datanya.
            sql = "UPDATE mahasiswa SET nama=%s, NIM=%s, email=%s, jurusan=%s, angkatan=%s, no_hp=%s, alamat=%s WHERE user_id=%s"
            params = (nama, nim, email, jurusan, angkatan, no_hp, alamat, user_id)
            flash_message = "Profil berhasil diperbarui!"
        else:
            # Jika profil belum ada, INSERT data baru.
            sql = "INSERT INTO mahasiswa (user_id, nama, NIM, email, jurusan, angkatan, no_hp, alamat) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            params = (user_id, nama, nim, email, jurusan, angkatan, no_hp, alamat)
            flash_message = "Profil berhasil disimpan!"

        cur.execute(sql, params)
        con.commit()
        flash(flash_message, 'success')

    except psycopg2.Error as err:
        con.rollback()
        flash(f'Terjadi kesalahan database: {err.msg}', 'danger')
    finally:
        cur.close()

    return redirect(url_for('dashboard'))

# GANTI FUNGSI LAMA ANDA DENGAN YANG INI JUGA

@app.route('/update_dosen_profile', methods=['POST'])
def update_dosen_profile():
    if session.get('role') != 'dosen':
        return redirect(url_for('login'))

    user_id = session['user_id']
    nama = request.form.get('nama')
    nip = request.form.get('nip')
    email = request.form.get('email')
    departemen = request.form.get('departemen')

    if not all([nama, nip, email]):
        flash('Nama, NIP, dan Email wajib diisi.', 'danger')
        return redirect(url_for('dashboard'))

    con = get_db()
    cur = con.cursor(dictionary=True)
    try:
        cur.execute("SELECT user_id FROM dosen WHERE user_id = %s", (user_id,))
        profil_exists = cur.fetchone()

        # Logika INSERT vs UPDATE juga diterapkan di sini
        if profil_exists:
            sql = "UPDATE dosen SET nama = %s, nip = %s, email = %s, departemen = %s WHERE user_id = %s"
            params = (nama, nip, email, departemen, user_id)
            flash_message = 'Profil berhasil diperbarui!'
        else:
            # Sebenarnya profil dosen sudah dibuat saat signup, tapi ini untuk jaga-jaga
            sql = "INSERT INTO dosen (user_id, nama, nip, email, departemen) VALUES (%s, %s, %s, %s, %s)"
            params = (user_id, nama, nip, email, departemen)
            flash_message = 'Profil berhasil dibuat!'

        cur.execute(sql, params)
        con.commit()
        flash(flash_message, 'success')

    except mysql.connector.Error as err:
        con.rollback()
        flash(f'Terjadi kesalahan database: {err.msg}', 'danger')
    finally:
        cur.close()

    return redirect(url_for('dashboard'))

# ==============================================================================
# 6. MATERI PEMBELAJARAN (KODE DENGAN SEMUA PERBAIKAN)
# ============================================================================== 

@app.route('/materi')
def materi():
    # 1. Proteksi Login
    if 'role' not in session:
        return redirect(url_for('login'))

    role = session['role']
    user_id = session['user_id']
    db = get_db()
    
    # Menggunakan RealDictCursor agar hasil query bisa diakses sebagai dictionary (kelas['nama_kelas'])
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        # --- Logika untuk SISWA ---
        if role == 'siswa':
            # Ambil daftar kelas yang diikuti siswa melalui tabel enrollment
            cur.execute("""
                SELECT k.id_kelas, k.nama_kelas, k.level_bahasa, u.nama_lengkap as nama_pengajar
                FROM kelas k
                JOIN enrollment e ON k.id_kelas = e.id_kelas
                JOIN users u ON k.id_pengajar = u.id
                WHERE e.id_siswa = %s AND e.status_aktif = TRUE
                ORDER BY k.nama_kelas
            """, (user_id,))
            kelas_list = cur.fetchall()

            # Ambil materi untuk setiap kelas yang ditemukan
            for kelas in kelas_list:
                cur.execute("""
                    SELECT * FROM materi 
                    WHERE id_kelas = %s 
                    ORDER BY urutan ASC, created_at DESC
                """, (kelas['id_kelas'],))
                kelas['materi'] = cur.fetchall()

            # Tetap menggunakan folder lama agar tidak perlu ganti nama folder template
            return render_template('siswa/materi.html', kelas_list=kelas_list)

        # --- Logika untuk PENGAJAR ---
        elif role == 'pengajar':
            # Pengajar langsung melihat kelas yang mereka ampu (id_pengajar di tabel kelas)
            cur.execute("SELECT * FROM kelas WHERE id_pengajar = %s ORDER BY nama_kelas", (user_id,))
            kelas_list = cur.fetchall()

            # Ambil materi untuk setiap kelas yang diampu pengajar
            for kelas in kelas_list:
                cur.execute("""
                    SELECT * FROM materi 
                    WHERE id_kelas = %s 
                    ORDER BY urutan ASC, created_at DESC
                """, (kelas['id_kelas'],))
                kelas['materi'] = cur.fetchall()

            return render_template('pengajar/materi.html', kelas_list=kelas_list)

    except Exception as e:
        # Log error ke terminal untuk debugging
        print(f"Error pada rute materi: {str(e)}")
        flash("Terjadi kesalahan saat memuat data materi.", "danger")
        return redirect(url_for('index'))

    except Exception as e:
        flash(f"Terjadi kesalahan saat memuat materi: {e}", "danger")
        traceback.print_exc()
        return redirect(url_for('dashboard'))
    finally:
        if cur: cur.close()

@app.route('/upload_materi', methods=['GET', 'POST'])
def upload_materi():
    if session.get('role') != 'dosen':
        flash("Hanya dosen yang dapat mengakses halaman ini.", "danger")
        return redirect(url_for('login'))

    try:
        con = get_db()
        cur = con.cursor(dictionary=True)
    except mysql.connector.Error as err:
        flash(f"Koneksi ke database gagal: {err}", "danger")
        return redirect(url_for('dashboard'))

    try:
        if request.method == 'GET':
            cur.execute("SELECT id_dosen FROM dosen WHERE user_id = %s", (session['user_id'],))
            dosen = cur.fetchone()

            if not dosen or not dosen.get('id_dosen'):
                flash("Profil dosen Anda tidak lengkap atau tidak ditemukan. Tidak dapat memuat form upload.", "danger")
                return redirect(url_for('materi'))

            id_dosen_ditemukan = dosen['id_dosen']
            cur.execute("SELECT id_kelas, nama_kelas FROM kelas WHERE id_dosen = %s", (id_dosen_ditemukan,))
            kelas_list = cur.fetchall()
            return render_template('/dosen/upload_materi.html', kelas_list=kelas_list)

        elif request.method == 'POST':
            title = request.form.get('title')
            content = request.form.get('content')
            id_kelas = request.form.get('id_kelas')
            file = request.files.get('file')

            if not title or not id_kelas:
                flash("Judul dan Kelas wajib diisi.", "danger")
                return redirect(request.url)

            filename = None
            if file and file.filename != '':
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                else:
                    flash("Format file tidak didukung!", "danger")
                    return redirect(request.url)

            cur.execute("""
                INSERT INTO materi (title, content, file_name, uploaded_by, id_kelas)
                VALUES (%s, %s, %s, %s, %s)
            """, (title, content, filename, session['user_id'], id_kelas))

            con.commit()
            flash("Materi berhasil diunggah!", "success")
            return redirect(url_for('materi'))

    except mysql.connector.Error as err:
        con.rollback()
        flash(f"DATABASE ERROR: Gagal menyimpan. Periksa struktur tabel Anda. Pesan: {err.msg}", "danger")
        traceback.print_exc()
        return redirect(url_for('materi'))
    except Exception as e:
        con.rollback()
        flash(f"TERJADI KESALAHAN FATAL: {e}", "danger")
        traceback.print_exc()
        return redirect(url_for('materi'))
    finally:
        if cur:
            cur.close()


@app.route('/edit_materi/<int:materi_id>', methods=['GET', 'POST'])
def edit_materi(materi_id):
    if session.get('role') != 'dosen':
        return redirect(url_for('login'))

    con = get_db()
    cur = con.cursor(dictionary=True)

    # Verifikasi kepemilikan materi
    cur.execute("SELECT * FROM materi WHERE id = %s AND uploaded_by = %s", (materi_id, session['user_id']))
    materi = cur.fetchone()
    if not materi:
        cur.close()
        flash("Materi tidak ditemukan atau Anda tidak berhak mengedit.", "danger")
        return redirect(url_for('materi'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        if not title or not content:
            flash("Judul dan Konten tidak boleh kosong.", "danger")
            return render_template('dosen/edit_materi.html', materi=materi)

        new_filename = materi['file_name']
        file = request.files.get('file')

        if file and file.filename != '':
            if allowed_file(file.filename):
                # Hapus file lama jika ada
                if materi['file_name']:
                    old_file_path = os.path.join(app.config['UPLOAD_FOLDER'], materi['file_name'])
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)

                # Simpan file baru
                timestamp = str(int(time.time()))
                filename, ext = os.path.splitext(secure_filename(file.filename))
                new_filename = f"{filename}_{timestamp}{ext}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
            else:
                flash("Format file baru tidak didukung!", "danger")
                cur.close()
                return render_template('dosen/edit_materi.html', materi=materi)

        try:
            cur.execute("""
                UPDATE materi SET title = %s, content = %s, file_name = %s, updated_at = NOW()
                WHERE id = %s
            """, (title, content, new_filename, materi_id))
            con.commit()
            flash("Materi berhasil diperbarui.", "success")
            return redirect(url_for('materi'))
        except psycopg2.Error as err:
            con.rollback()
            flash(f"Gagal memperbarui materi: {err.msg}", "danger")
        finally:
            cur.close()
            return redirect(url_for('edit_materi', materi_id=materi_id))

    # Untuk method GET
    cur.close()
    return render_template('dosen/edit_materi.html', materi=materi)


@app.route('/delete_materi/<int:materi_id>', methods=['POST'])
def delete_materi(materi_id):
    if session.get('role') != 'dosen':
        return redirect(url_for('login'))

    try:
        con = get_db()
        cur = con.cursor(dictionary=True)

        # Ambil nama file untuk dihapus dari sistem file
        cur.execute("SELECT file_name FROM materi WHERE id = %s AND uploaded_by = %s", (materi_id, session['user_id']))
        materi = cur.fetchone()

        if materi:
            # Hapus record dari database
            cur.execute("DELETE FROM materi WHERE id = %s", (materi_id,))
            con.commit()

            # Hapus file fisik jika ada
            if materi['file_name']:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], materi['file_name'])
                if os.path.exists(file_path):
                    os.remove(file_path)
            flash("Materi berhasil dihapus.", "success")
        else:
            flash("Materi tidak ditemukan atau Anda tidak berhak menghapus.", "danger")

    except mysql.connector.Error as err:
        flash(f"Gagal menghapus materi: {err.msg}", "danger")
    finally:
        if 'cur' in locals(): cur.close()

    return redirect(url_for('materi'))


# ==============================================================================
# MODUL KUIS & LEARNING ANALYTICS (ADAPTED NAMSAN)
# ==============================================================================

# ------------------------- RUTE PENGAJAR -------------------------
@app.route('/kuis_pengajar')
def kuis_pengajar():
    if session.get('role') != 'pengajar':
        return redirect(url_for('login'))
    
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    # Menampilkan daftar kuis yang dibuat oleh pengajar ini
    cur.execute("""
        SELECT k.id_kuis, k.judul_kuis, k.durasi_menit, k.created_at, c.nama_kelas,
               (SELECT COUNT(*) FROM soal_kuis s WHERE s.id_kuis = k.id_kuis) as total_soal
        FROM kuis k
        JOIN kelas c ON k.id_kelas = c.id_kelas
        WHERE c.id_pengajar = %s
        ORDER BY k.created_at DESC
    """, (session['user_id'],))
    kuis_list = cur.fetchall()
    cur.close()
    
    return render_template('pengajar/kuis.html', kuis_list=kuis_list)

@app.route('/create_kuis', methods=['GET', 'POST'])
def create_kuis():
    if session.get('role') != 'pengajar':
        return redirect(url_for('login'))
        
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    if request.method == 'POST':
        id_kelas = request.form.get('id_kelas')
        judul_kuis = request.form.get('judul_kuis')
        durasi = request.form.get('durasi', 30)

        try:
            # 1. Simpan Data Kuis Utama (Pake RETURNING id untuk PostgreSQL)
            cur.execute("""
                INSERT INTO kuis (id_kelas, judul_kuis, durasi_menit)
                VALUES (%s, %s, %s) RETURNING id_kuis
            """, (id_kelas, judul_kuis, durasi))
            id_kuis = cur.fetchone()['id_kuis']

            # 2. Ambil array soal dari form HTML
            pertanyaan_list = request.form.getlist('pertanyaan[]')
            kategori_list = request.form.getlist('kategori_kompetensi[]')
            opsi_a_list = request.form.getlist('opsi_a[]')
            opsi_b_list = request.form.getlist('opsi_b[]')
            opsi_c_list = request.form.getlist('opsi_c[]')
            opsi_d_list = request.form.getlist('opsi_d[]')
            jawaban_list = request.form.getlist('jawaban_benar[]')

            # 3. Looping untuk menyimpan setiap soal
            for i in range(len(pertanyaan_list)):
                # Default kategori ke Reading jika form lama belum diupdate
                kategori = kategori_list[i] if i < len(kategori_list) else 'Reading'
                
                cur.execute("""
                    INSERT INTO soal_kuis 
                    (id_kuis, pertanyaan, kategori_kompetensi, pilihan_a, pilihan_b, pilihan_c, pilihan_d, jawaban_benar)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (id_kuis, pertanyaan_list[i], kategori, 
                      opsi_a_list[i], opsi_b_list[i], opsi_c_list[i], opsi_d_list[i], jawaban_list[i]))
            
            db.commit()
            flash('Kuis beserta soal berhasil dibuat!', 'success')
            return redirect(url_for('kuis_pengajar'))
            
        except Exception as e:
            db.rollback()
            print("Error Create Kuis:", e)
            flash(f'Terjadi error saat membuat kuis: {str(e)}', 'danger')

    # Untuk Method GET (Tampilkan Form)
    cur.execute("SELECT id_kelas, nama_kelas FROM kelas WHERE id_pengajar = %s", (session['user_id'],))
    kelas_list = cur.fetchall()
    cur.close()
    
    return render_template('dosen/create_kuis.html', kelas_list=kelas_list)

@app.route('/delete_kuis/<int:id_kuis>', methods=['POST'])
def delete_kuis(id_kuis):
    if session.get('role') != 'pengajar':
        return redirect(url_for('login'))
    
    try:
        db = get_db()
        cur = db.cursor()
        # ON DELETE CASCADE di PostgreSQL akan otomatis menghapus soal_kuis dan log_aktivitas
        cur.execute("DELETE FROM kuis WHERE id_kuis = %s", (id_kuis,))
        db.commit()
        cur.close()
        flash('Kuis berhasil dihapus.', 'success')
    except Exception as e:
        flash('Gagal menghapus kuis.', 'danger')
        
    return redirect(url_for('kuis_pengajar'))


# ------------------------- RUTE SISWA & ENGINE AI -------------------------
@app.route('/kuis_siswa')
def kuis_siswa():
    if session.get('role') != 'siswa':
        return redirect(url_for('login'))
        
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    # Ambil kuis dari kelas yang diikuti siswa
    cur.execute("""
        SELECT k.*, c.nama_kelas,
               (SELECT COUNT(*) FROM soal_kuis s WHERE s.id_kuis = k.id_kuis) as total_soal
        FROM kuis k
        JOIN kelas c ON k.id_kelas = c.id_kelas
        JOIN enrollment e ON c.id_kelas = e.id_kelas
        WHERE e.id_siswa = %s
        ORDER BY k.created_at DESC
    """, (session['user_id'],))
    kuis_list = cur.fetchall()
    cur.close()
    
    return render_template('mahasiswa/kuis.html', kuis_list=kuis_list)

@app.route('/kerjakan_kuis/<int:id_kuis>')
def kerjakan_kuis(id_kuis):
    if session.get('role') != 'siswa':
        return redirect(url_for('login'))
        
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    cur.execute("SELECT * FROM kuis WHERE id_kuis = %s", (id_kuis,))
    kuis = cur.fetchone()
    
    # Kirim soal ke template tanpa kunci jawaban agar aman
    cur.execute("""
        SELECT id_soal, pertanyaan, kategori_kompetensi, pilihan_a, pilihan_b, pilihan_c, pilihan_d 
        FROM soal_kuis WHERE id_kuis = %s
    """, (id_kuis,))
    soal_list = cur.fetchall()
    cur.close()
    
    # Template ini nanti harus dirancang khusus untuk merekam "waktu pengerjaan (detik)" via JavaScript
    return render_template('mahasiswa/kerjakan_kuis.html', kuis=kuis, soal_list=soal_list)

@app.route('/submit_kuis/<int:id_kuis>', methods=['POST'])
def submit_kuis(id_kuis):
    """
    Ini adalah rute paling penting untuk AI! 
    Menerima JSON dari frontend yang berisi array jawaban beserta durasi berpikir siswa.
    """
    if session.get('role') != 'siswa':
        return jsonify({'status': 'error', 'message': 'Akses ditolak'})
        
    id_siswa = session['user_id']
    data = request.json
    jawaban_siswa = data.get('jawaban', []) # Format ex: [{'id_soal': 1, 'jawaban': 'A', 'waktu_detik': 15}]
    
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    benar = 0
    total_soal = len(jawaban_siswa)
    
    try:
        for item in jawaban_siswa:
            id_soal = item.get('id_soal')
            jawaban_user = item.get('jawaban')
            waktu_detik = item.get('waktu_detik', 0) # Bahan bakar untuk model Machine Learning
            
            # Cek kunci jawaban
            cur.execute("SELECT jawaban_benar FROM soal_kuis WHERE id_soal = %s", (id_soal,))
            soal = cur.fetchone()
            is_correct = False
            
            if soal and soal['jawaban_benar'] == jawaban_user:
                is_correct = True
                benar += 1
                
            # SIMPAN LOG AKTIVITAS (OTAK AI)
            cur.execute("""
                INSERT INTO log_aktivitas_kuis (id_siswa, id_kuis, id_soal, jawaban_user, is_correct, waktu_pengerjaan_detik)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (id_siswa, id_kuis, id_soal, jawaban_user, is_correct, waktu_detik))
            
        # Hitung Nilai Akhir
        skor_total = (benar / total_soal) * 100 if total_soal > 0 else 0
        
        cur.execute("SELECT skor_minimum FROM kuis WHERE id_kuis = %s", (id_kuis,))
        kuis_info = cur.fetchone()
        skor_min = kuis_info['skor_minimum'] if kuis_info else 60
        status_lulus = skor_total >= skor_min
        
        # Simpan nilai akhir
        cur.execute("""
            INSERT INTO nilai_akhir_kuis (id_siswa, id_kuis, skor_total, status_lulus)
            VALUES (%s, %s, %s, %s)
        """, (id_siswa, id_kuis, skor_total, status_lulus))
        
        db.commit()
        return jsonify({'status': 'success', 'skor': skor_total, 'benar': benar, 'total': total_soal})
        
    except Exception as e:
        db.rollback()
        print("Error Submit Kuis:", e)
        return jsonify({'status': 'error', 'message': str(e)})
    finally:
        cur.close()

# ==============================================================================
# 8. API ENDPOINTS (UNTUK JAVASCRIPT/AJAX)
# ==============================================================================

@app.route('/api/kuis/<int:id_kuis>/soal')
def api_get_soal_kuis(id_kuis):
    """API untuk mengambil soal kuis dalam format JSON."""
    if session.get('role') != 'mahasiswa':
        return jsonify({'error': 'Unauthorized'}), 401

    con = get_db()
    cur = con.cursor(dictionary=True)
    try:
        cur.execute("SELECT id_pertanyaan, teks_pertanyaan, jenis FROM pertanyaan_kuis WHERE id_kuis = %s ORDER BY id_pertanyaan", (id_kuis,))
        pertanyaan_rows = cur.fetchall()

        if not pertanyaan_rows:
            return jsonify({'error': 'Kuis tidak memiliki soal'}), 404

        questions_for_frontend = []
        for p_row in pertanyaan_rows:
            question_data = {
                'id_soal': p_row['id_pertanyaan'],
                'pertanyaan': p_row['teks_pertanyaan'],
                'tipe': p_row['jenis'], # 'pilihan_ganda' atau 'esai'
                'opsi': []
            }
            if p_row['jenis'] == 'pilihan_ganda':
                cur.execute("SELECT id_pilihan, teks_pilihan FROM pilihan_jawaban WHERE id_pertanyaan = %s ORDER BY id_pilihan", (p_row['id_pertanyaan'],))
                opsi_rows = cur.fetchall()
                question_data['opsi'] = [{'id_opsi': o['id_pilihan'], 'teks_opsi': o['teks_pilihan']} for o in opsi_rows]
            questions_for_frontend.append(question_data)

        return jsonify({'soal': questions_for_frontend})
    finally:
        cur.close()


# Ganti seluruh fungsi api_submit_kuis yang lama dengan versi baru yang lebih aman ini.

# GANTI TOTAL FUNGSI INI DI APP.PY - INI ADALAH VERSI DENGAN MANAJEMEN TRANSAKSI YANG BENAR

@app.route('/api/kuis/<int:id_kuis>/submit', methods=['POST'])
def api_submit_kuis(id_kuis):
    if session.get('role') != 'mahasiswa':
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    if not data or 'jawaban' not in data:
        return jsonify({'error': 'Data jawaban tidak valid'}), 400

    con = get_db()
    cur = con.cursor(dictionary=True)

    try:
        # === SEMUA OPERASI DATABASE DI BAWAH INI DIANGGAP SATU TRANSAKSI ===

        cur.execute("SELECT NIM FROM mahasiswa WHERE user_id = %s", (session['user_id'],))
        mahasiswa = cur.fetchone()
        if not mahasiswa or not mahasiswa.get('NIM'):
            return jsonify({'error': 'Data mahasiswa tidak ditemukan'}), 404
        nim_mahasiswa = mahasiswa['NIM']

        # 1. Hapus pengerjaan lama (jika ada)
        cur.execute("DELETE FROM jawaban_mahasiswa WHERE id_mahasiswa = %s AND id_pertanyaan IN (SELECT id_pertanyaan FROM pertanyaan_kuis WHERE id_kuis = %s)", (nim_mahasiswa, id_kuis))
        cur.execute("DELETE FROM hasil_kuis WHERE id_kuis = %s AND NIM = %s", (id_kuis, nim_mahasiswa))

        # 2. Buat log pengerjaan baru
        cur.execute("INSERT INTO hasil_kuis (id_kuis, NIM, waktu_mulai, status) VALUES (%s, %s, NOW(), 'sedang_dikerjakan')", (id_kuis, nim_mahasiswa))
        id_hasil_kuis = cur.lastrowid # Ambil ID dari hasil_kuis yang baru dibuat

        # 3. Proses dan simpan setiap jawaban
        jawaban_dari_client = data.get('jawaban', {})
        total_score_pg, jumlah_soal_pg, has_essay = 0.0, 0, False

        for id_soal_str, jawaban_client in jawaban_dari_client.items():
            id_soal = int(id_soal_str)
            cur.execute("SELECT jenis FROM pertanyaan_kuis WHERE id_pertanyaan = %s", (id_soal,))
            pertanyaan_db = cur.fetchone()

            if not pertanyaan_db or not pertanyaan_db.get('jenis'):
                print(f"PERINGATAN: Soal dengan ID {id_soal} dilewati karena tidak memiliki tipe soal.")
                continue

            id_pilihan_terpilih, jawaban_teks_essay, nilai_pertanyaan = None, None, 0.0
            jenis_soal_bersih = pertanyaan_db['jenis'].strip().lower()

            if jenis_soal_bersih == 'pilihan_ganda':
                jumlah_soal_pg += 1
                if jawaban_client is not None:
                    id_pilihan_terpilih = int(jawaban_client)
                    cur.execute("SELECT is_jawaban_benar FROM pilihan_jawaban WHERE id_pilihan = %s", (id_pilihan_terpilih,))
                    pilihan_db = cur.fetchone()
                    if pilihan_db and pilihan_db['is_jawaban_benar']: nilai_pertanyaan = 100.0
                total_score_pg += nilai_pertanyaan

            elif jenis_soal_bersih in ['esai', 'essay']:
                has_essay = True
                jawaban_teks_essay = jawaban_client if jawaban_client else None
                nilai_pertanyaan = None

            cur.execute(
                "INSERT INTO jawaban_mahasiswa (id_pertanyaan, id_mahasiswa, id_pilihan, jawaban_teks, nilai) VALUES (%s, %s, %s, %s, %s)",
                (id_soal, nim_mahasiswa, id_pilihan_terpilih, jawaban_teks_essay, nilai_pertanyaan)
            )

        # 4. Hitung nilai akhir dan update log pengerjaan
        status_akhir = 'belum_dinilai' if has_essay else 'sudah_dinilai'
        nilai_akhir_total = None
        if not has_essay and jumlah_soal_pg > 0:
            nilai_akhir_total = total_score_pg / jumlah_soal_pg
        elif not has_essay:
            nilai_akhir_total = 0

        cur.execute(
            "UPDATE hasil_kuis SET status = %s, waktu_selesai = NOW(), nilai_total = %s WHERE id_hasil = %s",
            (status_akhir, nilai_akhir_total, id_hasil_kuis)
        )

        # [PERBAIKAN FINAL] Commit hanya dilakukan satu kali di paling akhir jika SEMUA proses di atas berhasil
        con.commit()

        # Siapkan respons JSON untuk ditampilkan di modal hasil
        grade, message, badgeClass = 'N/A', 'Jawaban esai Anda akan dinilai oleh dosen.', 'bg-info'
        if nilai_akhir_total is not None:
            if nilai_akhir_total >= 85: grade, message, badgeClass = 'A', 'Luar Biasa!', 'bg-success'
            elif nilai_akhir_total >= 75: grade, message, badgeClass = 'B', 'Kerja Bagus!', 'bg-primary'
            else: grade, message, badgeClass = 'D', 'Perlu perbaikan.', 'bg-danger'
        return jsonify({'success': True, 'message': message, 'nilai': nilai_akhir_total, 'grade': grade, 'badgeClass': badgeClass})

    except Exception as e:
        # Jika ada error di mana pun di dalam blok 'try', batalkan semua perubahan
        if con and con.is_connected(): con.rollback()
        traceback.print_exc()
        return jsonify({'error': f'Terjadi kesalahan pada server: {e}'}), 500
    finally:
        if con and con.is_connected(): cur.close()


@app.route('/api/check_quiz_status/<int:id_kuis>')
def check_quiz_status(id_kuis):
    """API untuk memeriksa apakah mahasiswa sudah mengerjakan kuis tertentu."""
    if session.get('role') != 'mahasiswa':
        return jsonify({'error': 'Unauthorized'}), 401

    con = get_db()
    cur = con.cursor(dictionary=True)
    try:
        cur.execute("SELECT NIM FROM mahasiswa WHERE user_id = %s", (session['user_id'],))
        mahasiswa = cur.fetchone()
        if not mahasiswa:
            return jsonify({'has_taken': False, 'error': 'Mahasiswa tidak ditemukan'}), 404

        cur.execute("SELECT status, nilai_total FROM hasil_kuis WHERE id_kuis = %s AND NIM = %s", (id_kuis, mahasiswa['NIM']))
        hasil = cur.fetchone()

        if hasil:
            return jsonify({'has_taken': True, 'status': hasil['status'], 'score': hasil['nilai_total']})
        else:
            return jsonify({'has_taken': False})

    except Exception as e:
        return jsonify({'error': f'Terjadi kesalahan server: {e}'}), 500
    finally:
        cur.close()


# ==============================================================================
# 9. FORUM DISKUSI (VERSI PERBAIKAN)
# ==============================================================================

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if 'role' not in session:
        return redirect(url_for('login'))

    con = get_db()
    cur = con.cursor(dictionary=True)

    try:
        # Penanganan untuk membuat postingan baru (method POST)
        if request.method == 'POST':
            content = request.form.get('content')
            if not content or not content.strip():
                flash("Postingan tidak boleh kosong.", "warning")
            else:
                try:
                    cur.execute("INSERT INTO posts (content, role, author_id) VALUES (%s, %s, %s)",
                                (content, session['role'], session['user_id']))
                    con.commit()
                    flash("Postingan berhasil ditambahkan.", "success")
                except mysql.connector.Error as err:
                    con.rollback()
                    # Menghilangkan f-string
                    flash("Gagal memposting: {}".format(err.msg), "danger")
            return redirect(url_for('forum'))

        # Logika untuk menampilkan semua postingan (method GET)
        cur.execute("""
            SELECT p.id, p.content, p.author_id, p.role, p.created_at, u.username
            FROM posts p JOIN users u ON p.author_id = u.id
            ORDER BY p.created_at DESC
        """)
        posts = cur.fetchall()

        if posts:
            post_ids = [post['id'] for post in posts]

            # --- [PERBAIKAN] F-STRING DIHAPUS TOTAL ---

            # 1. Buat placeholder dinamis, contoh: '%s, %s, %s'
            query_placeholder = ','.join(['%s'] * len(post_ids))

            # 2. Bangun string SQL menggunakan string concatenation
            sql_query_for_comments = (
                "SELECT c.id, c.post_id, c.content, c.created_at, c.author_id, u.username, u.role "
                "FROM comments c JOIN users u ON c.author_id = u.id "
                "WHERE c.post_id IN (" + query_placeholder + ") ORDER BY c.created_at ASC"
            )

            # 3. Jalankan query dengan string dan parameter yang sudah jadi
            cur.execute(sql_query_for_comments, tuple(post_ids))
            comments_all = cur.fetchall()
            # --- SELESAI PERBAIKAN ---

            comments_by_post = {post_id: [] for post_id in post_ids}
            for comment in comments_all:
                comments_by_post[comment['post_id']].append(comment)

            for post in posts:
                post['comments'] = comments_by_post.get(post['id'], [])

        return render_template('forum.html', posts=posts)

    except Exception as e:
        # Menghilangkan f-string
        flash("Terjadi kesalahan fatal saat memuat forum: {}".format(e), "danger")
        traceback.print_exc()
        return render_template('forum.html', posts=[])
    finally:
        if cur:
            cur.close()


@app.route('/comment/<int:post_id>', methods=['POST'])
def comment(post_id):
    if 'role' not in session:
        return redirect(url_for('login'))

    content = request.form.get('content')
    if not content or not content.strip():
        flash("Komentar tidak boleh kosong.", "warning")
        return redirect(url_for('forum'))

    con = get_db()
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO comments (content, post_id, author_id) VALUES (%s, %s, %s)",
                    (content, post_id, session['user_id']))
        con.commit()
        flash("Komentar berhasil ditambahkan.", "success")
    except mysql.connector.Error as err:
        con.rollback()
        flash(f"Gagal berkomentar: {err.msg}", "danger")
    finally:
        if cur:
            cur.close()

    return redirect(url_for('forum'))

# ============================================================
# TAMBAHKAN FUNGSI BARU INI UNTUK HAPUS KOMENTAR
# ============================================================
@app.route('/delete_comment/<int:comment_id>', methods=['POST'])
def delete_comment(comment_id):
    # 1. Pastikan user sudah login
    if 'user_id' not in session:
        flash("Anda harus login untuk menghapus komentar.", "warning")
        return redirect(url_for('login'))

    con = get_db()
    cur = con.cursor(dictionary=True)
    try:
        # 2. Ambil informasi komentar untuk verifikasi kepemilikan
        cur.execute("SELECT author_id FROM comments WHERE id = %s", (comment_id,))
        comment = cur.fetchone()

        if not comment:
            flash("Komentar tidak ditemukan.", "danger")
            return redirect(url_for('forum'))

        # 3. Security Check: Hanya penulis komentar atau admin yang bisa menghapus
        if comment['author_id'] == session['user_id'] or session['role'] == 'admin':
            cur.execute("DELETE FROM comments WHERE id = %s", (comment_id,))
            con.commit()
            flash("Komentar berhasil dihapus.", "success")
        else:
            flash("Anda tidak memiliki izin untuk menghapus komentar ini.", "danger")

        return redirect(url_for('forum'))

    except mysql.connector.Error as err:
        con.rollback()
        flash(f"Gagal menghapus komentar: {err.msg}", "danger")
        return redirect(url_for('forum'))
    finally:
        if cur:
            cur.close()


# ==============================================================================
# 10. LIVE CLASS
# ==============================================================================

# Ganti seluruh fungsi live_class yang lama dengan versi baru ini

@app.route('/live_class')
def live_class():
    if 'role' not in session:
        flash('Silakan login terlebih dahulu untuk mengakses halaman ini.', 'warning')
        return redirect(url_for('login'))

    con = None
    try:
        con = get_db()
        cur = con.cursor(dictionary=True)
        role = session['role']
        user_id = session['user_id']

        sort_method = request.args.get('sort', 'class')

        if sort_method == 'time':
            order_clause = "ORDER BY lc.date_time ASC"
        else:
            order_clause = "ORDER BY k.nama_kelas, lc.date_time ASC"

        live_classes_flat = []

        if role == 'dosen':
            cur.execute("SELECT id_dosen FROM dosen WHERE user_id = %s", (user_id,))
            dosen = cur.fetchone()
            if dosen and dosen.get('id_dosen'):
                query = f"""
                    SELECT lc.*, k.nama_kelas, k.kode_matkul
                    FROM live_class lc JOIN kelas k ON lc.id_kelas = k.id_kelas
                    WHERE k.id_dosen = %s {order_clause}
                """
                cur.execute(query, (dosen['id_dosen'],))
                live_classes_flat = cur.fetchall()

        elif role == 'mahasiswa':
            cur.execute("SELECT NIM FROM mahasiswa WHERE user_id = %s", (user_id,))
            mahasiswa = cur.fetchone()
            if mahasiswa and mahasiswa.get('NIM'):
                query = f"""
                    SELECT lc.*, k.nama_kelas, k.kode_matkul FROM live_class lc
                    JOIN kelas_mahasiswa km ON lc.id_kelas = km.id_kelas
                    JOIN kelas k ON k.id_kelas = lc.id_kelas
                    WHERE km.NIM = %s {order_clause}
                """
                cur.execute(query, (mahasiswa['NIM'],))
                live_classes_flat = cur.fetchall()

        grouped_classes = None
        if sort_method == 'class' and live_classes_flat:
            grouped_classes = OrderedDict()
            for lc in live_classes_flat:
                class_key = (lc['id_kelas'], lc['nama_kelas'], lc.get('kode_matkul', ''))
                if class_key not in grouped_classes:
                    grouped_classes[class_key] = []
                grouped_classes[class_key].append(lc)

        template_name = f"{role}/live_class.html"

        # =================================================================
        # [PERBAIKAN] Sesuaikan waktu server (UTC) ke waktu lokal (WIB)
        # =================================================================
        now_wib = datetime.utcnow() + timedelta(hours=7)

        return render_template(template_name,
                               sort_method=sort_method,
                               grouped_classes=grouped_classes,
                               live_classes_flat=live_classes_flat,
                               now=now_wib,  # Gunakan variabel now_wib yang sudah disesuaikan
                               timedelta=timedelta)

    except Exception as e:
        flash(f'Terjadi kesalahan sistem: {str(e)}', 'danger')
        traceback.print_exc()
        return redirect(url_for('dashboard'))
    finally:
        if con and con.is_connected():
            con.close()

@app.route('/create_live_class', methods=['GET', 'POST'])
def create_live_class():
    if session.get('role') != 'dosen':
        return redirect(url_for('login'))

    con = get_db()
    cur = con.cursor(dictionary=True)
    try:
        cur.execute("SELECT id_dosen FROM dosen WHERE user_id = %s", (session['user_id'],))
        dosen = cur.fetchone()
        if not dosen:
            flash('Data dosen tidak ditemukan.', 'error')
            return redirect(url_for('dashboard'))

        if request.method == 'POST':
            id_kelas = request.form.get('id_kelas')
            title = request.form.get('title')
            date_time = request.form.get('date_time')
            duration = request.form.get('duration')
            link = request.form.get('link')
            description = request.form.get('description')

            if not all([id_kelas, title, date_time, duration, link]):
                flash("Semua field kecuali deskripsi wajib diisi.", "danger")
            else:
                cur.execute("""
                    INSERT INTO live_class (id_kelas, title, date_time, duration, description, link, id_dosen)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (id_kelas, title, date_time, duration, description, link, dosen['id_dosen']))
                con.commit()
                flash('Live Class berhasil dijadwalkan!', 'success')
                return redirect(url_for('live_class'))

        # Untuk GET atau jika POST gagal validasi
        cur.execute("SELECT id_kelas, nama_kelas FROM kelas WHERE id_dosen = %s", (dosen['id_dosen'],))
        kelas_list = cur.fetchall()
        return render_template('dosen/create_live_class.html', kelas_list=kelas_list)

    except Exception as e:
        if con.is_connected(): con.rollback()
        flash(f'Terjadi kesalahan: {str(e)}', 'error')
        return redirect(url_for('dashboard'))
    finally:
        cur.close()


@app.route('/edit_live_class/<int:id>', methods=['GET', 'POST'])
def edit_live_class(id):
    if session.get('role') != 'dosen':
        return redirect(url_for('login'))

    con = get_db()
    cur = con.cursor(dictionary=True)

    try:
        cur.execute("SELECT id_dosen FROM dosen WHERE user_id = %s", (session['user_id'],))
        dosen = cur.fetchone()
        if not dosen:
            flash('Data dosen tidak ditemukan.', 'error')
            return redirect(url_for('dashboard'))

        # Ambil live class dan verifikasi kepemilikan
        cur.execute("""
            SELECT lc.* FROM live_class lc JOIN kelas k ON lc.id_kelas = k.id_kelas
            WHERE lc.id = %s AND k.id_dosen = %s
        """, (id, dosen['id_dosen']))
        lc = cur.fetchone()

        if not lc:
            flash('Jadwal tidak ditemukan atau Anda tidak berhak mengeditnya.', 'error')
            return redirect(url_for('live_class'))

        if request.method == 'POST':
            # Proses update
            id_kelas = request.form.get('id_kelas')
            title = request.form.get('title')
            date_time = request.form.get('date_time')
            duration = request.form.get('duration')
            link = request.form.get('link')
            description = request.form.get('description')

            cur.execute("""
                UPDATE live_class SET id_kelas=%s, title=%s, date_time=%s, duration=%s, link=%s, description=%s
                WHERE id = %s
            """, (id_kelas, title, date_time, duration, link, description, id))
            con.commit()
            flash('Jadwal live class berhasil diperbarui!', 'success')
            return redirect(url_for('live_class'))

        # Untuk method GET
        if isinstance(lc.get('date_time'), datetime):
            lc['datetime_for_input'] = lc['date_time'].strftime('%Y-%m-%dT%H:%M')

        cur.execute("SELECT id_kelas, nama_kelas FROM kelas WHERE id_dosen = %s", (dosen['id_dosen'],))
        kelas_list = cur.fetchall()
        return render_template('dosen/edit_live_class.html', lc=lc, kelas_list=kelas_list)

    except Exception as e:
        if con.is_connected(): con.rollback()
        flash(f"Terjadi kesalahan: {e}", "error")
        return redirect(url_for('live_class'))
    finally:
        cur.close()


@app.route('/delete_live_class/<int:id>', methods=['POST'])
def delete_live_class(id):
    if session.get('role') != 'dosen':
        return redirect(url_for('login'))

    con = get_db()
    cur = con.cursor()
    try:
        # Tambahkan verifikasi kepemilikan sebelum menghapus
        # (Logika mirip seperti di edit_live_class)
        cur.execute("DELETE FROM live_class WHERE id = %s", (id,))
        con.commit()
        flash('Jadwal live class berhasil dihapus.', 'success')
    except mysql.connector.Error as err:
        con.rollback()
        flash(f"Gagal menghapus jadwal: {err.msg}", "danger")
    finally:
        cur.close()

    return redirect(url_for('live_class'))



# ============================================================
# TAMBAHKAN FUNGSI BARU INI KE flask_app.py ANDA
# ============================================================
@app.route('/admin/create_class', methods=['GET', 'POST'])
@admin_required
def create_class():
    """Halaman untuk admin membuat kelas baru dan menugaskan dosen."""
    con = get_db()
    cur = con.cursor(dictionary=True)

    try:
        if request.method == 'POST':
            nama_kelas = request.form.get('nama_kelas')
            kode_matkul = request.form.get('kode_matkul')
            id_dosen = request.form.get('id_dosen')

            if not all([nama_kelas, kode_matkul, id_dosen]):
                flash('Semua field wajib diisi.', 'danger')
            else:
                cur.execute(
                    "INSERT INTO kelas (nama_kelas, kode_matkul, id_dosen) VALUES (%s, %s, %s)",
                    (nama_kelas, kode_matkul, id_dosen)
                )
                con.commit()
                flash('Kelas baru berhasil dibuat!', 'success')
                return redirect(url_for('dashboard'))

        # Untuk method GET, ambil daftar semua dosen untuk ditampilkan di form
        cur.execute("SELECT id_dosen, nama FROM dosen ORDER BY nama")
        dosen_list = cur.fetchall()

        return render_template('admin/create_class.html', dosen_list=dosen_list)

    except Exception as e:
        flash(f"Terjadi error: {e}", "danger")
        traceback.print_exc()
        return redirect(url_for('dashboard'))
    finally:
        if cur:
            cur.close()

@app.route('/admin/users')
@admin_required
def manage_users():
    """Halaman untuk admin melihat semua pengguna."""
    con = get_db()
    cur = con.cursor(dictionary=True)
    # Query untuk mengambil semua user dan join dengan profil dosen/mahasiswa
    cur.execute("""
        SELECT
            u.id, u.username, u.role,
            m.nama as nama_mahasiswa, m.NIM,
            d.nama as nama_dosen, d.nip
        FROM users u
        LEFT JOIN mahasiswa m ON u.id = m.user_id
        LEFT JOIN dosen d ON u.id = d.user_id
        ORDER BY u.id
    """)
    users = cur.fetchall()
    cur.close()
    return render_template('admin/manage_users.html', users=users)

@app.route('/admin/enrollment/<int:kelas_id>', methods=['GET', 'POST'])
@admin_required
def manage_class_enrollment(kelas_id):
    """Halaman untuk menambah/mengeluarkan mahasiswa dari kelas."""
    con = get_db()
    cur = con.cursor(dictionary=True)

    try:
        if request.method == 'POST':
            mahasiswa_to_enroll = request.form.getlist('mahasiswa_to_enroll')

            # Hapus semua pendaftaran lama untuk kelas ini agar mudah
            cur.execute("DELETE FROM kelas_mahasiswa WHERE id_kelas = %s", (kelas_id,))

            # Daftarkan semua mahasiswa yang dipilih (yang memiliki NIM)
            if mahasiswa_to_enroll:
                # Pastikan hanya NIM yang valid yang dimasukkan
                placeholders = ', '.join(['%s'] * len(mahasiswa_to_enroll))
                query = f"INSERT INTO kelas_mahasiswa (id_kelas, NIM) SELECT %s, NIM FROM mahasiswa WHERE NIM IN ({placeholders})"

                # Buat tuple parameter
                params = [kelas_id]
                params.extend(mahasiswa_to_enroll)

                cur.execute(query, tuple(params))

            con.commit()
            flash('Daftar peserta kelas berhasil diperbarui!', 'success')
            return redirect(url_for('dashboard'))

        # --- BAGIAN GET DENGAN QUERY BARU ---
        # 1. Dapatkan info kelas
        cur.execute("SELECT * FROM kelas WHERE id_kelas = %s", (kelas_id,))
        kelas = cur.fetchone()

        # 2. Dapatkan daftar semua mahasiswa dari tabel USERS dan gabungkan dengan profil
        cur.execute("""
            SELECT
                u.username,
                m.NIM,
                m.nama
            FROM users u
            LEFT JOIN mahasiswa m ON u.id = m.user_id
            WHERE u.role = 'mahasiswa'
            ORDER BY m.nama, u.username
        """)
        all_mahasiswa = cur.fetchall()

        # 3. Dapatkan daftar NIM mahasiswa yang sudah terdaftar di kelas ini
        cur.execute("SELECT NIM FROM kelas_mahasiswa WHERE id_kelas = %s", (kelas_id,))
        enrolled_nims = {row['NIM'] for row in cur.fetchall()}

        return render_template(
            'admin/manage_enrollment.html',
            kelas=kelas,
            all_mahasiswa=all_mahasiswa,
            enrolled_nims=enrolled_nims
        )
    except Exception as e:
        flash(f"Terjadi error: {e}", "danger")
        traceback.print_exc()
        return redirect(url_for('dashboard'))
    finally:
        if cur:
            cur.close()


# ==============================================================================
# GANTI KEDUA FUNGSI EDIT DI BAWAH INI DENGAN VERSI YANG SUDAH DIPERBAIKI
# ==============================================================================

# GANTI FUNGSI LAMA ANDA DENGAN VERSI BARU INI

@app.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user_by_admin(user_id):
    """
    Halaman untuk admin mengedit detail mahasiswa dan mereset password.
    NIM hanya bisa dilihat (readonly).
    """
    con = get_db()
    cur = con.cursor(dictionary=True)

    try:
        # Ambil data user yang akan diedit
        cur.execute("""
            SELECT u.id, u.username, u.role, m.* FROM users u
            LEFT JOIN mahasiswa m ON u.id = m.user_id
            WHERE u.id = %s AND u.role = 'mahasiswa'
        """, (user_id,))
        user_data = cur.fetchone()

        if not user_data:
            flash('User mahasiswa tidak ditemukan.', 'danger')
            return redirect(url_for('manage_users'))

        if request.method == 'POST':
            # Ambil data dari form yang diisi admin
            nama = request.form.get('nama')
            email = request.form.get('email')
            jurusan = request.form.get('jurusan')
            new_password = request.form.get('new_password')

            # Update data profil di tabel mahasiswa
            cur.execute(
                "UPDATE mahasiswa SET nama=%s, email=%s, jurusan=%s WHERE user_id=%s",
                (nama, email, jurusan, user_id)
            )

            # Jika admin mengisi password baru, reset password di tabel users
            if new_password:
                hashed_password = generate_password_hash(new_password)
                cur.execute("UPDATE users SET password=%s WHERE id=%s", (hashed_password, user_id))

            con.commit()
            flash(f'Data untuk user {user_data["username"]} berhasil diperbarui!', 'success')
            return redirect(url_for('manage_users'))

        # Untuk method GET, tampilkan form dengan data yang ada
        return render_template('admin/edit_user.html', user_data=user_data)

    except Exception as e:
        if con.is_connected(): con.rollback()
        flash(f"Terjadi error: {e}", "danger")
        traceback.print_exc()
        return redirect(url_for('manage_users'))
    finally:
        if cur: cur.close()


# GANTI FUNGSI LAMA ANDA DENGAN VERSI BARU INI

@app.route('/admin/edit_lecturer/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_lecturer_by_admin(user_id):
    """
    Halaman untuk admin mengedit detail dosen dan mereset password.
    NIP hanya bisa dilihat (readonly).
    """
    con = get_db()
    cur = con.cursor(dictionary=True)

    try:
        # Ambil data user yang akan diedit
        cur.execute("""
            SELECT u.id, u.username, u.role, d.* FROM users u
            LEFT JOIN dosen d ON u.id = d.user_id
            WHERE u.id = %s AND u.role = 'dosen'
        """, (user_id,))
        user_data = cur.fetchone()

        if not user_data:
            flash('User dosen tidak ditemukan.', 'danger')
            return redirect(url_for('manage_users'))

        if request.method == 'POST':
            nama = request.form.get('nama')
            email = request.form.get('email')
            departemen = request.form.get('departemen')
            new_password = request.form.get('new_password')

            cur.execute(
                "UPDATE dosen SET nama=%s, email=%s, departemen=%s WHERE user_id=%s",
                (nama, email, departemen, user_id)
            )

            if new_password:
                hashed_password = generate_password_hash(new_password)
                cur.execute("UPDATE users SET password=%s WHERE id=%s", (hashed_password, user_id))

            con.commit()
            flash(f'Data untuk user {user_data["username"]} berhasil diperbarui!', 'success')
            return redirect(url_for('manage_users'))

        return render_template('admin/edit_lecturer.html', user_data=user_data)

    except Exception as e:
        if con.is_connected(): con.rollback()
        flash(f"Terjadi error: {e}", "danger")
        traceback.print_exc()
        return redirect(url_for('manage_users'))
    finally:
        if cur: cur.close()

# ==============================================================================
# JALANKAN SERVER FLASK
# ==============================================================================
if __name__ == '__main__':
    app.run(debug=True)






