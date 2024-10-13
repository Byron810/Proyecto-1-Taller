import struct
import tkinter as tk
from tkinter import filedialog, messagebox
import struct

DIMENSIONES = None
ventana = None
crucigrama_3d = {}
z_actual = 0
vista_actual = 'XY'  # Para controlar la vista actual: 'XY' o 'YZ'

def seleccionar_archivo():
    """Función para seleccionar archivo"""
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo de crucigrama",
        filetypes=[("C3D Files", "*.c3d")]
    )
    
    if archivo:
        try:
            cargar_crucigrama(archivo)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")

def cargar_crucigrama(ruta):
    """Cargar el archivo de crucigrama y convertirlo a estructura"""
    global crucigrama_3d, DIMENSIONES
    with open(ruta, 'rb') as file:
        # Leer versión del formato (1 byte)
        version = struct.unpack('B', file.read(1))[0]
        
        if version != 1:
            raise ValueError("Versión de archivo no compatible.")
        
        # Leer las dimensiones X, Y, Z (3 enteros)
        DIMENSIONES = struct.unpack('iii', file.read(12))
        x_dim, y_dim, z_dim = DIMENSIONES
        
        # Inicializar el diccionario del crucigrama 3D vacío
        crucigrama_3d = {(x, y, z): " " for x in range(x_dim) for y in range(y_dim) for z in range(z_dim)}
        
        # Leer el número de palabras (1 entero)
        num_palabras = struct.unpack('i', file.read(4))[0]
        
        # Leer cada palabra y su información
        for _ in range(num_palabras):
            # Longitud de la palabra (1 byte)
            longitud_palabra = struct.unpack('B', file.read(1))[0]
            # Palabra
            palabra = file.read(longitud_palabra).decode('utf-8')
            
            # Longitud de la definición (2 bytes)
            longitud_definicion = struct.unpack('H', file.read(2))[0]
            # Definición
            definicion = file.read(longitud_definicion).decode('utf-8')
            
            # Leer posición inicial (x, y, z) y dirección (1 byte)
            x, y, z, direccion = struct.unpack('iiiB', file.read(13))
            
            # Insertar la palabra en el crucigrama_3d
            insertar_palabra(palabra, x, y, z, direccion)
    
    crear_crucigrama(x_dim)  # Crear la ventana con las dimensiones del crucigrama

def insertar_palabra(palabra, x, y, z, direccion):
    """Inserta una palabra en el crucigrama_3d en la posición y dirección dadas"""
    global crucigrama_3d
    if direccion == 0:  # Dirección 0 significa horizontal (en X)
        for i, letra in enumerate(palabra):
            crucigrama_3d[(x + i, y, z)] = letra
    elif direccion == 1:  # Dirección 1 significa vertical (en Y)
        for i, letra in enumerate(palabra):
            crucigrama_3d[(x, y + i, z)] = letra

def crear_crucigrama(dimensiones):
    """Iniciar la creación del crucigrama"""
    global DIMENSIONES, ventana, crucigrama_3d, z_actual, vista_actual
    DIMENSIONES = dimensiones
    z_actual = 0
    vista_actual = 'XY'  # Comenzamos con la vista inicial en X-Y

    # Limpiar ventana existente
    for widget in ventana.winfo_children():
        widget.destroy()

    mostrar_plano(z_actual)  # Mostrar automáticamente el plano inicial (X-Y)

def mostrar_plano(z):
    """ Mostrar el plano actual del crucigrama en la interfaz"""
    global crucigrama_3d, DIMENSIONES, z_actual, vista_actual
    z_actual = z

    # Limpiar ventana para actualizar
    for widget in ventana.winfo_children():
        widget.destroy()

    if vista_actual == 'XY':
        label_plano = tk.Label(ventana, text=f"Plano Z = {z_actual} (Vista X-Y)", font=("Arial", 14))
        label_plano.grid(row=0, column=0, columnspan=DIMENSIONES)

        # Mostrar la capa X-Y correspondiente en una tabla de botones
        for x in range(DIMENSIONES):
            for y in range(DIMENSIONES):
                letra = crucigrama_3d.get((x, y, z), " ")
                boton = tk.Button(ventana, text=letra, width=4, height=2)
                boton.grid(row=x + 1, column=y)

    elif vista_actual == 'YZ':
        label_plano = tk.Label(ventana, text=f"Vista Y-Z en X = {z_actual}", font=("Arial", 14))
        label_plano.grid(row=0, column=0, columnspan=DIMENSIONES)

        # Mostrar el plano Y-Z correspondiente en una tabla de botones (rotado)
        for y in range(DIMENSIONES):
            for z in range(len(crucigrama_3d)):
                letra = crucigrama_3d.get((z_actual, y, z), " ")
                boton = tk.Button(ventana, text=letra, width=4, height=2)
                boton.grid(row=y + 1, column=z)

    btn_anterior = tk.Button(ventana, text="Plano Anterior", command=plano_anterior)
    btn_anterior.grid(row=DIMENSIONES + 1, column=0)

    btn_siguiente = tk.Button(ventana, text="Plano Siguiente", command=plano_siguiente)
    btn_siguiente.grid(row=DIMENSIONES + 1, column=1)

    btn_rotar = tk.Button(ventana, text="Cambiar Vista", command=cambiar_vista)
    btn_rotar.grid(row=DIMENSIONES + 1, column=2)

def plano_anterior():
    """ Cambiar al plano anterior en Z"""
    global z_actual
    if z_actual > 0:
        z_actual -= 1
        mostrar_plano(z_actual)

def plano_siguiente():
    """ Cambiar al siguiente plano en Z"""
    global z_actual, crucigrama_3d
    if z_actual < DIMENSIONES - 1:
        z_actual += 1
        mostrar_plano(z_actual)

def cambiar_vista():
    """Cambiar entre las vistas X-Y y Y-Z"""
    global vista_actual
    if vista_actual == 'XY':
        vista_actual = 'YZ'
    else:
        vista_actual = 'XY'
    mostrar_plano(z_actual)

def iniciar_programa(ventana_existente):
    """ Función principal para iniciar el programa"""
    global ventana
    ventana = ventana_existente
    
    if messagebox.askyesno("Cargar crucigrama", "¿Deseas cargar un archivo de crucigrama?"):
        seleccionar_archivo()

# Llama a iniciar_programa en el módulo principal
