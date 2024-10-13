import tkinter as tk
import struct
from tkinter import filedialog, messagebox

DIMENSIONES = 6
crucigrama_3d = {}

def guardar_crucigrama():
    """Función para guardar el crucigrama en formato binario"""
    archivo = filedialog.asksaveasfilename(defaultextension=".c3d", filetypes=[("C3D files", "*.c3d")])
    if archivo:
        try:
            with open(archivo, 'wb') as file:
                # Encabezado
                version = 1
                file.write(struct.pack('B', version))  # Versión del formato
                file.write(struct.pack('iii', DIMENSIONES, DIMENSIONES, DIMENSIONES))  # Dimensiones X, Y, Z
                
                # Recopilar palabras y definiciones
                palabras = []  # Lista de tuplas (palabra, definición, (x, y, z), dirección)
                
                # Agregar tus palabras aquí manualmente para la prueba
                palabras.append(("PYTHON", "Lenguaje de programación", (0, 1, 0), 0))  # Ejemplo
                palabras.append(("CODE", "Escribir programas", (4, 0, 0), 1))  # Ejemplo
                
                num_palabras = len(palabras)
                file.write(struct.pack('i', num_palabras))  # Número total de palabras
                
                for palabra, definicion, (x, y, z), direccion in palabras:
                    longitud_palabra = len(palabra)
                    longitud_definicion = len(definicion)
                    file.write(struct.pack('B', longitud_palabra))  # Longitud de la palabra
                    file.write(palabra.encode('utf-8'))  # Palabra
                    file.write(struct.pack('H', longitud_definicion))  # Longitud de la definición
                    file.write(definicion.encode('utf-8'))  # Definición
                    file.write(struct.pack('iiiB', x, y, z, direccion))  # Posición inicial y dirección

            messagebox.showinfo("Éxito", "Crucigrama guardado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo: {str(e)}")

def iniciar_ventana_edicion():
    ventana = tk.Tk()
    ventana.title("Editor de Crucigrama")
    
    # Botón para guardar el crucigrama
    boton_guardar = tk.Button(ventana, text="Guardar Crucigrama", command=guardar_crucigrama)
    boton_guardar.pack(pady=10)
    
    ventana.mainloop()

if __name__ == "__main__":
    iniciar_ventana_edicion()
