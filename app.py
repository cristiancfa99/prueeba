from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
import psycopg2
from psycopg2.extras import RealDictCursor
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = 'cris1232'

# Usuario administrador
ADMIN_USERS = ['cristiancfa','coceres']  

def connect_db():
    try:
        conn = psycopg2.connect(
            dbname='bnmtshjy0t7ckmhsqyz1',
            user='uek5h49jfgqinljgrire',
            password='LQF4QumsoMp7tPKDEECN21Rs2rrprG',
            host='bnmtshjy0t7ckmhsqyz1-postgresql.services.clever-cloud.com',
            port='50013'
        )
        print("Conexión a la base de datos exitosa.")
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Por favor, inicia sesión primero.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session or session['username'] not in ADMIN_USERS:
            flash('No tienes permiso para acceder a esta página.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = connect_db()
        if conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            try:
                cursor.execute('SELECT * FROM usuarios WHERE username = %s AND password = %s', (username, password))
                user = cursor.fetchone()
                if user:
                    session['logged_in'] = True
                    session['username'] = user['username']
                    flash(f'Bienvenido, {user["username"]}!', 'success')
                    return redirect(url_for('index'))
                else:
                    flash('Usuario o contraseña incorrectos', 'danger')
            except Exception as e:
                flash(f'Error al buscar el usuario: {e}', 'danger')
            finally:
                conn.close()
        else:
            flash('Error al conectar a la base de datos', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('welcome.html', ADMIN_USERS=ADMIN_USERS)

@app.route('/register', methods=['GET', 'POST'])
@login_required
@admin_required
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO usuarios (username, password) VALUES (%s, %s)', (username, password))
                conn.commit()
                flash('Usuario registrado exitosamente', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                flash(f'Error al registrar usuario: {e}', 'danger')
            finally:
                conn.close()
        else:
            flash('Error al conectar a la base de datos', 'danger')
    return render_template('register.html')

@app.route('/cargar_pelicula', methods=['GET', 'POST'])
@login_required
def cargar_pelicula():
    if request.method == 'POST':
        return agregar_pelicula()
    return render_template('cargar_pelicula.html')

@app.route('/api/peliculas', methods=['POST'])
@login_required
def agregar_pelicula():
    data = request.get_json()
    print(data)  # Imprimir los datos recibidos

    
    if not all(key in data for key in ['titulo', 'director', 'genero']):  
        return jsonify({'error': 'Faltan datos requeridos'}), 400

    titulo = data.get('titulo').upper()
    director = data.get('director')
    genero = data.get('genero')

    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            print(f"Insertando: {titulo}, {director}, {genero}")  # Imprimir valores
            cursor.execute('INSERT INTO peliculas (titulo, director, genero) VALUES (%s, %s, %s)', (titulo, director, genero)) 
            conn.commit()
            return jsonify({'message': 'Película agregada exitosamente'}), 201
        except Exception as e:
            print(f"Error al agregar película: {e}")
            return jsonify({'error': str(e)}), 400
        finally:
            conn.close()
    return jsonify({'error': 'Error al conectar a la base de datos'}), 500

@app.route('/eliminar_pelicula/<int:id>', methods=['POST'])
@login_required
def eliminar_pelicula(id):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM peliculas WHERE id = %s', (id,))
            conn.commit()
            flash('Película eliminada exitosamente', 'success')
            return redirect(url_for('listar_peliculas'))
        except Exception as e:
            print(f"Error al eliminar película: {e}")
            flash('Error al eliminar la película', 'danger')
        finally:
            conn.close()
    return jsonify({'error': 'Error al conectar a la base de datos'}), 500

@app.route('/listar_peliculas', methods=['GET'])
@login_required
@admin_required
def listar_peliculas():
    titulo = request.args.get('titulo', '')

    conn = connect_db()
    if conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        query = 'SELECT * FROM peliculas WHERE 1=1'
        params = []

        if titulo:
            query += ' AND UPPER(titulo) LIKE %s'
            params.append(f'%{titulo.upper()}%')

        cursor.execute(query, params)
        peliculas = cursor.fetchall()
        conn.close()
        return render_template('listar_peliculas.html', peliculas=peliculas, titulo=titulo)

    return 'Error al conectar a la base de datos', 500

# Rutas para cargar y listar series
@app.route('/cargar_serie', methods=['GET', 'POST'])
@login_required
def cargar_serie():
    if request.method == 'POST':
        return agregar_serie()
    return render_template('cargar_serie.html')

@app.route('/api/series', methods=['POST'])
@login_required
def agregar_serie():
    data = request.get_json()
    
    if not all(key in data for key in ['titulo', 'director', 'genero', 'temporadas', 'episodios', 'año_estreno', 'descripcion']):
        return jsonify({'error': 'Faltan datos requeridos'}), 400

    titulo = data.get('titulo').upper()
    director = data.get('director')
    genero = data.get('genero')
    temporadas = data.get('temporadas')
    episodios = data.get('episodios')
    año_estreno = data.get('año_estreno')
    descripcion = data.get('descripcion')

    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO series (titulo, director, genero, temporadas, episodios, año_estreno, descripcion) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                (titulo, director, genero, temporadas, episodios, año_estreno, descripcion)
            )
            conn.commit()
            return jsonify({'message': 'Serie agregada exitosamente'}), 201
        except Exception as e:
            print(f"Error al agregar serie: {e}")
            return jsonify({'error': 'Error al guardar la serie en la base de datos.'}), 500
        finally:
            conn.close()
    
    return jsonify({'error': 'Error al conectar a la base de datos'}), 500
      

@app.route('/eliminar_serie/<int:id>', methods=['POST'])
@login_required
@admin_required
def eliminar_serie(id):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM series WHERE id = %s', (id,))
            conn.commit()
            flash('Serie eliminada exitosamente', 'success')
            return redirect(url_for('listar_series'))
        except Exception as e:
            print(f"Error al eliminar serie: {e}")
            flash('Error al eliminar la serie', 'danger')
        finally:
            conn.close()
    return jsonify({'error': 'Error al conectar a la base de datos'}), 500

@app.route('/listar_series', methods=['GET'])
@login_required
@admin_required
def listar_series():
    titulo = request.args.get('titulo', '')
    año = request.args.get('año', '')

    conn = connect_db()
    if conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        query = 'SELECT * FROM series WHERE 1=1'
        params = []

        if titulo:
            query += ' AND UPPER(titulo) LIKE %s'
            params.append(f'%{titulo.upper()}%')
        if año:
            query += ' AND año_estreno = %s'
            params.append(año)

        cursor.execute(query, params)
        series = cursor.fetchall()
        conn.close()
        return render_template('listar_series.html', series=series, titulo=titulo, año=año)

    return 'Error al conectar a la base de datos', 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

