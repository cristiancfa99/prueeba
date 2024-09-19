from flask import Flask, request, jsonify, render_template, redirect
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = Flask(__name__)

# Conexión a la base de datos PostgreSQL usando variables de entorno
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

# Funciones CRUD
def create_movie(data):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            titulo = data['titulo'].upper()
            cursor.execute('SELECT COUNT(*) FROM peliculas WHERE titulo = %s', (titulo,))
            if cursor.fetchone()[0] > 0:
                return {"error": "El título de la película ya existe."}, 400
            else:
                cursor.execute('INSERT INTO peliculas (titulo, director, genero, "año") VALUES (%s, %s, %s, %s)', 
                               (titulo, data['director'], data['genero'], data['año']))
                conn.commit()
                return {"mensaje": "Película agregada exitosamente."}, 201
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            conn.close()
    else:
        return {"error": "Error al conectar a la base de datos"}, 500

def read_movies():
    conn = connect_db()
    if conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("SELECT * FROM peliculas")
            peliculas = cursor.fetchall()
            return peliculas, 200
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            conn.close()
    else:
        return {"error": "Error al conectar a la base de datos"}, 500

def create_series(data):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            titulo = data['titulo'].upper()
            cursor.execute('SELECT * FROM serie WHERE titulo = %s', (titulo,))
            if cursor.fetchone():
                return {"error": "El título de la serie ya existe."}, 400
            else:
                cursor.execute('INSERT INTO serie (titulo, director, genero, temporadas, episodios, año_estreno, descripcion) VALUES (%s, %s, %s, %s, %s, %s, %s)', 
                               (titulo, data['director'], data['genero'], data['temporadas'], data['episodios'], data['año_estreno'], data['descripcion']))
                conn.commit()
                return {"mensaje": "Serie agregada exitosamente."}, 201
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            conn.close()
    else:
        return {"error": "Error al conectar a la base de datos"}, 500

def read_series():
    conn = connect_db()
    if conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("SELECT * FROM serie")
            series = cursor.fetchall()
            return series, 200
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            conn.close()
    else:
        return {"error": "Error al conectar a la base de datos"}, 500

def delete_movie(id):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM peliculas WHERE id = %s', (id,))
            conn.commit()
            return {"mensaje": "Película eliminada exitosamente."}, 200
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            conn.close()
    else:
        return {"error": "Error al conectar a la base de datos"}, 500

def delete_series(id):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM serie WHERE id = %s', (id,))
            conn.commit()
            return {"mensaje": "Serie eliminada exitosamente."}, 200
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            conn.close()
    else:
        return {"error": "Error al conectar a la base de datos"}, 500

def update_movie(id, data):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('UPDATE peliculas SET titulo = %s, director = %s, genero = %s, "año" = %s WHERE id = %s', 
                           (data['titulo'], data['director'], data['genero'], data['año'], id))
            conn.commit()
            return {"mensaje": "Película actualizada exitosamente."}, 200
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            conn.close()
    else:
        return {"error": "Error al conectar a la base de datos"}, 500

def update_series(id, data):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('UPDATE serie SET titulo = %s, director = %s, genero = %s, temporadas = %s, episodios = %s, año_estreno = %s, descripcion = %s WHERE id = %s', 
                           (data['titulo'], data['director'], data['genero'], data['temporadas'], data['episodios'], data['año_estreno'], data['descripcion'], id))
            conn.commit()
            return {"mensaje": "Serie actualizada exitosamente."}, 200
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            conn.close()
    else:
        return {"error": "Error al conectar a la base de datos"}, 500
# Rutas para API
@app.route('/api/peliculas', methods=['GET'])
def listar_peliculas():
    peliculas, status_code = read_movies()
    return jsonify(peliculas), status_code

@app.route('/api/peliculas', methods=['POST'])
def agregar_pelicula():
    data = request.json
    response, status_code = create_movie(data)
    return jsonify(response), status_code

# Rutas para páginas HTML
@app.route('/')
def index():
    # Redirige a la página de cargar película
    return redirect('/cargar_pelicula')

@app.route('/cargar_pelicula')
def cargar_pelicula():
    return render_template('cargar_pelicula.html')

@app.route('/cargar_serie')
def cargar_serie():
    return render_template('cargar_serie.html')

if __name__ == '__main__':
    # Usa la variable de entorno PORT si está disponible, de lo contrario usa 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=os.getenv('PORT', 5000))

