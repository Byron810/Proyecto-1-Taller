import tkinter as tk
from tkinter import messagebox

class Crucigrama:
    def __init__(self, nombre, filas, columnas, master, columna_offset):
        self.nombre = nombre
        self.filas = filas
        self.columnas = columnas
        self.cuadrícula = [["" for _ in range(columnas)] for _ in range(filas)]
        self.descripciones = {}  # Diccionario para almacenar las descripciones de las palabras
        self.contador = 1  # Contador para numerar las descripciones
        
        self.ventana = tk.Frame(master)  # Usar Frame para manejar la ventana del crucigrama
        self.crear_cuadricula()

        # Campo de entrada para la palabra
        self.entrada_palabra = tk.Entry(self.ventana)
        self.entrada_palabra.grid(row=filas, column=0, columnspan=columnas)

        # Campo de entrada para la descripción
        self.entrada_descripcion = tk.Entry(self.ventana)
        self.entrada_descripcion.grid(row=filas + 1, column=0, columnspan=columnas)

        # Botón para agregar la palabra y la descripción
        boton_agregar = tk.Button(self.ventana, text="Agregar Palabra", command=self.agregar_palabra)
        boton_agregar.grid(row=filas + 2, column=0, columnspan=columnas)

        # Cuadro para mostrar las descripciones
        self.cuadro_descripcion = tk.Text(self.ventana, width=30, height=10, bg="lightgrey")
        self.cuadro_descripcion.grid(row=filas + 3, column=0, columnspan=columnas)

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
                self.cuadrícula[fila][columna + k]['text'] = palabra[k]
            self.descripciones[self.contador] = self.entrada_descripcion.get()  # Guardar la descripción con un número
        elif direccion == "vertical":
            for k in range(len(palabra)):
                self.cuadrícula[fila + k][columna]['text'] = palabra[k]
            self.descripciones[self.contador] = self.entrada_descripcion.get()  # Guardar la descripción con un número

        self.mostrar_descripciones()  # Actualizar el cuadro de descripciones
        self.contador += 1  # Incrementar el contador

    def mostrar_descripciones(self):
        # Limpiar el cuadro
        current_content = self.cuadro_descripcion.get(1.0, tk.END).strip()  # Obtener contenido actual
        if current_content:
            current_content += "\n"  # Agregar nueva línea si ya hay contenido
        # Agregar cada descripción numerada al cuadro sin borrar el contenido anterior
        for numero, descripcion in self.descripciones.items():
            current_content += f"{numero}. {descripcion}\n"  # Mostrar la descripción con número

        self.cuadro_descripcion.delete(1.0, tk.END)  # Limpiar el cuadro
        self.cuadro_descripcion.insert(tk.END, current_content)  # Insertar el nuevo contenido

    def agregar_palabra(self):
        palabra = self.entrada_palabra.get()
        descripcion = self.entrada_descripcion.get()
        self.entrada_palabra.delete(0, tk.END)  # Limpiar la entrada de la palabra
        self.entrada_descripcion.delete(0, tk.END)  # Limpiar la entrada de la descripción

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

class App:
    def __init__(self):
        self.ventana_principal = tk.Tk()
        self.ventana_principal.title("Crucigramas 3D")

        # Crear un Frame para la línea separadora
        self.frame_linea = tk.Frame(self.ventana_principal, width=2, bg="black")
        self.frame_linea.grid(row=0, column=1, sticky="ns")  # Colocar en columna 1 y estirarlo verticalmente

        # Crear dos crucigramas, uno en cada columna
        self.crucigrama_xy = Crucigrama("xy", 6, 6, self.ventana_principal, columna_offset=0)
        self.crucigrama_yz = Crucigrama("yz", 6, 6, self.ventana_principal, columna_offset=2)  # Cambiado a columna 2

        # Ajustar el tamaño de la ventana
        self.ventana_principal.geometry("800x400")

        # Iniciar el bucle principal
        self.ventana_principal.mainloop()

# Crear la aplicación
App()
