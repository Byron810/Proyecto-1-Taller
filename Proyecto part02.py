import tkinter as tk
from tkinter import Menu

def on_new():
    print("Nuevo archivo creado")

def on_open():
    print("Archivo abierto")

def on_exit():
    root.quit()

# Crear la ventana principal
root = tk.Tk()
root.title("Mi Aplicación")
root.geometry("800x600")  # Ajustar el tamaño de la ventana (ancho x alto)

# Crear el menú
menu_bar = Menu(root)

# Agregar un menú de archivo
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Nuevo", command=on_new)
file_menu.add_command(label="Abrir", command=on_open)
file_menu.add_separator()
file_menu.add_command(label="Salir", command=on_exit)

menu_bar.add_cascade(label="Archivo", menu=file_menu)

# Configurar la barra de menú en la ventana
root.config(menu=menu_bar)

# Iniciar el bucle principal de la interfaz
root.mainloop()
