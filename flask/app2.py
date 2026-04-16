from flask import Flask, render_template, request, redirect, url_for, session, g, flash, jsonify
import mysql.connector
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
import os
import time
from werkzeug.utils import secure_filename
from datetime import datetime
import traceback

app = Flask(__name__)
app.secret_key = 'secretkey'

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max 16MB

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="elearning"
        )
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Custom filter untuk format datetime
@app.template_filter('format_datetime')
def format_datetime(value):
    if value is None:
        return ''
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        except:
            return value
    return value.strftime('%d %B %Y, %H:%M')


# --- Rute Autentikasi & User ---

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        con = get_db()
        cur = con.cursor()
        cur.execute("SELECT id, password, role FROM users WHERE username=%s", (username,))
        user = cur.fetchone()
        con.close()

        if user and user[1] == password:
            session['user_id'] = user[0]
            session['username'] = username
            session['role'] = user[2]
            return redirect(url_for('dashboard'))
        else:
            error = "Login gagal. Cek username atau password."

    return render_template('login.html', error=error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    success = None
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form['role']
        
        if not all([username, password, confirm_password, role]):
            error = "Semua field harus diisi"
        elif password != confirm_password:
            error = "Password dan konfirmasi password tidak cocok"
        elif len(password) < 6:
            error = "Password minimal 6 karakter"
        elif role not in ['mahasiswa', 'dosen']:
            error = "Role tidak valid"
        else:
            try:
                con = get_db()
                cur = con.cursor()
                
                cur.execute("SELECT id FROM users WHERE username = %s", (username,))
                if cur.fetchone():
                    error = "Username sudah digunakan"
                else:
                    cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
                    user_id = cur.lastrowid
                    
                    if role == 'dosen':
                        cur.execute("INSERT INTO dosen (user_id, nama) VALUES (%s, %s)", (user_id, username))
                    
                    con.commit()
                    success = "Akun berhasil dibuat! Silakan login."
                con.close()
            except Exception as e:
                error = f"Terjadi kesalahan: {str(e)}"
    
    return render_template('signup.html', error=error, success=success)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- Rute Dashboard & Profil ---

@app.route('/dashboard')
def dashboard():
    if 'role' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    role = session['role']
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if role == 'dosen':
        cursor.execute("SELECT * FROM dosen WHERE user_id = %s", (user_id,))
        dosen_info = cursor.fetchone()
        if dosen_info:
            cursor.execute("SELECT * FROM kelas WHERE id_dosen = %s", (dosen_info['id_dosen'],))
            kelas_list = cursor.fetchall()
        else:
            kelas_list = []
        conn.close()
        return render_template('/dosen/dashboard_dosen.html', dosen_info=dosen_info, kelas_list=kelas_list)

    elif role == 'mahasiswa':
        cursor.execute("SELECT * FROM mahasiswa WHERE user_id = %s", (user_id,))
        mahasiswa_info = cursor.fetchone()
        kelas_list = []
        if mahasiswa_info:
            cursor.execute("""
                SELECT k.*, d.nama as nama_dosen FROM kelas k
                JOIN dosen d ON k.id_dosen = d.id_dosen
                JOIN kelas_mahasiswa km ON k.id_kelas = km.id_kelas
                WHERE km.NIM = %s ORDER BY k.nama_kelas
            """, (mahasiswa_info['NIM'],))
            kelas_list = cursor.fetchall()
        conn.close()
        return render_template('/mahasiswa/dashboard_mahasiswa.html', mahasiswa_info=mahasiswa_info, kelas_list=kelas_list)

    return redirect(url_for('login'))

@app.route('/update_mahasiswa_profile', methods=['POST'])
def update_mahasiswa_profile():
    if session.get('role') != 'mahasiswa':
        return redirect(url_for('login'))
    
    user_id, nama, nim, email, jurusan = session['user_id'], request.form['nama'], request.form['nim'], request.form['email'], request.form['jurusan']
    angkatan, no_hp, alamat = request.form.get('angkatan'), request.form.get('no_hp'), request.form.get('alamat')
    
    if not all([nama, nim, email, jurusan]):
        flash('Data wajib harus diisi', 'error')
        return redirect(url_for('dashboard'))
    
    try:
        conn, cursor = get_db(), get_db().cursor(dictionary=True)
        cursor.execute("SELECT * FROM mahasiswa WHERE user_id = %s", (user_id,))
        existing_data = cursor.fetchone()
        
        query_check_nim = "SELECT * FROM mahasiswa WHERE NIM = %s AND user_id != %s" if existing_data else "SELECT * FROM mahasiswa WHERE NIM = %s"
        params_check_nim = (nim, user_id) if existing_data else (nim,)
        cursor.execute(query_check_nim, params_check_nim)
        
        if cursor.fetchone():
            flash('NIM sudah digunakan oleh mahasiswa lain', 'error')
            return redirect(url_for('dashboard'))
        
        if existing_data:
            cursor.execute("UPDATE mahasiswa SET nama=%s, NIM=%s, email=%s, jurusan=%s, angkatan=%s, no_hp=%s, alamat=%s WHERE user_id=%s",
                           (nama, nim, email, jurusan, angkatan, no_hp, alamat, user_id))
            flash('Data berhasil diperbarui!', 'success')
        else:
            cursor.execute("INSERT INTO mahasiswa (user_id, nama, NIM, email, jurusan, angkatan, no_hp, alamat) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                           (user_id, nama, nim, email, jurusan, angkatan, no_hp, alamat))
            flash('Data berhasil disimpan!', 'success')
        
        conn.commit()
    except Exception as e:
        flash(f'Terjadi kesalahan: {str(e)}', 'error')
    finally:
        if conn.is_connected(): conn.close()
    return redirect(url_for('dashboard'))

# --- Rute Materi ---

@app.route('/materi')
def materi():
    if 'username' not in session:
        return redirect(url_for('login'))

    role = session['role']
    user_id = session['user_id']

    conn = pymysql.connect(host='localhost', user='root', password='', db='elearning')
    c = conn.cursor(pymysql.cursors.DictCursor)

    if role == 'mahasiswa':
        # Ambil NIM dari mahasiswa
        c.execute("SELECT NIM FROM mahasiswa WHERE user_id = %s", (user_id,))
        result = c.fetchone()
        if not result:
            conn.close()
            return "Data mahasiswa tidak ditemukan", 404

        nim = result['NIM']

        # Ambil kelas yang diambil mahasiswa
        c.execute("""
            SELECT k.id_kelas, k.nama_kelas, k.kode_matkul, d.nama AS nama_dosen, k.tahun_ajaran
            FROM kelas k
            JOIN kelas_mahasiswa km ON k.id_kelas = km.id_kelas
            JOIN dosen d ON k.id_dosen = d.id_dosen
            WHERE km.NIM = %s
        """, (nim,))
        kelas_list = c.fetchall()

        # Tambahkan materi_list untuk setiap kelas
        for kelas in kelas_list:
            c.execute("""
                SELECT id, title, content, file_name, created_at
                FROM materi
                WHERE id_kelas = %s
                ORDER BY created_at DESC
            """, (kelas['id_kelas'],))
            materi_list = c.fetchall()
            kelas['materi_list'] = materi_list

        conn.close()
        return render_template('/mahasiswa/materi_m.html', username=session['username'], kelas_list=kelas_list)

    elif role == 'dosen':
        # Ambil id_dosen berdasarkan user_id
        c.execute("SELECT id_dosen FROM dosen WHERE user_id = %s", (user_id,))
        result = c.fetchone()
        if not result:
            conn.close()
            return "Data dosen tidak ditemukan", 404

        id_dosen = result['id_dosen']

        # Ambil kelas yang diampu dosen
        c.execute("""
            SELECT id_kelas, nama_kelas, kode_matkul
            FROM kelas
            WHERE id_dosen = %s
        """, (id_dosen,))
        kelas_list = c.fetchall()

        # Tambahkan materi_list untuk setiap kelas
        for kelas in kelas_list:
            c.execute("""
                SELECT id, title AS judul, content AS deskripsi, file_name
                FROM materi
                WHERE id_kelas = %s AND uploaded_by = %s
            """, (kelas['id_kelas'], user_id))
            materi_list = c.fetchall()
            kelas['materi_list'] = materi_list

        conn.close()
        return render_template('/dosen/materi_d.html', username=session['username'], kelas_list=kelas_list)

    else:
        conn.close()
        return "Role tidak dikenali", 403

@app.route('/upload_materi', methods=['GET', 'POST'])
def upload_materi():
    if session.get('role') != 'dosen':
        return redirect(url_for('login'))

    con = get_db()
    cur = con.cursor()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        id_kelas = request.form.get('id_kelas') or None  # bisa kosong/null
        file = request.files.get('file')

        filename = None
        if file and file.filename != '':  # hanya jika file diisi
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
            else:
                con.close()
                return "Format file tidak didukung!"

        cur.execute("""
            INSERT INTO materi (title, content, file_name, uploaded_by, id_kelas)
            VALUES (%s, %s, %s, %s, %s)
        """, (title, content, filename, session['user_id'], id_kelas))
        con.commit()
        con.close()
        return redirect(url_for('materi'))

    # Ambil daftar kelas untuk dropdown
    cur.execute("SELECT id_kelas, nama_kelas, kode_matkul FROM kelas")
    rows = cur.fetchall()
    con.close()

    kelas_list = [
        {'id_kelas': row[0], 'nama_kelas': row[1], 'kode_matkul': row[2]}
        for row in rows
    ]

    return render_template('/dosen/upload_materi.html', kelas_list=kelas_list)

@app.route('/edit_materi/<int:materi_id>', methods=['GET', 'POST'])
def edit_materi(materi_id):
    # Cari materi berdasarkan materi_id di database menggunakan dict cursor
    con = get_db()
    cur = con.cursor()
    
    # Menggunakan dictionary cursor untuk akses by column name
    cur.execute("SELECT id, title, content, uploaded_by, file_name, id_kelas, created_at, updated_at FROM materi WHERE id = %s", (materi_id,))
    result = cur.fetchone()

    if result is None:
        con.close()
        return "Materi tidak ditemukan", 404
    
    # Convert tuple to dict untuk akses yang lebih mudah
    materi = {
        'id': result[0],
        'title': result[1],
        'content': result[2], 
        'uploaded_by': result[3],
        'file_name': result[4],
        'id_kelas': result[5],
        'created_at': result[6],
        'updated_at': result[7]
    }

    if request.method == 'POST':
        try:
            # Debug info
            print("Form data:", request.form)
            print("Files:", request.files)
            print("Current materi:", materi)
            
            # Ambil data dari form
            title = request.form.get('title', '').strip()
            content = request.form.get('content', '').strip()
            
            # Validasi input
            if not title:
                return "Title tidak boleh kosong", 400
            if not content:
                return "Content tidak boleh kosong", 400
            
            # Ambil filename lama
            current_filename = materi['file_name'] if materi['file_name'] and materi['file_name'] != 'NULL' else None
            new_filename = current_filename
            
            print(f"Current filename: {current_filename}")
            
            # Handle file upload
            if 'file' in request.files:
                file = request.files['file']
                print(f"File uploaded: {file.filename}")
                
                if file and file.filename != '':
                    # Hapus file lama jika ada
                    if current_filename:
                        upload_folder = app.config.get('UPLOAD_FOLDER', 'uploads')
                        old_file_path = os.path.join(upload_folder, str(current_filename))
                        if os.path.exists(old_file_path):
                            try:
                                os.remove(old_file_path)
                                print(f"Deleted old file: {old_file_path}")
                            except OSError as e:
                                print(f"Error deleting old file: {e}")
                    
                    # Simpan file baru
                    filename = secure_filename(file.filename)
                    timestamp = str(int(time.time()))
                    name, ext = os.path.splitext(filename)
                    new_filename = f"{name}_{timestamp}{ext}"
                    
                    # Pastikan folder upload ada
                    upload_folder = app.config.get('UPLOAD_FOLDER', 'uploads')
                    if not os.path.exists(upload_folder):
                        os.makedirs(upload_folder)
                    
                    file_path = os.path.join(upload_folder, new_filename)
                    file.save(file_path)
                    print(f"Saved new file: {file_path}")
            
            # Update data materi
            cur.execute("""
                UPDATE materi 
                SET title = %s, content = %s, file_name = %s, updated_at = NOW()
                WHERE id = %s
            """, (title, content, new_filename, materi_id))
            
            if cur.rowcount == 0:
                return "Tidak ada data yang diupdate", 400
                
            con.commit()
            con.close()
            
            print("Update successful")
            return redirect(url_for('materi'))
            
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            
            try:
                con.rollback()
                con.close()
            except:
                pass
            return f"Error updating materi: {str(e)}", 500

    con.close()
    return render_template('dosen/edit_materi.html', materi=materi, materi_id=materi_id)

@app.route('/delete_materi/<int:materi_id>', methods=['POST'])
def delete_materi(materi_id):
    # Hapus materi berdasarkan materi_id
    con = get_db()
    cur = con.cursor()
    cur.execute("DELETE FROM materi WHERE id = %s", (materi_id,))
    con.commit()
    con.close()

    # Redirect ke halaman materi setelah dihapus
    return redirect(url_for('materi'))

# --- Rute Live Class ---

@app.route('/live_class')
def live_class():
    if 'role' not in session:
        flash('Silakan login terlebih dahulu', 'error')
        return redirect(url_for('login'))

    try:
        con = get_db()
        cur = con.cursor(dictionary=True)

        role = session['role']
        user_id = session['user_id']

        if role == 'mahasiswa':
            cur.execute("SELECT NIM FROM mahasiswa WHERE user_id = %s", (user_id,))
            mhs = cur.fetchone()
            if not mhs:
                con.close()
                flash('Data mahasiswa tidak ditemukan', 'error')
                return redirect(url_for('dashboard'))

            cur.execute("""
                SELECT lc.*, k.nama_kelas, k.kode_matkul
                FROM live_class lc
                JOIN kelas_mahasiswa km ON lc.id_kelas = km.id_kelas
                JOIN kelas k ON k.id_kelas = lc.id_kelas
                WHERE km.NIM = %s
                ORDER BY lc.date_time DESC
            """, (mhs['NIM'],))
            live_classes = cur.fetchall()

            # Ubah date_time menjadi datetime object
            for lc in live_classes:
                if isinstance(lc['date_time'], str):
                    try:
                        lc['date_time'] = datetime.strptime(lc['date_time'], '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        pass

            con.close()
            return render_template('mahasiswa/live_class.html', live_classes=live_classes)

        elif role == 'dosen':
            cur.execute("SELECT id_dosen FROM dosen WHERE user_id = %s", (user_id,))
            dosen = cur.fetchone()
            if not dosen:
                con.close()
                flash('Data dosen tidak ditemukan', 'error')
                return redirect(url_for('dashboard'))

            cur.execute("""
                SELECT lc.*, k.nama_kelas, k.kode_matkul
                FROM live_class lc
                JOIN kelas k ON k.id_kelas = lc.id_kelas
                WHERE k.id_dosen = %s
                ORDER BY lc.date_time DESC
            """, (dosen['id_dosen'],))
            live_classes = cur.fetchall()

            # Ubah date_time menjadi datetime object
            for lc in live_classes:
                if isinstance(lc['date_time'], str):
                    try:
                        lc['date_time'] = datetime.strptime(lc['date_time'], '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        pass

            con.close()
            return render_template('dosen/live_class.html', live_classes=live_classes)

    except Exception as e:
        print(f"Exception in create_live_class: {str(e)}")
        flash(f'Terjadi kesalahan: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

    flash('Role tidak valid', 'error')
    return redirect(url_for('login'))

@app.route('/create_live_class', methods=['GET', 'POST'])
def create_live_class():
    if session.get('role') != 'dosen':
        flash('Hanya dosen yang dapat membuat live class', 'error')
        return redirect(url_for('login'))

    con = None
    dosen_info_for_template = None
    kelas_list_for_template = []

    try:
        con = get_db()
        cur = con.cursor(dictionary=True)
        user_id = session['user_id']

        # Ambil data dosen
        dosen_queries = [
            "SELECT id_dosen, nama FROM dosen WHERE user_id = %s",
            "SELECT id as id_dosen, nama FROM dosen WHERE user_id = %s",
            "SELECT id_dosen, nama FROM dosen WHERE id = %s",
            "SELECT id as id_dosen, nama FROM dosen WHERE id = %s",
            "SELECT id_dosen, nama FROM dosen WHERE id_dosen = %s"
        ]
        dosen_db_data = None
        for query in dosen_queries:
            try:
                cur.execute(query, (user_id,))
                result = cur.fetchone()
                if result and (result.get('id_dosen') or result.get('id')):
                    dosen_db_data = {
                        'id_dosen': result.get('id_dosen') or result.get('id'),
                        'nama': result.get('nama')
                    }
                    dosen_info_for_template = dosen_db_data
                    break
            except Exception as e:
                print(f"Error executing dosen query {query}: {e}")
                continue

        if not dosen_db_data:
            flash('Data dosen tidak ditemukan. Silakan hubungi admin.', 'warning')
            return render_template('dosen/create_live_class.html', kelas_list=[], dosen_info=None, form_data=request.form if request.method == 'POST' else {})

        # Ambil daftar kelas dosen
        kelas_queries = [
            "SELECT id_kelas, nama_kelas, kode_matkul FROM kelas WHERE id_dosen = %s ORDER BY nama_kelas",
            "SELECT id as id_kelas, nama_kelas, kode_matkul FROM kelas WHERE id_dosen = %s ORDER BY nama_kelas",
        ]
        fetched_kelas_list = []
        for query in kelas_queries:
            try:
                cur.execute(query, (dosen_db_data['id_dosen'],))
                result = cur.fetchall()
                if result:
                    for k_item in result:
                        fetched_kelas_list.append({
                            'id_kelas': k_item.get('id_kelas') or k_item.get('id'),
                            'nama_kelas': k_item.get('nama_kelas'),
                            'kode_matkul': k_item.get('kode_matkul')
                        })
                    kelas_list_for_template = fetched_kelas_list
                    break
            except Exception as e:
                print(f"Error executing kelas query {query}: {e}")
                continue

        if not fetched_kelas_list and request.method == 'GET':
            flash('Anda belum memiliki kelas. Silakan hubungi admin.', 'info')

        # Handle POST
        if request.method == 'POST':
            form_data = request.form

            title = form_data.get('title', '').strip()
            date_time_str = form_data.get('date_time', '').strip()
            description = form_data.get('description', '').strip()
            duration_str = form_data.get('duration', '').strip()
            link = form_data.get('link', '').strip()
            id_kelas_str = form_data.get('id_kelas', '').strip()
            id_dosen_int = dosen_db_data['id_dosen']

            error_messages = []
            if not title: error_messages.append('Judul Live Class')
            if not date_time_str: error_messages.append('Tanggal dan Waktu')
            if not duration_str: error_messages.append('Durasi')
            if not link: error_messages.append('Link Meeting')
            if not id_kelas_str: error_messages.append('Pilih Kelas')

            if error_messages:
                flash(f'Field berikut wajib diisi: {", ".join(error_messages)}.', 'error')
                return render_template('dosen/create_live_class.html', kelas_list=fetched_kelas_list, dosen_info=dosen_db_data, form_data=form_data)

            try:
                duration_int = int(duration_str)
                id_kelas_int = int(id_kelas_str)

                if not (15 <= duration_int <= 180):
                    flash('Durasi harus antara 15 hingga 180 menit.', 'error')
                    return render_template('dosen/create_live_class.html', kelas_list=fetched_kelas_list, dosen_info=dosen_db_data, form_data=form_data)

                try:
                    parsed_datetime = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M')
                    if parsed_datetime <= datetime.now():
                        flash('Tanggal dan waktu Live Class harus di masa depan.', 'error')
                        return render_template('dosen/create_live_class.html', kelas_list=fetched_kelas_list, dosen_info=dosen_db_data, form_data=form_data)
                    db_formatted_datetime = parsed_datetime.strftime('%Y-%m-%d %H:%M:%S')
                except ValueError:
                    flash('Format tanggal dan waktu tidak valid.', 'error')
                    return render_template('dosen/create_live_class.html', kelas_list=fetched_kelas_list, dosen_info=dosen_db_data, form_data=form_data)

                is_valid_class_owner = any((k.get('id_kelas') or k.get('id')) == id_kelas_int for k in fetched_kelas_list)
                if not is_valid_class_owner:
                    flash('Kelas yang dipilih tidak valid atau bukan milik Anda.', 'error')
                    return render_template('dosen/create_live_class.html', kelas_list=fetched_kelas_list, dosen_info=dosen_db_data, form_data=form_data)

                cur.execute("SELECT id FROM live_class WHERE id_kelas = %s AND date_time = %s", (id_kelas_int, db_formatted_datetime))
                if cur.fetchone():
                    flash('Sudah ada Live Class yang dijadwalkan untuk kelas dan waktu yang sama.', 'error')
                    return render_template('dosen/create_live_class.html', kelas_list=fetched_kelas_list, dosen_info=dosen_db_data, form_data=form_data)

                description_to_insert = description if description else None

                cur.execute("""
                    INSERT INTO live_class (id_kelas, title, date_time, duration, description, link, id_dosen)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (id_kelas_int, title, db_formatted_datetime, duration_int, description_to_insert, link, id_dosen_int))

                con.commit()
                print(f"Successfully inserted live class. Last Inserted ID: {cur.lastrowid}")
                flash('Live Class berhasil dijadwalkan!', 'success')
                return redirect(url_for('live_class'))

            except ValueError as ve:
                traceback.print_exc()
                flash('Terjadi kesalahan pada input data (pastikan durasi dan ID kelas berupa angka).', 'error')
                return render_template('dosen/create_live_class.html', kelas_list=fetched_kelas_list, dosen_info=dosen_db_data, form_data=form_data)

            except mysql.connector.Error as db_err:
                if con: con.rollback()
                traceback.print_exc()
                flash(f'Database error saat menyimpan Live Class: {db_err.msg}', 'error')
                return render_template('dosen/create_live_class.html', kelas_list=fetched_kelas_list, dosen_info=dosen_db_data, form_data=form_data)

            except Exception as e:
                if con: con.rollback()
                traceback.print_exc()
                flash(f'Terjadi kesalahan sistem yang tidak terduga: {str(e)}', 'error')
                return render_template('dosen/create_live_class.html', kelas_list=fetched_kelas_list, dosen_info=dosen_db_data, form_data=form_data)

        # Render GET
        return render_template('dosen/create_live_class.html', kelas_list=kelas_list_for_template, dosen_info=dosen_info_for_template, form_data=request.form if request.method == 'POST' else {})

    except Exception as e:
        traceback.print_exc()
        flash(f'Terjadi kesalahan sistem: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/edit_live_class/<int:id>', methods=['GET', 'POST'])
def edit_live_class(id):
    if session.get('role') != 'dosen':
        flash('Hanya dosen yang dapat mengedit live class', 'error')
        return redirect(url_for('login'))

    try:
        con = get_db()
        cur = con.cursor(dictionary=True)

        # Ambil data dosen berdasarkan user login
        cur.execute("SELECT id_dosen FROM dosen WHERE user_id = %s", (session['user_id'],))
        dosen = cur.fetchone()

        if not dosen:
            flash('Data dosen tidak ditemukan', 'error')
            return redirect(url_for('dashboard'))

        # Debug: tampilkan id dosen dan id live class
        print(f"[DEBUG] Dosen ID: {dosen['id_dosen']}, Live Class ID: {id}")

        # Cek apakah live class milik dosen
        cur.execute("""
            SELECT lc.*, k.id_dosen 
            FROM live_class lc
            JOIN kelas k ON lc.id_kelas = k.id_kelas
            WHERE lc.id = %s
        """, (id,))
        lc = cur.fetchone()

        if not lc:
            flash('Live class tidak ditemukan', 'error')
            return redirect(url_for('live_class'))

        if lc['id_dosen'] != dosen['id_dosen']:
            flash('Anda tidak berhak mengedit live class ini', 'error')
            return redirect(url_for('live_class'))

        # Ambil semua kelas milik dosen
        cur.execute("SELECT id_kelas, nama_kelas FROM kelas WHERE id_dosen = %s", (dosen['id_dosen'],))
        kelas_list = cur.fetchall()

        if request.method == 'POST':
            title = request.form.get('title', '').strip()
            date_time_str = request.form.get('date_time', '').strip()
            duration_str = request.form.get('duration', '').strip()
            link = request.form.get('link', '').strip()
            description = request.form.get('description', '').strip()
            id_kelas_str = request.form.get('id_kelas', '').strip()

            if not all([title, date_time_str, duration_str, link, id_kelas_str]):
                flash('Semua field wajib harus diisi', 'error')
                return render_template('dosen/edit_live_class.html', lc=lc, kelas_list=kelas_list)

            try:
                duration = int(duration_str)
                id_kelas = int(id_kelas_str)

                if duration < 15 or duration > 180:
                    flash('Durasi harus antara 15 hingga 180 menit', 'error')
                    raise ValueError('Durasi tidak valid')

                try:
                    parsed_datetime = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M')
                    if parsed_datetime <= datetime.now():
                        flash('Tanggal dan waktu harus di masa depan', 'error')
                        raise ValueError('Waktu tidak valid')
                    formatted_datetime = parsed_datetime.strftime('%Y-%m-%d %H:%M:%S')
                except ValueError:
                    flash('Format tanggal dan waktu tidak valid', 'error')
                    raise

                # Validasi kelas milik dosen
                cur.execute("SELECT id_kelas FROM kelas WHERE id_kelas = %s AND id_dosen = %s", 
                            (id_kelas, dosen['id_dosen']))
                if not cur.fetchone():
                    flash('Kelas tidak valid atau bukan milik Anda', 'error')
                    raise ValueError('Kelas tidak valid')

                # Update data live class
                cur.execute("""
                    UPDATE live_class
                    SET title = %s, date_time = %s, duration = %s, link = %s, description = %s, id_kelas = %s
                    WHERE id = %s
                """, (title, formatted_datetime, duration, link, description if description else None, id_kelas, id))

                con.commit()
                flash('Live class berhasil diupdate!', 'success')
            except ValueError:
                flash('Durasi dan Kelas harus berupa angka valid', 'error')
                return render_template('dosen/edit_live_class.html', lc=lc, kelas_list=kelas_list)
            return redirect(url_for('live_class'))

        # Format tanggal untuk input datetime-local
        print(f"[DEBUG] Tipe date_time: {type(lc['date_time'])}, Nilai: {lc['date_time']}")

        if lc.get('date_time'):
            try:
                if isinstance(lc['date_time'], str):
                    dt_obj = datetime.strptime(lc['date_time'], '%Y-%m-%d %H:%M:%S')
                else:
                    dt_obj = lc['date_time']
                lc['date_time'] = dt_obj.strftime('%Y-%m-%dT%H:%M')
            except Exception as e:
                print(f"[ERROR] Parsing datetime: {e}")
                lc['date_time'] = ''


        return render_template('dosen/edit_live_class.html', lc=lc, kelas_list=kelas_list)

    except Exception as e:
        flash(f'Terjadi kesalahan: {str(e)}', 'error')
        return redirect(url_for('live_class'))

@app.route('/delete_live_class/<int:id>', methods=['POST'])
def delete_live_class(id):
    if session.get('role') != 'dosen':
        flash('Hanya dosen yang dapat menghapus live class', 'error')
        return redirect(url_for('login'))

    try:
        con = get_db()
        cur = con.cursor(dictionary=True)

        # Ambil data dosen
        cur.execute("SELECT id_dosen FROM dosen WHERE user_id = %s", (session['user_id'],))
        dosen = cur.fetchone()
        if not dosen:
            con.close()
            flash('Data dosen tidak ditemukan', 'error')
            return redirect(url_for('dashboard'))

        # Pastikan live class milik dosen ini
        cur.execute("""
            SELECT lc.id 
            FROM live_class lc
            JOIN kelas k ON lc.id_kelas = k.id_kelas
            WHERE lc.id = %s AND k.id_dosen = %s
        """, (id, dosen['id_dosen']))
        
        if not cur.fetchone():
            con.close()
            flash('Live class tidak ditemukan atau bukan milik Anda', 'error')
            return redirect(url_for('live_class'))

        # Hapus live class
        cur.execute("DELETE FROM live_class WHERE id = %s", (id,))
        con.commit()
        con.close()
        flash('Live class berhasil dihapus!', 'success')

    except Exception as e:
        flash(f'Terjadi kesalahan saat menghapus: {str(e)}', 'error')

    return redirect(url_for('live_class'))

# --- Rute Forum ---

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if 'role' not in session:
        return redirect(url_for('login'))

    con = get_db()
    cur = con.cursor()

    # Ambil postingan yang sudah ada
    cur.execute("SELECT p.id, p.content, p.author_id, p.role, p.created_at, u.username FROM posts p JOIN users u ON p.author_id = u.id ORDER BY p.created_at DESC")
    posts = cur.fetchall()

    # Ambil komentar untuk setiap postingan
    posts_with_comments = []
    for post in posts:
        cur.execute("SELECT c.id, c.content, c.author_id, c.created_at, u.username FROM comments c JOIN users u ON c.author_id = u.id WHERE c.post_id = %s ORDER BY c.created_at", (post[0],))
        comments = cur.fetchall()
        posts_with_comments.append({'post': post, 'comments': comments})

    con.close()

    if request.method == 'POST':
        post_content = request.form['content']
        post_role = session['role']
        post_author_id = session['user_id']

        con = get_db()
        cur = con.cursor()
        cur.execute("INSERT INTO posts (content, role, author_id) VALUES (%s, %s, %s)", (post_content, post_role, post_author_id))
        con.commit()
        con.close()

        return redirect(url_for('forum'))

    return render_template('forum.html', posts=posts_with_comments)

@app.route('/comment/<int:post_id>', methods=['POST'])
def comment(post_id):
    if 'role' not in session:
        return redirect(url_for('login'))

    comment_content = request.form['content']
    comment_author_id = session['user_id']

    con = get_db()
    cur = con.cursor()
    cur.execute("INSERT INTO comments (content, post_id, author_id) VALUES (%s, %s, %s)", 
                (comment_content, post_id, comment_author_id))
    con.commit()
    con.close()

    return redirect(url_for('forum'))

# --- Rute Kuis (Manajemen & Tampilan Daftar) ---

@app.route('/kuis')
def kuis():
    if 'role' not in session:
        return redirect(url_for('login'))
    
    role, user_id = session['role'], session['user_id']
    con, cur = get_db(), get_db().cursor(dictionary=True)

    try:
        if role == 'mahasiswa':
            cur.execute("SELECT NIM FROM mahasiswa WHERE user_id = %s", (user_id,))
            mahasiswa = cur.fetchone()
            if not mahasiswa: return "Data mahasiswa tidak ditemukan."

            cur.execute("""
                SELECT k.*, COUNT(pk.id_pertanyaan) as jumlah_pertanyaan, h.nilai_total, h.waktu_selesai
                FROM kuis k
                LEFT JOIN pertanyaan_kuis pk ON k.id_kuis = pk.id_kuis
                LEFT JOIN hasil_kuis h ON k.id_kuis = h.id_kuis AND h.NIM = %s
                GROUP BY k.id_kuis ORDER BY k.tanggal_dibuat DESC
            """, (mahasiswa['NIM'],))
            kuis_list = cur.fetchall()

            for k in kuis_list:
                k['hasil_mahasiswa'] = {session['user_id']: {'nilai': k['nilai_total'], 'tanggal_selesai': k['waktu_selesai']}} if k.get('nilai_total') is not None else {}
            
            return render_template('kuis.html', kuis_list=kuis_list)
        
        elif role == 'dosen':
            cur.execute("SELECT id_dosen FROM dosen WHERE user_id = %s", (user_id,))
            dosen = cur.fetchone()
            if not dosen: return "Data dosen tidak ditemukan."
            
            cur.execute("""
                SELECT k.*, COUNT(DISTINCT p.id_pertanyaan) as jumlah_pertanyaan, COUNT(DISTINCT h.NIM) as jumlah_peserta
                FROM kuis k
                LEFT JOIN pertanyaan_kuis p ON k.id_kuis = p.id_kuis
                LEFT JOIN hasil_kuis h ON k.id_kuis = h.id_kuis
                WHERE k.id_dosen = %s GROUP BY k.id_kuis ORDER BY k.tanggal_dibuat DESC
            """, (dosen['id_dosen'],))
            kuis_list = cur.fetchall()
            return render_template('/dosen/kuis.html', kuis_list=kuis_list)
    finally:
        if con.is_connected(): con.close()
    return redirect(url_for('login'))

@app.route('/create_kuis', methods=['GET', 'POST'])
def create_kuis():
    if session.get('role') != 'dosen':
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            # Debugging input
            print("==== FORM DATA MASUK ====")
            print(request.form)

            judul = request.form.get('title', '').strip()
            status = 'aktif' if request.form.get('status') == 'aktif' else 'nonaktif'
            durasi = int(request.form.get('durasi', 30))
            formatted_questions_raw = request.form.get('formatted_questions', '')
            formatted_questions = formatted_questions_raw.strip().split('\n')

            print("Judul:", judul)
            print("Status:", status)
            print("Durasi:", durasi)
            print("Jumlah Pertanyaan:", len(formatted_questions))

            # Koneksi DB
            con = get_db()
            cur = con.cursor(dictionary=True)

            user_id = session.get('user_id')
            print("User ID dari session:", user_id)

            # Cek dosen
            cur.execute("SELECT id_dosen FROM dosen WHERE user_id = %s", (user_id,))
            dosen = cur.fetchone()
            if not dosen:
                print("Dosen tidak ditemukan")
                return "Dosen tidak ditemukan"

            # Insert kuis
            cur.execute("""
                INSERT INTO kuis (judul, status, durasi, id_dosen)
                VALUES (%s, %s, %s, %s)
            """, (judul, status, durasi, dosen['id_dosen']))
            id_kuis = cur.lastrowid
            print("ID kuis baru:", id_kuis)

            # Insert pertanyaan
            for baris in formatted_questions:
                baris = baris.strip()
                if not baris:
                    continue
                if '[Jawaban:' in baris:
                    try:
                        teks = baris.split('[')[0].strip()
                        opsi_part = baris.split('[')[1].split(']')[0]
                        jawaban = baris.split('[Jawaban:')[1].strip(' ]')
                        print("PG:", teks)
                        print("Opsi:", opsi_part)
                        print("Jawaban:", jawaban)

                        cur.execute("""
                            INSERT INTO pertanyaan_kuis (id_kuis, teks_pertanyaan, jenis)
                            VALUES (%s, %s, 'pilihan_ganda')
                        """, (id_kuis, teks))
                        id_pertanyaan = cur.lastrowid

                        for opsi_text in opsi_part.split(';'):
                            if '.' not in opsi_text:
                                continue
                            kode, isi = opsi_text.strip().split('.', 1)
                            benar = (kode.strip() == jawaban)
                            cur.execute("""
                                INSERT INTO pilihan_jawaban (id_pertanyaan, teks_pilihan, is_jawaban_benar)
                                VALUES (%s, %s, %s)
                            """, (id_pertanyaan, isi.strip(), benar))
                    except Exception as e:
                        print("ERROR parsing PG:", e)
                else:
                    print("Essay:", baris)
                    cur.execute("""
                        INSERT INTO pertanyaan_kuis (id_kuis, teks_pertanyaan, jenis)
                        VALUES (%s, %s, 'essay')
                    """, (id_kuis, baris))

            con.commit()
            print("Berhasil menyimpan kuis.")
            return redirect(url_for('kuis'))

        except Exception as e:
            print("GAGAL menyimpan kuis:", e)
            con.rollback()
            return f"Terjadi kesalahan saat menyimpan: {e}"

        finally:
            con.close()

    return render_template('/dosen/create_kuis.html')

@app.route('/edit_kuis/<int:id_kuis>', methods=['GET', 'POST'])
def edit_kuis(id_kuis):
    print(f"DEBUG: Akses edit_kuis dengan id_kuis = {id_kuis}")
    print("DEBUG: Session =", session)

    if 'username' not in session or session.get('role') != 'dosen':
        print("DEBUG: Tidak login sebagai dosen. Redirect ke login.")
        return redirect(url_for('login'))
    
    con = get_db()
    cur = con.cursor(dictionary=True)
    
    if request.method == 'GET':
        try:
            # Cek data kuis
            print("DEBUG: Mengambil data kuis...")
            # Solusi 2: Gunakan JOIN dalam satu query
            cur.execute("""
                SELECT k.* FROM kuis k
                INNER JOIN dosen d ON k.id_dosen = d.id_dosen
                WHERE k.id_kuis = %s AND d.user_id = %s
            """, (id_kuis, session.get('user_id')))
            
            kuis = cur.fetchone()
            print("DEBUG: Hasil kuis =", kuis)

            if not kuis:
                con.close()
                flash('Kuis tidak ditemukan atau Anda tidak memiliki akses', 'error')
                print("DEBUG: Kuis tidak ditemukan atau tidak cocok dengan dosen.")
                return redirect(url_for('kuis'))
            
            # Ambil pertanyaan
            print("DEBUG: Mengambil daftar pertanyaan...")
            cur.execute("""
                SELECT * FROM pertanyaan_kuis 
                WHERE id_kuis = %s
                ORDER BY id_pertanyaan
            """, (id_kuis,))
            
            pertanyaan_list = cur.fetchall()
            print(f"DEBUG: Total pertanyaan ditemukan = {len(pertanyaan_list)}")
            
            # Ambil pilihan untuk setiap pertanyaan
            for p in pertanyaan_list:
                cur.execute("""
                    SELECT id_pilihan, teks_pilihan, is_jawaban_benar 
                    FROM pilihan_jawaban 
                    WHERE id_pertanyaan = %s
                    ORDER BY id_pilihan
                """, (p['id_pertanyaan'],))
                
                pilihan_results = cur.fetchall()
                p['pilihan_list'] = [
                    {
                        'id': pilihan['id_pilihan'],
                        'text': pilihan['teks_pilihan'],
                        'is_correct': bool(pilihan['is_jawaban_benar'])
                    } for pilihan in pilihan_results
                ]
            
            con.close()
            print("DEBUG: Render halaman edit_kuis.html")
            return render_template('dosen/edit_kuis.html', kuis=kuis, pertanyaan_list=pertanyaan_list)
        
        except Exception as e:
            con.close()
            print("DEBUG: ERROR saat load GET edit_kuis:", str(e))
            flash(f'Error loading kuis: {str(e)}', 'error')
            return redirect(url_for('kuis'))

    # POST handling bisa kamu debug dengan pola serupa    
    elif request.method == 'POST':
        try:
            # Update data kuis
            judul = request.form.get('judul', '').strip()
            deskripsi = request.form.get('deskripsi', '').strip()
            durasi = request.form.get('durasi')
            status = request.form.get('status', 'nonaktif')
            
            # Validasi input
            if not judul:
                flash('Judul kuis tidak boleh kosong', 'error')
                return redirect(url_for('edit_kuis', id_kuis=id_kuis))
            
            if not durasi or int(durasi) <= 0:
                flash('Durasi harus lebih dari 0 menit', 'error')
                return redirect(url_for('edit_kuis', id_kuis=id_kuis))
            
            # Cek apakah kuis milik dosen yang login
            cur.execute("""
                SELECT id_kuis FROM kuis 
                WHERE id_kuis = %s AND id_dosen = %s
            """, (id_kuis, session['user_id']))
            
            if not cur.fetchone():
                con.close()
                flash('Kuis tidak ditemukan atau Anda tidak memiliki akses', 'error')
                return redirect(url_for('kuis'))
            
            cur.execute("""
                UPDATE kuis 
                SET judul = %s, deskripsi = %s, durasi = %s, status = %s
                WHERE id_kuis = %s AND id_dosen = %s
            """, (judul, deskripsi, int(durasi), status, id_kuis, session['user_id']))
            
            # Update pertanyaan jika ada
            if 'update_questions' in request.form:
                # Hapus pilihan jawaban lama
                cur.execute("""
                    DELETE pj FROM pilihan_jawaban pj
                    JOIN pertanyaan_kuis p ON pj.id_pertanyaan = p.id_pertanyaan
                    WHERE p.id_kuis = %s
                """, (id_kuis,))
                
                # Hapus pertanyaan lama
                cur.execute("DELETE FROM pertanyaan_kuis WHERE id_kuis = %s", (id_kuis,))
                
                # Tambah pertanyaan baru
                pertanyaan_count = int(request.form.get('pertanyaan_count', 0))
                
                for i in range(1, pertanyaan_count + 1):
                    teks_pertanyaan = request.form.get(f'pertanyaan_{i}', '').strip()
                    jenis = request.form.get(f'jenis_{i}', 'pilihan_ganda')
                    
                    if teks_pertanyaan:
                        cur.execute("""
                            INSERT INTO pertanyaan_kuis (id_kuis, teks_pertanyaan, jenis)
                            VALUES (%s, %s, %s)
                        """, (id_kuis, teks_pertanyaan, jenis))
                        
                        id_pertanyaan = cur.lastrowid
                        
                        if jenis == 'pilihan_ganda':
                            # Validasi ada jawaban benar
                            jawaban_benar = request.form.get(f'jawaban_{i}')
                            if not jawaban_benar:
                                con.rollback()
                                con.close()
                                flash(f'Pertanyaan {i} harus memiliki jawaban yang benar', 'error')
                                return redirect(url_for('edit_kuis', id_kuis=id_kuis))
                            
                            # Tambah pilihan jawaban
                            pilihan_kosong = 0
                            for j in ['a', 'b', 'c', 'd']:
                                pilihan_text = request.form.get(f'pilihan_{i}_{j}', '').strip()
                                if pilihan_text:
                                    is_correct = jawaban_benar == j
                                    cur.execute("""
                                        INSERT INTO pilihan_jawaban (id_pertanyaan, teks_pilihan, is_jawaban_benar)
                                        VALUES (%s, %s, %s)
                                    """, (id_pertanyaan, pilihan_text, is_correct))
                                else:
                                    pilihan_kosong += 1
                            
                            # Validasi minimal ada 2 pilihan
                            if pilihan_kosong > 2:
                                con.rollback()
                                con.close()
                                flash(f'Pertanyaan {i} harus memiliki minimal 2 pilihan jawaban', 'error')
                                return redirect(url_for('edit_kuis', id_kuis=id_kuis))
            
            con.commit()
            con.close()
            
            flash('Kuis berhasil diperbarui!', 'success')
            return redirect(url_for('lihat_kuis', id_kuis=id_kuis))
            
        except ValueError as ve:
            con.rollback()
            con.close()
            flash('Data input tidak valid', 'error')
            return redirect(url_for('edit_kuis', id_kuis=id_kuis))
            
        except Exception as e:
            con.rollback()
            con.close()
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('edit_kuis', id_kuis=id_kuis))

@app.route('/hapus_kuis/<int:id_kuis>', methods=['POST'])
def hapus_kuis(id_kuis):
    if session.get('role') != 'dosen':
        return redirect(url_for('login'))
    
    con = get_db()
    cur = con.cursor()
    
    # Hapus kuis (cascade akan menghapus pertanyaan dan jawaban terkait)
    cur.execute("DELETE FROM kuis WHERE id_kuis = %s", (id_kuis,))
    con.commit()
    con.close()
    
    return redirect(url_for('kuis'))

# --- [BARU & DIPERBAIKI] API ENDPOINTS UNTUK KUIS ---

@app.route('/api/kuis/<int:id_kuis>/soal')
def api_get_soal_kuis(id_kuis):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    try:
        con, cur = get_db(), get_db().cursor(dictionary=True)
        cur.execute("SELECT id_pertanyaan, teks_pertanyaan, jenis FROM pertanyaan_kuis WHERE id_kuis = %s ORDER BY id_pertanyaan", (id_kuis,))
        pertanyaan_rows = cur.fetchall()

        if not pertanyaan_rows: return jsonify({'error': 'Kuis tidak memiliki soal'}), 404
        
        questions_for_frontend = []
        for p_row in pertanyaan_rows:
            question_data = {'id_soal': p_row['id_pertanyaan'], 'pertanyaan': p_row['teks_pertanyaan'], 'tipe': 'pilihan_ganda' if p_row['jenis'] == 'pilihan_ganda' else 'esai', 'opsi': []}
            if p_row['jenis'] == 'pilihan_ganda':
                cur.execute("SELECT id_pilihan, teks_pilihan FROM pilihan_jawaban WHERE id_pertanyaan = %s ORDER BY id_pilihan", (p_row['id_pertanyaan'],))
                opsi_rows = cur.fetchall()
                question_data['opsi'] = [{'id_opsi': o['id_pilihan'], 'teks_opsi': o['teks_pilihan']} for o in opsi_rows]
            questions_for_frontend.append(question_data)
        return jsonify({'soal': questions_for_frontend})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': 'Kesalahan pada server'}), 500
    finally:
        if 'con' in locals() and con.is_connected(): con.close()

@app.route('/api/kuis/<int:id_kuis>/submit', methods=['POST'])
def api_submit_kuis(id_kuis):
    if session.get('role') != 'mahasiswa': return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json()
    if not data or 'jawaban' not in data: return jsonify({'error': 'Data jawaban tidak valid'}), 400

    try:
        con, cur = get_db(), get_db().cursor(dictionary=True)
        user_id = session['user_id']

        cur.execute("SELECT NIM FROM mahasiswa WHERE user_id = %s", (user_id,))
        mahasiswa = cur.fetchone()
        if not mahasiswa: return jsonify({'error': 'Data mahasiswa tidak ditemukan'}), 404
        NIM = mahasiswa['NIM']

        cur.execute("DELETE FROM jawaban_mahasiswa WHERE NIM = %s AND id_pertanyaan IN (SELECT id_pertanyaan FROM pertanyaan_kuis WHERE id_kuis = %s)", (NIM, id_kuis))
        cur.execute("SELECT id_hasil FROM hasil_kuis WHERE id_kuis = %s AND NIM = %s", (id_kuis, NIM))
        if not cur.fetchone():
            cur.execute("INSERT INTO hasil_kuis (id_kuis, NIM, waktu_mulai, status) VALUES (%s, %s, NOW(), 'sedang_dikerjakan')", (id_kuis, NIM))
        
        total_nilai_pg, jumlah_soal_pg, ada_esai = 0, 0, False
        for id_soal_str, jawaban_client in data['jawaban'].items():
            id_soal = int(id_soal_str)
            cur.execute("SELECT jenis FROM pertanyaan_kuis WHERE id_pertanyaan = %s", (id_soal,))
            pertanyaan = cur.fetchone()
            if not pertanyaan: continue

            nilai, id_pilihan, teks = None, None, None
            if pertanyaan['jenis'] == 'pilihan_ganda':
                jumlah_soal_pg += 1
                if jawaban_client is not None:
                    id_pilihan = int(jawaban_client)
                    cur.execute("SELECT is_jawaban_benar FROM pilihan_jawaban WHERE id_pilihan = %s", (id_pilihan,))
                    pilihan = cur.fetchone()
                    nilai = 100.00 if pilihan and pilihan['is_jawaban_benar'] else 0.00
                    total_nilai_pg += nilai
            elif pertanyaan['jenis'] == 'esai':
                ada_esai, teks = True, jawaban_client
            
            cur.execute("INSERT INTO jawaban_mahasiswa (id_pertanyaan, id_mahasiswa, id_pilihan, jawaban_teks, nilai) VALUES (%s, %s, %s, %s, %s)",
                        (id_soal, NIM, id_pilihan, teks, nilai))

        status_akhir = 'belum_dinilai' if ada_esai else 'sudah_dinilai'
        nilai_total_akhir = (total_nilai_pg / jumlah_soal_pg) if not ada_esai and jumlah_soal_pg > 0 else None
        
        cur.execute("UPDATE hasil_kuis SET status = %s, nilai_total = %s, waktu_selesai = NOW() WHERE id_kuis = %s AND NIM = %s",
                    (status_akhir, nilai_total_akhir, id_kuis, NIM))
        con.commit()

        grade, message, badgeClass = 'E', 'Perlu belajar lebih giat!', 'bg-danger'
        if nilai_total_akhir is not None:
            if nilai_total_akhir >= 85: grade, message, badgeClass = 'A', 'Luar Biasa!', 'bg-success'
            elif nilai_total_akhir >= 75: grade, message, badgeClass = 'B', 'Kerja Bagus!', 'bg-primary'
            elif nilai_total_akhir >= 65: grade, message, badgeClass = 'C', 'Cukup Baik.', 'bg-warning'

        return jsonify({'success': True, 'nilai': nilai_total_akhir, 'message': message if nilai_total_akhir is not None else "Jawaban esai Anda akan dinilai oleh dosen.", 'grade': grade if nilai_total_akhir is not None else '-', 'badgeClass': badgeClass if nilai_total_akhir is not None else 'bg-info'})
    except Exception as e:
        if 'con' in locals() and con: con.rollback()
        traceback.print_exc()
        return jsonify({'error': 'Kesalahan pada server'}), 500
    finally:
        if 'con' in locals() and con.is_connected(): con.close()


if __name__ == '__main__':
    app.run(debug=True)