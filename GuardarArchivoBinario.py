import tkinter as tk

def extraer_texto():
    texto = texto_entry.get("1.0", tk.END)  # Obtener el texto del cuadro de texto
    print("Texto ingresado:", texto.strip())  # Mostrar el texto en la consola

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Extractor de Oraciones")

# Crear un cuadro de texto donde el usuario puede escribir
texto_entry = tk.Text(ventana, width=40, height=10)
texto_entry.pack(pady=10)

# Crear un botón que llame a la función para extraer el texto
boton_extraer = tk.Button(ventana, text="Extraer Texto", command=extraer_texto)
boton_extraer.pack(pady=5)

# Ejecutar el bucle principal de la aplicación
ventana.mainloop()