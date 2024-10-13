import tkinter as tk
import creacionAutomatica as creacion
import FuncionResolucion

# Variables globales
ventana = None
frame_menu = None
frame_crucigrama = None  # Añadir variable para el marco del crucigrama

# Modo resolución de crucigramas
def resolucion():
    global frame_menu
    frame_menu.pack_forget()  # Ocultar el menú
    FuncionResolucion.iniciar_programa(ventana)

# Modo creación de crucigramas
def modo_creacion():
    global frame_crucigrama  # Usar la variable global
    frame_menu.pack_forget()  # Ocultar el menú
    if frame_crucigrama is not None:  # Si ya existe, eliminarlo
        frame_crucigrama.destroy()  # Destruir el marco anterior
    frame_crucigrama = tk.Frame(ventana)  # Crear un nuevo marco para el crucigrama
    frame_crucigrama.pack()  # Empaquetar el marco en la ventana
    creacion.iniciar_crucigrama(frame_crucigrama)  # Iniciar el crucigrama en el marco

# Función para mostrar el menú principal usando Tkinter
def menu_principal():
    global ventana
    ventana = tk.Tk()
    ventana.title("Menú Principal - Crucigramas 3D")
    ventana.geometry("300x200")  # Tamaño de la ventana

    # Crear un Frame para el menú
    global frame_menu
    frame_menu = tk.Frame(ventana)
    frame_menu.pack(pady=20)

    # Crear título
    label_titulo = tk.Label(frame_menu, text="---Crucigramas---", font=("Arial", 16))
    label_titulo.pack(pady=10)

    # Crear botones del menú principal
    boton_creacion = tk.Button(frame_menu, text="Modo Creación", width=20, command=modo_creacion)
    boton_creacion.pack(pady=5)

    boton_resolucion = tk.Button(frame_menu, text="Modo Resolución", width=20, command=resolucion)
    boton_resolucion.pack(pady=5)

    boton_salir = tk.Button(frame_menu, text="Salir", width=20, command=ventana.quit)
    boton_salir.pack(pady=5)

    # Ejecutar el bucle principal de Tkinter
    ventana.mainloop()

# Ejecutar ventana
if __name__ == "__main__":
    menu_principal()
