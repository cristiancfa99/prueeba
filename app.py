from flask import Flask, request, jsonify, render_template
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = Flask(__name__)

# Conexión a la base de datos PostgreSQL usando variables de entorno
def connect_db():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# Función CRUD: Crear una nueva película
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

# Función CRUD: Leer todas las películas
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

# Función CRUD: Crear una nueva serie
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

# Función CRUD: Leer todas las series
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

# Ruta para listar todas las películas (usar función CRUD)
@app.route('/api/peliculas', methods=['GET'])
def listar_peliculas():
    peliculas, status_code = read_movies()
    return jsonify(peliculas), status_code

# Ruta para agregar una nueva película (usar función CRUD)
@app.route('/api/peliculas', methods=['POST'])
def agregar_pelicula():
    data = request.json
    response, status_code = create_movie(data)
    return jsonify(response), status_code

# Ruta para listar todas las series (usar función CRUD)
@app.route('/api/series', methods=['GET'])
def listar_series():
    series, status_code = read_series()
    return jsonify(series), status_code

# Ruta para agregar una nueva serie (usar función CRUD)
@app.route('/api/series', methods=['POST'])
def agregar_serie():
    data = request.json
    response, status_code = create_series(data)
    return jsonify(response), status_code

# Ruta para cargar película desde el navegador
@app.route('/cargar_pelicula')
def cargar_pelicula():
    return render_template('cargar_pelicula.html')

# Ruta para cargar serie desde el navegador
@app.route('/cargar_serie')
def cargar_serie():
    return render_template('cargar_serie.html')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=os.getenv('PORT', 5000))

