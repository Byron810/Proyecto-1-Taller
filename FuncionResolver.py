import struct
import tkinter as tk
from tkinter import filedialog, messagebox
import FuncionLectura as FL
import MenuPrincipal

def leer_crucigrama(archivo):
    """
    Lee la información de un crucigrama desde un archivo binario.
    """
    with open(archivo, 'rb') as archivo:
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
    ventana = tk.Tk()
    ventana.title("Crucigramas en paralelo")
    ventana.geometry("1600x900")
    
    marco1 = tk.Frame(ventana)
    marco1.grid(row=0, column=0, padx=10, pady=10)
    
    marco2 = tk.Frame(ventana)
    marco2.grid(row=0, column=1, padx=10, pady=10)

    # Crear cuadrículas editables para el primer crucigrama
    dimension_x1, dimension_y1, _ = dimensiones1
    celdas1 = [[tk.Entry(marco1, width=3, font=("Helvetica", 16), justify='center') 
                for _ in range(dimension_y1)] for _ in range(dimension_x1)]
    
    for i in range(dimension_x1):
        for j in range(dimension_y1):
            celdas1[i][j].grid(row=i, column=j)

    # Crear cuadrículas editables para el segundo crucigrama
    dimension_x2, dimension_y2, _ = dimensiones2
    celdas2 = [[tk.Entry(marco2, width=3, font=("Helvetica", 16), justify='center') 
                for _ in range(dimension_y2)] for _ in range(dimension_x2)]
    
    for i in range(dimension_x2):
        for j in range(dimension_y2):
            celdas2[i][j].grid(row=i, column=j)

    # Botón para validar respuestas
    btn_validar1 = tk.Button(ventana, text="Validar Crucigrama 1", command=lambda: validar_crucigrama(celdas1, palabras1))
    btn_validar1.grid(row=1, column=0, pady=10)
    
    btn_validar2 = tk.Button(ventana, text="Validar Crucigrama 2", command=lambda: validar_crucigrama(celdas2, palabras2))
    btn_validar2.grid(row=1, column=1, pady=10)

    # Botón para ver la resolución
    boton_ver_resolucion = tk.Button(ventana, text="Ver Resolución", width=20, command=FL.iniciar_programa)  # Sin paréntesis
    boton_ver_resolucion.grid(row=1, column=2, pady=10)

    boton_salir = tk.Button(ventana, text="Salir", width=20, command=MenuPrincipal.menu_principal)
    boton_salir.grid(row=1, column=3, pady=10)

    ventana.mainloop()

def validar_crucigrama(celdas, palabras):
    """Valida si las entradas del crucigrama son correctas."""
    errores = []
    
    for palabra, _, posicion, direccion in palabras:
        x, y, _ = posicion
        if direccion == 0:  # Horizontal
            for i, letra in enumerate(palabra):
                if celdas[y][x + i].get().strip().lower() != letra.lower():
                    errores.append(f"Error en ({y+1}, {x+i+1})")
        elif direccion == 1:  # Vertical
            for i, letra in enumerate(palabra):
                if celdas[y + i][x].get().strip().lower() != letra.lower():
                    errores.append(f"Error en ({y+i+1}, {x+1})")

    if errores:
        messagebox.showerror("Errores", "\n".join(errores))
    else:
        messagebox.showinfo("Correcto", "¡Todos los campos son correctos!")

def cargar_crucigramas():
    """Cargar dos crucigramas a partir de archivos seleccionados."""
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
    ventana.geometry("1600x900")
    
    btn_cargar = tk.Button(ventana, text="Cargar Crucigramas", command=cargar_crucigramas)
    btn_cargar.pack(pady=20)

    ventana.mainloop()

if __name__ == "__main__":
    iniciar_programa()
