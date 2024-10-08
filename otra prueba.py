import os
import tkinter as tk

# Función para limpiar consola (sólo para uso fuera de Tkinter)
def limpiar_consola():
    os.system("cls" if os.name == "nt" else "clear")

# Función para leer crucigrama guardado desde un archivo
def leer_crucigrama_guardado():
    """
    Lee un crucigrama guardado en un archivo de texto y devuelve una lista de palabras,
    definiciones y los ejes en que se deben colocar.
    """
    
    try:
        with open("palabras.txt", "r") as archivo:
            crucigrama = []
            for linea in archivo:
                palabra, definicion, eje = linea.strip().split(',')
                crucigrama.append((palabra, definicion, eje))
            return crucigrama
    except FileNotFoundError:
        print("No se encontró un archivo de crucigrama guardado.")
        return None

# Modo creación de crucigramas
def modo_creacion():
    """
    Función que inicia el modo de creación de crucigramas 3D.
    Permite al usuario definir dimensiones y añadir palabras o cargar un crucigrama existente.
    """
    

    # Si no se carga un crucigrama, procede con la creación
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
            definicion = input("Ingrese la definición: ")
            eje = input("Ingrese el eje en el que quiere que se coloque la palabra (X, Y, Z): ")
            limpiar_consola()
            palabras_definiciones.write(f"{palabra},{definicion},{cuadricula},{eje}\n")

    # Iniciar la creación del crucigrama
    crear_crucigrama(int(cuadricula))

# Crear ventana principal del crucigrama
def crear_crucigrama(dimensiones, crucigrama_cargado=None):
    """
    Función para crear la ventana del crucigrama y mostrarla.
    Si se pasa un crucigrama cargado, se insertan las palabras en las posiciones correspondientes.
    """
    global DIMENSIONES, ventana, crucigrama_3d, eje_actual
    DIMENSIONES = dimensiones
    ventana = tk.Tk()
    ventana.title("Crucigrama 3D")
    eje_actual = "XY"  # Por defecto, empieza mostrando el plano X-Y
    crucigrama_3d = {}

    # Si hay un crucigrama cargado, se colocan las palabras
    if crucigrama_cargado:
        for palabra, definicion, cuadricula, eje in crucigrama_cargado:
            colocar_palabra_en_crucigrama(palabra, eje)

    mostrar_plano(eje_actual)

# Función para colocar una palabra en el crucigrama basado en su eje
def colocar_palabra_en_crucigrama(palabra, eje):
    """
    Coloca la palabra en el crucigrama 3D según el eje dado (X, Y o Z).
    """
    longitud = len(palabra)
    
    if eje.upper() == "X":
        for i, letra in enumerate(palabra):
            crucigrama_3d[(i, 0, 0)] = letra  # Coloca la palabra a lo largo del eje X, en (i, 0, 0)
    elif eje.upper() == "Y":
        for i, letra in enumerate(palabra):
            crucigrama_3d[(0, i, 0)] = letra  # Coloca la palabra a lo largo del eje Y, en (0, i, 0)
    elif eje.upper() == "Z":
        for i, letra in enumerate(palabra):
            crucigrama_3d[(0, 0, i)] = letra  # Coloca la palabra a lo largo del eje Z, en (0, 0, i)

# Función para mostrar el plano actual en Tkinter
def mostrar_plano(eje):
    # Limpiar la ventana de cualquier widget existente
    for widget in ventana.winfo_children():
        widget.destroy()

    # Mostrar el plano actual según el eje seleccionado
    if eje == "XY":
        for x in range(DIMENSIONES):
            for y in range(DIMENSIONES):
                valor = crucigrama_3d.get((x, y, 0), "")
                entrada = tk.Entry(ventana, width=3, justify='center')
                entrada.grid(row=x, column=y)
                entrada.insert(0, valor)

                def actualizar_celda(event, x=x, y=y):
                    crucigrama_3d[(x, y, 0)] = event.widget.get()

                entrada.bind("<KeyRelease>", actualizar_celda)
    elif eje == "YZ":
        for y in range(DIMENSIONES):
            for z in range(DIMENSIONES):
                valor = crucigrama_3d.get((0, y, z), "")
                entrada = tk.Entry(ventana, width=3, justify='center')
                entrada.grid(row=y, column=z)
                entrada.insert(0, valor)

                def actualizar_celda(event, y=y, z=z):
                    crucigrama_3d[(0, y, z)] = event.widget.get()

                entrada.bind("<KeyRelease>", actualizar_celda)

    # Botones para cambiar entre ejes XY y YZ
    boton_cambiar_xy = tk.Button(ventana, text="Eje XY", command=lambda: cambiar_plano("XY"))
    boton_cambiar_xy.grid(row=DIMENSIONES, column=0)

    boton_cambiar_yz = tk.Button(ventana, text="Eje YZ", command=lambda: cambiar_plano("YZ"))
    boton_cambiar_yz.grid(row=DIMENSIONES, column=1)

    label_plano = tk.Label(ventana, text=f"Mostrando eje {eje}")
    label_plano.grid(row=DIMENSIONES, column=2, columnspan=2)

# Función para cambiar el plano (XY o YZ)
def cambiar_plano(nuevo_eje):
    global eje_actual
    eje_actual = nuevo_eje
    mostrar_plano(eje_actual)

# Verificar si las palabras se cruzan correctamente
def verificar_cruces(crucigrama):
    """
    Verifica que haya cruces entre las palabras en el crucigrama.
    Si no los hay, informa al usuario.
    """
    cruces = False
    posiciones = set()

    for palabra, definicion, eje in crucigrama:
        if eje.upper() == "X":
            for i in range(len(palabra)):
                if (i, 0, 0) in posiciones:
                    cruces = True
                posiciones.add((i, 0, 0))
        elif eje.upper() == "Y":
            for i in range(len(palabra)):
                if (0, i, 0) in posiciones:
                    cruces = True
                posiciones.add((0, i, 0))
        elif eje.upper() == "Z":
            for i in range(len(palabra)):
                if (0, 0, i) in posiciones:
                    cruces = True
                posiciones.add((0, 0, i))

    if not cruces:
        print("No hay palabras que se crucen en el crucigrama.")

def salir():
    ventana.quit()

# Función para mostrar el menú principal usando Tkinter
def menu_principal():
    ventana = tk.Tk()
    ventana.title("Menú Principal - Crucigramas 3D")
    ventana.geometry("300x200")  # Tamaño de la ventana

    # Crear título
    label_titulo = tk.Label(ventana, text="---Crucigramas---", font=("Arial", 16))
    label_titulo.pack(pady=10)

    # Crear botones del menú principal
    boton_creacion = tk.Button(ventana, text="Modo Creación", width=20, command=modo_creacion)
    boton_creacion.pack(pady=5)

    boton_resolucion = tk.Button(ventana, text="Modo Resolución", width=20, command=leer_crucigrama_guardado)
    boton_resolucion.pack(pady=5)

    boton_salir = tk.Button(ventana, text="Salir", width=20, command=salir)
    boton_salir.pack(pady=5)

    # Ejecutar el bucle principal de Tkinter
    ventana.mainloop()

# Ejecutar ventana 
if __name__ == "__main__":
    menu_principal()
    # Iniciar el bucle de eventos de Tkinter si se crea la ventana
    tk.mainloop()
