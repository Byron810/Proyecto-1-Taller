import os
import tkinter as tk

# Función para limpiar consola (sólo para uso fuera de Tkinter)
def limpiar_consola():
    os.system("cls" if os.name == "nt" else "clear")

# Modo creación de crucigramas
def modo_creacion():
    """
    Función que inicia el modo de creación de crucigramas 3D.
    Permite al usuario definir dimensiones y añadir palabras.
    """
    while True:
        print("Dimensiones:\n1 - 6x6x6 \n2 - 7x7x7 \n3 - 8x8x8")
        cuadricula = input("Ingrese las dimensiones de la cuadricula: ")
        limpiar_consola()
        
        if cuadricula == "1":
            cuadricula = 6
            break
        elif cuadricula == "2":
            cuadricula = 7
            break
        elif cuadricula == "3":
            cuadricula = 8
            break
        else:
            print("Opción no válida. Intente de nuevo.")
   
    with open("palabras.txt", "a") as palabras_definiciones:
        for i in range(int(cuadricula)):  # La cantidad de palabras la define la cuadricula
            palabra = input("Ingresa una palabra: ")
            definicion = input("Ingrese la definicion: ")
            eje = input("Ingrese el eje en el que quiere que se coloque la palabra (X, Y, Z): ")
            limpiar_consola()
            palabras_definiciones.write(f"{palabra},{definicion},{eje}\n")

    # Iniciar la creación del crucigrama
    crear_crucigrama(int(cuadricula))

# Crear ventana principal del crucigrama
def crear_crucigrama(dimensiones):
    global DIMENSIONES, ventana, crucigrama_3d, z_actual
    DIMENSIONES = dimensiones
    ventana = tk.Tk()
    ventana.title("Crucigrama 3D")
    z_actual = 0
    crucigrama_3d = {}
    mostrar_plano(z_actual)

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

# Menú principal (no utilizado con Tkinter, solo ejemplo)
def menu_principal():
    """
    Función para mostrar el menú principal del juego y permitir al usuario
    elegir entre crear un crucigrama, resolver un crucigrama o salir.
    """
    print("---Crucigramas---\n\nMenu Principal \n1 - Modo Creacion \n2 - Modo Resolucion")
    modo_creacion()

# Ejecutar ventana y mostrar el primer plano (Z=0)
if __name__ == "__main__":
    menu_principal()
    # Iniciar el bucle de eventos de Tkinter si se crea la ventana
    ventana.mainloop()
