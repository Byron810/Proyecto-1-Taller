import tkinter as tk
from tkinter import messagebox, filedialog
import struct
import MenuPrincipal

class Crucigrama:
    def __init__(self, nombre, filas, columnas, master, columna_offset):
        self.nombre = nombre
        self.filas = filas
        self.columnas = columnas
        self.cuadrícula = [["" for _ in range(columnas)] for _ in range(filas)]
        self.descripciones = []  # Lista para almacenar las descripciones de las palabras
        self.palabras_info = []  # Lista para almacenar información de las palabras
        
        self.ventana = tk.Frame(master)  # Usar Frame para manejar la ventana del crucigrama
        self.crear_cuadricula()

        # Campo de entrada para la palabra
        self.entrada_palabra = tk.Entry(self.ventana)
        self.entrada_palabra.grid(row=filas, column=0, columnspan=columnas)

        # Botón para agregar la palabra
        boton_agregar = tk.Button(self.ventana, text="Agregar Palabra", command=self.agregar_palabra)
        boton_agregar.grid(row=filas + 1, column=0, columnspan=columnas)

        # Botón para guardar el crucigrama
        boton_guardar = tk.Button(self.ventana, text="Guardar Crucigrama", command=self.guardar_crucigrama)
        boton_guardar.grid(row=filas + 2, column=0, columnspan=columnas)

        # Cuadro de texto para escribir descripciones
        self.texto_entry = tk.Text(self.ventana, width=40, height=10)
        self.texto_entry.grid(row=filas + 3, column=0, columnspan=columnas, pady=10)

        # Botón para extraer texto y guardarlo en la lista
        boton_extraer = tk.Button(self.ventana, text="Extraer Texto", command=self.extraer_texto)
        boton_extraer.grid(row=filas + 4, column=0, columnspan=columnas, pady=5)

        # Colocar el Frame en la ventana principal
        self.ventana.grid(row=0, column=columna_offset)

    def crear_cuadricula(self):
        for i in range(self.filas):
            for j in range(self.columnas):
                # Crear un botón en la posición (i, j)
                boton = tk.Button(self.ventana, text="", width=5, height=2, bg="white")
                boton.grid(row=i, column=j)
                # Guardar el botón en la cuadrícula
                self.cuadrícula[i][j] = boton

    def puede_colocarse(self, palabra, fila, columna, direccion):
        if direccion == "horizontal":
            if columna + len(palabra) > self.columnas:  # Comprobar que no se salga
                return False
            for k in range(len(palabra)):
                # Validar que si hay letra existente, debe coincidir
                if self.cuadrícula[fila][columna + k]['text'] not in ["", palabra[k]]:
                    return False
            return True  # Se puede colocar horizontalmente
            
        elif direccion == "vertical":
            if fila + len(palabra) > self.filas:  # Comprobar que no se salga
                return False
            for k in range(len(palabra)):
                if self.cuadrícula[fila + k][columna]['text'] not in ["", palabra[k]]:
                    return False
            return True  # Se puede colocar verticalmente
        
        return False

    def colocar_palabra(self, palabra, fila, columna, direccion):
        if direccion == "horizontal":
            for k in range(len(palabra)):
                self.cuadrícula[fila][columna + k]['text'] = palabra[k]  # Colocar la letra de la palabra
            tipo = "Horizontal"
        elif direccion == "vertical":        
            for k in range(len(palabra)):
                self.cuadrícula[fila + k][columna]['text'] = palabra[k]  # Colocar la letra de la palabra
            tipo = "Vertical"

        # Guardar la descripción (de momento no se usa para agregar la palabra)
        self.descripciones.append(f"Descripción de {palabra}")  # Agregar la descripción a la lista
        self.palabras_info.append((palabra, fila, columna, direccion))  # Agregar información de la palabra

    def extraer_texto(self):
        texto = self.texto_entry.get("1.0", tk.END).strip()  # Extraer texto del cuadro de texto
        self.descripciones.append(texto)  # Guardar en la lista
        self.texto_entry.delete("1.0", tk.END)  # Limpiar el cuadro de texto
        messagebox.showinfo("Éxito", "Texto extraído y almacenado correctamente.")

    def agregar_palabra(self):
        palabra = self.entrada_palabra.get()
        self.entrada_palabra.delete(0, tk.END)  # Limpiar la entrada de la palabra

        # Intentar acomodar la palabra
        for i in range(self.filas):
            for j in range(self.columnas):
                # Probar colocación horizontal
                if len(palabra) <= self.columnas and self.puede_colocarse(palabra, i, j, "horizontal"):
                    self.colocar_palabra(palabra, i, j, "horizontal")
                    return

                # Probar colocación vertical
                if len(palabra) <= self.filas and self.puede_colocarse(palabra, i, j, "vertical"):
                    self.colocar_palabra(palabra, i, j, "vertical")
                    return

        messagebox.showinfo("Error", "No se pudo acomodar la palabra en la cuadrícula.")

    def guardar_crucigrama(self):
        # Abrir diálogo para guardar archivo
        archivo_guardar = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de Texto", "*.c3d")])
        if not archivo_guardar:
            return  # Si el usuario cancela, no hacer nada

        # Guardar en formato de texto
        with open(archivo_guardar, "w", encoding='utf-8') as archivo:
            # Escribir la versión del formato
            version = 1
            archivo.write(f"Versión: {version}\n")  # Escribir la versión

            # Escribir dimensiones
            archivo.write(f"Dimensiones: {self.columnas} x {self.filas}\n")  # Dimensiones X, Y, Z

            # Escribir número de palabras
            num_palabras = len(self.palabras_info)
            archivo.write(f"Número de palabras: {num_palabras}\n")  # Número total de palabras

            # Escribir cada palabra y su información
            for index, (palabra, fila, columna, direccion) in enumerate(self.palabras_info):
                # Longitud de la palabra
                longitud_palabra = len(palabra)
                descripcion = self.descripciones[index] if index < len(self.descripciones) else ""
                archivo.write(f"Palabra: {palabra} (Longitud: {longitud_palabra})\n")
                archivo.write(f"Descripción: {descripcion}\n")
                archivo.write(f"Posición: ({columna}, {fila})\n")
                archivo.write(f"Dirección: {'Horizontal' if direccion == 'horizontal' else 'Vertical'}\n\n")

        messagebox.showinfo("Éxito", "El crucigrama y las descripciones se han guardado correctamente.")
    

class App:
    def __init__(self, master, volver_al_menu):
        self.ventana_principal = tk.Frame(master)  # Usar un Frame en lugar de una ventana
        self.ventana_principal.pack()
        self.volver_al_menu = volver_al_menu  # Guardar referencia a la función de volver al menú

        # Crear un Frame para la línea separadora
        self.frame_linea = tk.Frame(self.ventana_principal, width=2, bg="black")
        self.frame_linea.grid(row=0, column=1, sticky="ns")  # Colocar en columna 1 y estirarlo verticalmente

        # Crear dos crucigramas, uno en cada columna
        self.crucigrama_xy = Crucigrama("xy", 6, 6, self.ventana_principal, columna_offset=0)
        self.crucigrama_xz = Crucigrama("xz", 6, 6, self.ventana_principal, columna_offset=2)

        # Botón para volver al menú
        boton_volver = tk.Button(self.ventana_principal, text="Volver al Menú", command=MenuPrincipal.menu_principal)
        boton_volver.grid(row=2, column=0, columnspan=3)  # Coloca el botón en una nueva fila

# Inicializar la aplicación
def main():
    root = tk.Tk()
    root.title("Aplicación de Crucigramas")
    app = App(root, MenuPrincipal)  # Aquí pasas la función para volver al menú
    root.mainloop()

if __name__ == "__main__":
    main()
