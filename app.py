from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from functools import wraps
import bcrypt  # Asegúrate de haber instalado bcrypt

app = Flask(__name__)
app.secret_key = 'Cistian@1232'  # Cambia esto por una clave secreta segura

# Conexión a la base de datos PostgreSQL
def connect_db():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME', 'bouinetzwnfsu76o1zlr'),
            user=os.getenv('DB_USER', 'u6nzvrfvpmi9ucxmomlu'),
            password=os.getenv('DB_PASSWORD', 'ieafyev5G4hqdpeoADfzxlBDkLQfO9'),
            host=os.getenv('DB_HOST', 'bouinetzwnfsu76o1zlr-postgresql.services.clever-cloud.com'),
            port=os.getenv('DB_PORT', '50013')
        )
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# Decorador para rutas protegidas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Por favor, inicia sesión primero.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Ruta para la página de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = connect_db()
        if conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            try:
                # Busca el usuario en la base de datos usando el nombre de usuario
                cursor.execute('SELECT * FROM usuarios WHERE username = %s', (username,))
                user = cursor.fetchone()
                
                if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
                    # Si el hash coincide, el usuario está autenticado
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

# Ruta para cerrar sesión
@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('login'))

# Ruta protegida, solo accesible si el usuario está autenticado
@app.route('/')
@login_required
def index():
    return redirect(url_for('cargar_pelicula'))

# Rutas para cargar películas y series, ahora protegidas
@app.route('/cargar_pelicula')
@login_required
def cargar_pelicula():
    return render_template('cargar_pelicula.html')

@app.route('/cargar_serie')
@login_required
def cargar_serie():
    return render_template('cargar_serie.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)


