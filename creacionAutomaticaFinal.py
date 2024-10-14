import tkinter as tk
from tkinter import messagebox, filedialog
import MenuPrincipal

class Crucigrama:
    def __init__(self, nombre, filas, columnas, master, columna_offset):
        """
        Inicializa una instancia de Crucigrama.

        Parámetros:
        - nombre: Nombre del crucigrama (usado para identificarlo).
        - filas: Número de filas del crucigrama.
        - columnas: Número de columnas del crucigrama.
        - master: Ventana o marco padre donde se mostrará el crucigrama.
        - columna_offset: Posición de inicio en la ventana principal (para colocar el crucigrama).
        """
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
        """
        Crea la cuadrícula visual del crucigrama con botones en cada celda.
        """
        for i in range(self.filas):
            for j in range(self.columnas):
                # Crear un botón en la posición (i, j)
                boton = tk.Button(self.ventana, text="", width=5, height=2, bg="white")
                boton.grid(row=i, column=j)
                # Guardar el botón en la cuadrícula
                self.cuadrícula[i][j] = boton

    def puede_colocarse(self, palabra, fila, columna, direccion):
        """
        Verifica si una palabra se puede colocar en la cuadrícula sin sobrepasar los límites
        o chocar con otras letras que no coincidan.

        Parámetros:
        - palabra: La palabra que se intenta colocar.
        - fila: La fila inicial donde se quiere colocar.
        - columna: La columna inicial donde se quiere colocar.
        - direccion: La dirección en que se intenta colocar la palabra ("horizontal" o "vertical").

        Retorna:
        - True si la palabra se puede colocar, False si no.
        """
        if direccion == "horizontal":
            if columna + len(palabra) > self.columnas:  # Comprobar que no se salga
                return False
            for k in range(len(palabra)):
                if self.cuadrícula[fila][columna + k]['text'] not in ["", palabra[k]]:
                    return False
            return True
            
        elif direccion == "vertical":
            if fila + len(palabra) > self.filas:  # Comprobar que no se salga
                return False
            for k in range(len(palabra)):
                if self.cuadrícula[fila + k][columna]['text'] not in ["", palabra[k]]:
                    return False
            return True
        
        return False

    def colocar_palabra(self, palabra, fila, columna, direccion):
        """
        Coloca una palabra en la cuadrícula y guarda su información.

        Parámetros:
        - palabra: La palabra que se va a colocar.
        - fila: La fila donde comenzará la palabra.
        - columna: La columna donde comenzará la palabra.
        - direccion: La dirección en la que se colocará la palabra (horizontal o vertical).
        """
        if direccion == "horizontal":
            for k in range(len(palabra)):
                self.cuadrícula[fila][columna + k]['text'] = palabra[k]  # Colocar la letra de la palabra
        elif direccion == "vertical":        
            for k in range(len(palabra)):
                self.cuadrícula[fila + k][columna]['text'] = palabra[k]  # Colocar la letra de la palabra

        # Guardar la descripción y la información de la palabra
        self.descripciones.append(f"Descripción de {palabra}")
        self.palabras_info.append((palabra, fila, columna, direccion))

    def extraer_texto(self):
        """
        Extrae el texto del cuadro de texto de descripciones y lo guarda en la lista de descripciones.
        """
        texto = self.texto_entry.get("1.0", tk.END).strip()  # Extraer texto del cuadro de texto
        self.descripciones.append(texto)  # Guardar en la lista
        self.texto_entry.delete("1.0", tk.END)  # Limpiar el cuadro de texto
        messagebox.showinfo("Éxito", "Texto extraído y almacenado correctamente.")

    def agregar_palabra(self):
        """
        Intenta agregar una palabra en la cuadrícula en la primera posición disponible.
        Primero intenta colocar la palabra horizontalmente, luego verticalmente.
        """
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
        """
        Guarda el crucigrama actual en un archivo de texto con formato personalizado.
        """
        archivo_guardar = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de Texto", "*.c3d")])
        if not archivo_guardar:
            return  # Si el usuario cancela, no hacer nada

        # Guardar en formato de texto
        with open(archivo_guardar, "w", encoding='utf-8') as archivo:
            version = 1
            archivo.write(f"Versión: {version}\n")  # Escribir la versión
            archivo.write(f"Dimensiones: {self.columnas} x {self.filas}\n")  # Dimensiones

            num_palabras = len(self.palabras_info)
            archivo.write(f"Número de palabras: {num_palabras}\n")  # Número total de palabras

            for index, (palabra, fila, columna, direccion) in enumerate(self.palabras_info):
                longitud_palabra = len(palabra)
                descripcion = self.descripciones[index] if index < len(self.descripciones) else ""
                archivo.write(f"Palabra: {palabra} (Longitud: {longitud_palabra})\n")
                archivo.write(f"Descripción: {descripcion}\n")
                archivo.write(f"Posición: ({columna}, {fila})\n")
                archivo.write(f"Dirección: {'Horizontal' if direccion == 'horizontal' else 'Vertical'}\n\n")

        messagebox.showinfo("Éxito", "El crucigrama y las descripciones se han guardado correctamente.")
    

class App:
    def __init__(self, master, volver_al_menu):
        """
        Inicializa la aplicación principal.

        Parámetros:
        - master: Ventana o marco principal donde se mostrará la aplicación.
        - volver_al_menu: Función que se ejecutará para volver al menú principal.
        """
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
    """
    Función principal que inicia la aplicación de crucigramas.
    """
    root = tk.Tk()
    root.title("Aplicación de Crucigramas")
    app = App(root, MenuPrincipal)  # Aquí pasas la función para volver al menú
    root.mainloop()

if __name__ == "__main__":
    main()
