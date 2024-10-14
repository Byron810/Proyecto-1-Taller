import struct
import tkinter as tk
from tkinter import filedialog, messagebox
import FuncionResolver as resolver

def leer_crucigrama(archivo):
    """
    Lee la información de un crucigrama desde un archivo binario.

    Args:
        archivo (str): Nombre del archivo binario que contiene el crucigrama.
    
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
            palabra = archivo.read(longitud_palabra).decode('ascii')
            longitud_definicion = struct.unpack('H', archivo.read(2))[0]
            definicion = archivo.read(longitud_definicion).decode('ascii')
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
        x, y, _ = posicion
        if direccion == 0:  # Horizontal
            for i, letra in enumerate(palabra):
                if x + i < dimension_x1:
                    celdas1[y][x + i].config(text=letra)
        elif direccion == 1:  # Vertical
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
        x, y, _ = posicion
        if direccion == 0:  # Horizontal
            for i, letra in enumerate(palabra):
                if x + i < dimension_x2:
                    celdas2[y][x + i].config(text=letra)
        elif direccion == 1:  # Vertical
            for i, letra in enumerate(palabra):
                if y + i < dimension_y2:
                    celdas2[y + i][x].config(text=letra)

    # Ejecutar el bucle principal de la ventana
    ventana.mainloop()

def cargar_crucigramas():
    """Cargar dos crucigramas a partir de archivos seleccionados."""
    # Seleccionar el primer archivo
    archivo1 = filedialog.askopenfilename(
        title="Seleccionar archivo de crucigrama 1",
        filetypes=[("Archivos de Crucigrama", "*.C3D")]
    )

    if archivo1:
        try:
            version1, dimensiones1, palabras1 = leer_crucigrama(archivo1)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo 1: {str(e)}")
            return

        # Seleccionar el segundo archivo
        archivo2 = filedialog.askopenfilename(
            title="Seleccionar archivo de crucigrama 2",
            filetypes=[("Archivos de Crucigrama", "*.C3D")]
        )

        if archivo2:
            try:
                version2, dimensiones2, palabras2 = leer_crucigrama(archivo2)
                crear_ventana_crucigramas(dimensiones1, palabras1, dimensiones2, palabras2)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo 2: {str(e)}")

def iniciar_programa():
    """Función principal para iniciar el programa."""
    ventana = tk.Tk()
    ventana.title("Menú Principal")
    
    # Botón para cargar crucigramas
    btn_cargar = tk.Button(ventana, text="Cargar Crucigramas", command=cargar_crucigramas)
    btn_cargar.pack(pady=20)

    # Ejecutar el bucle principal de la ventana
    ventana.mainloop()

# Llama a iniciar_programa en el módulo principal
if __name__ == "__main__":
    iniciar_programa()

    
