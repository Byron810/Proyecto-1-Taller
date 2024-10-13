import tkinter as tk
from tkinter import messagebox

# Función para crear la cuadrícula
def crear_cuadricula(filas, columnas):
    for i in range(filas):
        for j in range(columnas):
            # Crear un botón en la posición (i, j)
            boton = tk.Button(ventana, text="", width=5, height=2, bg="white")
            boton.grid(row=i, column=j)
            # Guardar el botón en la cuadrícula
            cuadrícula[i][j] = boton

# Función para verificar si la palabra puede colocarse
def puede_colocarse(palabra, fila, columna, direccion):
    if direccion == "horizontal":
        if columna + len(palabra) > 6:  # Comprobar que no se salga
            return False
        for k in range(len(palabra)):
            if cuadrícula[fila][columna + k]['text'] not in ["", palabra[k]]:
                return False
    elif direccion == "vertical":
        if fila + len(palabra) > 6:  # Comprobar que no se salga
            return False
        for k in range(len(palabra)):
            if cuadrícula[fila + k][columna]['text'] not in ["", palabra[k]]:
                return False
    return True

# Función para colocar la palabra en la cuadrícula
def colocar_palabra(palabra, fila, columna, direccion):
    if direccion == "horizontal":
        for k in range(len(palabra)):
            cuadrícula[fila][columna + k]['text'] = palabra[k]
    elif direccion == "vertical":
        for k in range(len(palabra)):
            cuadrícula[fila + k][columna]['text'] = palabra[k]

# Función para agregar la palabra a la cuadrícula
def agregar_palabra():
    palabra = entrada_palabra.get()
    entrada_palabra.delete(0, tk.END)  # Limpiar la entrada

    # Intentar acomodar la palabra
    for i in range(6):
        for j in range(6):
            # Probar colocación horizontal
            if puede_colocarse(palabra, i, j, "horizontal"):
                colocar_palabra(palabra, i, j, "horizontal")
                return
            
            # Probar colocación vertical
            if puede_colocarse(palabra, i, j, "vertical"):
                colocar_palabra(palabra, i, j, "vertical")
                return

    messagebox.showinfo("Error", "No se pudo acomodar la palabra en la cuadrícula.")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Crucigrama 6x6")

# Inicializar la cuadrícula
cuadrícula = [["" for _ in range(6)] for _ in range(6)]
crear_cuadricula(6, 6)

# Campo de entrada para la palabra
entrada_palabra = tk.Entry(ventana)
entrada_palabra.grid(row=7, column=0, columnspan=6)

# Botón para agregar la palabra
boton_agregar = tk.Button(ventana, text="Agregar Palabra", command=agregar_palabra)
boton_agregar.grid(row=8, column=0, columnspan=6)

# Iniciar el bucle principal de la interfaz gráfica
ventana.mainloop()
