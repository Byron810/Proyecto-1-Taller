import tkinter as tk
from tkinter import filedialog, messagebox

DIMENSIONES = None
ventana = None
crucigrama_3d = {}
z_actual = 0
vista_actual = 'XY'  # Para controlar la vista actual: 'XY' o 'YZ'


def seleccionar_archivo():
    """Función para seleccionar archivo
    """
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo de crucigrama",
        filetypes=[("Text Files", "*.txt")]
    )
    
    if archivo:
        try:
            cargar_crucigrama(archivo)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")


def cargar_crucigrama(ruta):
    """ Cargar el archivo de crucigrama y convertirlo a estructura

    Args:
        ruta (_type_): _description_
    """
    global crucigrama_3d
    with open(ruta, 'r') as file:
        contenido = file.readlines()
    
    """Convertir el contenido a una lista 3D (por ejemplo, dividiendo por z, x, y)
    """
    crucigrama_3d = []
    capa_actual = []
    for linea in contenido:
        if linea.strip():  # Si no es una línea vacía, se toma como parte del crucigrama
            capa_actual.append(list(linea.strip()))
        else:
            crucigrama_3d.append(capa_actual)
            capa_actual = []
    if capa_actual:
        crucigrama_3d.append(capa_actual)  # Agregar la última capa
    crear_crucigrama(len(crucigrama_3d[0]))  # Crear la ventana con las dimensiones del crucigrama


def crear_crucigrama(dimensiones):
    """Iniciar la creación del crucigrama

    Args:
        dimensiones (_type_): _description_
    """
    global DIMENSIONES, ventana, crucigrama_3d, z_actual, vista_actual
    DIMENSIONES = dimensiones
    ventana = tk.Tk()
    ventana.title("Crucigrama 3D")
    z_actual = 0
    vista_actual = 'XY'  # Comenzamos con la vista inicial en X-Y
    mostrar_plano(z_actual)  # Mostrar automáticamente el plano inicial (X-Y)


def mostrar_plano(z):
    """ Mostrar el plano actual del crucigrama en la interfaz

    Args:
        z (_type_): _description_
    """
    global crucigrama_3d, DIMENSIONES, z_actual, vista_actual
    z_actual = z

    # Limpiar ventana para actualizar
    for widget in ventana.winfo_children():
        widget.destroy()

    if vista_actual == 'XY':
        label_plano = tk.Label(ventana, text=f"Plano Z = {z_actual} (Vista X-Y)", font=("Arial", 14))
        label_plano.grid(row=0, column=0, columnspan=DIMENSIONES)

        # Mostrar la capa X-Y correspondiente en una tabla de botones
        for i in range(DIMENSIONES):
            for j in range(DIMENSIONES):
                letra = crucigrama_3d[z][i][j] if crucigrama_3d[z][i][j] != " " else ""
                boton = tk.Button(ventana, text=letra, width=4, height=2)
                boton.grid(row=i + 1, column=j)

    elif vista_actual == 'YZ':
        label_plano = tk.Label(ventana, text=f"Vista Y-Z en X = {z_actual}", font=("Arial", 14))
        label_plano.grid(row=0, column=0, columnspan=DIMENSIONES)

        # Mostrar el plano Y-Z correspondiente en una tabla de botones (rotado)
        for y in range(DIMENSIONES):
            for z in range(len(crucigrama_3d)):
                letra = crucigrama_3d[z][y][z_actual] if crucigrama_3d[z][y][z_actual] != " " else ""
                boton = tk.Button(ventana, text=letra, width=4, height=2)
                boton.grid(row=y + 1, column=z)

    # Añadir controles para cambiar plano (Z)
    btn_anterior = tk.Button(ventana, text="Plano Anterior", command=plano_anterior)
    btn_anterior.grid(row=DIMENSIONES + 1, column=0)

    btn_siguiente = tk.Button(ventana, text="Plano Siguiente", command=plano_siguiente)
    btn_siguiente.grid(row=DIMENSIONES + 1, column=1)

    # Botón para cambiar entre vista X-Y y Y-Z
    btn_rotar = tk.Button(ventana, text="Cambiar Vista", command=cambiar_vista)
    btn_rotar.grid(row=DIMENSIONES + 1, column=2)

    ventana.mainloop()

def plano_anterior():
    """ Cambiar al plano anterior en Z
    """
    global z_actual
    if z_actual > 0:
        z_actual -= 1
        mostrar_plano(z_actual)

# Cambiar al siguiente plano en Z
def plano_siguiente():
    """ Cambiar al siguiente plano en Z
    """
    global z_actual, crucigrama_3d
    if z_actual < len(crucigrama_3d) - 1:
        z_actual += 1
        mostrar_plano(z_actual)


def cambiar_vista():
    """Cambiar entre las vistas X-Y y Y-Z
    """
    global vista_actual
    if vista_actual == 'XY':
        vista_actual = 'YZ'
    else:
        vista_actual = 'XY'
    mostrar_plano(z_actual)


def iniciar_programa():
    """ Función principal para iniciar el programa
    """
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal de Tkinter
    
    if messagebox.askyesno("Cargar crucigrama", "¿Deseas cargar un archivo de crucigrama?"):
        seleccionar_archivo()

iniciar_programa()

