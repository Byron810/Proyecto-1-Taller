import tkinter as tk
import creacionAuto as creacion
import FuncionResolucion

# Variables globales
ventana = None

# Modo resolución de crucigramas
def resolucion():
    FuncionResolucion.iniciar_programa(ventana)

# Modo creación de crucigramas
def modo_creacion():
    creacion.iniciar_programSa(ventana)
    pass

# Función para mostrar el menú principal usando Tkinter
def menu_principal():
    global ventana
    ventana = tk.Tk()
    ventana.title("Menú Principal - Crucigramas 3D")
    ventana.geometry("300x200")  # Tamaño de la ventana

    # Crear título
    label_titulo = tk.Label(ventana, text="---Crucigramas---", font=("Arial", 16))
    label_titulo.pack(pady=10)

    # Crear botones del menú principal
    boton_creacion = tk.Button(ventana, text="Modo Creación", width=20, command=modo_creacion)
    boton_creacion.pack(pady=5)

    boton_resolucion = tk.Button(ventana, text="Modo Resolución", width=20, command=resolucion)
    boton_resolucion.pack(pady=5)

    boton_salir = tk.Button(ventana, text="Salir", width=20, command=ventana.quit)
    boton_salir.pack(pady=5)

    # Ejecutar el bucle principal de Tkinter
    ventana.mainloop()

# Ejecutar ventana
if __name__ == "__main__":
    menu_principal()
