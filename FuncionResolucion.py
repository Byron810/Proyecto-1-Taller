import struct
import tkinter as tk
from tkinter import messagebox, filedialog

class LectorCrucigrama:
    def __init__(self, master):
        self.master = master
        self.filas = 0
        self.columnas = 0
        self.cuadricula = []

    def cargar_crucigrama(self, archivo):
        try:
            with open(archivo, 'rb') as f:
                # Leer el encabezado
                version = struct.unpack('B', f.read(1))[0]  # 1 byte
                dimensiones = struct.unpack('3I', f.read(12))  # 3 enteros de 4 bytes cada uno
                self.columnas, self.filas, _ = dimensiones

                # Inicializar la cuadrícula
                self.cuadricula = [["" for _ in range(self.columnas)] for _ in range(self.filas)]

                # Leer número de palabras
                numero_palabras = struct.unpack('I', f.read(4))[0]  # 1 entero de 4 bytes

                # Crear ventana para mostrar el crucigrama
                self.ventana_crucigrama = tk.Toplevel(self.master)
                self.ventana_crucigrama.title("Crucigrama Cargado")
                self.ventana_crucigrama.geometry("400x400")

                # Crear botones en la cuadrícula
                for i in range(self.filas):
                    for j in range(self.columnas):
                        boton = tk.Button(self.ventana_crucigrama, text="", width=5, height=2, bg="white")
                        boton.grid(row=i, column=j)
                        self.cuadricula[i][j] = boton

                # Leer cada palabra y su definición
                for _ in range(numero_palabras):
                    longitud_palabra = struct.unpack('B', f.read(1))[0]  # 1 byte
                    palabra = f.read(longitud_palabra).decode('utf-8')  # Cadena de texto en binario
                    longitud_definicion = struct.unpack('H', f.read(2))[0]  # 2 bytes
                    definicion = f.read(longitud_definicion).decode('utf-8')  # Cadena de texto en binario
                    posicion = struct.unpack('3I', f.read(12))  # 3 enteros de 4 bytes cada uno
                    direccion = struct.unpack('B', f.read(1))[0]  # 1 byte

                    # Colocar la palabra en la cuadrícula
                    if direccion == 0:  # Eje X
                        self.colocar_palabra(palabra, posicion[1], posicion[0], "horizontal")
                    elif direccion == 1:  # Eje Y
                        self.colocar_palabra(palabra, posicion[0], posicion[1], "vertical")

                messagebox.showinfo("Éxito", "Crucigrama cargado correctamente.")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el crucigrama: {e}")

    def colocar_palabra(self, palabra, fila, columna, direccion):
        if direccion == "horizontal":
            for k in range(len(palabra)):
                self.cuadricula[fila][columna + k]['text'] = palabra[k]
        elif direccion == "vertical":
            for k in range(len(palabra)):
                self.cuadra[fila + k][columna]['text'] = palabra[k]

    def iniciar_programa(self):
        archivo = filedialog.askopenfilename(defaultextension=".c3d", filetypes=[("Crucigramas 3D", "*.c3d")])
        if archivo:
            self.cargar_crucigrama(archivo)

# Función que se llamará desde el menú principal
def iniciar_programa(master):
    lector = LectorCrucigrama(master)
    lector.iniciar_programa()
