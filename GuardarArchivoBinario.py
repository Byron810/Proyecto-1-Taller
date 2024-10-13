import struct

class Crossword3D:
    def __init__(self, version, dimensions, words):
        self.version = version
        self.dimensions = dimensions  # (X, Y, Z)
        self.words = words            # List of (word, definition, position, direction)

    def __repr__(self):
        return f"Crossword3D(version={self.version}, dimensions={self.dimensions}, words={self.words})"


def read_crossword(filename):
    try:
        with open(filename, 'rb') as file:
            # Leer el encabezado
            header = file.read(1)
            if not header:
                raise ValueError("El archivo está vacío o no se puede leer.")

            version = struct.unpack('B', header)[0]  # Versión del formato (1 byte)

            # Leer dimensiones (3 enteros de 4 bytes cada uno)
            dimensions = struct.unpack('iii', file.read(12))  # X, Y, Z (3 * 4 bytes)

            # Leer número de palabras
            num_words = struct.unpack('i', file.read(4))[0]  # Número total de palabras (4 bytes)

            words = []

            for _ in range(num_words):
                # Leer longitud de la palabra (1 byte)
                word_length = struct.unpack('B', file.read(1))[0]
                
                # Leer palabra (n bytes)
                word_bytes = file.read(word_length)
                word = word_bytes.decode('utf-8')  # Decodificar a cadena

                # Leer longitud de la definición (2 bytes)
                definition_length = struct.unpack('H', file.read(2))[0]

                # Leer definición (n bytes)
                definition_bytes = file.read(definition_length)
                definition = definition_bytes.decode('utf-8')  # Decodificar a cadena

                # Leer posición inicial (3 enteros de 4 bytes cada uno)
                position = struct.unpack('iii', file.read(12))  # (X, Y, Z)

                # Leer dirección de la palabra (1 byte)
                direction = struct.unpack('B', file.read(1))[0]

                words.append((word, definition, position, direction))

            return Crossword3D(version, dimensions, words)

    except FileNotFoundError:
        print(f"Error: El archivo '{filename}' no se encuentra.")
    except struct.error as e:
        print(f"Error de lectura en el archivo: {e}")
    except Exception as e:
        print(f"Se produjo un error: {e}")


# Ejemplo de uso
if __name__ == "__main__":
    crossword = read_crossword("crucigrama_general.c3d")
    if crossword:
        print(crossword)

        # Imprimir detalles de las palabras
        for word_info in crossword.words:
            word, definition, position, direction = word_info
            print(f"Palabra: {word}, Definición: {definition}, Posición: {position}, Dirección: {direction}")
