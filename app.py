import bcrypt
import psycopg2
import os

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

def create_user(username, password):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            # Verificar si el usuario ya existe
            cursor.execute('SELECT username FROM usuarios WHERE username = %s', (username,))
            if cursor.fetchone():
                print("El nombre de usuario ya existe.")
                return

            # Generar un hash para la contraseña
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Insertar el nuevo usuario en la base de datos
            cursor.execute('INSERT INTO usuarios (username, password_hash) VALUES (%s, %s)', (username, hashed_password))
            conn.commit()
            print("Usuario creado exitosamente.")
        except Exception as e:
            print(f"Error al crear el usuario: {e}")
        finally:
            conn.close()
    else:
        print("Error al conectar a la base de datos")

if __name__ == "__main__":
    username = input("Ingrese el nombre de usuario: ")
    password = input("Ingrese la contraseña: ")
    create_user(username, password)

