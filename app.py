from flask import Flask, request, jsonify, render_template
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Conexión a la base de datos PostgreSQL
import os
from flask import Flask, request, jsonify, render_template
import psycopg2
from psycopg2.extras import RealDictCursor


app = Flask(__name__)

@app.route('/')
def home():
    # Your code to handle the root path request
    return "Welcome to my Flask app!"

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


# Ruta para listar todas las películas
@app.route('/api/peliculas', methods=['GET'])
def listar_peliculas():
    conn = connect_db()
    if conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("SELECT * FROM peliculas")
            peliculas = cursor.fetchall()
            return jsonify(peliculas)
        except Exception as e:
            return jsonify({"error": str(e)})
        finally:
            conn.close()
    else:
        return jsonify({"error": "Error al conectar a la base de datos"})

# Ruta para agregar una nueva película
@app.route('/api/peliculas', methods=['POST'])
def agregar_pelicula():
    data = request.json
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            titulo = data['titulo'].upper()
            cursor.execute('SELECT COUNT(*) FROM peliculas WHERE titulo = %s', (titulo,))
            if cursor.fetchone()[0] > 0:
                return jsonify({"error": "El título de la película ya existe."}), 400
            else:
                cursor.execute('INSERT INTO peliculas (titulo, director, genero, "año") VALUES (%s, %s, %s, %s)', 
                               (titulo, data['director'], data['genero'], data['año']))
                conn.commit()
                return jsonify({"mensaje": "Película agregada exitosamente."})
        except Exception as e:
            return jsonify({"error": str(e)})
        finally:
            conn.close()
    else:
        return jsonify({"error": "Error al conectar a la base de datos"})

# Ruta para listar todas las series
@app.route('/api/series', methods=['GET'])
def listar_series():
    conn = connect_db()
    if conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute("SELECT * FROM serie")
            series = cursor.fetchall()
            return jsonify(series)
        except Exception as e:
            return jsonify({"error": str(e)})
        finally:
            conn.close()
    else:
        return jsonify({"error": "Error al conectar a la base de datos"})

# Ruta para agregar una nueva serie
@app.route('/api/series', methods=['POST'])
def agregar_serie():
    data = request.json
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            titulo = data['titulo'].upper()
            cursor.execute('SELECT * FROM serie WHERE titulo = %s', (titulo,))
            if cursor.fetchone():
                return jsonify({"error": "El título de la serie ya existe."}), 400
            else:
                cursor.execute('INSERT INTO serie (titulo, director, genero, temporadas, episodios, año_estreno, descripcion) VALUES (%s, %s, %s, %s, %s, %s, %s)', 
                               (titulo, data['director'], data['genero'], data['temporadas'], data['episodios'], data['año_estreno'], data['descripcion']))
                conn.commit()
                return jsonify({"mensaje": "Serie agregada exitosamente."})
        except Exception as e:
            return jsonify({"error": str(e)})
        finally:
            conn.close()
    else:
        return jsonify({"error": "Error al conectar a la base de datos"})

# Ruta para cargar película desde el navegador
@app.route('/cargar_pelicula')
def cargar_pelicula():
    return render_template('cargar_pelicula.html')

# Ruta para cargar serie desde el navegador
@app.route('/cargar_serie')
def cargar_serie():
    return render_template('cargar_serie.html')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
