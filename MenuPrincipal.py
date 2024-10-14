import tkinter as tk
import creacionAutomatica as creacion
import FuncionResolver

# Variables globales
ventana = None
frame_menu = None   
frame_crucigrama = None  # Variable para el marco del crucigrama

def resolucion():
    """
    Inicia el modo de resolución de crucigramas.

    Oculta el menú principal y llama a la función que inicia la resolución de crucigramas.
    """
    global frame_menu
    frame_menu.pack_forget()  # Ocultar el menú
    FuncionResolver.iniciar_programa()

def modo_creacion():
    """
    Inicia el modo de creación de crucigramas.

    Oculta el menú principal y muestra el marco de creación de crucigramas usando 
    la clase `App` de `creacionAutomatica`.
    """
    global frame_menu, frame_crucigrama
    frame_menu.pack_forget()  # Ocultar el menú
    
    # Crear un nuevo marco para el crucigrama y mostrarlo
    frame_crucigrama = creacion.App(ventana, volver_al_menu)
    frame_crucigrama.pack()

def menu_principal():
    """
    Muestra el menú principal de la aplicación con opciones para creación y resolución de crucigramas.

    Crea una ventana con Tkinter y muestra botones para acceder al modo de creación o resolución,
    además de un botón para salir del programa.
    """
    global ventana
    ventana = tk.Tk()
    ventana.title("Menú Principal - Crucigramas 3D")
    ventana.geometry("1600x900")  # Tamaño de la ventana

    # Crear un Frame para el menú
    global frame_menu
    frame_menu = tk.Frame(ventana)
    frame_menu.pack(pady=20)

    # Crear título
    label_titulo = tk.Label(frame_menu, text="---Crucigramas---", font=("Arial", 60))
    label_titulo.pack(pady=10)

    # Crear botones del menú principal
    boton_creacion = tk.Button(frame_menu, text="Modo Creación", width=50, command=modo_creacion)
    boton_creacion.pack(pady=5)

    boton_resolucion = tk.Button(frame_menu, text="Modo Resolución", width=50, command=resolucion)
    boton_resolucion.pack(pady=5)

    boton_salir = tk.Button(frame_menu, text="Salir", width=50, command=ventana.quit)
    boton_salir.pack(pady=5)

    # Ejecutar el bucle principal de Tkinter
    ventana.mainloop()

def volver_al_menu():
    """
    Vuelve al menú principal desde el marco de creación o resolución de crucigramas.

    Oculta el marco del crucigrama y vuelve a mostrar el menú principal.
    """
    global frame_crucigrama, frame_menu
    frame_crucigrama.pack_forget()  # Ocultar el marco del crucigrama
    frame_menu.pack()  # Volver a mostrar el menú

# Ejecutar ventana
if __name__ == "__main__":
    menu_principal()
