import struct
import tkinter as tk
from tkinter import filedialog, messagebox


def leer_crucigrama(archivo):
    """
    Lee la información de un crucigrama desde un archivo binario.

    Args:
        nombre_archivo (str): Nombre del archivo binario que contiene el crucigrama.
    
    Returns:
        tuple: Contiene la versión, las dimensiones y la lista de palabras.
    """
    with open(archivo, 'rb') as archivo:
        # Leer el encabezado
        version = struct.unpack('B', archivo.read(1))[0]
        dimension_x = struct.unpack('i', archivo.read(4))[0]
        dimension_y = struct.unpack('i', archivo.read(4))[0]
        dimension_z = struct.unpack('i', archivo.read(4))[0]
        num_palabras = struct.unpack('I', archivo.read(4))[0]

        palabras = []
        for _ in range(num_palabras):
            longitud_palabra = struct.unpack('B', archivo.read(1))[0]
            palabra = archivo.read(longitud_palabra).decode('ascii')  # Leer la palabra (n bytes)
            longitud_definicion = struct.unpack('H', archivo.read(2))[0]
            definicion = archivo.read(longitud_definicion).decode('ascii')  # Leer la definición (n bytes)
            posicion_x = struct.unpack('i', archivo.read(4))[0]
            posicion_y = struct.unpack('i', archivo.read(4))[0]
            posicion_z = struct.unpack('i', archivo.read(4))[0]
            direccion = struct.unpack('B', archivo.read(1))[0]
            palabras.append((palabra, definicion, (posicion_x, posicion_y, posicion_z), direccion))

    return version, (dimension_x, dimension_y, dimension_z), palabras

def crear_ventana_crucigramas(dimensiones1, palabras1, dimensiones2, palabras2):
    # Crear la ventana principal de Tkinter
    ventana = tk.Tk()
    ventana.title("Crucigramas en paralelo")
    
    # Crear un marco para cada crucigrama
    marco1 = tk.Frame(ventana)
    marco1.grid(row=0, column=0, padx=10, pady=10)
    
    marco2 = tk.Frame(ventana)
    marco2.grid(row=0, column=1, padx=10, pady=10)

    # Crear la cuadrícula para el primer crucigrama
    dimension_x1, dimension_y1, _ = dimensiones1
    celdas1 = [[tk.Label(marco1, text=" ", width=3, height=2, borderwidth=1, relief="solid", font=("Helvetica", 16)) 
                for _ in range(dimension_y1)] for _ in range(dimension_x1)]
    
    # Colocar cada etiqueta en su posición dentro de la cuadrícula del primer crucigrama
    for i in range(dimension_x1):
        for j in range(dimension_y1):
            celdas1[i][j].grid(row=i, column=j)
    
    # Colocar las palabras en la cuadrícula del primer crucigrama
    for palabra, _, posicion, direccion in palabras1:
        x, y, _ = posicion  # Ignoramos Z en este ejemplo de 2D
        if direccion == 0:  # Horizontal (eje X)
            for i, letra in enumerate(palabra):
                if x + i < dimension_x1:
                    celdas1[y][x + i].config(text=letra)
        elif direccion == 1:  # Vertical (eje Y)
            for i, letra in enumerate(palabra):
                if y + i < dimension_y1:
                    celdas1[y + i][x].config(text=letra)

    # Crear la cuadrícula para el segundo crucigrama
    dimension_x2, dimension_y2, _ = dimensiones2
    celdas2 = [[tk.Label(marco2, text=" ", width=3, height=2, borderwidth=1, relief="solid", font=("Helvetica", 16)) 
                for _ in range(dimension_y2)] for _ in range(dimension_x2)]
    
    # Colocar cada etiqueta en su posición dentro de la cuadrícula del segundo crucigrama
    for i in range(dimension_x2):
        for j in range(dimension_y2):
            celdas2[i][j].grid(row=i, column=j)
    
    # Colocar las palabras en la cuadrícula del segundo crucigrama
    for palabra, _, posicion, direccion in palabras2:
        x, y, _ = posicion  # Ignoramos Z en este ejemplo de 2D
        if direccion == 0:  # Horizontal (eje X)
            for i, letra in enumerate(palabra):
                if x + i < dimension_x2:
                    celdas2[y][x + i].config(text=letra)
        elif direccion == 1:  # Vertical (eje Y)
            for i, letra in enumerate(palabra):
                if y + i < dimension_y2:
                    celdas2[y + i][x].config(text=letra)

    # Ejecutar el bucle principal de la ventana
    ventana.mainloop()

# Leer los archivos de los dos crucigramas


"""Función para seleccionar archivo"""
archivo = filedialog.askopenfilename(
    title="Seleccionar archivo de crucigrama",
    filetypes=[("Text Files", "*.C3D")]
)

if archivo:
    try:
        version1, dimensiones1, palabras1 = leer_crucigrama(archivo)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")

archivo = filedialog.askopenfilename(
    title="Seleccionar archivo de crucigrama",
    filetypes=[("Text Files", "*.C3D")]
)

if archivo:
    try:
        version2, dimensiones2, palabras2 = leer_crucigrama(archivo)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")




# Crear la ventana con ambos crucigramas
crear_ventana_crucigramas(dimensiones1, palabras1, dimensiones2, palabras2)



def iniciar_programa(ventana_existente):
    """ Función principal para iniciar el programa"""
    global ventana
    ventana = ventana_existente
    
    if messagebox.askyesno("Cargar crucigrama", "¿Deseas cargar un archivo de crucigrama?"):
        crear_ventana_crucigramas()

# Llama a iniciar_programa en el módulo principal