import struct

def guardar_crucigrama_binario(nombre_archivo, dimensiones, palabras):
    """
    Guarda la información del crucigrama en un archivo binario.

    :param nombre_archivo: Nombre del archivo a guardar.
    :param dimensiones: Una tupla que contiene (dim_x, dim_y, dim_z).
    :param palabras: Lista de tuplas con información de palabras en el formato:
                     (palabra, definicion, posicion, direccion)
                     donde posicion es (x, y, z) y direccion es 0 (X), 1 (Y), o 2 (Z).
    """
    # Extraer dimensiones
    dim_x, dim_y, dim_z = dimensiones
    num_palabras = len(palabras)

    with open(nombre_archivo, 'wb') as f:
        # Escribir encabezado
        f.write(struct.pack('B', 1))  # Versión del formato (1 byte)
        f.write(struct.pack('I', dim_x))  # Dimensiones X (4 bytes)
        f.write(struct.pack('I', dim_y))  # Dimensiones Y (4 bytes)
        f.write(struct.pack('I', dim_z))  # Dimensiones Z (4 bytes)
        f.write(struct.pack('I', num_palabras))  # Número total de palabras (4 bytes)

        # Escribir palabras y definiciones
        for palabra, definicion, posicion, direccion in palabras:
            longitud_palabra = len(palabra)
            longitud_definicion = len(definicion)

            # Escribir longitud de la palabra y la palabra
            f.write(struct.pack('B', longitud_palabra))  # Longitud de la palabra (1 byte)
            f.write(palabra.encode('utf-8'))  # Palabra (n bytes)

            # Escribir longitud de la definición y la definición
            f.write(struct.pack('H', longitud_definicion))  # Longitud de la definición (2 bytes)
            f.write(definicion.encode('utf-8'))  # Definición (n bytes)

            # Escribir posición inicial
            f.write(struct.pack('I', posicion[0]))  # Posición X (4 bytes)
            f.write(struct.pack('I', posicion[1]))  # Posición Y (4 bytes)
            f.write(struct.pack('I', posicion[2]))  # Posición Z (4 bytes)

            # Escribir dirección de la palabra
            f.write(struct.pack('B', direccion))  # Dirección (1 byte)

# Ejemplo de uso
dimensiones = (10, 10, 5)
palabras = [
    ("PYTHON", "Lenguaje de programación", (0, 1, 0), 0),  # Dirección X
    ("CODE", "Escribir programas", (4, 0, 0), 1),         # Dirección Y
]

guardar_crucigrama_binario("crucigrama.bin", dimensiones, palabras)
