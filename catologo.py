import tkinter as tk
from ttkbootstrap import Style
from tkinter import messagebox
from tkinter import ttk
import psycopg2

# Conexión a la base de datos PostgreSQL
def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="bouinetzwnfsu76o1zlr",
            user="u6nzvrfvpmi9ucxmomlu",
            password="ieafyev5G4hqdpeoADfzxlBDkLQfO9",
            host="bouinetzwnfsu76o1zlr-postgresql.services.clever-cloud.com",
            port="50013"
        )
        return conn
    except Exception as e:
        messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        return None

# Función para agregar una nueva película
def agregar_pelicula():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            # Convertir el título a mayúsculas
            titulo = titulo_var.get().upper()
            
            # Verificar si el título ya existe en la tabla de películas
            cursor.execute('SELECT COUNT(*) FROM peliculas WHERE titulo = %s', (titulo,))
            if cursor.fetchone()[0] > 0:
                messagebox.showwarning("Advertencia", "El título de la película ya existe.")
            else:
                cursor.execute('INSERT INTO peliculas (titulo, director, genero, "año") VALUES (%s, %s, %s, %s)', 
                               (titulo, director_entry.get(), genero_entry.get(), año_entry.get()))
                conn.commit()
                messagebox.showinfo("Éxito", "Película agregada exitosamente.")
                listar_peliculas()
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar la película: {e}")
        finally:
            conn.close()

# Función para listar todas las películas
def listar_peliculas():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM peliculas")
            rows = cursor.fetchall()
            # Limpiar la vista del Treeview
            for item in peliculas_treeview.get_children():
                peliculas_treeview.delete(item)
            # Insertar nuevas filas
            for row in rows:
                peliculas_treeview.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar las películas: {e}")
        finally:
            conn.close()

# Función para buscar películas por año
def buscar_por_año():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM peliculas WHERE "año" = %s', (año_busqueda_entry.get(),))
            rows = cursor.fetchall()
            # Limpiar la vista del Treeview
            for item in peliculas_treeview.get_children():
                peliculas_treeview.delete(item)
            # Insertar resultados de la búsqueda
            for row in rows:
                peliculas_treeview.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar películas por año: {e}")
        finally:
            conn.close()

# Función para abrir la ventana de edición de películas
def abrir_ventana_edicion_pelicula():
    try:
        selected_item = peliculas_treeview.selection()[0]
        item_values = peliculas_treeview.item(selected_item, 'values')
        
        # Abrir la ventana de edición
        ventana_edicion = tk.Toplevel(root)
        ventana_edicion.title("Editar Película")
        ventana_edicion.geometry("300x250")
        
        tk.Label(ventana_edicion, text="ID (solo lectura)").grid(row=0, column=0, pady=5, padx=5)
        tk.Label(ventana_edicion, text=item_values[0]).grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(ventana_edicion, text="Título").grid(row=1, column=0, pady=5, padx=5)
        titulo_entry_edit = tk.Entry(ventana_edicion)
        titulo_entry_edit.grid(row=1, column=1, pady=5, padx=5)
        titulo_entry_edit.insert(0, item_values[1])
        
        tk.Label(ventana_edicion, text="Director").grid(row=2, column=0, pady=5, padx=5)
        director_entry_edit = tk.Entry(ventana_edicion)
        director_entry_edit.grid(row=2, column=1, pady=5, padx=5)
        director_entry_edit.insert(0, item_values[2])
        
        tk.Label(ventana_edicion, text="Género").grid(row=3, column=0, pady=5, padx=5)
        genero_entry_edit = tk.Entry(ventana_edicion)
        genero_entry_edit.grid(row=3, column=1, pady=5, padx=5)
        genero_entry_edit.insert(0, item_values[3])
        
        tk.Label(ventana_edicion, text="Año").grid(row=4, column=0, pady=5, padx=5)
        año_entry_edit = tk.Entry(ventana_edicion)
        año_entry_edit.grid(row=4, column=1, pady=5, padx=5)
        año_entry_edit.insert(0, item_values[4])
        
        def guardar_cambios_pelicula():
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute('UPDATE peliculas SET titulo = %s, director = %s, genero = %s, "año" = %s WHERE id = %s',
                                   (titulo_entry_edit.get(), director_entry_edit.get(), genero_entry_edit.get(), año_entry_edit.get(), item_values[0]))
                    conn.commit()
                    messagebox.showinfo("Éxito", "Película actualizada exitosamente.")
                    listar_peliculas()
                    ventana_edicion.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"Error al actualizar la película: {e}")
                finally:
                    conn.close()
        
        tk.Button(ventana_edicion, text="Guardar Cambios", command=guardar_cambios_pelicula).grid(row=5, column=0, columnspan=2, pady=10, padx=5)
    
    except IndexError:
        messagebox.showwarning("Advertencia", "Selecciona una película para editar.")

# Función para agregar una nueva serie
def agregar_serie():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            # Convertir el título a mayúsculas
            titulo = titulo_var.get().upper()
            
            # Verificar si el título ya existe
            cursor.execute('SELECT * FROM serie WHERE titulo = %s', (titulo,))
            if cursor.fetchone():
                messagebox.showwarning("Advertencia", "El título de la serie ya existe.")
            else:
                cursor.execute('INSERT INTO serie (titulo, director, genero, temporadas, episodios, año_estreno, descripcion) VALUES (%s, %s, %s, %s, %s, %s, %s)', 
                               (titulo, director_entry.get(), genero_entry.get(), temporadas_entry.get(), episodios_entry.get(), año_entry.get(), descripcion_entry.get()))
                conn.commit()
                messagebox.showinfo("Éxito", "Serie agregada exitosamente.")
                listar_series()
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar la serie: {e}")
        finally:
            conn.close()

# Función para listar todas las series
def listar_series():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM serie")
            rows = cursor.fetchall()
            # Limpiar la vista del Treeview
            for item in series_treeview.get_children():
                series_treeview.delete(item)
            # Insertar nuevas filas
            for row in rows:
                series_treeview.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar las series: {e}")
        finally:
            conn.close()

# Función para abrir la ventana de edición de series
def abrir_ventana_edicion_serie():
    try:
        selected_item = series_treeview.selection()[0]
        item_values = series_treeview.item(selected_item, 'values')
        
        # Abrir la ventana de edición
        ventana_edicion = tk.Toplevel(root)
        ventana_edicion.title("Editar Serie")
        ventana_edicion.geometry("300x300")
        
        tk.Label(ventana_edicion, text="ID (solo lectura)").grid(row=0, column=0, pady=5, padx=5)
        tk.Label(ventana_edicion, text=item_values[0]).grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(ventana_edicion, text="Título").grid(row=1, column=0, pady=5, padx=5)
        titulo_entry_edit = tk.Entry(ventana_edicion)
        titulo_entry_edit.grid(row=1, column=1, pady=5, padx=5)
        titulo_entry_edit.insert(0, item_values[1])
        
        tk.Label(ventana_edicion, text="Director").grid(row=2, column=0, pady=5, padx=5)
        director_entry_edit = tk.Entry(ventana_edicion)
        director_entry_edit.grid(row=2, column=1, pady=5, padx=5)
        director_entry_edit.insert(0, item_values[2])
        
        tk.Label(ventana_edicion, text="Género").grid(row=3, column=0, pady=5, padx=5)
        genero_entry_edit = tk.Entry(ventana_edicion)
        genero_entry_edit.grid(row=3, column=1, pady=5, padx=5)
        genero_entry_edit.insert(0, item_values[3])
        
        tk.Label(ventana_edicion, text="Temporadas").grid(row=4, column=0, pady=5, padx=5)
        temporadas_entry_edit = tk.Entry(ventana_edicion)
        temporadas_entry_edit.grid(row=4, column=1, pady=5, padx=5)
        temporadas_entry_edit.insert(0, item_values[4])
        
        tk.Label(ventana_edicion, text="Episodios").grid(row=5, column=0, pady=5, padx=5)
        episodios_entry_edit = tk.Entry(ventana_edicion)
        episodios_entry_edit.grid(row=5, column=1, pady=5, padx=5)
        episodios_entry_edit.insert(0, item_values[5])
        
        tk.Label(ventana_edicion, text="Año Estreno").grid(row=6, column=0, pady=5, padx=5)
        año_entry_edit = tk.Entry(ventana_edicion)
        año_entry_edit.grid(row=6, column=1, pady=5, padx=5)
        año_entry_edit.insert(0, item_values[6])
        
        tk.Label(ventana_edicion, text="Descripción").grid(row=7, column=0, pady=5, padx=5)
        descripcion_entry_edit = tk.Entry(ventana_edicion)
        descripcion_entry_edit.grid(row=7, column=1, pady=5, padx=5)
        descripcion_entry_edit.insert(0, item_values[7])
        
        def guardar_cambios_serie():
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute('UPDATE serie SET titulo = %s, director = %s, genero = %s, temporadas = %s, episodios = %s, año_estreno = %s, descripcion = %s WHERE id = %s',
                                   (titulo_entry_edit.get(), director_entry_edit.get(), genero_entry_edit.get(), temporadas_entry_edit.get(), episodios_entry_edit.get(), año_entry_edit.get(), descripcion_entry_edit.get(), item_values[0]))
                    conn.commit()
                    messagebox.showinfo("Éxito", "Serie actualizada exitosamente.")
                    listar_series()
                    ventana_edicion.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"Error al actualizar la serie: {e}")
                finally:
                    conn.close()
        
        tk.Button(ventana_edicion, text="Guardar Cambios", command=guardar_cambios_serie).grid(row=8, column=0, columnspan=2, pady=10, padx=5)
    
    except IndexError:
        messagebox.showwarning("Advertencia", "Selecciona una serie para editar.")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Catálogo de Películas y Series")
root.configure(bg='black')
root.geometry("800x600")

# Aplicar el estilo con ttkbootstrap
style = Style(theme='darkly')

# Función para mostrar el menú de selección
def mostrar_menu_seleccion():
    seleccion_frame = tk.Frame(root, bg='black')
    seleccion_frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(seleccion_frame, text="Seleccione una opción:", bg='black', fg='white', font=('Helvetica', 16)).pack(pady=20)

    peliculas_btn = tk.Button(seleccion_frame, text="Gestionar Películas", command=lambda: abrir_gestion_peliculas(seleccion_frame), bg='#347083', fg='white', font=('Helvetica', 14))
    peliculas_btn.pack(pady=10)
    

    series_btn = tk.Button(seleccion_frame, text="Gestionar Series", command=lambda: abrir_gestion_series(seleccion_frame), bg='#347083', fg='white', font=('Helvetica', 14))
    series_btn.pack(pady=10)

def abrir_gestion_peliculas(frame):
    frame.destroy()
    gestionar_peliculas()
 # Función para editar una película al hacer doble clic
    def editar_pelicula_doble_clic(event):
        selected_item = peliculas_treeview.selection()[0]
        abrir_ventana_edicion_pelicula()

    peliculas_treeview.bind("<Double-1>", editar_pelicula_doble_clic)

def abrir_gestion_series(frame):
    frame.destroy()
    gestionar_series()
    def editar_serie_doble_clic(event):
        selected_item = series_treeview.selection()[0]
        abrir_ventana_edicion_serie()

    series_treeview.bind("<Double-1>", editar_serie_doble_clic)

def gestionar_peliculas():
    gestion_frame = tk.Frame(root, bg='black')
    gestion_frame.pack(fill=tk.BOTH, expand=True)
    
    global peliculas_treeview
    peliculas_treeview = ttk.Treeview(gestion_frame, columns=("ID", "Título", "Director", "Género", "Año"), show='headings', height=10)
    peliculas_treeview.heading("ID", text="ID")
    peliculas_treeview.heading("Título", text="Título")
    peliculas_treeview.heading("Director", text="Director")
    peliculas_treeview.heading("Género", text="Género")
    peliculas_treeview.heading("Año", text="Año")
    peliculas_treeview.pack(pady=20)

    listar_peliculas()
    
    global titulo_var, director_entry, genero_entry, año_entry
    titulo_var = tk.StringVar()
    
    tk.Label(gestion_frame, text="Título", bg='black', fg='white').pack()
    titulo_entry = tk.Entry(gestion_frame, textvariable=titulo_var)
    titulo_entry.pack()

    tk.Label(gestion_frame, text="Director", bg='black', fg='white').pack()
    director_entry = tk.Entry(gestion_frame)
    director_entry.pack()

    tk.Label(gestion_frame, text="Género", bg='black', fg='white').pack()
    genero_entry = tk.Entry(gestion_frame)
    genero_entry.pack()

    tk.Label(gestion_frame, text="Año", bg='black', fg='white').pack()
    año_entry = tk.Entry(gestion_frame)
    año_entry.pack()

    tk.Button(gestion_frame, text="Agregar Película", command=agregar_pelicula).pack(pady=5)
    tk.Button(gestion_frame, text="Editar Película", command=abrir_ventana_edicion_pelicula).pack(pady=5)
    tk.Button(gestion_frame, text="Buscar por Año", command=buscar_por_año).pack(pady=5)

def gestionar_series():
    gestion_frame = tk.Frame(root, bg='black')
    gestion_frame.pack(fill=tk.BOTH, expand=True)
    
    global series_treeview
    series_treeview = ttk.Treeview(gestion_frame, columns=("ID", "Título", "Director", "Género", "Temporadas", "Episodios", "Año Estreno", "Descripción"), show='headings', height=10)
    series_treeview.heading("ID", text="ID")
    series_treeview.heading("Título", text="Título")
    series_treeview.heading("Director", text="Director")
    series_treeview.heading("Género", text="Género")
    series_treeview.heading("Temporadas", text="Temporadas")
    series_treeview.heading("Episodios", text="Episodios")
    series_treeview.heading("Año Estreno", text="Año Estreno")
    series_treeview.heading("Descripción", text="Descripción")
    series_treeview.pack(pady=20)

    listar_series()
    
    global titulo_var, director_entry, genero_entry, temporadas_entry, episodios_entry, año_entry, descripcion_entry
    titulo_var = tk.StringVar()
    
    tk.Label(gestion_frame, text="Título", bg='black', fg='white').pack()
    titulo_entry = tk.Entry(gestion_frame, textvariable=titulo_var)
    titulo_entry.pack()

    tk.Label(gestion_frame, text="Director", bg='black', fg='white').pack()
    director_entry = tk.Entry(gestion_frame)
    director_entry.pack()

    tk.Label(gestion_frame, text="Género", bg='black', fg='white').pack()
    genero_entry = tk.Entry(gestion_frame)
    genero_entry.pack()

    tk.Label(gestion_frame, text="Temporadas", bg='black', fg='white').pack()
    temporadas_entry = tk.Entry(gestion_frame)
    temporadas_entry.pack()

    tk.Label(gestion_frame, text="Episodios", bg='black', fg='white').pack()
    episodios_entry = tk.Entry(gestion_frame)
    episodios_entry.pack()

    tk.Label(gestion_frame, text="Año Estreno", bg='black', fg='white').pack()
    año_entry = tk.Entry(gestion_frame)
    año_entry.pack()

    tk.Label(gestion_frame, text="Descripción", bg='black', fg='white').pack()
    descripcion_entry = tk.Entry(gestion_frame)
    descripcion_entry.pack()

    tk.Button(gestion_frame, text="Agregar Serie", command=agregar_serie).pack(pady=5)
    tk.Button(gestion_frame, text="Editar Serie", command=abrir_ventana_edicion_serie).pack(pady=5)

# Mostrar el menú de selección al iniciar la aplicación
mostrar_menu_seleccion()

root.mainloop()