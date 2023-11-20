from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

app = Flask(__name__)

# konfigurasi mysql
app.secret_key = 'anggotakel'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_anggota'
mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/data_anggota', methods=['GET', 'POST'])
def dataa():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM tbl_anggota')
    data = cur.fetchall()
    cur.close()
    return render_template('data_anggota.html', tbl_anggota=data)


@app.route('/isianggota', methods=['GET', 'POST'])
def isik():
    if request.method == 'POST':
        id_admin = request.form['id_anggota']
        nama = request.form['nama']
        kelas = request.form['kelas']
        jabatan = request.form['jabatan']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO tbl_anggota VALUES (%s, %s, %s, %s)', (id_admin, nama, kelas, jabatan))
        mysql.connection.commit()
        return redirect(url_for('dataa'))

    return render_template('isi_anggota.html')


@app.route('/update2/<int:id_anggota>', methods=['GET', 'POST'])
def update2(id_anggota):
    if request.method == 'POST':
        nama = request.form['nama']
        kelas = request.form['kelas']
        jabatan = request.form['jabatan']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE tbl_anggota SET nama=%s, kelas=%s, jabatan=%s WHERE id_anggota=%s",
                    (nama, kelas, jabatan, id_anggota))
        mysql.connection.commit()
        cur.close()
        return redirect('/data_anggota')

    cur = mysql.connection.cursor()
    cur.execute(
    "SELECT * FROM tbl_anggota WHERE id_anggota = %s", (id_anggota,))
    anggota = cur.fetchone()
    cur.close()
    return render_template('edit2.html', anggota=anggota)


@app.route('/delete/<int:id_anggota>')
def delete(id_anggota):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tbl_anggota WHERE id_anggota=%s", (id_anggota,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('dataa'))



 
if __name__ == '__main__':
    app.run(debug=True)
