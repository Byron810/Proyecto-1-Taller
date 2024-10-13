import tkinter as tk
from tkinter import messagebox, filedialog
import random
import struct

class Crucigrama:
    def __init__(self, nombre, filas, columnas, master, columna_offset):
        self.nombre = nombre
        self.filas = filas
        self.columnas = columnas
        self.cuadrícula = [["" for _ in range(columnas)] for _ in range(filas)]
        self.descripciones = {}  # Diccionario para almacenar las descripciones de las palabras
        self.contador = 1  # Contador para numerar las descripciones
        self.palabras_info = []  # Lista para almacenar información de las palabras
        
        self.ventana = tk.Frame(master)  # Usar Frame para manejar la ventana del crucigrama
        self.crear_cuadricula()

        # Campo de entrada para la palabra
        self.entrada_palabra = tk.Entry(self.ventana)
        self.entrada_palabra.grid(row=filas, column=0, columnspan=columnas)

        # Campo de entrada para la descripción
        self.entrada_descripcion = tk.Entry(self.ventana)
        self.entrada_descripcion.grid(row=filas + 1, column=0, columnspan=columnas)

        # Botón para agregar la palabra y la descripción
        boton_agregar = tk.Button(self.ventana, text="Agregar Palabra", command=self.agregar_palabra)
        boton_agregar.grid(row=filas + 2, column=0, columnspan=columnas)

        # Botón para guardar el crucigrama
        boton_guardar = tk.Button(self.ventana, text="Guardar Crucigrama", command=self.guardar_crucigrama)
        boton_guardar.grid(row=filas + 3, column=0, columnspan=columnas)

        # Cuadro para mostrar las descripciones
        self.cuadro_descripcion = tk.Text(self.ventana, width=30, height=10, bg="lightgrey")
        self.cuadro_descripcion.grid(row=filas + 4, column=0, columnspan=columnas)

        # Colocar el Frame en la ventana principal
        self.ventana.grid(row=0, column=columna_offset)

    def crear_cuadricula(self):
        for i in range(self.filas):
            for j in range(self.columnas):
                # Crear un botón en la posición (i, j)
                boton = tk.Button(self.ventana, text="", width=5, height=2, bg="white")
                boton.grid(row=i, column=j)
                # Guardar el botón en la cuadrícula
                self.cuadrícula[i][j] = boton

    def puede_colocarse(self, palabra, fila, columna, direccion):
        if direccion == "horizontal":
            if columna + len(palabra) > self.columnas:  # Comprobar que no se salga
                return False
            for k in range(len(palabra)):
                # Validar que si hay letra existente, debe coincidir
                if self.cuadrícula[fila][columna + k]['text'] not in ["", palabra[k]]:
                    return False
            return True  # Se puede colocar horizontalmente
            
        elif direccion == "vertical":
            if fila + len(palabra) > self.filas:  # Comprobar que no se salga
                return False
            for k in range(len(palabra)):
                if self.cuadrícula[fila + k][columna]['text'] not in ["", palabra[k]]:
                    return False
            return True  # Se puede colocar verticalmente
        
        return False

    def colocar_palabra(self, palabra, fila, columna, direccion):
        if direccion == "horizontal":
            # Colocar el resto de la palabra
            for k in range(len(palabra)):
                self.cuadrícula[fila][columna + k]['text'] = palabra[k]  # Colocar la letra de la palabra
            tipo = "Horizontal"
        elif direccion == "vertical":        
            # Colocar el resto de la palabra
            for k in range(len(palabra)):
                self.cuadrícula[fila + k][columna]['text'] = palabra[k]  # Colocar la letra de la palabra
            tipo = "Vertical"

        # Guardar la descripción con un número y el tipo
        self.descripciones[self.contador] = (self.entrada_descripcion.get(), tipo)  
        self.palabras_info.append((palabra, self.entrada_descripcion.get(), fila, columna, direccion))  # Agregar información de la palabra
        self.mostrar_descripciones(self.contador)  # Actualizar el cuadro de descripciones
        self.contador += 1  # Incrementar el contador

    def mostrar_descripciones(self, contador_actual):
        # Obtener la descripción actual y el tipo
        descripcion_actual, tipo = self.descripciones[contador_actual]
        # Agregar la nueva descripción al final del cuadro
        if tipo == "Horizontal":
            self.cuadro_descripcion.insert(tk.END, f"H{contador_actual}. {descripcion_actual}\n")  # Insertar la nueva descripción con H
        else:
            self.cuadro_descripcion.insert(tk.END, f"V{contador_actual}. {descripcion_actual}\n")  # Insertar la nueva descripción con V

    def agregar_palabra(self):
        palabra = self.entrada_palabra.get()
        descripcion = self.entrada_descripcion.get()
        self.entrada_palabra.delete(0, tk.END)  # Limpiar la entrada de la palabra
        self.entrada_descripcion.delete(0, tk.END)  # Limpiar la entrada de la descripción

        # Intentar acomodar la palabra
        for i in range(self.filas):
            for j in range(self.columnas):
                # Probar colocación horizontal
                if len(palabra) <= self.columnas and self.puede_colocarse(palabra, i, j, "horizontal"):
                    self.colocar_palabra(palabra, i, j, "horizontal")
                    return

                # Probar colocación vertical
                if len(palabra) <= self.filas and self.puede_colocarse(palabra, i, j, "vertical"):
                    self.colocar_palabra(palabra, i, j, "vertical")
                    return

        messagebox.showinfo("Error", "No se pudo acomodar la palabra en la cuadrícula.")

    def guardar_crucigrama(self):
        # Abrir diálogo para guardar archivo
        archivo_guardar = filedialog.asksaveasfilename(defaultextension=".c3d", filetypes=[("Crucigramas 3D", "*.c3d")])
        if not archivo_guardar:
            return  # Si el usuario cancela, no hacer nada

        # Guardar en formato binario
        with open(archivo_guardar, "wb") as archivo:
           

            # Escribir la versión del formato
            version = 1
            archivo.write(struct.pack('B', version))  # 1 byte

            # Escribir dimensiones
            archivo.write(struct.pack('iii', self.columnas, self.filas, 1))  # Dimensiones X, Y, Z

            # Escribir número de palabras
            num_palabras = len(self.palabras_info)
            archivo.write(struct.pack('i', num_palabras))  # Número total de palabras

            for palabra, definicion, fila, columna, direccion in self.palabras_info:
                # Longitud de la palabra
                longitud_palabra = len(palabra)
                archivo.write(struct.pack('B', longitud_palabra))  # 1 byte
                archivo.write(palabra.encode('utf-8'))  # Palabra en bytes

                # Longitud de la definición
                longitud_definicion = len(definicion)
                archivo.write(struct.pack('H', longitud_definicion))  # 2 bytes
                archivo.write(definicion.encode('utf-8'))  # Definición en bytes

                # Posición inicial (X, Y, Z)
                archivo.write(struct.pack('iii', columna, fila, 0))  # Posición inicial (X, Y, Z)

                # Dirección de la palabra
                direccion_num = 0 if direccion == "horizontal" else 1
                archivo.write(struct.pack('B', direccion_num))  # 1 byte

class App:
    def __init__(self):
        self.ventana_principal = tk.Tk()
        self.ventana_principal.title("Crucigramas 3D")

        # Crear un Frame para la línea separadora
        self.frame_linea = tk.Frame(self.ventana_principal, width=2, bg="black")
        self.frame_linea.grid(row=0, column=1, sticky="ns")  # Colocar en columna 1 y estirarlo verticalmente

        # Crear dos crucigramas, uno en cada columna
        self.crucigrama_xy = Crucigrama("xy", 6, 6, self.ventana_principal, columna_offset=0)
        self.crucigrama_xz = Crucigrama("xz", 6, 6, self.ventana_principal, columna_offset=2)

        self.ventana_principal.mainloop()

if __name__ == "__main__":
    App()
