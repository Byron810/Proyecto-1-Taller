import tkinter as tk
from tkinter import messagebox, filedialog
import json

# Función para crear la cuadrícula
def crear_cuadricula(filas, columnas, offset_row, plano):
    for i in range(filas):
        for j in range(columnas):
            # Crear una entrada en la posición (i, j)
            entrada = tk.Entry(ventana, width=5, font=('Arial', 16), justify='center')
            entrada.grid(row=i + offset_row, column=j)
            # Guardar la entrada en la cuadrícula
            cuadrícula[plano][i][j] = entrada

# Función para agregar definiciones
def agregar_definicion():
    numero = entrada_numero.get()
    definicion = entrada_definicion.get()
    entrada_numero.delete(0, tk.END)  # Limpiar la entrada
    entrada_definicion.delete(0, tk.END)  # Limpiar la entrada

    if numero and definicion:
        lista_definiciones[int(numero)] = definicion
        messagebox.showinfo("Éxito", f"Definición agregada para la palabra {numero}.")
    else:
        messagebox.showwarning("Advertencia", "Por favor, completa ambos campos.")

# Función para guardar el crucigrama en un archivo
def guardar_crucigrama():
    crucigrama = {}
    for plano in range(2):
        for i in range(6):
            for j in range(6):
                texto = cuadrícula[plano][i][j].get()
                if texto:
                    crucigrama[f"plano_{plano}_pos_{i},{j}"] = texto  # Guardar la posición y el texto

    # Guardar definiciones
    crucigrama['definiciones'] = lista_definiciones

    # Diálogo para seleccionar archivo
    archivo_guardado = filedialog.asksaveasfilename(defaultextension=".json",
                                                     filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    if archivo_guardado:
        with open(archivo_guardado, 'w') as f:
            json.dump(crucigrama, f)
        messagebox.showinfo("Éxito", "Crucigrama guardado con éxito.")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Crucigrama 3D Editable")

# Inicializar la cuadrícula
cuadrícula = [[[None for _ in range(6)] for _ in range(6)] for _ in range(2)]
crear_cuadricula(6, 6, 0, 0)  # Primer plano
crear_cuadricula(6, 6, 7, 1)  # Segundo plano (desplazado)

# Inicializar la lista de definiciones
lista_definiciones = {}

# Campo de entrada para el número de la palabra
entrada_numero = tk.Entry(ventana)
entrada_numero.grid(row=13, column=0, columnspan=3)

# Campo de entrada para la definición
entrada_definicion = tk.Entry(ventana)
entrada_definicion.grid(row=13, column=3, columnspan=3)

# Botón para agregar definición
boton_agregar_definicion = tk.Button(ventana, text="Agregar Definición", command=agregar_definicion)
boton_agregar_definicion.grid(row=14, column=0, columnspan=6)

# Botón para guardar el crucigrama
boton_guardar = tk.Button(ventana, text="Guardar Crucigrama", command=guardar_crucigrama)
boton_guardar.grid(row=15, column=0, columnspan=6)

# Etiquetas para identificar los planos
etiqueta_plano1 = tk.Label(ventana, text="Plano 1", font=('Arial', 18))
etiqueta_plano1.grid(row=0, column=0, columnspan=6)

etiqueta_plano2 = tk.Label(ventana, text="Plano 2", font=('Arial', 18))
etiqueta_plano2.grid(row=7, column=0, columnspan=6)

# Iniciar el bucle principal de la interfaz gráfica
ventana.mainloop()
