import tkinter as tk

# Tamaño del crucigrama (6x6x6 por defecto)
DIMENSIONES = 6

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Crucigrama 3D")

# Variable para almacenar el plano z actual
z_actual = 0

# Cuadro 3D: Diccionario que almacena cada celda en formato {(x, y, z): valor}
crucigrama_3d = {}

# Función para mostrar el plano actual en Tkinter
def mostrar_plano(z):
    # Limpiar la ventana de cualquier widget existente
    for widget in ventana.winfo_children():
        widget.destroy()

    # Mostrar el plano actual
    for x in range(DIMENSIONES):
        for y in range(DIMENSIONES):
            # Obtener el valor actual de la celda (vacía si no tiene valor)
            valor = crucigrama_3d.get((x, y, z), "")

            # Crear una entrada de texto para cada celda
            entrada = tk.Entry(ventana, width=3, justify='center')
            entrada.grid(row=x, column=y)
            entrada.insert(0, valor)

            # Función para actualizar el valor de la celda
            def actualizar_celda(event, x=x, y=y, z=z):
                crucigrama_3d[(x, y, z)] = event.widget.get()

            # Vincular la actualización de la celda al evento de escritura
            entrada.bind("<KeyRelease>", actualizar_celda)

    # Botones para navegar entre planos
    boton_arriba = tk.Button(ventana, text="Plano Z+", command=lambda: cambiar_plano(1))
    boton_arriba.grid(row=DIMENSIONES, column=0)

    boton_abajo = tk.Button(ventana, text="Plano Z-", command=lambda: cambiar_plano(-1))
    boton_abajo.grid(row=DIMENSIONES, column=1)

    label_plano = tk.Label(ventana, text=f"Plano Z = {z}")
    label_plano.grid(row=DIMENSIONES, column=2, columnspan=2)

# Función para cambiar el plano en el eje Z
def cambiar_plano(direccion):
    global z_actual
    z_actual += direccion
    z_actual = max(0, min(DIMENSIONES - 1, z_actual))  # Mantener z en el rango permitido
    mostrar_plano(z_actual)

# Mostrar el primer plano (Z=0)
mostrar_plano(z_actual)

# Ejecutar la ventana
ventana.mainloop()

